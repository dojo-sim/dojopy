import unittest
from dojopy import torch_interface
from julia import Main 
from julia import Base

# get an environment
env = dojo.get_environment('pendulum')
dojo.initialize_pendulum_b(env.mechanism, angle=0.0, angular_velocity=0.0)

# robot dimensions
nz = dojo.maximal_dimension(env.mechanism)
nx = dojo.minimal_dimension(env.mechanism)
nu = dojo.input_dimension(env.mechanism)

# get state
x1 = dojo.get_minimal_state(env.mechanism)
z1 = dojo.get_maximal_state(env.mechanism)

# zero control
u1 = Base.zeros(nu)

# step 
x2 = torch_step(env, x1, u1)

# Jacobians
dx, du = torch.autograd.functional.jacobian(lambda x, u: torch_step(env, x, u), (torch.tensor(x1), torch.tensor(u1)))
assert np.linalg.norm(x2.numpy() - env.state) < 1.0e-5
assert np.linalg.norm(dx.numpy() - env.dynamics_jacobian_state) < 1.0e-5
assert np.linalg.norm(du.numpy() - env.dynamics_jacobian_input) < 1.0e-5

# zero control
u1 = Base.rand(nu)

# step 
x2 = torch_step(env, x1, u1)

# Jacobians
dx, du = torch.autograd.functional.jacobian(lambda x, u: torch_step(env, x, u), (torch.tensor(x1), torch.tensor(u1)))
assert np.linalg.norm(x2.numpy() - env.state) < 1.0e-5
assert np.linalg.norm(dx.numpy() - env.dynamics_jacobian_state) < 1.0e-5
assert np.linalg.norm(du.numpy() - env.dynamics_jacobian_input) < 1.0e-5

