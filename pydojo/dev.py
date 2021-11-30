# import julia
# julia.install()

# from julia.api import Julia
# jl = Julia(compiled_modules=False)

from julia import Base

Base.sind(90)

# import julia.Base
# from julia.Base import Enums    # import a submodule
# from julia.Base import sin      # import a function from a module

# from julia import Main
# Main.xs = [1, 2, 3]

# a = Main.eval("sin.(xs)")
# print(a)

# from julia import LinearAlgebra as _LinearAlgebra
# b = Main.eval("LinearAlgebra.zeros")
# print(b)

# from julia import Dojo as _Dojo
# b = Main.eval("Dojo.controldim")
# print(b)
