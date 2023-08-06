calcDiameter: a method to find the maximum diameter of a ring-shaped protein complex of Cn symmetry. 

########################################

How it works
=============

It reads a 'Biological Assembly' PDB file and finds the right orientation such that the protein ring lies 'flat' on XY plane. Then, the maximum distance between any pair of residues residing in the same 'height slice' is returned.


Installation
============


Via pip from `PyPi <https://pypi.org/project/calcDiameter/>`_
(recommended):

.. code-block:: bash

    $ sudo pip install calcDiameter


If your system lacks pip, `install it first <https://www.makeuseof.com/tag/install-pip-for-python/>`_. 


Python version
--------------

The tool was developed using Python 2.7, however running under 
Python 3.x *should* work as well.




Usage
=====


Python 2.7 shell


.. code-block:: bash

    >>> from calcDiameter import *
    >>> calcDiameter('1qaw.pdb')
    Reading PDB file
    Obtaining approximate orientation by testing rotations about X and Y axes every 10 degrees...
    Obtaining accurate orientation by testing rotations about X and Y axes every 1 degree...
    Plotting projecton of CA atom coordinates onto the XY plane
    Max diameter between E:75 & K:17 is 79.701881
    (79.70188096903092, 'E:75', 'K:17')



You can set the tolerated height difference between points using the bin\_ parameter; by default=3 Angstrom, change to 30 (the Z component of the distance is disregarded regardless of the bin\_ parameter!):


.. code-block:: bash

    >>> calcDiameter.calcDiameter('1qaw.pdb', bin_=30)
    Reading PDB file
    Obtaining approximate orientation by testing rotations about X and Y axes every 10 degrees...
    Obtaining accurate orientation by testing rotations about X and Y axes every 1 degree...
    Plotting projecton of CA atom coordinates onto the XY plane
    Max diameter between E:75 & K:18 is 79.706971
    (79.70697056799868, 'E:75', 'K:18')

The full list of options is as follows

.. code-block:: bash

    >>>calcDiameter(pdb, plot=True, plot3d=False, no_rotation=False, bin_=3)

You can set 'no_rotation' to True if you believe that the pdb is already correctly oriented - the structure is already flat on the XY plane.

You can also set plot3d to True if you want to see the 3d plots of points making up the structure. First you will see the original orientation of the pdb - feel free to look at it from all angles, then close it to see the best orientation that the program has found - the structure should lie flat on the XY plane; close the plot to obtain the max diameter along the XY plane.


Licence
-------

MIT


Authors
-------

`Jan Zaucha <j.zaucha@tum.de>`_
