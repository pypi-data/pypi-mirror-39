# coding=utf-8
# Copyright 2018 The Cirq Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import absolute_import
from typing import Callable, Dict, List, NamedTuple, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from typing import Tuple, Dict, Optional

_HorizontalLine = NamedTuple(u'HorizontalLine', [
    (u'y', int),
    (u'x1', int),
    (u'x2', int),
    (u'emphasize', bool),
])
_VerticalLine = NamedTuple(u'VerticalLine', [
    (u'x', int),
    (u'y1', int),
    (u'y2', int),
    (u'emphasize', bool),
])
_DiagramText = NamedTuple(u'DiagramText', [
    (u'text', unicode),
    (u'transposed_text', unicode),
])


class TextDiagramDrawer(object):
    u"""A utility class for creating simple text diagrams.
    """

    def __init__(self):
        self.entries = dict()  # type: Dict[Tuple[int, int], _DiagramText]
        self.vertical_lines = []  # type: List[_VerticalLine]
        self.horizontal_lines = []  # type: List[_HorizontalLine]
        self.horizontal_padding = {}  # type: Dict[int, int]
        self.vertical_padding = {}  # type: Dict[int, int]

    def write(self, x, y, text, transposed_text = None):
        u"""Adds text to the given location.

        Args:
            x: The column in which to write the text.
            y: The row in which to write the text.
            text: The text to write at location (x, y).
            transposted_text: Optional text to write instead, if the text
                diagram is transposed.
        """
        entry = self.entries.get((x, y), _DiagramText(u'', u''))
        self.entries[(x, y)] = _DiagramText(
            entry.text + text,
            entry.transposed_text + (transposed_text if transposed_text
                                                     else text))

    def content_present(self, x, y):
        u"""Determines if a line or printed text is at the given location."""

        # Text?
        if (x, y) in self.entries:
            return True

        # Vertical line?
        if any(v.x == x and v.y1 < y < v.y2 for v in self.vertical_lines):
            return True

        # Horizontal line?
        if any(line_y == y and x1 < x < x2
               for line_y, x1, x2, _ in self.horizontal_lines):
            return True

        return False

    def grid_line(self, x1, y1, x2, y2,
                  emphasize = False):
        u"""Adds a vertical or horizontal line from (x1, y1) to (x2, y2).

        Horizontal line is selected on equality in the second coordinate and
        vertical line is selected on equality in the first coordinate.

        Raises:
            ValueError: If line is neither horizontal nor vertical.
        """
        if x1 == x2:
            self.vertical_line(x1, y1, y2, emphasize)
        elif y1 == y2:
            self.horizontal_line(y1, x1, x2, emphasize)
        else:
            raise ValueError(u"Line is neither horizontal nor vertical")

    def vertical_line(self, x, y1, y2, emphasize = False
                      ):
        u"""Adds a line from (x, y1) to (x, y2)."""
        y1, y2 = sorted([y1, y2])
        self.vertical_lines.append(_VerticalLine(x, y1, y2, emphasize))

    def horizontal_line(self, y, x1, x2, emphasize = False
                        ):
        u"""Adds a line from (x1, y) to (x2, y)."""
        x1, x2 = sorted([x1, x2])
        self.horizontal_lines.append(_HorizontalLine(y, x1, x2, emphasize))

    def transpose(self):
        u"""Returns the same diagram, but mirrored across its diagonal."""
        out = TextDiagramDrawer()
        out.entries = dict(((y, x), _DiagramText(v.transposed_text, v.text))
                       for (x, y), v in self.entries.items())
        out.vertical_lines = [_VerticalLine(*e)
                              for e in self.horizontal_lines]
        out.horizontal_lines = [_HorizontalLine(*e)
                                for e in self.vertical_lines]
        out.vertical_padding = self.horizontal_padding.copy()
        out.horizontal_padding = self.vertical_padding.copy()
        return out

    def width(self):
        u"""Determines how many entry columns are in the diagram."""
        max_x = -1
        for x, _ in self.entries.keys():
            max_x = max(max_x, x)
        for v in self.vertical_lines:
            max_x = max(max_x, v.x)
        for h in self.horizontal_lines:
            max_x = max(max_x, h.x1, h.x2)
        return 1 + max_x

    def height(self):
        u"""Determines how many entry rows are in the diagram."""
        max_y = -1
        for _, y in self.entries.keys():
            max_y = max(max_y, y)
        for h in self.horizontal_lines:
            max_y = max(max_y, h.y)
        for v in self.vertical_lines:
            max_y = max(max_y, v.y1, v.y2)
        return 1 + max_y

    def force_horizontal_padding_after(self, index, padding):
        u"""Change the padding after the given column."""
        self.horizontal_padding[index] = padding

    def force_vertical_padding_after(self, index, padding):
        u"""Change the padding after the given row."""
        self.vertical_padding[index] = padding

    def _transform_coordinates(
        self, func):
        u"""Helper method to transformer either row or column coordinates."""
        def func_x(x):
            return func(x, 0)[0]
        def func_y(y):
            return func(0, y)[1]
        self.entries = dict((func(x, y), v) for (x, y), v in self.entries.items())
        self.vertical_lines = [
            _VerticalLine(func_x(x), func_y(y1), func_y(y2), emph)
            for x, y1, y2, emph in self.vertical_lines]
        self.horizontal_lines = [
            _HorizontalLine(func_y(y), func_x(x1), func_x(x2), emph)
            for y, x1, x2, emph in self.horizontal_lines]
        self.horizontal_padding = dict((func_x(x), padding)
            for x, padding in self.horizontal_padding.items())
        self.vertical_padding = dict((func_y(y), padding)
            for y, padding in self.vertical_padding.items())

    def insert_empty_columns(self, x, amount = 1):
        u"""Insert a number of columns after the given column."""
        def transform_columns(column, row):
            return column + (amount if column >= x else 0), row
        self._transform_coordinates(transform_columns)

    def insert_empty_rows(self, y, amount = 1):
        u"""Insert a number of rows after the given row."""
        def transform_rows(column, row):
            return column, row + (amount if row >= y else 0)
        self._transform_coordinates(transform_rows)

    def render(self,
               horizontal_spacing = 1,
               vertical_spacing = 1,
               crossing_char = None,
               use_unicode_characters = True):
        u"""Outputs text containing the diagram."""

        char = _normal_char if use_unicode_characters else _ascii_char

        w = self.width()
        h = self.height()

        grid = [[u''] * w for _ in xrange(h)]
        horizontal_separator = [[u' '] * w for _ in xrange(h)]
        vertical_separator = [[u' '] * w for _ in xrange(h)]

        # Place lines.
        verticals = {
            (v.x, y): v.emphasize
            for v in self.vertical_lines
            for y in xrange(v.y1, v.y2)
        }
        horizontals = {
            (x, h.y): h.emphasize
            for h in self.horizontal_lines
            for x in xrange(h.x1, h.x2)
        }
        for (x, y), emph in verticals.items():
            c = char(u'│', emph)
            grid[y][x] = c
            vertical_separator[y][x] = c
        for (x, y), emph in horizontals.items():
            c = char(u'─', emph)
            grid[y][x] = c
            horizontal_separator[y][x] = c
        for x, y in set(horizontals.keys()) & set(verticals.keys()):
            grid[y][x] = crossing_char or _cross_char(
                not use_unicode_characters,
                horizontals[(x, y)],
                verticals[(x, y)])

        # Place entries.
        for (x, y), v in self.entries.items():
            grid[y][x] = v.text

        # Pad rows and columns to fit contents with desired spacing.
        multiline_grid = _pad_into_multiline(w,
                                             grid,
                                             horizontal_separator,
                                             vertical_separator,
                                             horizontal_spacing,
                                             vertical_spacing,
                                             self.horizontal_padding,
                                             self.vertical_padding)

        # Concatenate it all together.
        return u'\n'.join(u''.join(sub_row).rstrip()
                         for row in multiline_grid
                         for sub_row in row).rstrip()


