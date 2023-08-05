#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Jesse Rubin - py_euler sodoku.pyx test_pupy
"""
testing my sodoku.pyx solver

ty sudopedia
http://sudopedia.enjoysudoku.com/Invalid_Test_Cases.html
http://sudopedia.enjoysudoku.com/Valid_Test_Cases.html
"""

from pupy.sodoku import SodokuError, Sodoku
from pytest import raises


class Test_SodokuMethods(object):

    def test_neighbors(self):
        """

        """
        a = {0: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 72, 18, 19, 20, 27, 36, 45, 54, 63},
             13: {3, 4, 5, 67, 9, 10, 11, 12, 76, 14, 15, 16, 17, 21, 22, 23, 31, 40, 49, 58},
             14: {3, 4, 5, 68, 9, 10, 11, 12, 13, 77, 15, 16, 17, 21, 22, 23, 32, 41, 50, 59},
             22: {3, 4, 5, 67, 12, 13, 14, 76, 18, 19, 20, 21, 23, 24, 25, 26, 31, 40, 49, 58},
             23: {3, 4, 5, 68, 12, 13, 14, 77, 18, 19, 20, 21, 22, 24, 25, 26, 32, 41, 50, 59},
             35: {71, 8, 80, 17, 26, 27, 28, 29, 30, 31, 32, 33, 34, 42, 43, 44, 51, 52, 53, 62},
             43: {70, 7, 79, 16, 25, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 51, 52, 53, 61},
             52: {70, 7, 79, 16, 25, 33, 34, 35, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 53, 61}}

        for k, v in a.items():
            assert Sodoku.neighbors(k) == v

    def test_str_too(self):
        """

        """
        so_do_ku = ['123456789',
                    '123456789',
                    '123456789',
                    '123456789',
                    '123456789',
                    '123456789',
                    '123456789',
                    '123456789',
                    '123456789']
        s = Sodoku(''.join(so_do_ku))
        split_board = ['  S   O   D   O   K   U  ',
                       '╔═══════╦═══════╦═══════╗',
                       '║ 1 2 3 ║ 4 5 6 ║ 7 8 9 ║',
                       '║ 1 2 3 ║ 4 5 6 ║ 7 8 9 ║',
                       '║ 1 2 3 ║ 4 5 6 ║ 7 8 9 ║',
                       '╠═══════╬═══════╬═══════╣',
                       '║ 1 2 3 ║ 4 5 6 ║ 7 8 9 ║',
                       '║ 1 2 3 ║ 4 5 6 ║ 7 8 9 ║',
                       '║ 1 2 3 ║ 4 5 6 ║ 7 8 9 ║',
                       '╠═══════╬═══════╬═══════╣',
                       '║ 1 2 3 ║ 4 5 6 ║ 7 8 9 ║',
                       '║ 1 2 3 ║ 4 5 6 ║ 7 8 9 ║',
                       '║ 1 2 3 ║ 4 5 6 ║ 7 8 9 ║',
                       '╚═══════╩═══════╩═══════╝']
        assert '\n'.join(split_board) == s.__str__()
        assert True

    class Test_Not_Enough_Info(object):

        def test_empty_board(self):
            """

            """
            # empty board
            test_board = '.................................................................................'
            s = Sodoku(test_board)
            with raises(SodokuError):
                s.solve()

        def test_one_cell_given(self):
            """

            """
            # one cell
            test_board = '........................................1........................................'
            s = Sodoku(test_board)
            with raises(SodokuError):
                s.solve()

        def test_lt16_cells_given(self):
            """

            """
            # less than 16 values
            test_board = '...........5....9...4....1.2....3.5....7.....438...2......9.....1.4...6..........'
            s = Sodoku(test_board)
            with raises(SodokuError):
                s.solve()

    class Test_Duplicate(object):

        def test_duplicate_col(self):
            """

            """
            badcol = '6.159.....9..1............4.7.314..6.24.....5..3....1...6.....3...9.2.4......16..'
            with raises(SodokuError):
                sbc = Sodoku(badcol)
                sbc.solve()

        def test_duplicate_row(self):
            """

            """
            badrow = '.4.1..35.............2.5......4.89..26.....12.5.3....7..4...16.6....7....1..8..2.'
            with raises(SodokuError):
                sbr = Sodoku(badrow)
                sbr.solve()

        def test_duplicate_box(self):
            """

            """
            badbox = '..9.7...5..21..9..1...28....7...5..1..851.....5....3.......3..68........21.....87'
            with raises(SodokuError):
                sbb = Sodoku(badbox)
                sbb.solve()

    class Test_Unsolvable(object):

        def test_row_unsolvable(self):
            """

            """
            test_b = '9..1....4.14.3.8....3....9....7.8..18....3..........3..21....7...9.4.5..5...16..3'
            sodo = Sodoku(test_b)
            with raises(SodokuError):
                sodo.solve()

        def test_col_unsolvable(self):
            """

            """
            test_b = '....41....6.....2...2......32.6.........5..417.......2......23..48......5.1..2...'
            sodo = Sodoku(test_b)
            with raises(SodokuError):
                sodo.solve()

        def test_box_unsolvable(self):
            """

            """
            test_b = '.9.3....1....8..46......8..4.5.6..3...32756...6..1.9.4..1......58..2....2....7.6.'
            sodo = Sodoku(test_b)
            with raises(SodokuError):
                sodo.solve()

        def test_square_unsolvable(self):
            """

            """
            test_b = '..9.287..8.6..4..5..3.....46.........2.71345.........23.....5..9..4..8.7..125.3..'
            sodo = Sodoku(test_b)
            with raises(SodokuError):
                # sbc = Sodoku.from_oneline_str(badcol)
                sodo.solve()

    class TestValidCases(object):

        def test_already_solved(self):
            """

            """
            test_board = '974236158638591742125487936316754289742918563589362417867125394253649871491873625'
            s = Sodoku(test_board)
            s.solve()
            s_solved = s.get_oneline_str()
            assert s_solved == test_board

        def test_one_empty_square(self):
            """

            """
            test_board = '2564891733746159829817234565932748617128.6549468591327635147298127958634849362715'
            test_solution = '256489173374615982981723456593274861712836549468591327635147298127958634849362715'
            assert len(test_board) == len(test_solution)
            s = Sodoku(test_board)
            s.solve()
            s_solved = s.get_oneline_str()
            assert s_solved == test_solution
            # assert

        def test_hidden_singles(self):
            """

            """
            test_board = '..2.3...8' \
                         '.....8...' \
                         '.31.2....' \
                         '.6..5.27.' \
                         '.1.....5.' \
                         '2.4.6..31' \
                         '....8.6.5' \
                         '.......13' \
                         '..531.4..'
            test_solution = '672435198' \
                            '549178362' \
                            '831629547' \
                            '368951274' \
                            '917243856' \
                            '254867931' \
                            '193784625' \
                            '486592713' \
                            '725316489'
            assert len(test_board) == len(test_solution)
            s = Sodoku(test_board)
            s.solve()
            s_solved = s.get_oneline_str()
            assert s_solved == test_solution

        def test_naked_singles(self):
            """

            """
            test_board = '3.542.81.' \
                         '4879.15.6' \
                         '.29.56374' \
                         '85.793.41' \
                         '6132.8957' \
                         '.74.6528.' \
                         '2413.9.65' \
                         '5.867.192' \
                         '.965124.8'
            test_solution = '365427819' \
                            '487931526' \
                            '129856374' \
                            '852793641' \
                            '613248957' \
                            '974165283' \
                            '241389765' \
                            '538674192' \
                            '796512438'

            assert len(test_board) == len(test_solution)
            s = Sodoku(test_board)
            s.solve()
            s_solved = s.board
            assert s_solved == test_solution
