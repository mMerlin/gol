#!bin/python3
# coding=utf-8

'''
Game of Life
'''

# !/usr/bin/python3
# /home/phil/development/FritzingProjects/FritzingParts/repos/part-parse/fritzingParts.py
# /home/phil/development/FritzingProjects/FritzingParts/repos/part-parse/bHandler.py
# /home/phil/development/FritzingProjects/FritzingParts/repos/part-parse/pHandler.py

# /home/phil/development/FritzingProjects/FritzingParts/repos/part-parse/list_parts.py
# /home/phil/development/FritzingProjects/FritzingParts/repos/part-parse/explore.py
# /home/phil/development/FritzingProjects/FritzingParts/repos/part-parse/commonTools.py
# /home/phil/development/FritzingProjects/FritzingParts/repos/part-parse/dict.py

__author__ = 'H Phil Duby'

import sys
import hashlib
import tkinter as tk
import tkinter.filedialog as tkf
import tkinter.font as tkfont
# import tkinter.simpledialog as tkd
# from lxml import etree
from lxml import etree as ET
# from elementtree import ElementTree as ET
# from xml.etree import ElementTree as ET
import defusedxml.lxml as dfsET
# parse(), fromstring() RestrictedElement, GlobalParserTLS, getDefaultParser(), check_docinfo()
# import defusedxml.ElementTree as dfsET
# parse(), iterparse(), fromstring(), XMLParser
from defusedxml import defuse_stdlib
# import random
# from ca_datastore import CellularAutomatonLoader
from commontools import constant
from commontools import BoxSide
from commontools import BoundingBox2D
from commontools import random_id

# xmllint --noout --nonet --nocatalogs --schema ca.xsd test.xml


