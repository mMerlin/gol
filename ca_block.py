#!bin/python3
# coding=utf-8

'''Cellular Automaton block handling'''

# xmllint --noout --nonet --nocatalogs --schema ca.xsd test.xml

__author__ = 'H Phil Duby'

# from enum import Enum
# import sys
import hashlib
from lxml import etree as ET
# import defusedxml.lxml as dfsET
from defusedxml import defuse_stdlib
from commontools import constant
from commontools import BoxSide
from commontools import BoundingBox2D
from commontools import random_id


class CaBlock:
    '''Cellular Automaton block handling'''

    # pylint: disable=invalid-name,missing-docstring,no-method-argument,multiple-statements,too-many-instance-attributes
    @constant
    def DEAD_CELL(): return 0
    @constant
    def LIVING_CELL(): return 1
    @constant
    def BOARD_ROWS(): return 10
    @constant
    def BOARD_COLUMNS(): return 10
    @constant
    def SCH_ENCODING(): return 'utf-8'
    @constant
    def BYT_ENCODING(): return 'ascii'
    @constant
    def SCH_VERSION(): return '0.1.0-dev+build.2017.10.26'
    @constant
    def SCH_DEFAULT(): return 'http://www.cellularautomaton.org/'
    @constant
    def GOL_DIMENSIONS(): return '2,2'
    @constant
    def GOL_FAMILY(): return 'Moore'
    @constant
    def GOL_NEIGHBOURHOOD(): return 'base.gol'
    @constant
    def TAG_ROOT(): return 'cellular-automaton'
    @constant
    def TAG_NEIGHBOURHOODS(): return 'neighbourhoods'
    @constant
    def TAG_FAMILY(): return 'family'
    @constant
    def TAG_NEIGHBOURHOOD(): return 'neighbourhood'
    @constant
    def TAG_DEFINEDBLOCKS(): return 'defined-blocks'
    @constant
    def TAG_HASHES(): return 'hashes'
    @constant
    def TAG_BLOCKS(): return 'block'
    @constant
    def TAG_GENERATIONS(): return 'generations'
    @constant
    def TAG_GENERATION(): return 'generation'
    @constant
    def TAG_HASH(): return 'hash'
    @constant
    def TAG_REPRESENTATION(): return 'representation'
    @constant
    def ATR_SEMVERSION(): return 'semVersion'
    @constant
    def ATR_FAMILY(): return 'family'
    @constant
    def ATR_ID(): return 'id'
    @constant
    def ATR_DIMENSION(): return 'dimensions'
    @constant
    def ATR_CELLSTATE(): return 'cell-state'
    @constant
    def ATR_NEIGHBOURHOOD(): return 'neighbourhood'
    @constant
    def ATR_BOUNDINGBOX(): return 'boundingbox'
    @constant
    def ATR_VECTOR(): return 'vector'
    @constant
    def ATR_SEQUENCE(): return 'sequence'
    @constant
    def ATR_LIVING(): return 'living'
    @constant
    def ATR_EXTENT(): return 'extent'
    @constant
    def ATR_ROTATEFLIP(): return 'rotateflip'
    @constant
    def ATR_KEY(): return 'key'
    @constant
    def ATR_MD5(): return 'md5'
    @constant
    def ATR_MATCHES(): return 'matches'
    # pylint: enable=invalid-name,missing-docstring,no-method-argument,multiple-statements
    # pylint: enable=too-many-instance-attributes

    # def __init__(self, hashManagerCallback):
    # def __init__(self, contextObject):
    def __init__(self):
        '''construct cellular automaton instance'''
        # monkey patch to attempt to block [maliciously] malformed xml from
        # causing bomb problems
        defuse_stdlib()

        # If not loaded from a file (xml)
        input_context = {
            'family': 'Moore',
            'neighbourhood': 'base.gol',
            'dimensions': 2,  # 2d, square grid, Moore neighbourhood
        }

        self.rows = self.BOARD_ROWS
        self.columns = self.BOARD_COLUMNS
        self.board = [[self.DEAD_CELL for j in range(
            self.columns)] for i in range(self.rows)]
        self.board[2][1] = self.LIVING_CELL
        self.board[2][3] = self.LIVING_CELL
        self.generation_number = 0
        self.live_cells_count = 2
        self.blocks_wrapper = None
        self.hashes_wrapper = None
        self.gen_wrapper = None
        self.bounding_box = None

        # neighbourhood 'rule' applied to every living cell in bounding box,
        # or'd together and or'd with the original living cells
        # This is the region where a intersection with another (similarly
        # constructed) neighbourhood *could* change the next generation of the
        # current region/neighbourhood.
        # quick check: intersecting bounding boxes ?
        #  if yes, intersecting neighbourhoods ?
        #   if yes, possible (full) collision
        #    compare next generation with and without the interferring
        #    neighbourhood to see if really affected
        # self.neighbourhood #
        self.active_block = None
        self.neighbourhoods = None

        self.hashes = {}
        self.next_hash_key = 0
        # TODO populate hashes when load file (with hash tag elements)
    # end def __init__(…)

    def step(self):
        '''advance board configuration one step (generation)'''
        # TODO move to 'binary' block processing, maintaining history, with
        # functions to generate the xml from current, selected, all history
        self.accumulate_board_configuration()
    # end def step(…)

    def vertical_bounding_box_range(self):
        '''return the min and max of the vertical extent'''
        return range(self.bounding_box.top, self.bounding_box.bottom + 1)

    def horizontal_bounding_box_range(self):
        '''return the min and max of the horizontal extent'''
        return range(self.bounding_box.left, self.bounding_box.right + 1)

    def accumulate_board_configuration(self):
        '''
        Store information needed to describe and reproduce full board state
        '''
        if self.generation_number == 0:
            # create block wrapper for generation representation of board
            # configuration
            # TODO Need better check than generation_number == 0: could already
            # exist and be generation_number 0, if load / clear / modify after
            # previous block finished / cancelled
            self.build_board_configuration_block()

        print('bounding box', self.bounding_box)  # DEBUG
        # Now have a block element with generations child, though not fully
        # populated yet.
        # always need to create a generation element with representation child.
        # One time, need to copy info to block ??? do the copy AFTER stopping?
        # need to have a generations? element at the start, to have a place to
        # store the generation+representation elements
        gen = ET.SubElement(self.gen_wrapper, self.TAG_GENERATION)
        gen.set(self.ATR_LIVING, str(self.live_cells_count))
        gen.set(self.ATR_SEQUENCE, str(self.generation_number))
        # check the previous generation(s?) for sub blocks
        # check global hash for matching blocks

        print('board content from', self.bounding_box.left,
              self.bounding_box.top)  # DEBUG

        region_cells = []
        for row in self.vertical_bounding_box_range():
            for col in self.horizontal_bounding_box_range():
                # print(str.format('row:col {}:{} = {}', row, col,
                #       self.board[row][col]))  # DEBUG
                region_cells.append(self.board[row][col])
        print('board config', region_cells, '|', ','.join(
            map(str, region_cells)), '|')  # DEBUG
        # HPD TODO

        width = self.bounding_box.right - self.bounding_box.left + 1
        height = self.bounding_box.bottom - self.bounding_box.top + 1
        generation_extent = ','.join(map(str, [width, height]))
        generation_configuration = ','.join(map(str, region_cells))
        generation_byte_extent = bytearray(
            generation_extent, self.BYT_ENCODING)
        generation_byte_configuration = bytearray(
            generation_configuration, self.BYT_ENCODING)
        print(generation_byte_extent, generation_byte_configuration)  # DEBUG
        hshmd5 = hashlib.md5()
        hshmd5.update(generation_byte_extent)
        hshmd5.update(generation_byte_configuration)
        hash_key = hshmd5.hexdigest()
        # TODO get context to also pass to add check
        self.hash_add_check(hshmd5.digest())  # move to HashTrack method
        # TODO ? process result of check (if already existed)
        print(self.hashes)  # DEBUG
        print(hash_key, type(hash_key))  # DEBUG
        hsh = ET.Element(self.TAG_HASH)
        hsh.set(self.ATR_KEY, hash_key)

        self.hashes_wrapper.append(hsh)

        # for lookup ID/IDREF purposes, keep the hash elements before the
        # generation
        rep = ET.SubElement(gen, self.TAG_REPRESENTATION)
        rep.set(self.ATR_EXTENT, generation_extent)
        rep.set(self.ATR_CELLSTATE, generation_configuration)
        # rep.set(self.ATR_ROTATEFLIP, 'nf-r0')  # leave as default for now
    # end def accumulate_board_configuration(…)

    def build_board_configuration_block(self):
        '''
        Create wrapper for generation information about the current
        configuration
        '''
        print('build_board_configuration_block: gen_number live_cells_count',
              self.generation_number, self.live_cells_count)  # TRACE DEBUG
        if self.blocks_wrapper is None:
            self.blocks_wrapper = ET.Element(self.TAG_DEFINEDBLOCKS)  # Once
            self.hashes_wrapper = ET.SubElement(
                self.blocks_wrapper, self.TAG_HASHES)
            # if not already loaded from file or created for previous block

        blk = ET.Element(self.TAG_BLOCKS)
        blk.set(self.ATR_ID, random_id())
        gens = ET.SubElement(blk, self.TAG_GENERATIONS)
        gens.set(self.ATR_NEIGHBOURHOOD, self.GOL_NEIGHBOURHOOD)
        self.locate_board_neighbourhood()
        print('board_neighbourhood', self.bounding_box)  # DEBUG
        print(self.board[2])  # DEBUG

        self.active_block = blk
        self.gen_wrapper = gens
    # end def build_board_configuration_block(…)

    def locate_board_neighbourhood(self):
        '''
        Shrink the bounding box until live cells are encountered
        '''
        # Typically easier to check a row, since that is all one list
        bounds = BoundingBox2D(-1, -1, self.rows, self.columns)

        # There should really be a simpler way to do this
        while True:
            bounds.shrink(BoxSide.TOP)
            if self.LIVING_CELL in self.board[bounds.top]:
                break
        while True:
            bounds.shrink(BoxSide.BOTTOM)
            if self.LIVING_CELL in self.board[bounds.bottom]:
                break
        while True:
            bounds.shrink(BoxSide.LEFT)
            if self.islivingincolumn(bounds.left, bounds):
                break
        while True:
            bounds.shrink(BoxSide.RIGHT)
            if self.islivingincolumn(bounds.right, bounds):
                break
        self.bounding_box = bounds
        print('bounds bbBox', bounds, self.bounding_box)  # DEBUG: confirm is
        # same object instance
    # end def locate_board_neighbourhood(…)

    def islivingincolumn(self, col, bounds):
        '''
        Determine if any living cells exist in a column, in the current
        bounding box rows
        '''
        for row in range(bounds.top, bounds.bottom + 1):
            if self.LIVING_CELL == self.board[row][col]:
                return True
        return False
    # end def islivingincolumn(…)

    def build_root(self):
        '''
        create the wrapper to hold the cellular automaton information
        '''
        # ET.register_namespace(None, self.SCH_DEFAULT)
        # ET.register_namespace('', self.SCH_DEFAULT)
        # ET.register_namespace('ca', self.SCH_DEFAULT)
        namespacemap = {None: self.SCH_DEFAULT}
        caroot = ET.Element(self.TAG_ROOT, nsmap=namespacemap)
        caroot.set(self.ATR_SEMVERSION, self.SCH_VERSION)

        return ET.ElementTree(caroot)
    # end def build_root(…)

    def build_base_neighbourhoods(self):
        '''
        Create the base (nested) xml elements with keys referenced in
        the generation data
        '''
        nhoods = ET.Element(self.TAG_NEIGHBOURHOODS)
        fam = ET.SubElement(nhoods, self.TAG_FAMILY)
        fam.set(self.ATR_ID, self.GOL_FAMILY)
        nhood = ET.SubElement(nhoods, self.TAG_NEIGHBOURHOOD)
        nhood.set(self.ATR_ID, self.GOL_NEIGHBOURHOOD)
        nhood.set(self.ATR_FAMILY, self.GOL_FAMILY)
        self.neighbourhoods = nhoods
    # end def build_base_neighbourhoods(…)

    def get_block_from_generations(self):
        '''
        Determine block and generations wrapper information from generation
        history
        '''
        ET.dump(self.active_block)
        print()  # DEBUG spacer
        ET.dump(self.gen_wrapper)
        print()  # DEBUG spacer
        # for chld in self.gen_wrapper.iter(tag=self.TAG_GENERATION):
        for chld in self.gen_wrapper.iterchildren():
            ET.dump(chld)
            print('living', chld.get(self.ATR_LIVING))
            print('junk', chld.get('junk'))
        self.active_block.set(self.ATR_DIMENSION, '3,1')    # from sequence=0
        self.active_block.set(self.ATR_CELLSTATE, '1,0,1')  # from sequence=0

        self.gen_wrapper.set(self.ATR_BOUNDINGBOX, '3,1')  # from all sequences
    # end def get_block_from_generations(…)

    def save_history_as_xml(self):
        '''save the generation history to an xml file'''
        if self.active_block is not None:
            # Set overall block size and dimensions from existing generations
            # ?adjust? gen/rep vectors?
            self.get_block_from_generations()
            self.blocks_wrapper.append(self.active_block)
            # self.active_block = None

        if self.neighbourhoods is None:
            self.build_base_neighbourhoods()

        catree = self.build_root()
        caroot = catree.getroot()
        caroot.append(self.neighbourhoods)
        caroot.append(self.blocks_wrapper)

        # catree.write_c14n('test.xml')
        catree.write(
            'test.xml',
            encoding=self.SCH_ENCODING,
            xml_declaration=True,
            # default_namespace=self.SCH_DEFAULT,
            method='xml',
            # short_empty_elements=True
            pretty_print=True,
            )
        print('done write to test.xml')  # TRACE
    # end def save_history_as_xml(…)

    def hash_add_check(self, digest):
        '''apend a hash digest to the list'''
        # TODO move to HashTrack method
        # TODO check existing hashes dictionary for match
        self.hashes[self.next_hash_key] = digest
        self.next_hash_key += 1
    # end def hash_add_check(…)
# end class CaBlock


class HashTracker:
    '''track hash digests'''
    def __init__(self):
        self.digests = []

    def add_hash(self, digest, context) -> bool:
        '''apend a hash digest to the list'''
        if digest in self.digests:
            # append context ?
            return False
        self.digests[digest] = context
        return True
# end class HashTracker:


def mymain():
    '''wrapper for test/start code so that variables do not look like constants'''
    block = CaBlock()
    block.step()

    block.save_history_as_xml()


# Standalone module execution
if __name__ == "__main__":
    mymain()
