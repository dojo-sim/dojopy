# Solving an SOCP with cosmopy
import sys
sys.path.append('../')
import cosmopy as cosmo

import numpy as np
from scipy import sparse

# SOCP problem:
# max   0x + 1y + 1z
# s.t.  x == 1
# ||(y,z)|| <= x

# COSMO primal variable x = [x,y,z], i.e. q=[0, -1, -1]^T
# expected solution: x* = [1, 1/√2, 1/√2] and optimal value p*=√2

# define the problem
q = np.array([0, -1., -1])
A = sparse.csc_matrix([[1., 0, 0], [-1, 0, 0], [0, -1, 0], [0, 0, -1]])
b = np.array([1, 0., 0., 0.])

# 0-cone dimension 1, one second-order-cone of dimension 3
cone = {"f" : 1, "q" : [3]}


model = cosmo.Model()
model.setup(q = q, A = A, b = b, cone = cone, verbose = True, eps_abs = 1e-5)

# solve the problem
model.optimize()

# query solution info
obj_val = model.get_objective_value()
status = model.get_status()
times = model.get_times()
x = model.get_x()

print("Solved with objective value: ", obj_val, " in", times["solver_time"], "s.")
