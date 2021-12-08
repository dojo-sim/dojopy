class Env:
    def __init__(self, model):
        self.env = _Dojo.make(model)
        return 

    def seed(self, s=0):
        _Dojo.seed(self.env, s=s)
        return
    
    def step(self, u):
        observation, reward, done, info = _Dojo.step(self.env, u)
        return observation, reward, done, info

    def reset(self):
        _Dojo.reset(self.env)
        return

    def _get_obs(self):
        return _Dojo._get_obs(self)

    def render(self):
        _Dojo.render(self.env)
        return

    def close(self):
        _Dojo.close(self.env)
        return 
        