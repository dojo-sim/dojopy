import gym
import time
import numpy as np
from julia import Dojo as dojo
from julia import Base as Base

from stable_baselines3 import PPO
from dev.environment import Environment 

# env = gym.make("CartPole-v1")
# env = dojo.make("Pendulum") # julia env
env = Environment("Pendulum") # python wrapped env
env.open_vis()
env.reset()
env.render()


model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=10000)

obs = env.reset()
for i in range(1000):
    time.sleep(0.01)
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
      obs = env.reset()

env.close()