class Gol:
    """
    Conway´s Game Of Life
    """

    # Gather strings that would need alternates for internationalization
    # pylint: disable=invalid-name,missing-docstring,no-method-argument,multiple-statements
    @constant
    def APP_TITLE(): return "Conway's Game of Life"
    @constant
    def MNU_OPEN_LABEL(): return 'Open...'
    @constant
    def MNU_SAVE_LABEL(): return 'Save...'
    @constant
    def MNU_QUIT_LABEL(): return 'Quit'
    @constant
    def MNU_FILE_LABEL(): return 'File'
    @constant
    def MNU_CLEAR_LABEL(): return 'Clear'
    @constant
    def MNU_RANDOMIZE_LABEL(): return 'Randomize'
    @constant
    def MNU_EDIT_LABEL(): return 'Edit'
    @constant
    def BTN_START_LABEL(): return 'START'
    @constant
    def BTN_CLEAR_LABEL(): return 'CLEAR'
    @constant
    def BTN_PAUSE_LABEL(): return 'PAUSE'
    @constant
    def BTN_STEP_LABEL(): return 'STEP'
    @constant
    def BTN_RESET_LABEL(): return 'RESET'
    @constant
    def BTN_RANDOMIZE_LABEL(): return 'RANDOMIZE'
    @constant
    def SPN_DELAY_LABEL(): return 'Delay between steps:'
    @constant
    def CHK_WRAP_LABEL(): return 'Wrap around edges?'
    @constant
    def CHK_GRID_LABEL(): return 'show grid?'
    @constant
    def STS_LIVING_LABEL(): return 'living cells: '
    @constant
    def STS_GENERATION_LABEL(): return '\n\ngeneration: '
    @constant
    def GOL_FILETYPE_LABEL(): return 'game of life files'
    @constant
    def ALL_FILETYPE_LABEL(): return 'All files'

    @constant
    def CELL_WIDTH(): return 12
    @constant
    def CELL_HEIGHT(): return 12
    @constant
    def GENERATION_STEPS(): return 1000
    @constant
    def BUTTON_WIDTH(): return 10
    @constant
    def BUTTON_PADX(): return 10
    @constant
    def BUTTON_PADY(): return 10
    @constant
    def CONFIG_PADX(): return 10
    @constant
    def CONFIG_IPADX(): return 5
    @constant
    def CONFIG_PADY(): return 5
    @constant
    def DELAY_WIDTH(): return 5
    @constant
    def DELAY_VALUES(): return (5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400, 500, 1000)
    @constant
    def STS_POS_X(): return 10
    @constant
    def STS_POS_Y(): return 10
    @constant
    def STS_ANCHOR(): return 'nw'
    @constant
    def DEAD_CELL(): return 0
    @constant
    def LIVING_CELL(): return 1
    @constant
    def DEAD_INPUT_CELL(): return '.'
    @constant
    def LIVING_INPUT_CELL(): return '#'
    @constant
    def GOL_EXTENSION(): return '.gol'
    @constant
    def GOL_FILETYPE(): return '*.gol'
    @constant
    def ALL_FILETYPE(): return '*.*'
    # @constant
    # def GOL_FILETYPES(): return ((Gol.GOL_FILETYPE_LABEL(), Gol.GOL_FILETYPE()), (Gol.ALL_FILETYPE_LABEL(), Gol.ALL_FILETYPE()))
    @constant
    def UI_BG(): return 'white'
    @constant
    def LABEL_BG(): return 'white'
    @constant
    def WIDGET_BG(): return 'white'
    @constant
    def CANVAS_BG(): return 'grey'
    @constant
    def LIVING_COLOR(): return 'orange'
    @constant
    def LIVING_OUTLINE(): return 'black'
    @constant
    def STS_FILL_COLOR(): return 'white'

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
    # pylint: enable=invalid-name,missing-docstring,no-method-argument,multiple-statements

    def __init__(self, cell_rows, cell_columns):
        """
        Class instance constructor
        """
        # monkey patch to attempt to block [maliciously] malformed xml from causing bomb problems
        defuse_stdlib()
        # self.__SCH_DEFAULT = ''.join(['{', self.SCH_DEFAULT, '}'])
        self.run_paused = True
        self.openfile = None
        self.board = None
        self.board_bounding_box = None
        self.gen_num = None
        self.blocks_wrapper = None
        self.gen_wrapper = None
        self.active_block = None
        self.nei_hoods = None
        self.live_cells = None
        self.speedcontrol = None
        self.showgrid = None
        self.sequence_value = None
        self.rows = cell_rows
        self.columns = cell_columns
        self.sz_x = self.CELL_WIDTH
        self.sz_y = self.CELL_HEIGHT
        self.stop_steps = self.GENERATION_STEPS

        self.build_gui()
    # end def __init__(…)

    def build_gui(self):
        """
        Populate the user interface
        """
        s_rt = tk.Tk()
        self.root = s_rt
        s_rt.title(self.APP_TITLE)
        self.makemenu(s_rt)
        s_ui = self.build_main_controls(s_rt)
        s_ui2 = self.build_config_controls(s_rt)
        # self.globalKeyBindings()
        # self.bind_all('<…>', self.«method»)
        # self.bind_all('<Control-KeyPress-S>', self.save_board_to_file)
        # https://infohost.nmt.edu/tcc/help/pubs/tkinter/web/binding-levels.html
        cnvs = tk.Canvas(
            s_rt,
            width=self.columns * self.sz_x + 1,
            height=self.rows * self.sz_y + 1,
            highlightthickness=0, bd=0, bg=self.CANVAS_BG)
        self.gol_canvas = cnvs

        # TODO refactor whatever code is needed to repack on resize
        #  either manually, or when different size board is loaded
        # IDEA canvas methods to resize?
        # bottom frame truncates when main window sized below the intially
        # created dimensions (for the canvas).  Make canvas small to start
        # minimizes the issue

        #           Put everything on the screen
        self.clear()
        cnvs.bind("<Button-1>", self.switch_cell)
        s_ui.pack(side=tk.RIGHT, expand=tk.NO, fill=tk.BOTH)
        cnvs.pack(side=tk.TOP, expand=tk.YES, fill=tk.BOTH)
        s_ui2.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH, anchor=tk.W)
    # end def build_gui(…)

    def makemenu(self, win):
        """
        Add all menu options to the top level window
        """
        top = tk.Menu(win)          # win=top-level window
        win.config(menu=top)        # set its menu option

        filemenu = tk.Menu(top)
        filemenu.add_command(label=self.MNU_OPEN_LABEL, command=self.load_board, underline=0)
        filemenu.add_command(label=self.MNU_SAVE_LABEL, command=self.save_board_to_file, underline=0)
        filemenu.add_command(label=self.MNU_QUIT_LABEL, command=sys.exit, underline=0)
        top.add_cascade(label=self.MNU_FILE_LABEL, menu=filemenu, underline=0)

        edit = tk.Menu(top, tearoff=False)
        edit.add_command(label=self.MNU_CLEAR_LABEL, command=self.clear, underline=0)
        edit.add_command(label=self.MNU_RANDOMIZE_LABEL, command=self.rand_board, underline=0)
        edit.add_separator()
        top.add_cascade(label=self.MNU_EDIT_LABEL, menu=edit, underline=0)
    # end def makemenu(…)

    def build_main_controls(self, tk_rt):
        """
        build the application widget button controls interface
        """
        tk_ui = tk.Frame(tk_rt, bg=self.UI_BG)                  # user interface

        start_button = tk.Button(
            tk_ui, text=self.BTN_START_LABEL, width=self.BUTTON_WIDTH,
            command=lambda: self.life(from_start_button=True))
        # IDEA get rid of the pause button: change start to toggle between run and pause
        # toggle the label too?
        pause_button = tk.Button(
            tk_ui, text=self.BTN_PAUSE_LABEL, width=self.BUTTON_WIDTH,
            command=lambda: self.set_pause(p_sim=True))
        step_button = tk.Button(
            tk_ui, text=self.BTN_STEP_LABEL, width=self.BUTTON_WIDTH,
            command=lambda: self.life(from_step_button=True))
        clear_button = tk.Button(
            tk_ui, text=self.BTN_CLEAR_LABEL, width=self.BUTTON_WIDTH,
            command=self.clear)
        reload_button = tk.Button(
            tk_ui, text=self.BTN_RESET_LABEL, width=self.BUTTON_WIDTH,
            command=lambda: self.load_board(self.openfile))
        random_button = tk.Button(
            tk_ui, text=self.BTN_RANDOMIZE_LABEL, width=self.BUTTON_WIDTH,
            command=self.rand_board)
        # centerButton
        # shift«Left¦Right¦Up¦Down» (warn on data loss)

        self.sequence_value = 0
        start_button.grid(row=self.__next__(), column=0, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)
        pause_button.grid(row=self.__next__(), column=0, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)
        step_button.grid(row=self.__next__(), column=0, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)
        clear_button.grid(row=self.__next__(), column=0, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)
        reload_button.grid(row=self.__next__(), column=0, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)
        random_button.grid(row=self.__next__(), column=0, padx=self.BUTTON_PADX, pady=self.BUTTON_PADY)
        return tk_ui
    # end def build_main_controls(…)

    def build_config_controls(self, tk_rt):
        """
        build the board configuration widgets
        """
        s_ui = tk.Frame(tk_rt, bg=self.UI_BG)

        warp = tk.IntVar()                 # wrap around the edges ?
        self.showgrid = tk.IntVar()             # show the grid ?

        self.speedcontrol = tk.Spinbox(s_ui, width=self.DELAY_WIDTH, values=self.DELAY_VALUES)
        speedcontrol_label = tk.Label(s_ui, text=self.SPN_DELAY_LABEL, bg=self.WIDGET_BG)
        warpcontrol = tk.Checkbutton(s_ui, text=self.CHK_WRAP_LABEL, variable=warp, bg=self.WIDGET_BG)
        showgridcontrol = tk.Checkbutton(
            s_ui, text=self.CHK_GRID_LABEL,
            variable=self.showgrid, bg=self.WIDGET_BG, command=self.display_board)
        # board must be redrawn, because toggle grid will not be shown before
        # start is pressed because display_board() sits inside life()
        showgridcontrol.select()

        speedcontrol_label.grid(row=0, column=1, columnspan=2, padx=self.CONFIG_PADX, pady=self.CONFIG_PADY, sticky=tk.NW)
        self.speedcontrol.grid(row=0, column=3, padx=self.CONFIG_PADX, pady=self.CONFIG_PADY, sticky=tk.NW)
        warpcontrol.grid(row=1, column=4, columnspan=3, padx=self.CONFIG_PADX, ipadx=self.CONFIG_IPADX, sticky=tk.NW)
        showgridcontrol.grid(row=0, column=4, columnspan=2, padx=self.CONFIG_PADX, pady=self.CONFIG_PADY, ipadx=self.CONFIG_IPADX, sticky=tk.NW)

        # TODO HPD controls for (auto) recording generation representations
        return s_ui
    # end def build_config_controls(…)

    def __next__(self):
        """
        Internal function to increment a value and return it.
        Equivalent to __next__++ in other languages
        """
        self.sequence_value += 1
        return self.sequence_value

    # def create_random_board(self, density):

    def clear(self):
        """
        Clear the board to all empty (dead) cells
        """
        self.board = [[self.DEAD_CELL for j in range(self.columns)] for i in range(self.rows)]
        self.gen_num = 0
        self.display_board()

    def cell_neighbours(self, row, col):
        """
        get the number of currently living neighbours around the addressed cell
        """
        # ignore wrapping for now … always dead outside the current universe boundary

        # with the one time (per generation) preparation, no special edge case
        # checks are needed.  Always safe to access one row and column offset
        # from any valid board cell address
        neighbours = 0
        # print ('cell_neighbours of', row, col) # DEBUG
        for b_row in range(row - 1, row + 2):
            # there should be better pythonic way of counting living cells in
            # a slice of a list.  Only with NumPy?
            for b_col in range(col - 1, col + 2):
                # print ('neighbour', b_row, b_col) # DEBUG
                if self.board[b_row][b_col] == self.LIVING_CELL:
                    neighbours += 1
        # neighbours is actually the count of neighbours PLUS the address cell
        home_cells = 1 if self.board[row][col] == self.LIVING_CELL else 0

        # might as well take advantage of needing an explicit check of the target
        # cell, and return a 'living' count for it as well.  The caller needs that
        # anyway
        return home_cells, neighbours - home_cells
    # end def cell_neighbours(…)

    def step_generation(self):
        """
        Advance the current board cells one generation
        """
        # Create a new empty board
        after = [[self.DEAD_CELL for j in range(self.columns)] for i in range(self.rows)]
        # after = [list(self.DEAD_INPUT_CELL * self.columns) for i in range(self.rows)]
        # since above clears 'after', only need to set live cells
        # alternatively, creating a function to calculate the cell value, a comprehensive could do it all in one

        # ignore wrapping for now … always dead outside the current universe boundary

        # handle special cases where row or column is at the edge of the universe
        # … that is where row¦col == 0 or row¦col == self.«row¦column»s
        # Python lets us use index -1 to access the last list entry.  To make all
        # 1 step outside the universe accesses to be to dead cells, append a dead
        # cell at (only) the end of each row, and append an extra row of dead
        # cells.  Those will be accessed for both -1 and max+1 cases.
        # This will only exist in the (old) input board, not the new after
        for row in range(self.rows):
            self.board[row].append(self.DEAD_CELL)  # one extra dead cell at the end of each existing row
        # add one extra row of dead cells with the extra dead cell at the end
        self.board.append([self.DEAD_CELL for i in range(self.columns + 1)])
        # print( 'step_generation: after, board' ) # TRACE
        # print( after ) # DEBUG
        # print( self.board ) # DEBUG

        # Populate after with board plus one generation
        for row in range(self.rows):
            for col in range(self.columns):
                target, neighbours = self.cell_neighbours(row, col)
                # target is 0 or 1 when the center cell is dead or alive
                # neighbours is the number of living neighbours around target
                # print( 'context', row, col, target, neighbours) # DEBUG
                # The simplest logic I have found to determine a living cell
                if neighbours == 3 or (neighbours + target) == 3:
                    after[row][col] = self.LIVING_CELL
        # print( after ) # DEBUG
        # print( self.board ) # DEBUG
        self.board = after
    # end def step_generation(…)

    def switch_cell(self, event):
        """
        Toggle cell state at mouse click location
        """
        b_x = event.x // self.sz_x
        b_y = event.y // self.sz_y
        if b_x >= self.columns or b_y >= self.rows:
            return  # outside canvas

        self.board[b_y][b_x] = self.DEAD_CELL if self.board[b_y][b_x] == self.LIVING_CELL else self.LIVING_CELL
        self.display_board()
    # end def switch_cell(…)

    def display_board(self):
        """
        Refresh the canvas with the contents of the current board
        """
        self.gol_canvas.delete(tk.ALL)
        self.live_cells = 0
        outline_colours = [self.CANVAS_BG, self.LIVING_COLOR]
        dead_outline = outline_colours[self.showgrid.get()]
        for b_x in range(self.columns):
            for b_y in range(self.rows):
                rect = (b_x * self.sz_x, b_y * self.sz_y, (b_x+1) * self.sz_x, (b_y+1) * self.sz_y)
                if self.board[b_y][b_x] == self.LIVING_CELL:
                    self.gol_canvas.create_rectangle(rect, outline=self.LIVING_OUTLINE, fill=self.LIVING_COLOR)
                    self.live_cells += 1
                else:
                    self.gol_canvas.create_rectangle(rect, outline=dead_outline)
        stats = self.STS_LIVING_LABEL + str(self.live_cells) + self.STS_GENERATION_LABEL + str(self.gen_num)
        self.gol_canvas.create_text((self.STS_POS_X, self.STS_POS_Y), text=stats, fill=self.STS_FILL_COLOR, anchor=self.STS_ANCHOR, )  # show stats on canvas
        return self.live_cells
    # end def display_board(…)

    def life(self, from_start_button=False, from_step_button=False):
        """
        Advance cells one generation, and setup to call again when not paused
        """
        # early exit if from_start_button==True and not paused (2nd start click)
        # make sure is in paused state to start with (init, load, clear, reset)
        if from_start_button is True and not self.run_paused:
            print('Looks like double start: second ignored')  # INFO
            # This could be turned into a pause click instead?
            return
        # Early exit if no living cells
        if self.live_cells == 0:
            print('Simulation stopped: no living cells')
            self.set_pause(True)         # Force stop when no cells left
            return
            # IDEA find a way to also pause for static boards
            # even smarter, if only static and non intersecting oscillators (any 'stable')
            # above will need group detection, oscillator detection

        # TODO hpd Before advancing the generation, save the state of the current one
        # if self.saveGenerations:
        self.accumulate_board_configuration()

        self.gen_num += 1
        self.step_generation()
        self.display_board()            # draw board and count living cells

        # At next generation, now decide what else needs to be done
        if from_start_button is True:    # function explicitly called from start button
            # self.set_pause()
            self.set_pause(False)        # necessary for restart the start_button if pressed after the pause_button
        if self.gen_num <= self.stop_steps and not self.run_paused and not from_step_button:
            # if not reached maximum generation, and not single stepping, wait
            # a while, then call life again
            delay = self.speedcontrol.get()
            self.root.after(delay, self.life)
        # IDEA auto pause (and warn) when live cell enters outer margin
        # problem only really occurs when 3 adjacent live cells at edge
    # end def life(…)

    def set_pause(self, p_sim=False):
        """
        [un]pause a running simulation
        """
        self.run_paused = p_sim

    def accumulate_board_configuration(self):
        """
        Store information needed to describe and reproduce full board state
        """
        # TODO HPD analyze/store board generation representation
        print('accum_cfg: gen_num live_cells', self.gen_num, self.live_cells)  # TRACE DEBUG
        if self.gen_num == 0:
            # create block wrapper for generation representation of board configuration
            self.build_board_configuration_block()
            # This is the first (zero'th) generation, so need to fill in a bit more
            # information for the generation(s) wrappers
            # gens.set(self.ATR_VECTOR, str.format('{},{}',
            #     self.board_bounding_box.left, self.board_bounding_box.right))
            # gens.set(self.ATR_BOUNDINGBOX, str.format('{},{}',
            #     self.board_bounding_box.right - self.board_bounding_box.left + 1,
            #     self.board_bounding_box.bottom - self.board_bounding_box.top + 1))

        print('bounding box', self.board_bounding_box)  # DEBUG
        # Now have a block element with generations child, though might not be
        # fully populated yet.
        # always need to create a generation element with representation child
        # one time, need to copy info to block ??? do the copy AFTER stopping?
        # need to have a generations element at the start, to have a place to
        # store the generation+representation elements
        # self.active_block = blk
        # self.gen_wrapper = gens
        gen = ET.SubElement(self.gen_wrapper, self.TAG_GENERATION)
        gen.set(self.ATR_LIVING, str(self.live_cells))
        gen.set(self.ATR_SEQUENCE, str(self.gen_num))
        # check the previous generation(s?) for sub blocks
        # check global hash for matching blocks
        ET.dump(self.gen_wrapper)  # DEBUG

        print('board content from', self.board_bounding_box.left, self.board_bounding_box.top)  # DEBUG

        cells = []
        for row in range(self.board_bounding_box.top, self.board_bounding_box.bottom + 1):
            for col in range(self.board_bounding_box.left, self.board_bounding_box.right + 1):
                # print(str.format('row:col {}:{} = {}', row, col, self.board[row][col]))
                cells.append(self.board[row][col])
        print('board config', cells, '|', ','.join(map(str, cells)), '|')  # DEBUG
        # HPD TODO

        width = self.board_bounding_box.right - self.board_bounding_box.left + 1
        height = self.board_bounding_box.bottom - self.board_bounding_box.top + 1
        # print('x y extent', width, height) # DEBUG
        gen_extent = ','.join(map(str, [width, height]))
        gen_cfg = ','.join(map(str, cells))
        gen_extent_byt = bytearray(gen_extent, self.BYT_ENCODING)
        gen_cfg_byt = bytearray(gen_cfg, self.BYT_ENCODING)
        print(gen_extent_byt, gen_cfg_byt)  # DEBUG
        hshmd5 = hashlib.md5()
        hshmd5.update(gen_extent_byt)
        hshmd5.update(gen_cfg_byt)
        hsh_method = hshmd5.hexdigest()
        print(hsh_method, type(hsh_method))  # DEBUG
        hsh = ET.Element(self.TAG_HASH)
        hsh.set(self.ATR_KEY, hsh_method)

        # for lookup ID/IDREF purposes, keep the hash elements before the generation
        rep = ET.SubElement(gen, self.TAG_REPRESENTATION)
        rep.set(self.ATR_EXTENT, gen_extent)
        rep.set(self.ATR_CELLSTATE, gen_cfg)
        # rep.set(self.ATR_ROTATEFLIP, 'nf-r0') # default for now
        ET.dump(gen)  # DEBUG
        # self.blocks_wrapper.append(blk)
        print('at end accumulate_board_configuration:')  # DEBUG
        ET.dump(self.active_block)  # DEBUG
        print()  # DEBUG
        ET.dump(self.blocks_wrapper)  # DEBUG
    # end def accumulate_board_configuration(…)

    def save_board_to_file(self):
        """
        Save information about the current (and history) board configuration to permanent storage
        """
        # TODO handle multiple storage formats
        #  The old .gol straight 'text' matrix
        #
        # TODO load library files, and merge with new data
        # ?flag? to export the neighbourhoods information

        print('try loading the xmlschema')  # TRACE DEBUG
        # sch_tree = dfsET.parse('ca.xsd')
        sch_tree = ET.XMLSchema(file='ca.xsd')
        print('got xsd')  # TRACE DEBUG

        # TODO check the state of the recorded information, to decide if need to
        # store current generation (as well), or not

    def build_root(self):
        """
        create the wrapper to hold the cellular automaton information
        """
        # ET.register_namespace(None, self.SCH_DEFAULT)
        # ET.register_namespace('', self.SCH_DEFAULT)
        # ET.register_namespace('ca', self.SCH_DEFAULT)
        ns_map = {None: self.SCH_DEFAULT}
        ca_root = ET.Element(self.TAG_ROOT, ns_map=ns_map)
        ca_root.set(self.ATR_SEMVERSION, self.SCH_VERSION)

        return ET.ElementTree(ca_root)
    # end def build_root(…)

    def build_base_neighbourhoods(self):
        """
        Create the base (nested) xml elements with keys referenced in generation data
        """
        n_hoods = ET.Element(self.TAG_NEIGHBOURHOODS)
        fam = ET.SubElement(n_hoods, self.TAG_FAMILY)
        fam.set(self.ATR_ID, self.GOL_FAMILY)
        n_hood = ET.SubElement(n_hoods, self.TAG_NEIGHBOURHOOD)
        n_hood.set(self.ATR_ID, self.GOL_NEIGHBOURHOOD)
        n_hood.set(self.ATR_FAMILY, self.GOL_FAMILY)
        self.nei_hoods = n_hoods
    # end def build_base_neighbourhoods(…)

    def build_blocks_wrapper(self):
        """
        Create the wrapper element used to hold information about block configurations
        """
        self.blocks_wrapper = ET.Element(self.TAG_DEFINEDBLOCKS)
    # end def build_blocks_wrapper(…)

    def build_board_configuration_block(self):
        """
        Create wrapper for generation information about the current configuration
        """
        print('build_board_configuration_block: gen_num live_cells', self.gen_num, self.live_cells)  # TRACE DEBUG
        if self.blocks_wrapper is None:
            self.build_blocks_wrapper()
        blk = ET.Element(self.TAG_BLOCKS)
        blk.set(self.ATR_ID, random_id())
        gens = ET.SubElement(blk, self.TAG_GENERATIONS)
        gens.set(self.ATR_NEIGHBOURHOOD, self.GOL_NEIGHBOURHOOD)
        self.set_max_neighourhood()
        self.locate_board_neighbourhood()
        print('board_neighbourhood', self.board_bounding_box)  # DEBUG
        print(self.board[2])  # DEBUG

        self.active_block = blk
        self.gen_wrapper = gens

        ET.dump(self.blocks_wrapper)  # DEBUG
        ET.dump(blk)  # DEBUG
    # end def build_board_configuration_block(…)

    def set_max_neighourhood(self):
        """
        Make sure that global neighbourhood includes the whole board
        """
        # Set to one step out side of possible extents: shrink before test
        self.board_bounding_box = BoundingBox2D(-1, -1, self.rows, self.columns)
    # end def set_max_neighourhood(…)

    def locate_board_neighbourhood(self):
        """
        Shrink the bounding box until live cells are encountered
        """
        # Typically easier to check a row, since that is all one list
        brd_bb = self.board_bounding_box  # pointer copy, to shorten code references

        # There should really be a simpler way to do this
        while True:
            brd_bb.shrink(BoxSide.TOP)
            if self.LIVING_CELL in self.board[brd_bb.top]:
                break
        while True:
            brd_bb.shrink(BoxSide.BOTTOM)
            if self.LIVING_CELL in self.board[brd_bb.bottom]:
                break
        while True:
            brd_bb.shrink(BoxSide.LEFT)
            if self.living_in_column(brd_bb.left):
                break
        while True:
            brd_bb.shrink(BoxSide.RIGHT)
            if self.living_in_column(brd_bb.right):
                break
        print('brd bBox', brd_bb, self.board_bounding_box)  # DEBUG: confirm same object instance
    # end def locate_board_neighbourhood(…)

    def living_in_column(self, col, b_bx=None):
        '''determine if there is any living cell in a specified column'''
        if b_bx is None:
            b_bx = self.board_bounding_box
        for row in range(b_bx.top, b_bx.bottom + 1):
            if self.LIVING_CELL == self.board[row][col]:
                return True
        return False
    # end def living_in_column(…)

    def load_board(self, file=None):    # filename passed when reopening (resetting) same file
        """
        Setup a board from a file, and reset to generation number 1
        """
        self.load_board_from_file(file)
        self.gen_num = 1
        self.display_board()
    # end def load_board(…)

    def load_board_from_file(self, filename=None):
        """
        load a board configuration from a specified file, or browse for one
        """
        if filename is None:
            filename = tkf.askopenfilename(
                defaultextension=self.GOL_EXTENSION,
                filetypes=((self.GOL_FILETYPE_LABEL, self.GOL_FILETYPE), (self.ALL_FILETYPE_LABEL, self.ALL_FILETYPE)))
                # filetypes=self.GOL_FILETYPES)  # unable to find syntax to create constant property built from properties
            # depending whether a file was selected before the dialog was
            # cancelled or not, filename will be an empty string, or an empty
            # tuple
            if not isinstance(filename, str) or filename == "":
                return  # early exit if dialog cancelled

        board_f = open(filename, 'r')
        row = board_f.readline().strip('\n')
        self.board = []
        while row != "":
            self.board.append(list(row))
            row = board_f.readline().strip('\n')
        board_f.close()

        # TODO insert some tests here to check if the selected file meets the required file

        # TODO need to rebuild canvas? (resize) (if not same as previous)
        # auto resized, but hidden under controls, and resize changes all of the frames too

        self.openfile = filename
        self.rows = len(self.board)
        self.columns = len(self.board[0])  # fails when first record blank
    # end def load_board_from_file(…)

    def rand_board(self):
        '''randomize the current board'''
        # HPD (lowest priority)
        # pass

        if self.gen_num < 1:
            print('no history to save yet')  # INFO
            return
        self.set_pause(True)  # stop any running simulation after explict save to file

        # TODO hpd
        # process the generation and representation elements to populate some
        # self.active_block and self.gen_wrapper attributes
        # - adjust the representation vector attributes to compensate
        # gens.set(self.ATR_BOUNDINGBOX, '2,2')

        # common stuff, but should only need to populate before saving
        self.build_base_neighbourhoods()
        ca_tree = self.build_root()
        ca_root = ca_tree.getroot()
        ca_root.append(self.nei_hoods)
        ca_root.append(self.blocks_wrapper)

        # ET.dump(ca_tree)  # DEBUG
        # ET.dump(ca_root)  # DEBUG
        # TODO prompt for file to save
        # ca_tree.write_c14n('test.xml')
        ca_tree.write(
            'test.xml',
            encoding=self.SCH_ENCODING,
            xml_declaration=True,
            # default_namespace=self.SCH_DEFAULT,
            method='xml',
            # short_empty_elements=True
            pretty_print=True,
            )
        print('done write to test.xml')  # TRACE

    def run(self):
        """
        Start the simulation
        """
        self.root.mainloop()
    # end def run(…)
# end class Gol


def mymain():
    '''wrapper for test/start code so that variables do not look like constants'''
    gol = Gol(10, 10)
    # gol = Gol(60, 60)
    # gol = Gol(3, 3)
    gol.run()
    # print( gol.board )  # DEBUG
    # gol.board[0][0] = gol.LIVING_CELL
    # gol.board[0][1] = gol.LIVING_CELL
    # gol.board[1][1] = gol.LIVING_CELL
    # print( gol.board )  # DEBUG
    # gol.step_generation()
    # print( 'after step_generation' )  # DEBUG
    # print( gol.board )  # DEBUG


# Standalone module execution
if __name__ == "__main__":
    mymain()
