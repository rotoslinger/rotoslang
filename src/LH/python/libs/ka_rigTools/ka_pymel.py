#====================================================================================
#====================================================================================
#
# ka_pymel
#
# DESCRIPTION:
#   tools for working with pymel
#
# DEPENDENCEYS:
#   Maya
#   Pymel
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

import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya


##----------------------------------------------------------------------
#def getAsListOfPyNodes(inputA, returnList=[]):
    #"""takes an object that may be a collection of collections and returns
    #an list of all the contained pynodes (or strings, which will be returned as pyNodes)"""

    #if isinstance(inputA, dict):
        #for key in inputA:
            #value = inputA[key]
            #newDict[key] = getAsPyNodes(value)

        #return newDict

    #elif isinstance(inputA, list):
        #newList = []
        #for value in inputA:
            #newList.append(getAsPyNodes(value))

        #return newList

    #elif isinstance(inputA, tuple):
        #newList = []
        #for value in inputA:
            #newList.append(getAsPyNodes(value))

        #return newList

    #elif isinstance(inputA, basestring):
        #node = pymel.ls(inputA)
        #if node:
            #if len(node) == 1:
                #node = node[0]
                #return node

            #else:
                #pymel.error('more than 1 node matches name: '+value)

    #else:
        #return inputA


def getAsPyNodes(inputA):
    """takes an object that may be a collection of collections and returns
    an object that is structured the same, but with strings replaced with pyMelObjects"""

    if isinstance(inputA, dict):
        newDict = {}
        for key in inputA:
            value = inputA[key]
            newDict[key] = getAsPyNodes(value)

        return newDict

    elif isinstance(inputA, list):
        newList = []
        for value in inputA:
            newList.append(getAsPyNodes(value))

        return newList

    elif isinstance(inputA, tuple):
        newList = []
        for value in inputA:
            newList.append(getAsPyNodes(value))

        return newList

    elif isinstance(inputA, str):
        node = pymel.ls(inputA)
        if node:
            if len(node) == 1:
                node = node[0]
                return node

            else:
                pymel.error('more than 1 node matches name: '+value)

    else:
        return inputA


def getAsStrings(inputA):
    """takes an object that may be a collection of collections and returns
    an object that is structured the same, but with pyMelObjects replaced with strings"""

    if isinstance(inputA, dict):
        newDict = {}
        for key in inputA:
            value = inputA[key]
            newDict[key] = getAsStrings(value)

        return newDict

    elif isinstance(inputA, list):
        newList = []
        for value in inputA:
            newList.append(getAsStrings(value))

        return newList

    elif isinstance(inputA, tuple):
        newList = []
        for value in inputA:
            newList.append(getAsStrings(value))

        return newList

    elif hasattr(inputA, '__class__'):
        if hasattr(inputA.__class__, '__bases__'):
            if inputA.__class__.__bases__:
                for base in inputA.__class__.__bases__:
                    if 'pymel.core' in base.__module__:
                        return str(inputA)

    else:
        return inputA