#====================================================================================
#====================================================================================
#
# ka_math
#
# DESCRIPTION:
#   A collection of mathmatical functions
#
#
#
# AUTHOR:
#   Kris Andrews (3dkris@3dkris.com)
#
#====================================================================================
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are
#met:

    #(1) Redistributions of source code must retain the above copyright
    #notice, this list of conditions and the following disclaimer.

    #(2) Redistributions in binary form must reproduce the above copyright
    #notice, this list of conditions and the following disclaimer in
    #the documentation and/or other materials provided with the
    #distribution.

    #(3)The name of the author may not be used to
    #endorse or promote products derived from this software without
    #specific prior written permission.

#THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
#IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
#INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#POSSIBILITY OF SUCH DAMAGE.
#====================================================================================

import math


import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel

import ka_rigTools.ka_python as ka_python #;reload(ka_python)


def getMidpoint(points):
    """Return Mid poitn of given points
    Args:
        points - list of lists - a list of points, with each point being a list of values (ie: 3 values
                 for a 3d point 2 values for a 2d point
    """
    numOfPoints = len(points)
    midPoint = []

    dimensions = len(points[0])
    sums = []
    for each in range(dimensions): sums.append(0.0)

    for point in points:
        for i, n in enumerate(sums):
            sums[i] += point[i]

    for i, n in enumerate(sums): sums[i] /= 2.0


    return sums



def distanceBetween(pointA, pointB):
    '''returns distance between a list of 2d or 3d coordinates'''
    sum = 0
    for i, each in enumerate(pointA):
        sum += (pointA[i] - pointB[i])**2

    return math.sqrt( sum )

def getVolumeOfTetrahedron(points):
    """takes 4 points, and returns the volume the tetrahedron it forms"""
    vectorA = subtractVectors(points[1], points[0])
    vectorB = subtractVectors(points[2], points[0])
    vectorC = subtractVectors(points[3], points[0])
    return (abs(dotProduct(vectorA, crossProduct(vectorB, vectorC))) / 6)

def getVolume(points):
    numbOfPoints = len(points)
    if numbOfPoints == 4:
        return getVolumeOfTetrahedron(points)


