'''
@author: Jan Zaucha. Created on 12 Dec 2018

Purpose: To find the maximum diameter of a ring-shaped protein complex of Cn symmetry. 
'''
from Bio.PDB import *
import numpy as np
import pandas as pd
import random
from itertools import combinations
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import warnings
import urllib.request, urllib.error, urllib.parse
import requests
import gzip
import shutil

def queryPDB(n, res_min=0.0, res_max=3.0):
    """
    Uses PDB's restful API to query proteins with Cn symmetry. Returns list of accession ids. 
    """
    url = 'http://www.rcsb.org/pdb/rest/search'
    queryText = """
    <orgPdbQuery>
      <queryType>org.pdb.query.simple.PointGroupQuery</queryType>
      <description>Finds PDB entries based on symmetry: Protein Symmetry is C1 and R m s d min is 0.5 and R m s d max is 1.0</description>
        <pointGroup>C%s</pointGroup>
        <rMSDComparator>between</rMSDComparator>
        <rMSDMin>%s</rMSDMin>
        <rMSDMax>%s</rMSDMax>
    </orgPdbQuery>
    """ % (n,res_min, res_max)
    data = queryText.encode("utf-8")
    #data = urllib.parse.urlencode(queryText).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    f = urllib.request.urlopen(req)
    result = f.read().decode().split('\n')[:-1]
    return result

