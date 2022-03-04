
from julia import Dojo as dojo
import jax
import jax.numpy as jnp
from jax.config import config
config.update("jax_enable_x64", True)
from functools import partial

@partial(jax.custom_vjp, nondiff_argnums=(0,))
def jax_step(env, state, input):
	dojo.step(env, state, input, gradients=True)
	return env.state 

def jax_step_fwd(env, state, input):
	next_state = jax_step(env, state, input)
	jacobian_state = env.dynamics_jacobian_state 
	jacobian_input = env.dynamics_jacobian_input
	return next_state, (jacobian_state, jacobian_input)

def jax_step_bwd(env, res, g):
	jacobian_state, jacobian_input = res
	return (jacobian_state.T @ g, jacobian_input.T @ g)

jax_step.defvjp(jax_step_fwd, jax_step_bwd)
