import argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]


def Grid(N, file_name):
    grid = np.zeros((N, N))
    x_value = 0
    y_value = 0
    x = 0
    y = 0
    paramArgument = 0
    file = open(file_name, "r")
    lines = file.readlines()
    for inputline in lines:
        if inputline[0] == "#" or inputline[0] == "x":
            continue

        for i in inputline:
            if paramArgument == 0:
                param = 1
            else:
                param = paramArgument
            if i == 'b':
                x += param
                paramArgument = 0
            elif i == 'o':
                while param > 0:
                    grid[x, y] = ON
                    x = x + 1
                    param = param - 1
                paramArgument = 0
            elif i == '$':
                y += param
                x = 0
                paramArgument = 0
            elif '0' <= i <= '9':
                paramArgument = 10 * paramArgument + int(i)
            elif i == "!":
                break
    return grid


def update(frameNum, img, grid):
    newGrid = grid.copy()
    N = grid.shape[0]
    for i in range(N):
        for j in range(N):
            total = int((grid[i, (j - 1) % N] + grid[i, (j + 1) % N] +
                         grid[(i - 1) % N, j] + grid[(i + 1) % N, j] +
                         grid[(i - 1) % N, (j - 1) % N] + grid[(i - 1) % N, (j + 1) % N] +
                         grid[(i + 1) % N, (j - 1) % N] + grid[(i + 1) % N, (j + 1) % N]) / 255)

            if grid[i, j] == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON

    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,


def main():
    parser = argparse.ArgumentParser(
        description="Runs Conway's Game of Life simulation.")

    parser.add_argument('--file-name', dest='file_name', required=True)
    parser.add_argument('--generations', dest='gen', required=True)
    parser.add_argument('--show-animation', dest='anim', required=True)
    args = parser.parse_args()
    N = 300

    grid = Grid(N, args.file_name)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    if args.anim == "False":
        gen = int(args.gen)
        while gen > 0:
            update(1, img, grid)
            gen = gen - 1
    else:
        ani = animation.FuncAnimation(fig, update, fargs=(
            img, grid,), interval=50)

    plt.show()


# call main
if __name__ == '__main__':
    main()
