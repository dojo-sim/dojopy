from julia import Dojo as dojo

from ars.ars import * 
from dev.environment import * 


########################################################################################
# Train ARS on HalfCheetah with Mujoco
########################################################################################

env_name = 'HalfCheetah-v2'
main_loop_size = 20
hp = Hp(env_name, main_loop_size)
np.random.seed(hp.seed)
work_dir = mkdir('exp', 'brs')
monitor_dir = mkdir(work_dir, 'monitor')
env = gym.make(hp.env_name) ############################ uses MUJOCO ###################
# env = wrappers.Monitor(env, monitor_dir, force=True)
num_inputs = env.observation_space.shape[0]
num_outputs = env.action_space.shape[0]
policy = Policy(num_inputs, num_outputs, hp)
normalizer = Normalizer(num_inputs)
# train(env, policy, normalizer, hp)

display_policy(env, policy, normalizer, hp)

########################################################################################
# Train ARS on HalfCheetah with Dojo
########################################################################################

env_name = 'halfcheetah'
main_loop_size = 20
hp = Hp(env_name, main_loop_size)
np.random.seed(hp.seed)
work_dir = mkdir('exp', 'brs')
monitor_dir = mkdir(work_dir, 'monitor')
env = make(hp.env_name) ############################ uses DOJO #########################
env.open_vis()
# env = wrappers.Monitor(env, monitor_dir, force=True)
num_inputs = env.observation_space.shape[0]
num_outputs = env.action_space.shape[0]
policy = Policy(num_inputs, num_outputs, hp)
normalizer = Normalizer(num_inputs)
train(env, policy, normalizer, hp)

display_policy(env, policy, normalizer, hp)
env.action_space

########################################################################################
# Train ARS on Pendulum with Dojo
########################################################################################

env_name = 'pendulum'
main_loop_size = 20
hp = Hp(env_name, main_loop_size)
np.random.seed(hp.seed)
work_dir = mkdir('exp', 'brs')
monitor_dir = mkdir(work_dir, 'monitor')
env = make(hp.env_name) # this is using Dojo
env.open_vis()
# env = wrappers.Monitor(env, monitor_dir, force=True)
num_inputs = env.observation_space.shape[0]
num_outputs = env.action_space.shape[0]
policy = Policy(num_inputs, num_outputs, hp)
normalizer = Normalizer(num_inputs)
train(env, policy, normalizer, hp)


# display learned policy
display_policy(env, policy, normalizer, hp)



from julia import Dojo as dojo

from ars.ars import * 
from dev.environment import * 


########################################################################################
# Train ARS on Ant with Mujoco
########################################################################################

env_name = 'Ant-v2'
env_name = 'Hopper-v2'
env_name = 'Walker2d-v2'
main_loop_size = 20
hp = Hp(env_name, main_loop_size)
hp.horizon = 5000
np.random.seed(hp.seed)
work_dir = mkdir('exp', 'brs')
monitor_dir = mkdir(work_dir, 'monitor')
env = gym.make(hp.env_name) ############################ uses MUJOCO ###################
# env = wrappers.Monitor(env, monitor_dir, force=True)
num_inputs = env.observation_space.shape[0]
num_outputs = env.action_space.shape[0]
policy = Policy(num_inputs, num_outputs, hp)
normalizer = Normalizer(num_inputs)
# train(env, policy, normalizer, hp)

display_policy(env, policy, normalizer, hp)
display_random(env, hp)

env.sim.data.qpos
