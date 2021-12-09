import os
import sys
import numpy as np
import gym
from gym import wrappers
import mujoco_py
# import pybullet_envs

# hyper parameters
class Hp():
    def __init__(self):
        self.main_loop_size = 100
        self.horizon = 1000
        self.step_size = 0.02
        self.n_directions = 16
        self.b = 16
        assert self.b<=self.n_directions, "b must be <= n_directions"
        self.noise = 0.03
        self.seed = 1
        ''' chose your favourite '''
        # self.env_name = 'Reacher-v1'
        # self.env_name = 'Pendulum-v0'
        # self.env_name = 'HalfCheetahBulletEnv-v0'
        # self.env_name = 'Hopper-v1'#'HopperBulletEnv-v0'
        # self.env_name = 'Ant-v2'#'AntBulletEnv-v0'#
        self.env_name = 'HalfCheetah-v2'
        # self.env_name = 'Swimmer-v1'
        # self.env_name = 'Humanoid-v1'

# observation filter
class Normalizer():
    def __init__(self, num_inputs):
        self.n = np.zeros(num_inputs)
        self.mean = np.zeros(num_inputs)
        self.mean_diff = np.zeros(num_inputs)
        self.var = np.zeros(num_inputs)

    def observe(self, x):
        self.n += 1.
        last_mean = self.mean.copy()
        self.mean += (x-self.mean)/self.n
        self.mean_diff += (x-last_mean)*(x-self.mean)
        self.var = (self.mean_diff/self.n).clip(min=1e-2)

    def normalize(self, inputs):
        obs_mean = self.mean
        obs_std = np.sqrt(self.var)
        return (inputs-obs_mean)/obs_std

# linear policy
class Policy():
    def __init__(self, input_size, output_size):
        self.theta = np.zeros((output_size, input_size))

    def evaluate(self, input):
        return self.theta.dot(input)

    def positive_perturbation(self, input, delta):
        return (self.theta + hp.noise*delta).dot(input)

    def negative_perturbation(self, input, delta):
        return (self.theta - hp.noise*delta).dot(input)

    def sample_deltas(self):
        return [np.random.randn(*self.theta.shape) for _ in range(hp.n_directions)]

    def update(self, rollouts, sigma_r):
        step = np.zeros(self.theta.shape)
        for r_pos, r_neg, d in rollouts:
            step += (r_pos - r_neg)*d
        self.theta += hp.step_size * step / (sigma_r*hp.b)

# training loop
def train(env, policy, normalizer, hp):
    for episode in range(hp.main_loop_size):
        # init deltas and rewards
        deltas = policy.sample_deltas()
        reward_positive = [0]*hp.n_directions
        reward_negative = [0]*hp.n_directions

        # positive directions
        for k in range(hp.n_directions):
            state = env.reset()
            done = False
            num_plays = 0.
            while not done and num_plays<hp.horizon:
                normalizer.observe(state)
                state = normalizer.normalize(state)
                action = policy.positive_perturbation(state, deltas[k])
                state, reward, done, _ = env.step(action)
                reward = max(min(reward, 1), -1)
                reward_positive[k] += reward
                num_plays += 1

        # negative directions
        for k in range(hp.n_directions):
            state = env.reset()
            done = False
            num_plays = 0.
            while not done and num_plays<hp.horizon:
                normalizer.observe(state)
                state = normalizer.normalize(state)
                action = policy.negative_perturbation(state, deltas[k])
                state, reward, done, _ = env.step(action)
                reward = max(min(reward, 1), -1)
                reward_negative[k] += reward
                num_plays += 1

        all_rewards = np.array(reward_negative + reward_positive)
        sigma_r = all_rewards.std()

        # sort rollouts wrt max(r_pos, r_neg) and take (hp.b) best
        scores = {k:max(r_pos, r_neg) for k,(r_pos,r_neg) in enumerate(zip(reward_positive,reward_negative))}
        order = sorted(scores.keys(), key=lambda x:scores[x])[-hp.b:]
        rollouts = [(reward_positive[k], reward_negative[k], deltas[k]) for k in order[::-1]]

        # update policy:
        policy.update(rollouts, sigma_r)

        # evaluate
        state = env.reset()
        done = False
        num_plays = 1.
        reward_evaluation = 0
        while not done and num_plays<hp.horizon:
            normalizer.observe(state)
            state = normalizer.normalize(state)
            action = policy.evaluate(state)
            state, reward, done, _ = env.step(action)
            reward_evaluation += reward
            num_plays += 1

        # finish, print:
        print('episode',episode,'reward_evaluation',reward_evaluation)

def mkdir(base, name):
    path = os.path.join(base, name)
    if not os.path.exists(path):
        os.makedirs(path)
    return path
