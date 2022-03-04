import unittest
from dojopy import jax_interface
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
x2 = jax_step(env, x1, u1)

# Jacobians
dx = jax.jacobian(jax_step, argnums=1)(env, x1, u1)
du = jax.jacobian(jax_step, argnums=2)(env, x1, u1)

assert jnp.linalg.norm(x2 - env.state) < 1.0e-5
assert jnp.linalg.norm(dx - env.dynamics_jacobian_state) < 1.0e-5
assert jnp.linalg.norm(du - env.dynamics_jacobian_input) < 1.0e-5

# random control
u1 = Base.rand(nu)

# step 
x2 = jax_step(env, x1, u1)

# Jacobians
dx = jax.jacobian(jax_step, argnums=1)(env, x1, u1)
du = jax.jacobian(jax_step, argnums=2)(env, x1, u1)

assert jnp.linalg.norm(x2 - env.state) < 1.0e-5
assert jnp.linalg.norm(dx - env.jax_step_jacobian_state) < 1.0e-5
assert jnp.linalg.norm(du - env.jax_step_jacobian_input) < 1.0e-5
