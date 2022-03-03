from julia import Dojo as dojo
import dojopy.jax_interface as jax_interface
import jax.numpy as jnp
from jax.config import config
config.update("jax_enable_x64", True)

@partial(jax_interface.custom_vjp, nondiff_argnums=(0,))
def dynamics(env, state, input):
	dojo.step(env, state, input, diff=True)
	return env.state 

def dynamics_fwd(env, state, input):
	next_state = dynamics(env, state, input)
	jacobian_state = env.dynamics_jacobian_state 
	jacobian_input = env.dynamics_jacobian_input
	return next_state, (jacobian_state, jacobian_input)

def dynamics_bwd(env, res, g):
	jacobian_state, jacobian_input = res
	return (jacobian_state.T @ g, jacobian_input.T @ g)

dynamics.defvjp(dynamics_fwd, dynamics_bwd)
