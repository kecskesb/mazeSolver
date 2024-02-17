import unittest
from mazeSolver import Maze, Window


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, Window(120, 100))
        self.assertEqual(len(m1._cells), num_cols)
        self.assertEqual(len(m1._cells[0]), num_rows)

    def test_maze_break_entrance_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, Window(120, 100))
        self.assertFalse(m1._cells[0][0].has_top_wall)
        self.assertFalse(m1._cells[0][0].has_bottom_wall)
        self.assertFalse(m1._cells[0][0].has_left_wall)
        self.assertFalse(m1._cells[0][0].has_right_wall)

        self.assertFalse(m1._cells[-1][-1].has_top_wall)
        self.assertFalse(m1._cells[-1][-1].has_bottom_wall)
        self.assertFalse(m1._cells[-1][-1].has_left_wall)
        self.assertFalse(m1._cells[-1][-1].has_right_wall)

    def test_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, Window(120, 100))
        self.assertFalse(m1._cells[2][0].visited)
        self.assertFalse(m1._cells[5][2].visited)
        self.assertFalse(m1._cells[10][5].visited)


if __name__ == '__main__':
    unittest.main()
