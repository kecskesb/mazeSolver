from classes import Window, Maze


def main():
    win = Window(1610, 1210)

    maze = Maze(5, 5, 40, 30, 40, 40, win)
    maze.solve()

    win.wait_for_close()


if __name__ == '__main__':
    main()
