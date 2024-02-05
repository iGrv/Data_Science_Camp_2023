import sys
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.patches import Patch
from matplotlib.colors import ListedColormap

ALIVE = 1
DEAD = 0

# Number of seconds to pause the figure showing
WAIT_SECS = 1

# Colors of alive and dead cells
COLOR_ALIVE = "limegreen"
COLOR_DEAD = "lightgray"


class MatrixSystem:
    """Representation of system which contains a cell matrix."""

    def __init__(self, matrix):
        if matrix.ndim != 2:
            raise ValueError("matrix is not a 2-D array")

        self.matrix = np.copy(matrix)
        self.height, self.width = self.matrix.shape
        self.state = 0

    @classmethod
    def generate(cls, shape):
        """
        Creates a `shape` (tuple `(height, width)`) size matrix which
        contains cells with randomly generated values `ALIVE` or `DEAD`.

        Returns instance of `MatrixSystem` with generated matrix.
        """

        # Get random matrix with specified shape
        random_matrix = np.random.choice([ALIVE, DEAD], size=shape)

        # Create a system with the random matrix
        return cls(random_matrix)

    def change_matrix(self):
        """
        Computes new values of cells in matrix as follows
            - if an alive cell has 2 or 3 alive neighboring cells, it keeps be alive
            - if an alive cell has 1 or 0 alive neighboring cells, it becomes dead due to "loneliness"
            - if an alive cell has 4 or more alive neighboring cells, it becomes dead due to "overpopulation"
            - if a dead cell has exactly 3 alive neighboring cells, it becomes alive

        Computed new values of cells are stored in the cell matrix.
        """

        # Matrix that represents values of cells in the next state
        new_matrix = np.copy(self.matrix)

        # Loop over all cells of matrix
        for i in range(self.height):
            for j in range(self.width):

                # Number of alive neighboring cells
                alives = self.alive_neighbors((i, j))

                # Alive cell becomes dead if it has a few or many alive neighboring cells
                if self.matrix[i, j] == ALIVE and (alives <= 1 or alives >= 4):
                    new_matrix[i, j] = DEAD

                # Dead cell becomes alive if it has three alive neighboring cells
                elif self.matrix[i, j] == DEAD and alives == 3:
                    new_matrix[i, j] = ALIVE

        # Transit to the next state matrix and increment number of state
        self.matrix = new_matrix  
        self.state += 1

    def alive_neighbors(self, cell):
        """
        Returns number of alive neighboring cells to `cell` which is a pair `(i, j)`.
        Each cell has eight alive neighboring cells.
        """

        # Array of neighboring cells
        neighbors = np.array([

            # Get cell in matrix by index with boundary conditions (use modulo)
            self.matrix[i % self.height, j % self.width]

            # Cells in range of one row and one colums from cell
            for i in range(cell[0] - 1, cell[0] + 2)
            for j in range(cell[1] - 1, cell[1] + 2)
            if (i, j) != cell  # Ignore cell itself
        ])

        # Count a number of neighboring cells which are alive
        return np.sum(neighbors == ALIVE)

    def visualize_simulation(self):
        """
        Performs simulation of matrix changes and visualizes it using Matplotlib.
        During the visualization repeatedly shows images of cell matrix
        at each iteration with a time interval.
        """
        def on_close(event):
            sys.exit()

        # Set on_close function such that the program exits when the figure closes
        plt.connect("close_event", on_close)

        # Create a colormap which contains colors of alive and dead cell
        cell_colors = [COLOR_DEAD, COLOR_ALIVE] if DEAD < ALIVE else [COLOR_ALIVE, COLOR_DEAD]
        cell_cmap = ListedColormap(colors=cell_colors)

        # Create rectangle patches with specified colors
        patches = [
            Patch(color=COLOR_ALIVE, label="Alive"),
            Patch(color=COLOR_DEAD, label="Dead")
        ]

        # Define the legend and set it ub upper left of the figure
        plt.legend(handles=patches, title="Cell", bbox_to_anchor=(-0.05, 1), loc="upper right")

        # Show matrix images on creation when the interactive mode is on
        with plt.ion():

            # Show an image of the initial state of matrix
            if self.state == 0:
                plt.title("Matrix in initial state")
                plt.imshow(self.matrix, origin="upper", cmap=cell_cmap)
                plt.pause(WAIT_SECS)
                self.change_matrix()

            # Simulate repeatedly changes of matrix and show they in the figure
            while True:
                plt.title(f"Matrix after iteration {self.state}")
                plt.imshow(self.matrix, origin="upper", cmap=cell_cmap)
                plt.pause(WAIT_SECS)
                self.change_matrix()


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python task2_2.py height width")

    # Get height and width of matrix
    try:
        matrix_height = int(sys.argv[1])
        if matrix_height < 1:
            sys.exit("Error! Height of matrix is not positive.")
    except ValueError:
        sys.exit("Error! Height of matrix is not a correct integer.")
    try:
        matrix_width = int(sys.argv[2])
        if matrix_width < 1:
            sys.exit("Error! Width of matrix is not positive.")
    except ValueError:
        sys.exit("Error! Width of matrix is not a correct integer.")

    # Create randomly generated cell matrix system with specified size of matrix
    system = MatrixSystem.generate((matrix_height, matrix_width))

    # Start visualization of matrix changes simulation
    system.visualize_simulation()


if __name__ == "__main__":
    main()
