from julia import Dojo as dojo
import numpy as np
import torch

class TorchStep(torch.autograd.Function):
	@staticmethod
	def forward(ctx, env, state, input):
		if type(state) is np.ndarray:
			state = torch.tensor(state)
		if type(input) is np.ndarray:
			input = torch.tensor(input)
		# step 
		dojo.step(env, state.numpy(), input.numpy(), diff=True) # TODO: diff -> gradients
		# next state
		next_state = env.state 
		if type(next_state) is np.ndarray:
			next_state = torch.tensor(next_state)
		# Jacobians
		jacobian_state = torch.tensor(env.dynamics_jacobian_state)
		jacobian_input = torch.tensor(env.dynamics_jacobian_input)
		# cache
		ctx.save_for_backward(state, input, next_state, jacobian_state, jacobian_input)
		# output
		return next_state

	@staticmethod
	def backward(ctx, grad_output):
		s, i, ns, jacobian_state, jacobian_input = ctx.saved_tensors
		return None, jacobian_state.T @ grad_output, jacobian_input.T @ grad_output

torch_step = TorchStep.apply

