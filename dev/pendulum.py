from julia import Base
from julia import Main
from julia import LinearAlgebra as _LinearAlgebra
from julia import Dojo as _Dojo
import matplotlib.pyplot as plt


from env import Env



# Create environment
Main.vis = _Dojo.Visualizer()
_Dojo.open(Main.vis)

Main.mech = _Dojo.getbox()
Main.eval("Dojo.initialize!(mech, :box)")
Main.storage = Main.eval("Dojo.simulate!(Main.mech, 1.0, record = true, solver = :mehrotra!, verbose = true)")

_Dojo.visualize(Main.mech, Main.storage, vis = Main.vis)

Main.env = _Dojo.make("Pendulum", vis = Main.vis);
Main.o = _Dojo.reset(Main.env)

for t in range(200):
    print(t)
    Main.eval("\
        Dojo.render(env);\
        Base.sleep(0.05);\
        u = Dojo.sample(env.aspace);\
        u = [5.0];\
        o, r, done, info = step(env, u);\
        ")
    if Main.done:
        print("Episode finished after " + (t+1) + "timesteps")
        break

_Dojo.close(Main.env)



