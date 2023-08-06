calcDiameter: a method to find the maximum diameter of a ring-shaped protein complex of symmetry Cn. 

########################################

How it works
=============

It reads a 'Biological Assembly' PDB file and finds the right orientation such that the protein ring lies 'flat' on XY plane. Then, the maximum distance between any pair of residues residing in the same 'height slice' is returned. On top of that the method returns the 'effective radius'


Installation
============


Via pip from `PyPi <https://pypi.org/project/calcDiameter/>`_
(recommended):

.. code-block:: bash

    $ sudo pip install calcDiameter


If your system lacks pip, `install it first <https://www.makeuseof.com/tag/install-pip-for-python/>`_. 


Python version
--------------

The tool was developed using Python 3.7, however running under 
Python 3.x *should* work as well.




Usage
=====


Python 3.7 shell


.. code-block:: bash

    >>> from calcDiameter import *
    >>> calcDiameter('1qaw.pdb')
    Reading PDB file
    Obtaining approximate orientation by testing rotations about X and Y axes every 10 degrees...
    Obtaining accurate orientation by testing rotations about X and Y axes every 1 degree...
    Plotting projecton of CA atom coordinates onto the XY plane
    Max diameter between E:75 & K:17 is 79.701881; effective radius is 39.898543
    (79.70188096903092, 'E:75', 'K:17', 39.89854271684067)



You can set the tolerated height difference between points using the bin\_ parameter; by default=3 Angstrom, change to 30 (the Z component of the distance is disregarded regardless of the bin\_ parameter!). Note that the effective radius has not changed:


.. code-block:: bash

    >>> calcDiameter.calcDiameter('1qaw.pdb', bin_=30)
    Reading PDB file
    Obtaining approximate orientation by testing rotations about X and Y axes every 10 degrees...
    Obtaining accurate orientation by testing rotations about X and Y axes every 1 degree...
    Plotting projecton of CA atom coordinates onto the XY plane
    Max diameter between E:75 & K:18 is 79.706971; effective radius is 39.898543
    (79.70697056799868, 'E:75', 'K:18', 39.89854271684067)

The full list of options is as follows

.. code-block:: bash

    >>>calcDiameter(pdb, plot=True, plot3d=False, no_rotation=False, bin_=3, test=5)

You can set 'no_rotation' to True if you believe that the pdb is already correctly oriented - the structure is already flat on the XY plane.

You can also set plot3d to True if you want to see the 3d plots of points making up the structure. First you will see the original orientation of the pdb - feel free to look at it from all angles, then close it to see the best orientation that the program has found - the structure should lie flat on the XY plane; close the plot to obtain the max diameter along the XY plane. 

The test parameter specifies the radius of the structure (from its centre) that is expected to stay hollow provided we have found the right orientation for the structure.



Then you can query PDB to retrieve all structures of rotational symmetry Cn (specify n); returns a pandas data-frame with parameters calculated for the structures:


.. code-block:: bash

    >>> getDiametersCn(13)
    Retrieving list of PDBs that match the selected criteria...
	2JES,2X2V,3JVO,4CBJ,4CBK,4V2T,4XJN,6GY6
	Downloading PDB 2JES
	Reading 2JES PDB file
	Obtaining approximate orientation by testing rotations about X and Y axes every 10 degrees...
	(...)
	        Diameter label1 label2  Eff. radus  Cn
	2JES  162.626456   G:30   U:29   81.913051  13
	2X2V   60.312264   G:40   M:40   30.425173  13
	3JVO  110.369143    C:1   I:50   55.239389  13
	4CBJ   60.344003   F:40   M:40   30.422166  13
	4CBK   60.169909   E:40   L:40   30.276677  13
	4V2T  220.978870   C:82   X:82  111.307835  13
	4XJN  193.364481  B:110  M:110   97.363493  13
	6GY6  249.636369  I:151  S:151  125.730877  13

The full list of options is as follows: res_min & res_max are the minimum and maximum structure resolution thresholds - defaults 0.0 and 3.0, respectively:


.. code-block:: bash

	    >>>getDiametersCn(n, res_min = 0.0, res_max = 3.0, plot=True, bin_=3, test=5)

Licence
-------

MIT


Authors
-------

`Jan Zaucha <j.zaucha@tum.de>`_
