#====================================================================================
#====================================================================================
#
# ka_irs\core.py
#
# DESCRIPTION:
#   main list of functions that a user would want to access directly for ka_irs
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

import ka_rigTools.ka_irs.irsObject.irsObject as irsObject

import ka_rigTools.ka_irs.irsObject.irsRig.irsRig as irsRig
import ka_rigTools.ka_irs.irsObject.irsRig.irsRig_animation as irsRig_animation


import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb as irsLimb

import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_bipedLeg.irsLimb_bipedLeg as irsLimb_bipedLeg

#import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_bipedLeg.features.irsLimb_bipedLegFeature_fk as irsLimb_bipedLegFeature_fk

import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_spine.irsLimb_spine as irsLimb_spine
#import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_spine.features.irsLimb_bipedLegFeature_fk as irsLimb_bipedLegFeature_fk

def createHuman():
    cmds.file(newFile=True, force=True)
    controlRigObject = irsRig_animation.IrsAnimationRig()
    bipedLegObject = irsLimb_bipedLeg.IrsLimb_bipedLeg(name='leg', side='l', parent=controlRigObject.root)
    spineObject = irsLimb_spine.IrsLimb_spine(name='spine', side='c', parent=controlRigObject.root)
    OOOOOOO = 'spineObject.root';  print('%s = %s %s'%(str(OOOOOOO),str(eval(OOOOOOO)),str(type(eval(OOOOOOO)))))
    #bipedLegObject.addFeature('fk')