def crossProduct(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c

def magnitudeOfVector(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def normalizeVector(v):
    '''normalize vector'''
    vmag = magnitudeOfVector(v)
    return [ v[i]/vmag  for i in range(len(v)) ]

def addVectors(u, v):
    '''add vector'''
    return [ u[i]+v[i] for i in range(len(u)) ]

def subtractVectors(u, v):
    '''subtract Vector'''
    return [ u[i]-v[i] for i in range(len(u)) ]

def multiplyVectors(u, m):
    '''multiply Vector u by value m'''
    return [ u[i]*m for i in range(len(u)) ]

def dotProduct(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def averageVectors(u, v):
    return [ (u[i]+v[i])/2 for i in range(len(u)) ]


def sum_(a, b):
    if isinstance(a, list): return addVectors(a, b)
    else: return a + b

def subtract(a, b):
    if isinstance(a, list): return subtractVectors(a, b)
    else: return a - b

def mutliply(a, b):
    if isinstance(a, list): return multiplyVectors(a, b)
    else: return a + b

def angleBetween(vector1, vector2):
    r = math.acos(dotProduct(vector1, vector2) / (magnitudeOfVector(vector1) * magnitudeOfVector(vector2)))
    return math.degrees(r)

def normalize(v):
    if isinstance(v, list): return normalizeVector(v)

#def getDeterminant(a):
    #lenA = len(a)
    #a.append(a[0])
    #a.append(a[1])
    #x = 0
    #for i in range(lenA-2):
        #y=1
        #for j in range(lenA-2):
            #y *= a[i+j][j]
        #x += y

    #p = 0
    #for i in range(lenA-2):
        #y=1;
        #z = 0;
        #for j in range(2, -1, -1):
            #y *= a[i+z][j]
            #z+=1
        #z += 1
        #p += y

    #return x - p

def getDeterminant(matrix):
    lenOfMatrix = len(matrix) # rows
    if lenOfMatrix > 2:
        factor = 1 # flips between neg and pos
        iA=0
        determinant=0

        while iA <= lenOfMatrix-1:
            d={}
            iB=1

            while iB <= lenOfMatrix-1:
                iC=0
                d[iB]=[]
                while iC<=lenOfMatrix-1:
                    if (iC==iA):
                        u=0
                    else:
                        d[iB].append(matrix[iB][iC])
                    iC+=1
                iB+=1

            matrixB=[d[x] for x in d]
            determinant = sum(determinant, (mutliply(factor, mutliply(matrix[0][iA], getDeterminant(matrixB), ))))

            factor *= -1
            i += 1

        return determinant


    else:
        return subtract(mutliply(matrix[0][0], matrix[1][1]), mutliply(matrix[0][1],matrix[1][0]))

#def getDeterminant(matrix):
    #lenOfMatrix = len(matrix) # rows
    #factor = 1
    #for i in range(lenOfMatrix):
        #pass

pass

#def dete(a):
   #x = (a[0][0] * a[1][1] * a[2][2]) + (a[1][0] * a[2][1] * a[3][2]) + (a[2][0] * a[3][1] * a[4][2])
   #y = (a[0][2] * a[1][1] * a[2][0]) + (a[1][2] * a[2][1] * a[3][0]) + (a[2][2] * a[3][1] * a[4][0])

   #return x - y

#def sum():
    #pass

#def dete(a):
    #dimentions = len(a)
    #output = []
    #for i in range(dimentions):
        #row = []
        #for i in range(dimentions):
            #row.append(None)
        #output.append(row)


    #for ia in range(dimentions):

   #x =

   #y = (a[0][2] * a[1][1] * a[2][0]) + (a[1][2] * a[2][1] * a[3][0]) + (a[2][2] * a[3][1] * a[4][0])

   #return x - y
#[0,1,2
 #0,1,2
 #0,1,2]

#def getBarycentricCoordinates(simplex, point):
    #barycentricCoordinates = []
    #dimentions = len(point)
    #pointsInSimplex = len(simplex)
    #lastSimplexIndex = pointsInSimplex-1

    #matrix = []
    #for rowIndex in range(dimentions):
        #column = []
        #for columnIndex in range(pointsInSimplex):
            #if columnIndex != lastSimplexIndex:
                #vector = subtractVectors(simplex[columnIndex], simplex[lastSimplexIndex])
                #column.append(vector)
        #matrix.append(column)

    #print matrix
    #determinant = getDeterminant(matrix)

    #return determinant

def getBarycentricCoordinates(simplex, point):
    barycentricCoordinates = []
    dimentions = len(point)
    pointsInSimplex = len(simplex)
    lastSimplexIndex = pointsInSimplex-1

    if dimentions == 3:
        total_volume = getVolumeOfTetrahedron((simplex[0], simplex[1], simplex[2], simplex[3]))
        tetraA_volume = getVolumeOfTetrahedron((simplex[1], simplex[2], simplex[3], point))
        tetraB_volume = getVolumeOfTetrahedron((simplex[0], simplex[2], simplex[3], point))
        tetraC_volume = getVolumeOfTetrahedron((simplex[0], simplex[1], simplex[3], point))
        tetraD_volume = getVolumeOfTetrahedron((simplex[0], simplex[1], simplex[2], point))

        barycentricCoordinates = ((tetraA_volume/total_volume), (tetraB_volume/total_volume), (tetraC_volume/total_volume), (tetraD_volume/total_volume), )

        return barycentricCoordinates

#def tetrahedralizePoints(points):
    #tetrahedrons = []
    #tetrahedron = []

    #solvedTetrahedrons = {}
    #unsolvedTetrahedrons = {}

    #unsolvedPoints = {}
    #solvedPoints = {}
    #pointDict = {}
    #for i, point in enumerate(points):
        #pointDict[i] = point
        #unsolvedPoints[i] = None

    #currentTetra = (0,1,2,3)
    #while currentTetra:
        #for i in unsolvedPoints:
            #barryWeights = getBarycentricCoordinates([pointDict[currentTetra[0]], pointDict[currentTetra[1]], pointDict[currentTetra[2]], pointDict[currentTetra[3]]], pointDict[i])

            ## a point is inside the current tetra
            #if barryWeight[0] + barryWeights[1] + barryWeights[2] + barryWeights[3] <= 1:
                #pass

            #else:
                #solvedTetrahedrons.append(currentTetra)

    #for i in range(4):
        #tetrahedron.append(points[i])
    #tetrahedrons.append(tetrahedron)

    #return tetrahedrons


def testA():
    cmds.file(newFile=True, force=True)
    points = [[-0.9609970484, 0.365637511932, 2.22360586626],
               [-0.674784755617, 0.125772274035, -4.97449767664],
               [2.02942906326, 5.11446127606, -4.7692572918],
               [-4.56076916929, 5.15592487068, -4.58305108432],]

    for point in points:
        loc = pymel.spaceLocator()
        loc.t.set(point)

    interiorPoint = [-1.18105510866, 1.84263103104, -2.69437256414]
    loc = pymel.spaceLocator()
    loc.t.set(interiorPoint)

    print(getBarycentricCoordinates(points, interiorPoint))


def vectorProduct(input1, input2, operation, normalizeOutput=False):
    if operation in ['dotproduct', 'dotProduct', 1]:
        result = sum([ input1[i] * input2[i] for i in range(len(input1))])
    elif operation in ['crossproduct', 'crossProduct', 2]:
        a = newVector(a=input1)
        b = newVector(a=input2)
        result = a ^ b
    elif operation in ['vectormatrixproduct', 'vectorMatrixProduct', 3]:
        a = newVector(a=input1)
        mat = getWorldMat(input2)
        result = a * mat
    elif operation in ['pointmatrixproduct', 'pointMatrixProduct', 4]:
        a = newPoint(a=input1)
        mat = getWorldMat(input2)
        result = a * mat
    else:
        result = 0

    if normalizeOutput:
        if isinstance(result, float):
            result = 1.0
        else:
            result.normalize()
    if not isinstance(result, float):
        result = (result.x, result.y, result.z)
    return result
