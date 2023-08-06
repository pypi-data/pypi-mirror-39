from setuptools import setup

setup(name='calcDiameter',
      version='0.1',
      description='The program takes in a pdb as arument, finds the right orientation such that the torus sits on the XY plane projects all atoms onto the XY plane and calculates the max diameter',
      author='Jan Zaucha',
      author_email='j.zaucha@tum.de',
      license='MIT',
      packages=['calcDiameter'],
      install_requires=['numpy', 'scipy', 'biopython', 'matplotlib'],
      dependency_links=['http://biopython.org/DIST/'],
      zip_safe=False)
