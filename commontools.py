#!bin/python3
# coding=utf-8

'''A few commontools to use with other modules in the current application'''

from enum import Enum
import uuid


def constant(function_):
    '''Annotation to create something closer to real constants'''

    # pylint: disable=unused-argument
    def fset(self, value):
        '''Do not allow constants to be set'''
        raise TypeError

    def fget(self):
        '''Return the actual constant value'''
        return function_()
    # pylint: enable=unused-argument

    return property(fget, fset)


def random_id():
    '''Return a randomly generated uuid'''
    return ''.join(['u', str(uuid.uuid4())])


class XmlLintChecker:
    '''Process subprocess result for xmllint command'''

    @constant
    def NOSTDERR():  # pylint: disable=invalid-name
        # pylint: disable=no-method-argument
        '''Return constant informational message when the subprocess result
        does not include stderr output.
        '''
        return 'info: no stderr included with CompletedProcess results'

    def __init__(self):
        # https://bytebaker.com/2008/11/03/switch-case-statement-in-python/
        self.result_statuses = {
            0: 'valid',
            1: 'unclassified',
            2: 'bad_dtd',
            3: 'xml_not_valid',
            5: 'schema_error',
        }
        # 0 No error
        # 1 Unclassified
        # 2 Error in DTD
        # 3 Validation error
        # 4 Validation error
        # 5 Error in schema compilation
        # 6 Error writing output
        # 7 Error in pattern (generated when --pattern option is used)
        # 8 Error in Reader registration (generated when --chkregister option
        #   is used)
        # 9 Out of memory error
    # end def __init__(…)

    def parse(self, result):
        '''Return the parsed subprocess result'''
        try:
            rslt = {'state': self.result_statuses[result.returncode]}
            rslt['message'] = result.stderr if isinstance(
                result.stderr, type(None)) else self.NOSTDERR
        except KeyError as key_error:
            print('XmlLintChecker parse failed: key={}'.format(
                key_error))  # DEBUG
            raise NotImplementedError(
                'xmllint return code {} handling not implemented'.format(
                    key_error)) from None
        return rslt
# end class XmlLintChecker


# IDEA turn this into (bit) flag values, so can 'or' combinations together
class BoxSide(Enum):
    '''Setup names for the possible sides of a 2 dimensional box (rectangle)'''
    LEFT = 0
    TOP = 1  # pylint: disable=invalid-name
    RIGHT = 2
    BOTTOM = 3
    ALL = 4
# end class BoxSide


class BoundingBox2D:
    '''Manage a 2 dimensional bounding box'''

    @constant
    def STR_LAYOUT():  # pylint: disable=invalid-name
        # pylint: disable=no-method-argument
        '''Return constant format string for displaying a 2D bounding box'''
        return '[{} {}][{} {}]'

    def __init__(self, minX, minY, maxX, maxY):
        '''
        screen coordinate system, with y increasing downward
        '''
        self.top = minY
        self.left = minX
        self.bottom = maxY
        self.right = maxX
    # end def __init__(…)

    def __str__(self):
        return str.format(
            self.STR_LAYOUT, self.left, self.top, self.right, self.bottom)
    # end def __str__(…)

    def shrink(self, side: BoxSide):
        '''Shrink the bounding box one step on the specified side(s)'''
        # pylint: disable=too-many-branches
        if side == BoxSide.TOP:
            if self.top < self.bottom:
                self.top += 1
                return
            raise IndexError('top >= bottom') from None
        if side == BoxSide.BOTTOM:
            if self.bottom > self.top:
                self.bottom -= 1
                return
            raise IndexError('bottom <= top') from None
        if side == BoxSide.LEFT:
            if self.left < self.right:
                self.left += 1
                return
            raise IndexError('left >= right') from None
        if side == BoxSide.RIGHT:
            if self.right > self.left:
                self.right -= 1
                return
            raise IndexError('right < left') from None
        if side == BoxSide.ALL:
            if self.top < self.bottom:
                self.top += 1
                if self.bottom > self.top:
                    self.bottom -= 1
            else:
                raise IndexError('top >= bottom') from None
            if self.left < self.right:
                self.left += 1
                if self.right > self.left:
                    self.right -= 1
                return
            raise IndexError('left >= right') from None

        if isinstance(side, BoxSide):
            raise NotImplementedError(str.format(
                'shrink handling for the {} side has not been implemented',
                side.name)) from None
        raise TypeError('side must be a BoxSide enum') from None
    # end def shrink(…)

    def expand(self, side: BoxSide, amount=1):
        # pylint: disable=unused-argument
        '''Increase the 2D bounding box by 1 step on the specified side(s)'''
        if side == BoxSide.TOP:
            self.top -= 1
        elif side == BoxSide.BOTTOM:
            self.bottom += 1
        elif side == BoxSide.LEFT:
            self.left -= 1
        elif side == BoxSide.RIGHT:
            self.right += 1
        elif side == BoxSide.ALL:
            self.top -= 1
            self.bottom += 1
            self.left -= 1
            self.right += 1
        else:
            if isinstance(side, BoxSide):
                raise NotImplementedError(str.format(
                    'expand handling for the {} side has not been implemented',
                    side.name)) from None
            raise TypeError('side must be a BoxSide enum') from None
    # end def expand(…)
# end class BoundingBox2D
