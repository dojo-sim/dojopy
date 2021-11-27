from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pydojo',
      version='0.1.0',
      description='Differentiable Rigid Body Simulation in Python',
      long_description=readme(),
      long_description_content_type="text/markdown",
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Robotics'
      ],
      url='http://github.com/simon-lc/pydojo',
      keywords='rigid body dynamics simulator differentiable maximal coordinates',
      author='Simon Le Cleac'h and Taylor Howell',
      author_email='simonlc@stanford.edu',
      license='MIT',
      packages=['pydojo','pydojo.tests'],
      install_requires=['julia>=0.2'],
      include_package_data=True,
      zip_safe=False)
