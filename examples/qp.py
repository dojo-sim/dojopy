# Solving a QP with cosmopy
import sys
sys.path.append('../')
import cosmopy as cosmo

import numpy as np
from scipy import sparse

# define the problem
P = sparse.csc_matrix([[4., 1], [1, 2]])
q = np.array([1., 1])
A = sparse.csc_matrix([[1., 1], [1, 0], [0, 1], [-1., -1], [-1, 0], [0, -1]])
b = np.array([1, 0.7, 0.7, -1, 0, 0])
cone = {"l" : 6 }


model = cosmo.Model()
model.setup(P, q, A, b, cone, verbose = True, kkt_solver = "CholmodKKTSolver", eps_abs = 1e-5)

# warm starting
x = np.array([1., 0])
model.warm_start(x = x)

# solve the problem
model.optimize()

# query solution info
obj_val = model.get_objective_value()
status = model.get_status()
iter = model.get_iter()
times = model.get_times()
x = model.get_x()

print("Solved with objective value: ", obj_val, " in", times["solver_time"], "s.")
