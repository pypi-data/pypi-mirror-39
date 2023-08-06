from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='calcDiameter',
      version='0.14',
      description='The program takes in a Molecular Assembly PDB file as arument, finds the right orientation such that the ring sits on the XY plane, projects all atoms onto the XY plane and calculates the max diameter between two atoms that lie furthest apart on the XY plane',
      long_description=readme(),
      long_description_content_type='text/x-rst',
      author='Jan Zaucha',
      author_email='j.zaucha@tum.de',
      license='MIT',
      packages=['calcDiameter'],
      install_requires=['numpy', 'scipy', 'biopython', 'matplotlib'],
      dependency_links=['http://biopython.org/DIST/'],
      zip_safe=False)