_BoxChars = [
    (u'─', u'━', u'-'),
    (u'│', u'┃', u'|'),
    (u'┌', u'┏', u'/'),
    (u'└', u'┗', u'\\'),
    (u'┐', u'┓', u'\\'),
    (u'┘', u'┛', u'/'),
    (u'├', u'┣', u'>'),
    (u'┼', u'╋', u'+'),
    (u'┤', u'┫', u'<'),
    (u'┬', u'┳', u'v'),
    (u'┴', u'┻', u'^'),
]  # type: List[Tuple[str, ...]]

_EmphasisMap = dict((k, v) for k, v, _ in _BoxChars)
_AsciiMap = dict((k, v) for k, _, v in _BoxChars)


def _normal_char(k, emphasize = False):
    return _EmphasisMap.get(k, k) if emphasize else k


def _ascii_char(k, emphasize = False):
    del emphasize
    return _AsciiMap.get(k, k)


def _cross_char(use_ascii, horizontal_emph, vertical_emph
                ):
    if use_ascii:
        return u'+'
    if horizontal_emph != vertical_emph:
        return u'┿' if horizontal_emph else u'╂'
    return _normal_char(u'┼', horizontal_emph)


def _pad_into_multiline(width,
                        grid,
                        horizontal_separator,
                        vertical_separator,
                        horizontal_spacing,
                        vertical_spacing,
                        horizontal_padding,
                        vertical_padding
                        ):
    multiline_grid = []  # type: List[List[List[str]]]

    # Vertical padding.
    for row in xrange(len(grid)):
        multiline_cells = [cell.split(u'\n') for cell in grid[row]]
        row_height = max(1, max(len(cell) for cell in multiline_cells))
        row_height += vertical_padding.get(row, vertical_spacing)

        multiline_row = []
        for sub_row in xrange(row_height):
            sub_row_cells = []
            for col in xrange(width):
                cell_lines = multiline_cells[col]
                sub_row_cells.append(cell_lines[sub_row]
                                     if sub_row < len(cell_lines)
                                     else vertical_separator[row][col])
            multiline_row.append(sub_row_cells)

        multiline_grid.append(multiline_row)

    # Horizontal padding.
    for col in xrange(width):
        col_width = max(1, max(len(sub_row[col])
                               for row in multiline_grid
                               for sub_row in row))
        col_width += horizontal_padding.get(col, horizontal_spacing)
        for row in xrange(len(multiline_grid)):
            for sub_row in xrange(len(multiline_grid[row])):
                sub_row_contents = multiline_grid[row][sub_row]
                pad_char = (horizontal_separator[row][col]
                            if sub_row == 0
                            else u' ')
                sub_row_contents[col] = sub_row_contents[col].ljust(
                    col_width, pad_char)

    return multiline_grid
