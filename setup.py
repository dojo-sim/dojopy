from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='dojopy',
      version='0.1.0',
      description='Python interface to Dojo: A differentiable simulator for robotics',
      long_description=readme(),
      long_description_content_type="text/markdown",
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics'
      ],
      url='http://github.com/dojo-sim/dojopy',
      keywords='simulation robotics differentiable dynamics contact',
      author='Simon Le Cleac\'h and Taylor Howell',
      author_email='simonlc@stanford.edu and thowell@stanford.edu',
      license='MIT',
      packages=['dojopy','dojopy.tests'],
      install_requires=['julia>=0.2', 'jill'],
      include_package_data=True,
      zip_safe=False)
