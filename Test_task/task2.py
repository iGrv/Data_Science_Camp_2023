import sys
import os
import numpy as np

ALIVE = 1
DEAD = 0

# Command to clear the CLI screen depends on OS type 
CLEAR_CMD = "clear" if os.name == "posix" else "cls"


class MatrixSystem:
    """Representation of system which contains a cell matrix."""

    def __init__(self, matrix):
        if matrix.ndim != 2:
            raise ValueError("matrix is not a 2-D array")

        self.matrix = np.copy(matrix)
        self.height, self.width = self.matrix.shape
        self.state = 0

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

    def print_matrix(self, title=None):
        """
        Prints values of cell matrix in the command-line interface (CLI).
        Before print the values, runs in CLI the command to clear the screen.

        If `title` is provided, prints `title` together with values of cells.
        Othervise, prints values of cells only.
        """
        os.system(CLEAR_CMD)
        if title:
            print(title, self.matrix, sep="\n")
        else:
            print(self.matrix)


def main():
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python task2.py matrix.txt [iteration]")

    # Get iteration number where matrix change stops (1 by default)
    try:
        iteration = int(sys.argv[2]) if len(sys.argv) == 3 else 1
        if iteration < 1:
            sys.exit("Error! Iteration number is not positive.")
    except ValueError:
        sys.exit("Error! Iteration number is not a correct integer.")

    # Load a matrix from the text file
    try:
        data = load_data(sys.argv[1])
    except FileNotFoundError:
        sys.exit(f"Error! There is no such file '{sys.argv[1]}'.")
    except ValueError:
        sys.exit(
            f"Error! Content of file '{sys.argv[1]}' does not "
            f"correspond to number matrix with values {ALIVE} or {DEAD}."
        )

    # Cell matrix system contains loaded matrix
    system = MatrixSystem(data)

    # Repeatedly change the matrix until reach specified iteration number
    while True:
        system.change_matrix()

        if system.state == iteration:
            break

    system.print_matrix(f"Matrix after iteration {system.state}:")


def load_data(filename):
    """
    Loads cell matrix from the text file `filename`.

    Returns a NumPy `ndarray` which contains a matrix,
    where each cell has `ALIVE` or `DEAD` state.
    """

    # Use built-in NumPy function to load the matrix with int type
    data = np.loadtxt(filename, dtype=int)

    if not np.all((data == ALIVE)^(data == DEAD)):
        raise ValueError

    return data


if __name__ == "__main__":
    main()
