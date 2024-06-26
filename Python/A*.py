import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import heapq
from multiprocessing import Pool, cpu_count


class Node:
    def __init__(self, position, g=float("inf"), h=0, parent=None):
        self.position = position
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f or (self.f == other.f and self.h < other.h)


class BinaryHeap:
    def __init__(self):
        self.heap = []
        self.node_dict = {}

    def push(self, node):
        heapq.heappush(self.heap, node)
        self.node_dict[node.position] = node

    def pop(self):
        node = heapq.heappop(self.heap)
        del self.node_dict[node.position]
        return node

    def __bool__(self):
        return bool(self.heap)

    def __contains__(self, position):
        return position in self.node_dict

    def get(self, position):
        return self.node_dict.get(position)

    def update(self, node):
        old_node = self.node_dict[node.position]
        old_node.g = node.g
        old_node.h = node.h
        old_node.f = node.f
        old_node.parent = node.parent
        heapq.heapify(self.heap)


def process_neighbor(args):
    current, neighbor, end = args
    tentative_g = current.g + 1
    neighbor.g = tentative_g
    neighbor.h = AStar.manhattan_distance(neighbor.position, end)
    neighbor.f = neighbor.g + neighbor.h
    neighbor.parent = current
    return neighbor


class AStar:
    def __init__(self, grid):
        if not isinstance(grid, np.ndarray) or grid.ndim != 2:
            raise ValueError("Grid must be a 2D numpy array")
        self.grid = grid

    @staticmethod
    def manhattan_distance(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node):
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_pos = (node.position[0] + dx, node.position[1] + dy)
            if (
                0 <= new_pos[0] < self.grid.shape[0]
                and 0 <= new_pos[1] < self.grid.shape[1]
                and self.grid[new_pos] == 0
            ):
                neighbors.append(Node(new_pos))
        return neighbors

    def find_path(self, start, end):
        if not (
            0 <= start[0] < self.grid.shape[0] and 0 <= start[1] < self.grid.shape[1]
        ):
            raise ValueError("Start position is out of grid bounds")
        if not (0 <= end[0] < self.grid.shape[0] and 0 <= end[1] < self.grid.shape[1]):
            raise ValueError("End position is out of grid bounds")
        if self.grid[start] != 0 or self.grid[end] != 0:
            raise ValueError("Start or end position is an obstacle")

        start_node = Node(start, 0, self.manhattan_distance(start, end))
        end_node = Node(end)

        open_list = BinaryHeap()
        open_list.push(start_node)
        closed_set = set()

        path_history = []

        with Pool(processes=cpu_count()) as pool:
            while open_list:
                current = open_list.pop()

                path_history.append(self.reconstruct_path(current))

                if current.position == end:
                    return self.reconstruct_path(current), path_history

                closed_set.add(current.position)

                neighbors = self.get_neighbors(current)
                args = [
                    (current, neighbor, end)
                    for neighbor in neighbors
                    if neighbor.position not in closed_set
                ]
                processed_neighbors = pool.map(process_neighbor, args)

                for neighbor in processed_neighbors:
                    if neighbor.position not in open_list:
                        open_list.push(neighbor)
                    elif neighbor.g < open_list.get(neighbor.position).g: # type: ignore
                        open_list.update(neighbor)

        return [], path_history

    @staticmethod
    def reconstruct_path(node):
        path = []
        while node:
            path.append(node.position)
            node = node.parent
        return path[::-1]


def filter_manhattan_path(path):
    if not path:
        return path
    filtered_path = [path[0]]
    for i in range(1, len(path)):
        prev = filtered_path[-1]
        curr = path[i]
        if abs(prev[0] - curr[0]) + abs(prev[1] - curr[1]) == 1:
            filtered_path.append(curr)
    return filtered_path


def visualize_path(grid, path, path_history, start, end):
    fig, ax = plt.subplots(figsize=(10, 10))

    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()  # type: ignore

    cmap = LinearSegmentedColormap.from_list("custom", ["#FFFFFF", "#2C3E50"], N=2)
    ax.imshow(grid, cmap=cmap)
    ax.set_title("A* Pathfinding Visualization", fontsize=16)

    (main_line,) = ax.plot([], [], color="#1B5E20", linewidth=5, alpha=0.9)
    (explore_line,) = ax.plot([], [], color="#FF1744", linewidth=3, alpha=0.7)
    (backtrack_line,) = ax.plot([], [], color="#1E88E5", linewidth=1, alpha=0.5)

    ax.plot(start[1], start[0], marker="*", color="#2ECC71", markersize=15)
    ax.plot(end[1], end[0], marker="*", color="#E67E22", markersize=15)

    ax.set_xticks([])
    ax.set_yticks([])

    def update(frame):
        if frame < len(path_history):
            explore_path = filter_manhattan_path(path_history[frame])
            if explore_path:
                explore_x, explore_y = zip(*explore_path)
                explore_line.set_data(explore_y, explore_x)

            backtrack_paths = [
                filter_manhattan_path(p) for p in path_history[: frame + 1]
            ]
            backtrack_x, backtrack_y = [], []
            for p in backtrack_paths:
                if p:
                    x, y = zip(*p)
                    backtrack_x.extend(x)
                    backtrack_y.extend(y)
                    backtrack_x.append(None)
                    backtrack_y.append(None)
            backtrack_line.set_data(backtrack_y, backtrack_x)

        if frame == len(path_history) - 1:
            if path:
                main_path = filter_manhattan_path(path)
                main_x, main_y = zip(*main_path)
                main_line.set_data(main_y, main_x)
        return main_line, explore_line, backtrack_line

    ani = animation.FuncAnimation(
        fig, update, frames=len(path_history), interval=1, blit=True, repeat=False
    )

    plt.tight_layout()
    plt.show()


def main():
    try:
        grid_size = 100
        grid = np.random.choice([0, 1], size=(grid_size, grid_size), p=[0.7, 0.3])

        start = (0, 0)
        end = (grid_size - 1, grid_size - 1)
        grid[start] = grid[end] = 0

        print("Finding path...")
        astar = AStar(grid)
        path, path_history = astar.find_path(start, end)

        if path:
            print("Path found. Visualizing...")
        else:
            print("No path found. Visualizing exploration...")

        visualize_path(grid, path, path_history, start, end)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
