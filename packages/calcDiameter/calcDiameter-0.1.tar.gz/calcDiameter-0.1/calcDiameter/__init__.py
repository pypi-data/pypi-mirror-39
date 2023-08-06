import numpy as np
from scipy.optimize import leastsq
from Bio.PDB import *
import numpy as np
import random
from itertools import combinations
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D



def readPDB(filename):
    CA_coordinates = []
    p=PDBParser()
    structure=p.get_structure('name', filename)
    for model in structure:
        for chain in model:
            for residue in chain:
                try:
                    CA_coordinates.append([residue['CA'].get_vector()[0], residue['CA'].get_vector()[1], residue['CA'].get_vector()[2]])
                    #print [residue['CA'].get_vector()[0], residue['CA'].get_vector()[1], residue['CA'].get_vector()[2]]
                except:
                    continue
    CA_coordinates = np.array(CA_coordinates)
    return CA_coordinates


def rotX(points, theta):
    rotation = np.array([[1, 0, 0],[0, np.cos(theta), -1*np.sin(theta)],[0, np.sin(theta), np.cos(theta)]])
    rotated = [] 
    for point in points:
        rotated.append(np.matmul(point, rotation))
    return np.array(rotated)

def rotY(points, theta):
    rotation = np.array([[np.cos(theta), 0, np.sin(theta)],[0, 1, 0],[-1*np.sin(theta), 0, np.cos(theta)]])
    rotated = [] 
    for point in points:
        rotated.append(np.matmul(point, rotation))
    return np.array(rotated)

def distXY(p1,p2):
    return np.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)

def maxDistZ(coordinates):
    return max(coordinates[:,2])-min(coordinates[:,2])

def maxDistXY(coordinates, pairwise=False):
    '''
    if pairwse=True then check all pairs of atoms
    else max check distance from average x and average y 
    '''
    coordinates_=coordinates[:,:2]
    dist = []
    pair = []
    if pairwise:
        for comb in combinations(range(len(coordinates_)),2):
            dist.append(distXY(coordinates_[comb[0]], coordinates_[comb[1]]))
            pair.append(comb)
    id_ = dist.index(max(dist))
    p1 = coordinates_[pair[id_][0]]
    p2 = coordinates_[pair[id_][1]]
    return max(dist),p1,p2

def testRotations(coordinates, range_1, range_2):
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
    max_diameter, p1, p2 = maxDistXY(coordinates2, pairwise=True)
    return i_j[id_], max_diameter, coordinates2, p1, p2

def findDiameter(coordinates,name, plot=True):

    """
    If the protein is a long cylinder: keep rotating until cross sectional area is the smallest; then fit disc and the radius is what we want
    If the protein is a very short cylinder then this will fail to privide the right answer.  
    """  
    # max diameter when projecting on XY plane
    # try different rotations

    range_ = np.linspace(-np.pi/2.0, np.pi/2.0, num=19, endpoint=True)
    ij, min_diameter, rotated, p1, p2 = testRotations(coordinates, range_, range_)
    # ramp up the resolution around the chosen values
    range_ = range_.tolist()
    range_1 = np.linspace(range_[max(0, range_.index(ij[0])-1)], range_[min(len(range_), range_.index(ij[0])+1)], num=21, endpoint=True)
    range_2 = np.linspace(range_[max(0, range_.index(ij[1])-1)], range_[min(len(range_), range_.index(ij[1])+1)], num=21, endpoint=True)
    ij, max_diameter, rotated, p1, p2 = testRotations(coordinates, range_1, range_2)
    if plot:
        #first plot initial orientation
        #pyplot.clf()
        fig = pyplot.figure()
        ax = Axes3D(fig)
        ax.scatter(coordinates[:,0], coordinates[:,1], coordinates[:,2],alpha=0.5)
        ax.set_title('Initial orientation')
        pyplot.show()
        #pyplot.savefig('%s_initial.pdf' % name)
        # now plot best rotation
        #pyplot.clf()
        fig = pyplot.figure()
        ax = Axes3D(fig)
        ax.scatter(rotated[:,0], rotated[:,1], rotated[:,2],alpha=0.5)
        ax.set_title('Rotated')
        pyplot.show()
        #pyplot.savefig('%s_rotated.pdf' % name)
        #pyplot.clf()
        # finally plot projection and radius... 
        #pyplot.clf()
        pyplot.scatter(rotated[:,0], rotated[:,1], alpha=0.2)
        #pyplot.plot([np.mean(rotated[:,0])], [np.mean(rotated[:,1])], '+', color='r')
        pyplot.plot([p1[0],p2[0]],[p1[1],p2[1]],color = 'r')        
        pyplot.title('Max Diameter=%f' % (max_diameter))
        pyplot.savefig('%s_cross_section.pdf' % name)
    return min_diameter



def calcDiameter(pdb, plot=True):
    coords = readPDB("%s.pdb" % pdb)
    diameter = findDiameter(coords, pdb, plot=plot)
    print "Max diameter is %d" % diameter
    return diameter