def readPDB(filename):
    """
    Returns CA coordinates of residues in PDB & the residue identifiers (two lists)
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        CA_coordinates = []
        residues = []
        if filename.split('.')[-1]=='pdb':
            p=PDBParser()
        else:
            p = MMCIFParser()
        structure=p.get_structure('name', filename)
        print('Reading %s PDB file' % filename.split('/')[-1].split('.')[0])
        for model in structure:
            for chain in model:
                for residue in chain:
                    try:
                        chain_id = chain.get_id()
                        resid = residue.get_id()
                        CA_coordinates.append([residue['CA'].get_vector()[0], residue['CA'].get_vector()[1], residue['CA'].get_vector()[2]])
                        residues.append('%s:%s' % (chain_id, resid[1]))
                    except:
                        continue
        CA_coordinates = np.array(CA_coordinates)
        return CA_coordinates, residues


def rotX(points, theta):
    """
    Rotate a list of points (corresponding to the protein structure coordinates) by theta about X axis
    """
    rotation = np.array([[1, 0, 0],[0, np.cos(theta), -1*np.sin(theta)],[0, np.sin(theta), np.cos(theta)]])
    rotated = [] 
    for point in points:
        rotated.append(np.matmul(point, rotation))
    return np.array(rotated)

def rotY(points, theta):
    """
    Rotate a list of points (corresponding to the protein structure coordinates) by theta about Y axis
    """
    rotation = np.array([[np.cos(theta), 0, np.sin(theta)],[0, 1, 0],[-1*np.sin(theta), 0, np.cos(theta)]])
    rotated = [] 
    for point in points:
        rotated.append(np.matmul(point, rotation))
    return np.array(rotated)

def distXY(p1,p2):
    """
    Distance between two points along the XY plane (note that the Z component is disregarded!)
    """
    return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def maxDistZ(coordinates, orientation, num=5):
    """
    returns the maximum distance between the num top and num bottom points
    (num defines how many points should be considered - this guarantees that the estimate of the XY plane is roubust)
    if orientation is vertical actually return maximum XY span (for dealing with alpha helical bundles)
    """
    if orientation=='flat':
        return np.mean(sorted(coordinates[:,2])[-num:])-np.mean(sorted(coordinates[:,2])[:num])
    elif orientation=='vertical':
        return (max(coordinates[:,0])-min(coordinates[:,0]))**2+(max(coordinates[:,1])-min(coordinates[:,1]))**2

def maxDistXY(coordinates,residues, bin_ = 5, num = 5):
    """
    returns the maximum distance between any pair of points that are within bin_ Angstrom of one another along the Z axis
    as well as the x,y coordinates of each point and the corresponding residue labels 
    and the radius (calculated from num points furthest away from the centre) & the stucture's centre on the XY plane   
    """
    coordinates_=coordinates[:,:2]
    result = {}
    dist = []
    pair = []
    for comb in combinations(list(range(len(coordinates_))),2):
        if np.abs(coordinates[comb[0]][2]-coordinates[comb[1]][2])<=bin_:
            dist.append(distXY(coordinates_[comb[0]], coordinates_[comb[1]]))
            pair.append(comb)
    id_ = dist.index(max(dist))
    p1 = coordinates_[pair[id_][0]]
    p2 = coordinates_[pair[id_][1]]
    label1 = residues[pair[id_][0]]
    label2 = residues[pair[id_][1]]
    # calculate radius:
    x_mean, y_mean = np.mean(coordinates[:,0]), np.mean(coordinates[:,1])
    centre = [x_mean, y_mean]
    radii = []
    for point in coordinates_:
        radii.append(distXY(centre, point))
    #print coordinates[pair[id_][0]][2],coordinates[pair[id_][1]][2]
    return max(dist), p1,p2,label1,label2, np.mean(sorted(radii)[-num:]), centre


def testRotations(coordinates, range_1, range_2, residues, bin_=3, test=False, orientation='flat'):
    """
    tests ranges of rotations along the X and Y axes (when the disc lies flat on the XY plane, rotations about Z will be rotationally invariant)
    returns the maximal diameter for the best oriantation given the ranges of angles of rotations to test
    """
    min_height = []
    i_j = []
    for i in range_1:
        for j in range_2:
            coordinates1 = rotX(coordinates, i)
            coordinates2 = rotY(coordinates1, j)
            min_height.append(maxDistZ(coordinates2, orientation))
            i_j.append([i,j])
            # rotation matrices are not commutative so do it in the other order as well
            coordinates1 = rotX(coordinates, j)
            coordinates2 = rotY(coordinates1, i)
            min_height.append(maxDistZ(coordinates2, orientation))
            i_j.append([j,i])
    id_ = min_height.index(min(min_height))
    coordinates1 = rotX(coordinates, i_j[id_][0])
    coordinates2 = rotY(coordinates1, i_j[id_][1])
    max_diameter, p1, p2, label1, label2, radius, centre = maxDistXY(coordinates2, residues, bin_=bin_)
    if test:
        # Test if the dtsructre is hollow in the middle (if not, it is an indication that something is wrong)
        x_mean, y_mean = np.mean(coordinates2[:,0]), np.mean(coordinates2[:,1])
        success = True
        for point in coordinates2:
            if (point[0] - x_mean)**2 + (point[1] - y_mean)**2 < test**2:
                return False
    return i_j[id_], max_diameter, coordinates2, p1, p2, label1, label2, radius, centre

def findDiameter(coordinates,name,residues, plot3d=False, plot=True, no_rotation = False, bin_=3, test=5):

    """
    Main function that finds the best orientation such the structure such that it lies flat on the XY plane
    and then returns the maximum diameter in a given height slice

    """
    if not no_rotation:
        print('Obtaining approximate orientation by testing rotations about X and Y axes every 10 degrees...')  
        range_ = np.linspace(-np.pi/2.0, np.pi/2.0, num=19, endpoint=True)
        ij, max_diameter, rotated, p1, p2, label1, label2, radius, centre = testRotations(coordinates, range_, range_, residues, bin_=bin_, orientation='flat')
        # ramp up the resolution around the chosen values
        range_ = range_.tolist()
        range_1 = np.linspace(range_[max(0, range_.index(ij[0])-1)], range_[min(len(range_)-1, range_.index(ij[0])+1)], num=21, endpoint=True)
        range_2 = np.linspace(range_[max(0, range_.index(ij[1])-1)], range_[min(len(range_)-1, range_.index(ij[1])+1)], num=21, endpoint=True)
    if no_rotation:
        range_1=[0]
        range_2=[0]
    if not no_rotation:
        print('Obtaining accurate orientation by testing rotations about X and Y axes every 1 degree...')
    try:  
        ij, max_diameter, rotated, p1, p2, label1, label2, radius,centre = testRotations(coordinates, range_1, range_2, residues, bin_=bin_, test=test, orientation='flat')
        success = True
    except:
        if not no_rotation:
            print('Perhaps this is an alpha helical bundle, trying vertical orientation')  
            print('Obtaining approximate orientation by testing rotations about X and Y axes every 10 degrees...')  
            range_ = np.linspace(-np.pi/2.0, np.pi/2.0, num=19, endpoint=True)
            ij, max_diameter, rotated, p1, p2, label1, label2, radius, centre = testRotations(coordinates, range_, range_, residues, bin_=bin_, orientation='vertical')
            # ramp up the resolution around the chosen values
            range_ = range_.tolist()
            range_1 = np.linspace(range_[max(0, range_.index(ij[0])-1)], range_[min(len(range_)-1, range_.index(ij[0])+1)], num=21, endpoint=True)
            range_2 = np.linspace(range_[max(0, range_.index(ij[1])-1)], range_[min(len(range_)-1, range_.index(ij[1])+1)], num=21, endpoint=True)
        if no_rotation:
            range_1=[0]
            range_2=[0]
        if not no_rotation:
            print('Obtaining accurate orientation by testing rotations about X and Y axes every 1 degree...')
        try:  
            ij, max_diameter, rotated, p1, p2, label1, label2, radius,centre = testRotations(coordinates, range_1, range_2, residues, bin_=bin_, test=test, orientation='vertical')
            success = True
        except:
            success=False
            print("Something still looks off. Skipping structure %s" % name)
    if plot3d:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            #first plot initial orientation
            #pyplot.clf()
            fig = pyplot.figure()
            ax = Axes3D(fig)
            ax.scatter(coordinates[:,0], coordinates[:,1], coordinates[:,2],alpha=0.5)
            ax.set_xlabel('X axis')
            ax.set_ylabel('Y axis')
            ax.set_zlabel('Z axis')
            ax.set_title('Initial orientation')
            pyplot.show()
            # now plot best rotation
            fig = pyplot.figure()
            ax = Axes3D(fig)
            ax.set_xlabel('X axis')
            ax.set_ylabel('Y axis')
            ax.set_zlabel('Z axis')
            ax.scatter(rotated[:,0], rotated[:,1], rotated[:,2],alpha=0.5)
            ax.set_title('Rotated')
            pyplot.show()
    if plot and success:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            print('Plotting projecton of CA atom coordinates onto the XY plane')
            pyplot.clf()  
            f, ax = pyplot.subplots()
            ax.scatter(rotated[:,0], rotated[:,1], alpha=0.2)
            ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color = 'r')
            ax.plot([centre[0]], [centre[1]], 'x', color='r', mew=1, ms=6)
            circle = pyplot.Circle((centre[0], centre[1]), radius, color='g', alpha = 0.1, clip_on=False)
            ax.add_artist(circle)
            pyplot.axis('equal')  
            ax.set_xlabel('X axis')    
            ax.set_ylabel('Y axis')      
            ax.set_title('Max Diameter along XY plane=%f\nbetween %s & %s; Eff. diameter=%f' % (max_diameter, label1, label2, radius*2))
            f.savefig('%s_projection.pdf' % name)
    if success:
        return max_diameter, label1, label2, radius
    else:
        return success



def calcDiameter(pdb, plot=True, plot3d=False, no_rotation=False, bin_=3, test=5):
    """
    Function that reads the pdb (provide pdb file name or full path to file if you have it in another directory) and invokes the findDiameter function
    You can set the tolerated heigt difference between points using the bin_ parameter; default=3 Angstrom
    You can set no_rotation to True if you believe that the pdb is already correctly oriented - the structure is already flat on the XY plane
    You can inspect the initial and final orientations of the structure in 3d by setting plot3d to True. First you will see the initial orientation of the pdb - feel free to look at
    from all angles, then close it to see the best orientation that the program has found - the structure should lie flat on the XY plane; close the plot to obtain the max diameter
    along the XY plane (the Z component of the distance is diregarded regardless of the bin_ parameter!)
    By default, plot=True; the projection of all CA atom coordinates on the XY plane is plotted; the title of the plot specifies the max diamater in Angstroms and provides the labels for the two
    residues which are the furthest apart.
    """
    coords, residues = readPDB(pdb)
    name = pdb.split('/')[-1].split('.')[0]
    try:
        diameter, label1, label2, radius = findDiameter(coords, name, residues, plot3d=plot3d, plot=plot, no_rotation=no_rotation, bin_=bin_, test=test)
        print(("Max diameter between %s & %s is %f; effective radius is %f" % (label1, label2, diameter, radius)))
    except:
        print("Bad news, the method has failed to provide a result in this case. See if the structure looks reasonable, if yes contact the author.")
        return False
    return diameter, label1, label2, radius

def getDiametersCn(n, res_min = 0.0, res_max = 3.0, plot=True, bin_=3, test=5):
    """
    Get diameters of PDBs that have rotational symmetry Cn and specified min (0.0) and max resolution (3.0).
    This gives us a list of PDB accessions that match the criteria.

    How to download the 'biologica; assembly' files from PDB?
    1) Use PDBList() from Biopython. But this does not allow downloading biological assembly.
    pdblist = PDBList().download_pdb_files(pdbs, pdir=os.getcwd()) 
    2) Download directly from files.pdb
    files.rcsb.org/download/2EXS.pdb1.gz
    3) Download from the Pisa EBI server:
    http://www.ebi.ac.uk/pdbe/pisa/cgi-bin/multimer.pdb?2exs:1,1
    Here I try using option 2. 
    """
    pdbs = queryPDB(n=n, res_min=res_min, res_max=res_max)
    print("Retrieving list of PDBs that match the selected criteria...")
    print(','.join(pdbs))
    data = {}
    for pdbcode in pdbs:
        try:
            coords, residues = readPDB('%s.pdb' % pdbcode)
        except:
            try:
                print("Downloading PDB %s" % pdbcode)
                url = "http://files.rcsb.org/download/%s.pdb1.gz" % pdbcode
                fname = '%s.pdb' % pdbcode
                r = requests.get(url)
                num_bytes = open('%spdb.gz' % pdbcode , 'wb').write(r.content)
                with gzip.open('%spdb.gz' % pdbcode, 'rb') as f_in:
                    with open('%s.pdb' % pdbcode, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                coords, residues = readPDB('%s.pdb' % pdbcode)
            except:
                print("Downloading/unpacking %s failed; skipping..." % pdbcode)
                continue
        name = pdbcode
        try:
            diameter, label1, label2, radius = findDiameter(coords, name, residues, plot=plot, bin_=bin_, test=test)
            print(("%s max diameter between %s & %s is %f; effective radius is %f" % (pdbcode, label1, label2, diameter, radius)))
            data[pdbcode] = [diameter, label1, label2, radius, n]
        except:
            print(("%s failed. It is probably a nonstandard structure" % (pdbcode)))
            continue
    return pd.DataFrame.from_dict(data, orient='index',columns=['Diameter', 'label1', 'label2','Eff. radus', 'Cn'])



