from classes import Window, Maze


def main():
    win = Window(810, 610)

    maze = Maze(5, 5, 20, 15, 40, 40, win)
    print(maze.solve())

    win.wait_for_close()


if __name__ == '__main__':
    main()
