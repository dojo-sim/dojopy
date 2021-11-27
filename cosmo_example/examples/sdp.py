# Solving an SDP with cosmopy
import sys
sys.path.append('../')
import cosmopy as cosmo

import numpy as np
from scipy import sparse
from math import sqrt
# Solve the following problem:
# min <C, X>
# <A1, X> == b1
# <A2, X> == b2
# X is PSD
#
# with:
# A1 = [1.0 0 1; 0 3 7; 1 7 5];
# A2 = [0.0 2 8; 2 6 0; 8 0 4];
# C = [1.0 2 3; 2 9 0; 3 0 7];
# b1 = 11.0
# b2 = 19.0
#
# turn this into solver format:
# x is the upper triangle of X
# min upper(C) * x
# upper(A1)' * x == b1
# upper(A2)' * x == b2
# mat(x) is PsdConeTriangle

# take the upper triangles of the problem data
n = 6
q = np.array([1., 4, 9, 6, 0, 7]) #upper(C)

# equality constraints: Aj_t * x + s == bj, s in {0}
b = np.hstack((np.array([11., 19.]), np.zeros(6)))
A1_t = sparse.csc_matrix([1.0, 0, 3, 2, 14, 5])
A2_t = sparse.csc_matrix([0.0, 4, 6, 16, 0, 4])

# PSD cone constraint: -Is * x + s == 0, s in PSDConeTriangle
Is = -sparse.eye(n, format = "csc")
Is[1, 1] = Is[3, 3] = Is[4, 4] = -sqrt(2.)

A = sparse.vstack([A1_t, A2_t, Is], format = "csc" )

# 2 equality constraints and one PSD constraint of a 3x3-matrix (= 6 upper triangular entries)
cone = {"f" : 2, "s" : [6]}

model = cosmo.Model()
model.setup(q = q, A = A, b = b, cone = cone, verbose = True, eps_abs = 1e-4)

# solve the problem
model.optimize()

# optimal objective
opt_obj_val = model.get_objective_value()

# get optimal X*
xopt = model.get_x()

# populate a matrix Xopt with the upper triangular entries and symmetrize
Xopt = np.zeros((3, 3))
Xopt[np.triu_indices(3, 0)] = xopt
Xopt = Xopt + np.tril(Xopt.T, -1)
