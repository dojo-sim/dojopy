from julia import Base
from julia import Main
import time
from julia import LinearAlgebra as _LinearAlgebra
from julia import Dojo as dojo
import matplotlib.pyplot as plt
import meshcat


from dev.environment import Environment 

# Create environment
env = Environment("Pendulum")
env.open_vis()

Main.vis = Main.eval("vis = Dojo.Visualizer()")
Main.eval("Dojo.open(vis)")

env.seed()
env.reset()
env._get_obs()
env.close()
env.render()
u = [1.0]
env.step(u)
env.sample_action()

for t in range(200):
    print(t)
    env.render()
    time.sleep(0.05)
    u = env.sample_action()
    o, r, done, info = env.step(u)
    if done:
        print("Episode finished after " + (t+1) + "timesteps")
        break

env.close()




