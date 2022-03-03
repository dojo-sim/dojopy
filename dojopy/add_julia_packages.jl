using Pkg
Pkg.add(url="https://github.com/dojo-sim/Dojo.jl") # TODO: change to General repository
Pkg.add("PyCall")
Pkg.build("PyCall")

using Dojo
using PyCall
