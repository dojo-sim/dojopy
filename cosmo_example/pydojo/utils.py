# modified from https://github.com/oxfordcontrol/osqp-python/blob/master/module/utils.py
from warnings import warn
import numpy as np
from scipy import sparse

def get_dimension(cone):
    """
    `cone` holds the dimensions of the individual cones.
    Calculate and return the sum of all the cone dimensions.

    For PSD-cones consider the vector-length of the upper-triangle.
    """
    dim = 0
    for k in cone:
        if k == "f" or k == "l":
            dim += cone[k]
        elif k == "q" or k == "s":
            dim += sum(cone[k])
        elif k == "ep" or k == "ed":
            dim += cone[k] * 3
        elif k == "p":
            dim += len(cone[k]) * 3
        elif k == "b":
            dim += cone[k]
        else:
            raise ValueError("cone key unknown.")
    return dim


def prepare_data(P = None, q = None, A = None, b = None, cone = None, l = None, u = None):
        """
        Prepare problem data of the form

        minimize     1/2 x' * P * x + q' * x
        subject to   A * x + s == b, s in cone
                    A[b] * x + sb == b[b], l <= sb <= u
        solver settings can be specified as additional keyword arguments
        """

        #
        # Get problem dimensions
        #
        m, n = A.shape

        #
        # Create parameters if they are None
        #
        # Create elements if they are not specified
        if P is None:
            P = sparse.csc_matrix((np.zeros((0,), dtype=np.double),
                                   np.zeros((0,), dtype=np.int),
                                   np.zeros((n+1,), dtype=np.int)),
                                  shape=(n, n))
        if q is None:
            q = np.zeros(n)

        if b is None:
            b = np.zeros(n)

        #
        # Check vector dimensions
        #

        # Check if second dimension of A is correct
        # if A.shape[1] != n:
        #     raise ValueError("Dimension n in A and P does not match")
        if P.shape[1] != P.shape[0]:
            raise ValueError("P has to be a square matrix.")
        if P.shape[1] != A.shape[1]:
            raise ValueError("Dimension of nxn matrix P and mxn matrix A doesn't match.")
        if len(q) != P.shape[1]:
            raise ValueError("Dimension of P and q doesn't match.")
        if len(q) != n:
            raise ValueError("Incorrect dimension of q")
        if len(b) != m:
            raise ValueError("Incorrect dimension of b")
        
        if not type(cone) is dict:
            raise TypeError("cone has to be a dictionary of dimensions of the conic constraints.")

        if get_dimension(cone) != m:
            raise ValueError("The number of rows of the constraint matrix A does not match the sum of dimensions specified in `cone`.")
        #
        # Check or Sparsify Matrices
        #
        if not sparse.issparse(P) and isinstance(P, np.ndarray) and \
                len(P.shape) == 2:
            raise TypeError("P is required to be a sparse matrix")
        if not sparse.issparse(A) and isinstance(A, np.ndarray) and \
                len(A.shape) == 2:
            raise TypeError("A is required to be a sparse matrix")

        # Convert matrices in CSC form and to individual pointers
        if not sparse.isspmatrix_csc(P):
            warn("Converting sparse P to a CSC " +
                 "(compressed sparse column) matrix. (It may take a while...)")
            P = P.tocsc()
        if not sparse.isspmatrix_csc(A):
            warn("Converting sparse A to a CSC " +
                 "(compressed sparse column) matrix. (It may take a while...)")
            A = A.tocsc()

        # Check if P an A have sorted indices
        if not P.has_sorted_indices:
            P.sort_indices()
        if not A.has_sorted_indices:
            A.sort_indices()

        # check any potential box constraints
        if "b" in cone.keys():
            if len(u) != cone["b"]:
                raise ValueError("Dimension of supplied box constraint dimension cone[b] doesn't match length of boundary vector u.")
            if len(l) != cone["b"]:
                raise ValueError("Dimension of supplied box constraint dimension cone[b] doesn't match length of boundary vector l.")
        else:
            l = None
            u = None

        return (P.indices, P.indptr, P.data, q, A.indices, A.indptr, A.data, b, cone, l, u, m, n)
