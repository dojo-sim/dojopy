from julia.api import Julia
jl = Julia(compiled_modules=False)

from julia import Dojo as _Dojo
# import dojopy.utils as utils

# import numpy as np
# from scipy import sparse
# from warnings import warn


# class Model:
#     def __init__(self):
#         self.model = _Dojo.Model()
#         self.result = None
#         self.solved = False
#         self.setup_complete = False

#     def reset(self):
#         """
#         Reset the model by re-instantiating the _Dojo.Model
#         """
#         self.model = _Dojo.Model()
#         self.result = None
#         self.solved = False
#         self.setup_complete = False

#     def version(self):
#         """
#         Report Dojo.jl package version used.
#         """
#         _Dojo.print_version()

#     def setup(self, P = None, q = None, A = None, b = None, cone = None, l = None, u = None, **settings):
#         """
#         Setup Dojo solver problem of the form
#             minimize     1/2 x' * P * x + q' * x
#             subject to   A * x + s == b, s in cone
#                          A[b] * x + sb == b[b], l <= sb <= u
#         solver settings can be specified as additional keyword arguments
#         """
#         unpacked_data = utils.prepare_data(P, q, A, b, cone, l, u)
#         if settings == None:
#             # create standard settings in julia
#             _Dojo.set_b(self.model, *unpacked_data)
#         else:
#             # pass settings dictionary and let Dojo transform it internally
#             _Dojo.set_b(self.model, *unpacked_data, settings)
#         self.setup_complete = True

#     def optimize(self):
#         """
#         Solve conic problem and store result in self.result.
#         """
#         if self.setup_complete:
#             res = _Dojo.optimize_b(self.model)
#             self.result = res
#             self.solved = True
#         else:
#             warn('The problem has not been setup yet. Call setup().')


#     def warm_start(self, x=None, y=None):
#         """
#         Warm start primal or dual variables
#         """
#         # get problem dimensions
#         (m, n) = self.model.p.model_size

#         if x is not None:
#             if len(x) != n:
#                 raise ValueError("Wrong dimension for variable x")

#             if y is None:
#                 _Dojo.warm_start_primal_b(self.model, x)

#         if y is not None:
#             if len(y) != m:
#                 raise ValueError("Wrong dimension for variable y")

#             if x is None:
#                 _Dojo.warm_start_dual_b(self.model, y)

#         if x is not None and y is not None:
#                 _Dojo.warm_start_primal_b(self.model, x)
#                 _Dojo.warm_start_dual_b(self.model, y)

#         if x is None and y is None:
#             raise ValueError("Unrecognized fields")

#     # solution getters
#     def get_objective_value(self):
#         if self.solved:
#             return self.result.obj_val
#         else:
#             warn('The problem has not been solved yet. Call solve().')

#     def get_x(self):
#         if self.solved:
#             return self.result.x
#         else:
#             warn('The problem has not been solved yet. Call solve().')

#     def get_y(self):
#         if self.solved:
#             return self.result.y
#         else:
#             warn('The problem has not been solved yet. Call solve().')

#     def get_s(self):
#         if self.solved:
#             return self.result.s
#         else:
#             warn('The problem has not been solved yet. Call solve().')

#     def get_status(self):
#         if self.solved:
#             return self.result.status
#         else:
#             warn('The problem has not been solved yet. Call solve().')

#     def get_iter(self):
#         if self.solved:
#             return self.result.iter
#         else:
#             warn('The problem has not been solved yet. Call solve().')

#     def get_times(self):
#         if self.solved:
#             return {"solver_time" : self.result.times.solver_time,
#                     "setup_time" : self.result.times.setup_time,
#                     "scaling_time" : self.result.times.scaling_time,
#                     "graph_time" : self.result.times.graph_time,
#                     "init_factor_time" : self.result.times.init_factor_time,
#                     "factor_update_time" : self.result.times.factor_update_time,
#                     "iter_time" : self.result.times.iter_time,
#                     "proj_time" : self.result.times.proj_time,
#                     "post_time" : self.result.times.post_time}
#         else:
#             warn('The problem has not been solved yet. Call solve().')

#     def get_sol(self):
#         if self.solved:
#             return self.result.obj_val, self.result.x, self.result.y, self.result.s
