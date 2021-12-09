import time
from julia import Base as Base
from julia import Main
from julia import Dojo as dojo
from julia import as meshcat

Main.vis = Main.eval("Dojo.Visualizer()")
Main.eval("Dojo.open(vis)")
dojo.wait_for_server(Main.vis.core)



dojo.eval("Dojo.MeshCat.open(Main.vis)")

Main.eval("Dojo.wait_for_server(vis.core)")
dojo.MeshCat.wait_for_server(Main.vis.core)
Main.eval("Dojo.MeshCat.open_url(Dojo.MeshCat.url(vis.core))")
