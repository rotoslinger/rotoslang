#====================================================================================
#====================================================================================
#
# ka_advancedJoints_commands
#
# DESCRIPTION:
#   commands that are common to all advanced joint setups
#
# DEPENDENCEYS:
#   -Maya
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

import pymel.core as pymel
import maya.cmds as cmds
import maya.mel as mel

import ka_rigTools.ka_math as ka_math; importlib.reload(ka_math)
import ka_rigTools.ka_util as ka_util; importlib.reload(ka_util)
import ka_rigTools.ka_pymel as ka_pymel; importlib.reload(ka_pymel)
import ka_rigTools.ka_shapes as ka_shapes; importlib.reload(ka_shapes)
import ka_rigTools.ka_transforms as ka_transforms; importlib.reload(ka_transforms)
import ka_rigTools.ka_constraints as ka_constraints; importlib.reload(ka_constraints)
import importlib



def setRigTypes(nodes, rigTypes):

    # excepts args as list or single item
    if not isinstance(nodes, list):
	nodes = [nodes]
    if not isinstance(rigTypes, list):
	rigTypes = [rigTypes]

    for node in nodes:
	if not hasattr(node, 'rigType'):
	    node.addAttr('rigType', dataType='string', shortName='rigType')
	else:
	    node.rigType.set(lock=False)

	node.rigType.set(str(rigTypes))
	node.rigType.set(lock=True)

def getRigTypes(node):
    if hasattr(node, 'rigType'):
	rigTypes = eval(node.rigType.get())
	if isinstance(rigTypes, list):
	    if rigTypes:
		if isinstance(rigTypes[0], str):
		    return rigTypes

    return []