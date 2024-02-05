import sys
import numpy as np

from numpy.linalg import LinAlgError


def main():
    if len(sys.argv) not in [2, 3]:
        sys.exit(
            "Usage: python task1.py linsys.txt [method]\n"
            "method:\n"
            "  built-in \t - numpy built-in function\n"
            "  matrix \t - matrix solution\n"
            "  gauss \t - Gaussian elimination\n"
            "  cramer \t - Cramer's rule"
        )

    # Load matrix a and vector b from text file
    try:
        a, b = load_data(sys.argv[1])
    except FileNotFoundError:
        sys.exit(f"Error! There is no such file '{sys.argv[1]}'.")
    except ValueError:
        sys.exit(
            f"Error! Content of file '{sys.argv[1]}' does not "
             "correspond to number matrix with 3 rows and 4 columns."
        )
    
    # Get a method for solving the system of linear equations (built-in by default)
    method = sys.argv[2] if len(sys.argv) == 3 else "built-in"

    # Compute solution of the system of linear equations using the method
    if method == "built-in":
        x = np.linalg.solve(a, b)
    elif method == "matrix":
        x = solve_matrix(a, b)
    elif method == "gauss":
        x = solve_gauss(a, b)
    elif method == "cramer":
        x = solve_cramer(a, b)
    else:
        sys.exit(f"Error! '{method}' is not a correct name of method.")
    
    print(f"Solution of system of linear equations is {x}.")


def load_data(filename):
    """
    Loads from the text file `filename` left matrix and right column 
    vector of system of three linear equations.
    
    Returns tuple `(a, b)`, where `a` is coefficient matrix in linear
    system (NumPy `ndarray` with shape `(3, 3)`), and `b` is vector of
    right-sides of equations (NumPy `ndarray` with shape `(3,)`).
    """
    
    # Use built-in NumPy function to load data
    data = np.loadtxt(filename)

    # Data represents an array which is augmented matrix (with shape (3, 4))
    # of a coefficient matrix and a vector of right-sides of equations

    if data.shape != (3, 4):
        raise ValueError

    # Slice the augmented matrix
    a = data[:3, :3]  # Matrix a contains elements from first 3 rows and first 3 columns
    b = data[:, 3]  # Vector b contains elements from last column 

    return a, b


def solve_matrix(a, b):
    """
    Computes matrix solution for a system of linear equations.

    Returns `x` (NumPy `ndarray` with shape `(n,)`), solution, such that
    `a * x = b`, where `n` is number of equations, `a` is coefficient matrix
    (NumPy `ndarray` with shape `(n, n)`), `b` is is vector of right-sides of
    equations (NumPy `ndarray` with shape `(n,)`).
    """
    if a.shape[0] != a.shape[1]:
        raise ValueError("Matrix a is not square")
    if a.shape[0] != b.shape[0]:
        raise ValueError("Number of rows in matrix a is not equal to length of vector b")

    # For matrix solution compute inverse of matrix a, and then just compute
    # product of inverse of matrix a and vector b to get a vector x (solution)

    # Compute inverse of matrix a, using row reduction (Gauss-Jordan elimination),
    # where augmented matrix consists of matrix a and identity matrix n x n

    # After the elementary row operations are performed, matrix a becomes identity
    # matrix, and identity matrix n x n becomes inverse of initial matrix a
    _, a_inv = row_reduction(a, np.eye(a.shape[0]))

    # Solution is product of inverse of matrix a and vector b
    x = a_inv @ b
    return x


def solve_gauss(a, b):
    """
    Solves a system of linear equations using Gaussian elimination.

    Returns `x` (NumPy `ndarray` with shape `(n,)`), solution, such that
    `a * x = b`, where `n` is number of equations, `a` is coefficient matrix
    (NumPy `ndarray` with shape `(n, n)`), `b` is is vector of right-sides of
    equations (NumPy `ndarray` with shape `(n,)`).
    """
    if a.shape[0] != a.shape[1]:
        raise ValueError("Matrix a is not square")
    if a.shape[0] != b.shape[0]:
        raise ValueError("Number of rows in matrix a is not equal to length of vector b")

    # Using Gaussian elimination, create augmented matrix of matrix a and vector b, and
    # perform a sequence of elementary row operations until matrix a reaches row canonical form

    # After the elementary row operations are performed, matrix a in augmented matrix
    # becomes an identity matrix, and vector b becomes a vector x (solution)

    # For row_reduction function convert vector b from vector to matrix n x 1
    _, x = row_reduction(a, b.reshape(b.shape[0], 1))
    return x.reshape(x.shape[0],)  # Convert vector x from matrix to vector


