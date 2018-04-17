#!bin/python
# coding=utf-8

'''
unitests for the board module
'''

# using virtualenv
#   source bin/activate

__author__ = 'H Phil Duby'

# https://wiki.python.org/moin/PyUnit
# https://docs.python.org/3.5/library/unittest.html
import unittest
import unittest.mock
from board import Board


class TestEmptyBoard(unittest.TestCase):
    '''Do tests for an empty board'''
    def setUp(self):
        '''[re]Create empty board for each test'''
        self.brd = Board()

    def test_states_is_empty(self):
        '''there should not be any states for an empty board'''
        self.assertIsNone(self.brd.states)

    def test_dimensions_is_integer(self):
        '''empty board dimensions should be an integer'''
        self.assertTrue(isinstance(self.brd.dimensions, int))

    def test_dimensions_is_zero(self):
        '''empty board should have zero dimensions'''
        self.assertEqual(self.brd.dimensions, 0)

    def test_board_config_is_empty(self):
        '''empty board should not have any configuration'''
        self.assertIsNone(self.brd.config)

    def test_current_open_directory_is_empty(self):
        '''empty board should not have a current open path'''
        self.assertIsNone(self.brd._current_open_path)

    def test_current_save_directory_is_empty(self):
        '''empty board should not have a current save path'''
        self.assertIsNone(self.brd._current_save_path)

    def test_initial_file_is_empty(self):
        '''empty board should not have an initial file'''
        self.assertIsNone(self.brd.initial_file)

    def test_initial_paths_not_locked(self):
        '''empty board should not have a lock'''
        self.assertFalse(self.brd.lock_initial)


@unittest.skip("mocking not ready")
class TestLoadFromFile(unittest.TestCase):
    '''mock some tkinter methods for next level of board tests'''
    def setUp(self):
        '''[re]Create empty board for each test'''
        self.brd = Board()

    # https://stackoverflow.com/questions/42407302/unittest-tkinter-file-dialog-for-python-3-5
    # @mock.patch(Board.tkf)
    # @mock.patch(Board.Tkinter)
    # @mock.patch(Board.tkinter)
    # @mock.patch(Board.tkinter)
    # @unittest.mock.patch(Board.tkinter)
    # @unittest.mock.patch(Board.tkf)
    # @unittest.mock.patch(Board.Tkinter)
    # https://stackoverflow.com/questions/42407302/unittest-tkinter-file-dialog-for-python-3-5
    def test_cancel_file_open(self, mock_tkf):
        '''simulate canceling a file open'''
        pass


if __name__ == '__main__':
    unittest.main()
