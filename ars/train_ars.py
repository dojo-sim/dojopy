
from ars.ars import * 
from dev.environment import * 


########################################################################################
# Train ARS on HalfCheetah with Mujoco
########################################################################################

env_name = 'HalfCheetah-v2'
hp = Hp(env_name)
np.random.seed(hp.seed)
work_dir = mkdir('exp', 'brs')
monitor_dir = mkdir(work_dir, 'monitor')
env = gym.make(hp.env_name)
# env = wrappers.Monitor(env, monitor_dir, force=True)
num_inputs = env.observation_space.shape[0]
num_outputs = env.action_space.shape[0]
policy = Policy(num_inputs, num_outputs, hp)
normalizer = Normalizer(num_inputs)
train(env, policy, normalizer, hp)

# display learned policy
state = env.reset()
env.render()

done = False
num_plays = 1.
reward_evaluation = 0
while not done and num_plays<hp.horizon:
    env.render()
    normalizer.observe(state)
    state = normalizer.normalize(state)
    action = policy.evaluate(state)
    state, reward, done, _ = env.step(action)
    print(num_plays)
    print(done)
    reward_evaluation += reward
    num_plays += 1


########################################################################################
# Train ARS on Pendulum with Dojo
########################################################################################

env_name = 'Pendulum'
hp = Hp(env_name)
np.random.seed(hp.seed)
work_dir = mkdir('exp', 'brs')
monitor_dir = mkdir(work_dir, 'monitor')
env = make(hp.env_name) # this is using Dojo
# env = wrappers.Monitor(env, monitor_dir, force=True)
num_inputs = env.observation_space.shape[0]
num_outputs = env.action_space.shape[0]
policy = Policy(num_inputs, num_outputs, hp)
normalizer = Normalizer(num_inputs)
train(env, policy, normalizer, hp)
