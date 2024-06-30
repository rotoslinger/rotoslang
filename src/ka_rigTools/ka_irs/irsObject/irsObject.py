#====================================================================================
#====================================================================================
#
# irsObject
#
# DESCRIPTION:
#   base object for irs system
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

import ka_rigTools.ka_python as ka_python
import ka_rigTools.ka_naming as ka_naming


class IrsObject(object):

    def __init__(self, root=None, **kwargs):
        return self.__init__irsObject__(root=root, **kwargs)

    def __init__irsObject__(self, root=None, **kwargs):

        # set variables
        self.currentNamespace = None
        self.baseName = kwargs.get('name', 'defaultName')
        self.side = kwargs.get('side', 'c')
        self.sideInt = kwargs.get('sideInt', 1)
        self.parent = kwargs.get('parent', None)

        #if root:
            #self.wrap(root)

        #else:
            #self.create(**kwargs)

    def wrap(self, root):
        self.root = root


    def startIrsObject(self):
        """starts the irsObject by creating a root group, assigning informational
        attributes to it, and setting up the namespace"""
        self._startNameSpace(self.baseName)
        self._createRoot()



    def finishIrsObject(self):
        """finishes the irsObject, combining the namespace with the node name
        to create the final name"""
        self._finishNameSpace()


    def _createRoot(self, **kwargs):
        self.root = pymel.createNode('transform')
        self.setName(self.root, 'group')
        self.root.addAttr('irsRootMembers', at='message')
        if self.parent:
            self.root.setParent(self.parent)

    def _startNameSpace(self, nameSpace):
        """Sets name space that will be later combined with the node name
        to create the final node name"""
        if self.side == 'l' or self.side == 'r':
            self.currentNamespace = '%s_%s' % (self.side, nameSpace)
        else:
            self.currentNamespace = nameSpace

        if pymel.namespace( exists=':'+self.currentNamespace ):
            pymel.namespace( removeNamespace=':'+self.currentNamespace )

        nameSpaceObject = pymel.Namespace.create( self.currentNamespace )
        pymel.Namespace.setCurrent( nameSpaceObject )


    def _finishNameSpace(self):
        """Combines the current nameSpace with the member nodes names"""

        pymel.namespace( set=':' )
        namespaceContents = pymel.ls(self.currentNamespace+':*', dependencyNodes=True)
        for node in namespaceContents:
            if node.nodeType() not in ['facade', 'hikSolver', 'ikSCsolver', 'ikSplineSolver', 'ikRPSolver']:
                node.rename('%s_%s' % (self.currentNamespace, node.nodeName().split(':')[-1]))

                if node != self.root:
                    node.addAttr('irsRootNode', at='message')
                    self.root.irsRootMembers >> node.irsRootNode


    def setName(self, node, name, index='', grouping='', nodePurpose=''):
        ka_naming.setName(node, name, index=index, side='', grouping=grouping, nodePurpose=nodePurpose)
