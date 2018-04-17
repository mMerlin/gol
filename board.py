#!bin/python
# coding=utf-8

'''
Handle Cellular Automaton boards stored as lines (rows) of ascii characters
'''

# using virtualenv
#   source bin/activate

import os
# https://sites.google.com/a/pythontkinter.com/tkinter/tkinterconstants
import tkinter.filedialog as tkf
from commontools import constant

__author__ = 'H Phil Duby'


class Board:
    '''
    Class to work with a gome of life board structured as rows of text
    '''

    # The original .gol board files held a number of same length rows
    # containing "#" and "." characters for living and dead cell positions.
    # Standard Conway´s Game of Life in 2 dimension with 2 states.

    # IDEA: Expand on that original structure.

    # IFF the first line of a file contains a unique set of characters, they
    # are cell states: The first representing empty (dead) cells, and each
    # successive character representing the next state.  For this case, the
    # second line needs to be blank, and the 3rd line starts the normal
    # board configuration using the defined cell states.

    # Another blank line before the end of file is an increment in the 3rd
    # dimension.  With this structure, there is no easy way to use more than 3
    # dimensions.  1, 2, and 3 dimenstions work.

    # To reduce file size, any row can be truncated on the right.  Trailing
    # dead (state 0) cells are implied.  Each row needs at least one cell
    # specified to hold its place.  A blank line increments the 3rd diemension
    # index.  Which means that whole layer can be truncated with there are no
    # more living cells.

    # NOTE: A board configuration does not care at all about the neighbourhood
    # or generation rules that have been, or will be used.

    # Gather strings that would need alternates for internationalization

    # @constant
    # def GOL_DESCRIPTION(): return 'game of life files'

    # @constant
    # def GOL_PATTERN(): return '*.gol'

    # pylint: disable=invalid-name,missing-docstring,no-method-argument,multiple-statements
    @constant
    def GOL_TYPE(): return ('Game of life files', '.gol')
    @constant
    def ALL_TYPE(): return ('All files', '*.*')
    @constant
    def BOARD_EXTENSION(): return '.gol'
    @constant
    def OPEN_TITLE(): return 'Cellular Automaton configuration'
    @constant
    def TKF_KEY_FILE_TYPES(): return 'filetypes'
    @constant
    def TKF_KEY_DEF_EXTENSION(): return 'defaultextension'
    @constant
    def TKF_KEY_TITLE(): return 'title'
    @constant
    def TKF_KEY_START_DIR(): return 'initialdir'
    # pylint: enable=invalid-name,missing-docstring,no-method-argument,multiple-statements

    def __init__(self):
        self.states = None
        self.config = None
        self.dimensions = 0
        self._current_open_path = None
        self._current_save_path = None
        self.initial_file = None
        self.lock_initial = False
    # end def __init__(…)

    # https://docs.python.org/3.5/library/tkinter.html?highlight=tkinter
    # https://www.tcl.tk/man/tcl8.6/TkCmd/getOpenFile.htm
    def load_from_file(self, file_path=None):
        '''Load board file into memory'''
        # TODO return state/status Boolean (load fail/succeeded)
        if file_path is None:
            file_options = self._build_open_opts()
            file_path = tkf.askopenfilename(**file_options)
        print('open: |{}| {}'.format(file_path, type(file_path)))  # DEBUG
        # print('test: {}'.format(type("")))                     # DEBUG
        if not isinstance(file_path, str):
            print('file path is not a string')                   # DEBUG TRACE
            return  # canceled?
        if file_path == '':
            print('empty file path')                             # DEBUG TRACE
            return  # NULL

        # TODO open, read, parse the specified file

        # string to state dictionary
        # for state_index, key in enumerate(row):
        #     self.states[key] = state_index
        self.update_cur_from_load(file_path)
    # end def load_from_file(…)

    def _build_open_opts(self):
        '''Build file options for input board file'''
        open_options = {}
        open_options[self.TKF_KEY_FILE_TYPES] = (self.GOL_TYPE, self.ALL_TYPE)
        open_options[self.TKF_KEY_DEF_EXTENSION] = self.BOARD_EXTENSION
        open_options[self.TKF_KEY_TITLE] = self.OPEN_TITLE
        if self._current_open_path is not None:
            open_options[self.TKF_KEY_START_DIR] = self._current_open_path
        return open_options
    # end def _build_open_opts(…)

    def update_cur_from_load(self, file):
        '''Update the current path information from the specified file'''
        print('update_cur_from_load: |{}|'.format(file))  # DEBUG TRACE
        print(os.path.abspath(file))  # DEBUG
        print(os.path.dirname(os.path.abspath(file)))  # DEBUG
        if self.lock_initial:
            return  # Do not update anything if the values have been locked

        # https://docs.python.org/3.5/library/os.path.html
        (self._current_open_path, self.initial_file) = os.path.split(
            os.path.abspath(file))
        if self._current_save_path is None:
            # set an initial default, when nothing else (yet) available
            self._current_save_path = self._current_open_path
    # end def update_cur_from_load(…)
# end class Board


def mymain():
    '''wrapper for test/start code so that variables do not look like constants'''
    # pylint: disable=protected-access
    print("Board class being run directly")
    # print('file', __file__)  # DEBUG
    # print(os.path.realpath(__file__))  # DEBUG
    # print(os.path.abspath(__file__))  # DEBUG
    # print(os.path.dirname(os.path.realpath(__file__)))  # DEBUG
    # print(os.path.dirname(os.path.abspath(__file__)))  # DEBUG
    # print('cwd:', os.getcwd())  # DEBUG

    brd = Board()
    # brd._current_open_path = os.getcwd() + '/..'
    brd.load_from_file()
    print('cur open dir: {}'.format(brd._current_open_path))  # DEBUG
    print('cur save dir: {}'.format(brd._current_save_path))  # DEBUG
    print('initial file: {}'.format(brd.initial_file))  # DEBUG


# Standalone module execution
if __name__ == "__main__":
    mymain()
