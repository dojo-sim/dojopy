import setuptools
from os import path
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="dojopy",
    version="0.1.0",
    author="Simon Le Cleac'h and Taylor Howell",
    author_email="simonlc@stanford.edu",
    description="Differentiable Rigid-Body Simulation in Python",
    url="https://github.com/simon-lc/dojopy",
    install_requires=["numpy >= 1.7", "scipy >= 0.13.2", "julia >= 1.6.0"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages= setuptools.find_packages(),
    python_requires='>=3.6',
    license='MIT'
)
