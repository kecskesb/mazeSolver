import random
import time
from tkinter import Tk, Canvas


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2)
        canvas.pack()


class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk(className="mazeSolver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = Canvas(width=self.width, height=self.height)
        self.canvas.pack()
        self.running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line: Line, fill_color):
        line.draw(self.canvas, fill_color)


class Cell:
    def __init__(self, x1: int, y1: int, x2: int, y2: int, win: Window = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__win = win
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.visited = False

    def draw(self):
        black = "black"
        white = "#d9d9d9"
        fill_color = black if self.has_left_wall else white
        self.__win.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)), fill_color)
        fill_color = black if self.has_right_wall else white
        self.__win.draw_line(Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)), fill_color)
        fill_color = black if self.has_top_wall else white
        self.__win.draw_line(Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)), fill_color)
        fill_color = black if self.has_bottom_wall else white
        self.__win.draw_line(Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)), fill_color)

    def draw_move(self, to_cell, undo=False):
        if undo:
            fill_color = "gray"
        else:
            fill_color = "red"
        own_x = (self.__x1 + self.__x2) // 2
        own_y = (self.__y1 + self.__y2) // 2
        other_x = (to_cell.__x1 + to_cell.__x2) // 2
        other_y = (to_cell.__y1 + to_cell.__y2) // 2
        self.__win.draw_line(Line(Point(own_x, own_y), Point(other_x, other_y)), fill_color)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win: Window = None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [[Cell(self.x1 + i * self.cell_size_x, self.y1 + j * self.cell_size_y,
                             self.x1 + i * self.cell_size_x + self.cell_size_x, self.y1 + j * self.cell_size_y + self.cell_size_y,
                             self.win) for i in range(self.num_rows)] for j in range(self.num_cols)]
        for col in self._cells:
            for cell in col:
                cell.draw()
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.03)

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        exit_cell = self._cells[-1][-1]
        entrance_cell.has_top_wall = False
        entrance_cell.has_bottom_wall = False
        entrance_cell.has_left_wall = False
        entrance_cell.has_right_wall = False
        entrance_cell.draw()

        exit_cell.has_top_wall = False
        exit_cell.has_bottom_wall = False
        exit_cell.has_left_wall = False
        exit_cell.has_right_wall = False
        exit_cell.draw()

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            possible_directions = []
            if i > 0 and not self._cells[i - 1][j].visited:
                possible_directions.append("u")
            if i < self.num_cols - 1 and not self._cells[i + 1][j].visited:
                possible_directions.append("d")
            if j > 0 and not self._cells[i][j - 1].visited:
                possible_directions.append("l")
            if j < self.num_rows - 1 and not self._cells[i][j + 1].visited:
                possible_directions.append("r")
            if len(possible_directions) == 0:
                self._cells[i][j].draw()
                return
            direction = random.choice(possible_directions)
            if direction == "u":
                self._cells[i][j].has_top_wall = False
                self._cells[i - 1][j].has_bottom_wall = False
                self._break_walls_r(i - 1, j)
            elif direction == "d":
                self._cells[i][j].has_bottom_wall = False
                self._cells[i + 1][j].has_top_wall = False
                self._break_walls_r(i + 1, j)
            elif direction == "l":
                self._cells[i][j].has_left_wall = False
                self._cells[i][j - 1].has_right_wall = False
                self._break_walls_r(i, j - 1)
            elif direction == "r":
                self._cells[i][j].has_right_wall = False
                self._cells[i][j + 1].has_left_wall = False
                self._break_walls_r(i, j + 1)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if self._cells[i][j] == self._cells[-1][-1]:
            return True
        if i > 0 and not self._cells[i][j].has_top_wall and not self._cells[i - 1][j].visited:
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i - 1][j], True)
        if not self._cells[i][j].has_bottom_wall and not self._cells[i + 1][j].visited:
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i + 1][j], True)
        if j > 0 and not self._cells[i][j].has_left_wall and not self._cells[i][j - 1].visited:
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j - 1], True)
        if not self._cells[i][j].has_right_wall and not self._cells[i][j + 1].visited:
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j + 1], True)
        return False
