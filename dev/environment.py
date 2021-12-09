import numpy as np
from gym.spaces.box import Box
from julia import Dojo as dojo


class Environment:
    def __init__(self, model):
        self.env = dojo.make(model)
        aspace = self.env.aspace
        ospace = self.env.ospace
        self.action_space = Box(aspace.low, aspace.high, dtype = np.float64)
        self.observation_space = Box(ospace.low, ospace.high, dtype = np.float64)
        self.reward_range = None
        self.metadata = None
        return 

    def seed(self, s=None):
        if type(s) == int:
            dojo.seed(self.env, s=s)
        else:
            dojo.seed(self.env)
        return
    
    def step(self, u):
        observation, reward, done, info = dojo.step(self.env, u)
        return observation, reward, done, info

    def reset(self):
        return dojo.reset(self.env)

    def _get_obs(self):
        return dojo._get_obs(self.env)

    def render(self):
        dojo.render(self.env)
        return

    def close(self):
        dojo.close(self.env)
        return 

    def open_vis(self):
        dojo.open(self.env.vis)
        # We need to call wait_for_server twice after we opened the browser tab.
        dojo.wait_for_server(self.env.vis.core)
        dojo.wait_for_server(self.env.vis.core)
        dojo.wait_for_server(self.env.vis.core)
        dojo.wait_for_server(self.env.vis.core)
        dojo.wait_for_server(self.env.vis.core)
        dojo.wait_for_server(self.env.vis.core)
        dojo.wait_for_server(self.env.vis.core)
        dojo.wait_for_server(self.env.vis.core)        
        return

    def sample_action(self):
        return dojo.sample(self.env.aspace)


# aspace = BoxSpace(-np.ones(10), np.ones(10))
# aspace.sample()
# aspace.contains(np.zeros(10))
# gym.spaces.box.Box(-np.ones(10), np.ones(10))