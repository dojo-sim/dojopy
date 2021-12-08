from julia import Base
from julia import Main
from julia import LinearAlgebra as _LinearAlgebra
from julia import Dojo as _Dojo
import matplotlib.pyplot as plt

_LinearAlgebra.zeros(10)


b = Main.eval("Dojo.controldim")
print(b)

# Create a dice model
Main.mech = Main.eval("Dojo.getdice()")
eqcs = Main.eval("collect(mech.eqconstraints)")
eqcs[0]

Main.vis = Main.eval("vis = Dojo.Visualizer()")
Main.eval("Dojo.open(vis)")

Main.mech = _Dojo.getdice()
Main.eval("Dojo.initialize!(mech, :dice)")
Main.storage = Main.eval("Dojo.simulate!(Main.mech, 1.0, record = true, solver = :mehrotra!, verbose = true)")

_Dojo.visualize(Main.mech, Main.storage, vis = Main.vis)


