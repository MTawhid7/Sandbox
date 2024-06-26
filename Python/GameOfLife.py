import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


# Initialize the grid
def initialize_grid(size):
    return np.random.choice([0, 1], size * size, p=[0.8, 0.2]).reshape(size, size)


# Update the grid based on Conway's Game of Life rules
def update_grid(grid):
    new_grid = grid.copy()
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            total = int(
                (
                    grid[i, (j - 1) % grid.shape[1]]
                    + grid[i, (j + 1) % grid.shape[1]]
                    + grid[(i - 1) % grid.shape[0], j]
                    + grid[(i + 1) % grid.shape[0], j]
                    + grid[(i - 1) % grid.shape[0], (j - 1) % grid.shape[1]]
                    + grid[(i - 1) % grid.shape[0], (j + 1) % grid.shape[1]]
                    + grid[(i + 1) % grid.shape[0], (j - 1) % grid.shape[1]]
                    + grid[(i + 1) % grid.shape[0], (j + 1) % grid.shape[1]]
                )
            )

            # Apply Conway's rules
            if grid[i, j] == 1:
                if (total < 2) or (total > 3):
                    new_grid[i, j] = 0
            else:
                if total == 3:
                    new_grid[i, j] = 1
    return new_grid


# Animation function
def animate(frame, img, grid):
    new_grid = update_grid(grid)
    img.set_data(new_grid)
    grid[:] = new_grid[:]
    return (img,)


# Click event handler
def on_click(event, grid, img):
    if event.inaxes is not None:
        ix, iy = int(event.xdata), int(event.ydata)
        grid[iy, ix] = 1 - grid[iy, ix]  # Toggle the cell state
        img.set_data(grid)
        plt.draw()


# Main function
def main():
    size = 75
    grid = initialize_grid(size)

    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation="nearest", cmap="tab10")

    # Connect the click event handler
    fig.canvas.mpl_connect(
        "button_press_event", lambda event: on_click(event, grid, img)
    )

    ani = animation.FuncAnimation(
        fig, animate, fargs=(img, grid), frames=10, interval=100, save_count=50
    )

    plt.show()


if __name__ == "__main__":
    main()
