'''
@author: Jan Zaucha. Created on 12 Dec 2018

Purpose: To find the maximum diameter of a ring-shaped protein complex of Cn symmetry. 
'''
import numpy as np
from Bio.PDB import *
import numpy as np
import random
from itertools import combinations
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import warnings

def readPDB(filename):
    """
    Returns CA coordinates of residues in PDB & the residue identifiers (two lists)
    """
    print('Reading PDB file')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        CA_coordinates = []
        residues = []
        p=PDBParser()
        structure=p.get_structure('name', filename)
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

def maxDistZ(coordinates, num=7):
    """
    returns the maximum distance between the num top and num bottom points
    (num defines how many points should be considered - this guarantees that the estimate of the XY plane is roubust)
    """
    return np.mean(sorted(coordinates[:,2])[-num:])-np.mean(sorted(coordinates[:,2])[:num])

def maxDistXY(coordinates,residues, bin_ = 3):
    """
    returns the maximum distance between any pair of points that are within bin_ Angstrom of one another along the Z axis
    as well as the x,y coordinates of each point and the corresponding residue labels 
    """
    coordinates_=coordinates[:,:2]
    result = {}
    dist = []
    pair = []
    for comb in combinations(range(len(coordinates_)),2):
        if np.abs(coordinates[comb[0]][2]-coordinates[comb[1]][2])<=bin_:
            dist.append(distXY(coordinates_[comb[0]], coordinates_[comb[1]]))
            pair.append(comb)
    id_ = dist.index(max(dist))
    p1 = coordinates_[pair[id_][0]]
    p2 = coordinates_[pair[id_][1]]
    label1 = residues[pair[id_][0]]
    label2 = residues[pair[id_][1]]
    #print coordinates[pair[id_][0]][2],coordinates[pair[id_][1]][2]
    return max(dist), p1,p2,label1,label2


def testRotations(coordinates, range_1, range_2, residues, bin_=3):
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
            min_height.append(maxDistZ(coordinates2))
            i_j.append([i,j])
            # rotation matrices are not commutative so do it in the other order as well
            coordinates1 = rotX(coordinates, j)
            coordinates2 = rotY(coordinates1, i)
            min_height.append(maxDistZ(coordinates2))
            i_j.append([j,i])            
    id_ = min_height.index(min(min_height))
    coordinates1 = rotX(coordinates, i_j[id_][0])
    coordinates2 = rotY(coordinates1, i_j[id_][1])
    max_diameter, p1, p2, label1, label2 = maxDistXY(coordinates2, residues, bin_=bin_)
    return i_j[id_], max_diameter, coordinates2, p1, p2, label1, label2

def findDiameter(coordinates,name,residues, plot3d=False, plot=True, no_rotation = False, bin_=3):

    """
    Main function that finds the best orientation such the structure such that it lies flat on the XY plane
    and then returns the maximum diameter in a given height slice

    """
    print('Obtaining approximate orientation by testing rotations about X and Y axes every 10 degrees...')  
    range_ = np.linspace(-np.pi/2.0, np.pi/2.0, num=19, endpoint=True)
    ij, max_diameter, rotated, p1, p2, label1, label2 = testRotations(coordinates, range_, range_, residues, bin_=bin_)
    # ramp up the resolution around the chosen values
    range_ = range_.tolist()
    range_1 = np.linspace(range_[max(0, range_.index(ij[0])-1)], range_[min(len(range_), range_.index(ij[0])+1)], num=21, endpoint=True)
    range_2 = np.linspace(range_[max(0, range_.index(ij[1])-1)], range_[min(len(range_), range_.index(ij[1])+1)], num=21, endpoint=True)
    if no_rotation:
        range_1=[0]
        range_2=[0]
    if not no_rotation:
        print('Obtaining accurate orientation by testing rotations about X and Y axes every 1 degree...')  
    ij, max_diameter, rotated, p1, p2, label1, label2 = testRotations(coordinates, range_1, range_2, residues, bin_=bin_)
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
    if plot:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            print('Plotting projecton of CA atom coordinates onto the XY plane')
            pyplot.clf()  
            pyplot.scatter(rotated[:,0], rotated[:,1], alpha=0.2)
            pyplot.plot([p1[0],p2[0]],[p1[1],p2[1]],color = 'r') 
            pyplot.axis('equal')  
            pyplot.xlabel('X axis')    
            pyplot.ylabel('Y axis')      
            pyplot.title('Max Diameter along XY plane=%f\nBetween %s & %s' % (max_diameter, label1, label2))
            pyplot.savefig('%s_projection.pdf' % name)
    return max_diameter, label1, label2



def calcDiameter(pdb, plot=True, plot3d=False, no_rotation=False, bin_=3):
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
    diameter, label1, label2 = findDiameter(coords, name, residues, plot3d=plot3d, plot=plot, no_rotation=no_rotation, bin_=bin_)
    print ("Max diameter between %s & %s is %f" % (label1, label2, diameter))
    return diameter, label1, label2