def solve_cramer(a, b):
    """
    Solves a system of linear equations using Cramer's rule.

    Returns `x` (NumPy `ndarray` with shape `(n,)`), solution, such that
    `a * x = b`, where `n` is number of equations, `a` is coefficient matrix
    (NumPy `ndarray` with shape `(n, n)`), `b` is is vector of right-sides of
    equations (NumPy `ndarray` with shape `(n,)`).
    """
    if a.shape[0] != a.shape[1]:
        raise ValueError("Matrix a is not square")
    if a.shape[0] != b.shape[0]:
        raise ValueError("Number of rows in matrix a is not equal to length of vector b")

    # Compute determinant of matrix a
    d = det(a)
    if d == 0:
        raise LinAlgError("Determinant of matrix a is 0 (matrix a is singular)")

    # Compute determinants of matrices formed by replacing each column of of matrix a by vector b
    dx = np.array([])
    for j in range(a.shape[1]):
        ax = np.copy(a)
        ax[:, j] = b[:]
        dx = np.append(dx, det(ax))

    # Solution is results of dividing computed determinants by determinant of matrix a
    x = dx / d
    return x


def row_reduction(matrix1, matrix2):
    """
    Performs elementary row operations on augmented matrix which contains matrices `matrix1`
    (NumPy `ndarray` with shape `(n, n)`) and `matrix2` (NumPy `ndarray` with shape `(n, m)`)
    until `matrix1` reaches row canonical form, e.g. main diagonal of `matrix1` consist of ones
    and all elements above and below the main diagonal in `matrix1` are zeros.

    Returns a tuple of `matrix1` and `matrix2` which have new values.
    """
    if matrix1.shape[0] != matrix1.shape[1]:
        raise ValueError("matrix1 is not a square matrix")
    if matrix1.shape[0] != matrix2.shape[0]:
        raise ValueError("Number of rows in matrix1 is not equal number of rows in matrix2")
    
    # Augment matrix1 and matrix2
    augmented = np.hstack((matrix1, matrix2))
    size = matrix1.shape[0]  # Size of squared matrix1 and number of rows in augmented matrix

    # Set raising a FloatingPointError for division by zero
    with np.errstate(divide="raise"):
        try:
            # Forward elimination
            for i in range(size - 1):
                for j in range(i + 1, size):
                    augmented[j, :] += augmented[i, :] * (-augmented[j, i] / augmented[i, i])

            # Back substitution
            for i in range(size - 1, 0, -1):
                for j in range(i - 1, -1, -1):
                    augmented[j, :] += augmented[i, :] * (-augmented[j, i] / augmented[i, i])

            # Division by pivots (elements of main diagonal in matrix1)
            for k in range(size):
                augmented[k, :] /= augmented[k, k]
        
        # Raise a new error, when a FloatingPointError raises
        except FloatingPointError:
            raise LinAlgError("matrix1 contains zero element in main diagonal (matrix1 is singular)")

    # Splitted matrix1 and matrix2 with new values
    return augmented[:, :size], augmented[:, size:]


def det(matrix):
    """
    Returns determinant of `matrix` (NumPy `ndarray` with shape `(n, n)`) using Laplace expansion.
    """
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix is not square")
    
    # For matrix 1 x 1 determinant is value of single element of matrix
    if matrix.shape[0] == 1:
        return matrix[0, 0]

    # Compute cofactor of elements in 0th row of matrix
    cofactors = np.array([

        # Cofactor equals to minor (determinant of matrix without row and column of element)
        # multiplied by -1 in power of sum of row and column (indices) of element
        det(submat(matrix, 0, j)) * (-1)**j
        for j in range(matrix.shape[1])
    ])

    # Determinant is equal to sum of products of 0th row elements and its cofactors (Laplace expansion)
    return np.sum(matrix[0, :] * cofactors)


def submat(matrix, i, j):
    """
    Returns submatrix of `matrix` with `i`-th row and `j`-th column are eliminated.
    """
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("matrix is not square")

    # Mask indicates that elements of i-th row and
    # j-th column are not contained in submatrix
    mask = np.ones_like(matrix, dtype=bool)
    mask[i, :] = False  # Eliminate i-th row
    mask[:, j] = False  # Eliminate j-th column

    # Eliminate i-th row and j-th column using the mask
    return matrix[mask].reshape(matrix.shape[0] - 1, matrix.shape[1] - 1)


if __name__ == "__main__":
    main()
