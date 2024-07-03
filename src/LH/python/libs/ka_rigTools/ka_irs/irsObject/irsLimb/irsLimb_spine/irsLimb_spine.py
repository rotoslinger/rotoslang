#====================================================================================
#====================================================================================
#
# irsLimb_spine
#
# DESCRIPTION:
#   a limb representing a bipedLeg
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

import ka_rigTools.ka_math as ka_math
import ka_rigTools.ka_python as ka_python
import ka_rigTools.ka_attr as ka_attr
import ka_rigTools.ka_controls as ka_controls
import ka_rigTools.ka_transforms as ka_transforms

import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb as irsLimb
import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_spine.features.irsLimb_spineFeature_fk as irsLimb_spineFeature_fk
import ka_rigTools.ka_irs.irsObject.irsLimb.irsLimb_spine.features.irsLimb_spineFeature_ik as irsLimb_spineFeature_ik


DEFAULT_MATRICES = {'root':[1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, -1.7763568394002505e-15, 28.919381184266278, 1.2646744930629439, 1.0],
                    'pelvis':[2.2204460492503131e-16, -1.0, 0.0, 0.0, 2.2204460492503131e-16, 0.0, 1.0, 0.0, -1.0, -2.2204460492503131e-16, 2.2204460492503131e-16, 0.0, 0.0, 28.919381184266275, 1.2646744930629443, 1.0],
                    'pelvisEnd':[2.2204460492503131e-16, -1.0, 0.0, 0.0, 2.2204460492503131e-16, 0.0, 1.0, 0.0, -1.0, -2.2204460492503131e-16, 2.2204460492503131e-16, 0.0, 1.3954728578351823e-15, 22.634730141714108, 1.2646744930629434, 1.0],
                    'lowerSpines':None,
                    'upperSpine':[2.2204460492503131e-16, 1.0, 0.0, 0.0, -2.2204460492503128e-16, 0.0, 0.99999999999999989, 0.0, 1.0, -2.2204460492503131e-16, 2.2204460492503131e-16, 0.0, 8.1772042576454439e-16, 40.602066589032731, 1.2646744930629437, 1.0],
                    'upperSpineEnd':[2.2204460492503126e-16, 0.99999999999999978, 0.0, 0.0, -2.2204460492503123e-16, 0.0, 0.99999999999999967, 0.0, 1.0, -2.2204460492503131e-16, 2.2204460492503131e-16, 0.0, 8.0735799252421919e-15, 51.317196509575666, 1.264674493062941, 1.0],
                   }


DEFAULT_SIZES = {'root':10,
                 'pelvis':5,
                 'pelvisEnd':5,
                 'lowerSpines':5,
                 'upperSpine':5,
                 'upperSpineEnd':5,
                 }


class IrsLimb_spine(irsLimb.IrsLimb):
    features = [irsLimb_spineFeature_fk.IrsLimb_spineFeature_fk,
                irsLimb_spineFeature_ik.IrsLimb_spineFeature_ik,
               ]


    def __init__(self, root=None, **kwargs): #=======================================================================


        # modify kwargs --------------------------------------------------------------------------------------
        kwargs['name'] = kwargs.get('name', 'bipedLeg')

        # init superClass --------------------------------------------------------------------------------------
        self.__init__IrsLimb__(root, **kwargs)

        # set object variables --------------------------------------------------------------------------------------
        self.defaultXformsGroup = None
        self.defaultXform_root = None
        self.defaultXform_pelvis = None
        self.defaultXform_pelvisEnd = None
        self.defaultXform_lowerSpines = None
        self.defaultXform_upperSpine = None
        self.defaultXform_upperSpineEnd = None

        self.outputXformsGroup = None
        self.outputXform_root = None
        self.outputXform_pelvis = None
        self.outputXform_pelvisEnd = None
        self.outputXform_lowerSpines = None
        self.outputXform_upperSpine = None
        self.outputXform_upperSpineEnd = None

        self.drivenXformsGroup = None
        self.drivenXform_root = None
        self.drivenXform_pelvis = None
        self.drivenXform_pelvisEnd = None
        self.drivenXform_lowerSpines = None
        self.drivenXform_upperSpine = None
        self.drivenXform_upperSpineEnd = None

        self.matrixDict = kwargs.get('matrixDict', DEFAULT_MATRICES)
        self.sizeDict = kwargs.get('sizeDict', DEFAULT_SIZES)


        self.lenLowerSpine = 2
        #self.lenLowerControls = 2

        # get lower spine sizes
        if not isinstance(self.sizeDict['lowerSpines'], list):    # if not passed in
            value = self.sizeDict['lowerSpines']
            self.sizeDict['lowerSpines'] = []
            for i in range(self.lenLowerSpine):
                self.sizeDict['lowerSpines'].append(value)

        ## get lower spine matrices
        #if not self.matrixDict['lowerSpines']:
            #root_wPos = self.matrixDict['root'][11:14]
            #upperSpine_wPos = self.matrixDict['upperSpine'][11:14]
            #vectorToUpper = ka_math.subtract(upperSpine_wPos, root_wPos)
            #vectorToUpper = ka_math.normalize(vectorToUpper)

        # wrap or create
        if root:
            self.wrap(root)

        else:
            self.create()


    def create(self): #=============================================================================================
        self.startIrsObject()

        try:
            self._create()
        except:
            ka_python.printError()

        self.finishIrsObject()

        self.addFeature('fk')
        #self.addFeature('ik')

    def _create(self): #=============================================================================================
        self.createSwitchControl(modes=['fk', 'ik'])


        # create default xforms --------------------------------------------------------------------------------------
        self.defaultXformsGroup = pymel.createNode('transform')
        self.setName(self.defaultXformsGroup, 'defaultXform_group')

        self.defaultXform_root = pymel.createNode('transform')
        self.defaultXform_pelvis = pymel.createNode('transform')
        self.defaultXform_pelvisEnd = pymel.createNode('transform')
        self.defaultXform_upperSpine = pymel.createNode('transform')
        self.defaultXform_upperSpineEnd = pymel.createNode('transform')
        self.defaultXform_lowerSpines = []
        for i in range(self.lenLowerSpine):
            self.defaultXform_lowerSpines.append(pymel.createNode('transform'))


        self.setName(self.defaultXform_root, 'defaultXform_root')
        self.setName(self.defaultXform_pelvis, 'defaultXform_pelvis')
        self.setName(self.defaultXform_pelvisEnd, 'defaultXform_pelvisEnd')
        self.setName(self.defaultXform_upperSpine, 'defaultXform_upperSpine')
        self.setName(self.defaultXform_upperSpineEnd, 'defaultXform_upperSpineEnd')
        for i, lowerSpine in enumerate(self.defaultXform_lowerSpines):
            self.setName(lowerSpine, 'defaultXform_lowerSpine', index=i)


        self.defaultXformsGroup.setParent(self.root)
        self.defaultXform_root.setParent(self.defaultXformsGroup)
        self.defaultXform_pelvis.setParent(self.defaultXform_root)
        self.defaultXform_pelvisEnd.setParent(self.defaultXform_pelvis)
        parent = self.defaultXform_root
        for i, lowerSpine in enumerate(self.defaultXform_lowerSpines):
            lowerSpine.setParent(parent)
            parent = lowerSpine
        self.defaultXform_upperSpine.setParent(parent)
        self.defaultXform_upperSpineEnd.setParent(self.defaultXform_upperSpine)


        pymel.xform(self.defaultXform_root, matrix=self.matrixDict['root'], worldSpace=True)
        pymel.xform(self.defaultXform_pelvis, matrix=self.matrixDict['pelvis'], worldSpace=True)
        pymel.xform(self.defaultXform_pelvisEnd, matrix=self.matrixDict['pelvisEnd'], worldSpace=True)
        pymel.xform(self.defaultXform_upperSpine, matrix=self.matrixDict['upperSpine'], worldSpace=True)
        pymel.xform(self.defaultXform_upperSpineEnd, matrix=self.matrixDict['upperSpineEnd'], worldSpace=True)
        if self.matrixDict['lowerSpines'] == None:
            rootPos = pymel.xform(self.defaultXform_root, query=True, translation=True, worldSpace=True)
            upperSpinePos = pymel.xform(self.defaultXform_upperSpine, query=True, translation=True, worldSpace=True)
            upperSpineRotation = pymel.xform(self.defaultXform_upperSpine, query=True, rotation=True, worldSpace=True)
            distanceBetween = ka_math.distanceBetween(rootPos, upperSpinePos)
            segmentLength = distanceBetween / self.lenLowerSpine

            for i, lowerSpine in enumerate(self.defaultXform_lowerSpines):
                pymel.xform(lowerSpine, translation=rootPos, worldSpace=True)
                pymel.xform(lowerSpine, rotation=upperSpineRotation, worldSpace=True)
                lowerSpine.tx.set(segmentLength*i)

        else:
            for i, lowerSpineMatrix in enumerate(self.matrixDict['lowerSpines']):
                pymel.xform(self.defaultXform_lowerSpines[i], matrix=lowerSpineMatrix, worldSpace=True)

        pymel.xform(self.defaultXform_upperSpine, matrix=self.matrixDict['upperSpine'], worldSpace=True)
        pymel.xform(self.defaultXform_upperSpineEnd, matrix=self.matrixDict['upperSpineEnd'], worldSpace=True)


        # create outputXforms --------------------------------------------------------------------------------------
        self.outputXformsGroup = pymel.createNode('transform')
        self.setName(self.outputXformsGroup, 'outputXform_group')

        self.outputXform_root = pymel.createNode('joint')
        self.outputXform_pelvis = pymel.createNode('joint')
        self.outputXform_pelvisEnd = pymel.createNode('joint')
        self.outputXform_upperSpine = pymel.createNode('joint')
        self.outputXform_upperSpineEnd = pymel.createNode('joint')
        self.outputXform_lowerSpines = []
        for i in range(self.lenLowerSpine):
            self.outputXform_lowerSpines.append(pymel.createNode('joint'))

        self.setName(self.outputXform_root, 'outputXform_root')
        self.setName(self.outputXform_pelvis, 'outputXform_pelvis')
        self.setName(self.outputXform_pelvisEnd, 'outputXform_pelvisEnd')
        self.setName(self.outputXform_upperSpine, 'outputXform_upperSpine')
        self.setName(self.outputXform_upperSpineEnd, 'outputXform_upperSpineEnd')
        for i, lowerSpine in enumerate(self.outputXform_lowerSpines):
            self.setName(lowerSpine, 'outputXform_lowerSpine', index=i)

        self.outputXform_root.jointOrient.set([0,0,0], lock=True)
        self.outputXform_pelvis.jointOrient.set([0,0,0], lock=True)
        self.outputXform_pelvisEnd.jointOrient.set([0,0,0], lock=True)
        self.outputXform_upperSpine.jointOrient.set([0,0,0], lock=True)
        self.outputXform_upperSpineEnd.jointOrient.set([0,0,0], lock=True)
        for lowerSpine in self.outputXform_lowerSpines:
            lowerSpine.jointOrient.set([0,0,0], lock=True)

        self.outputXformsGroup.setParent(self.root)
        self.outputXform_root.setParent(self.outputXformsGroup)
        self.outputXform_pelvis.setParent(self.outputXform_root)
        self.outputXform_pelvisEnd.setParent(self.outputXform_pelvis)
        parent = self.outputXform_root
        for lowerSpine in self.outputXform_lowerSpines:
            lowerSpine.setParent(parent)
            parent = lowerSpine
        self.outputXform_upperSpine.setParent(parent)
        self.outputXform_upperSpineEnd.setParent(self.outputXform_upperSpine)

        ka_transforms.snap(self.outputXform_root, self.defaultXform_root, t=1, r=1)
        ka_transforms.snap(self.outputXform_pelvis, self.defaultXform_pelvis, t=1, r=1)
        ka_transforms.snap(self.outputXform_pelvisEnd, self.defaultXform_pelvisEnd, t=1, r=1)
        for i, lowerSpine in enumerate(self.outputXform_lowerSpines):
            ka_transforms.snap(self.outputXform_lowerSpines[i], self.defaultXform_lowerSpines[i], t=1, r=1)
        ka_transforms.snap(self.outputXform_upperSpine, self.defaultXform_upperSpine, t=1, r=1)
        ka_transforms.snap(self.outputXform_upperSpineEnd, self.defaultXform_upperSpineEnd, t=1, r=1)


        # create drivenXforms --------------------------------------------------------------------------------------
        self.drivenXformsGroup = pymel.createNode('transform')
        self.setName(self.drivenXformsGroup, 'drivenXform_group')

        self.drivenXform_root = pymel.createNode('joint')
        self.drivenXform_pelvis = pymel.createNode('joint')
        self.drivenXform_pelvisEnd = pymel.createNode('joint')
        self.drivenXform_upperSpine = pymel.createNode('joint')
        self.drivenXform_upperSpineEnd = pymel.createNode('joint')
        self.drivenXform_lowerSpines = []
        for i in range(self.lenLowerSpine):
            self.drivenXform_lowerSpines.append(pymel.createNode('joint'))

        self.drivenXforms = [self.drivenXform_root, self.drivenXform_pelvis, self.drivenXform_pelvisEnd,]
        self.drivenXforms.extend(self.drivenXform_lowerSpines)
        self.drivenXforms.extend([self.drivenXform_upperSpine, self.drivenXform_upperSpineEnd,])

        self.setName(self.drivenXform_root, 'drivenXform_root')
        self.setName(self.drivenXform_pelvis, 'drivenXform_pelvis')
        self.setName(self.drivenXform_pelvisEnd, 'drivenXform_pelvisEnd')
        self.setName(self.drivenXform_upperSpine, 'drivenXform_upperSpine')
        self.setName(self.drivenXform_upperSpineEnd, 'drivenXform_upperSpineEnd')
        for i, lowerSpine in enumerate(self.drivenXform_lowerSpines):
            self.setName(lowerSpine, 'drivenXform_lowerSpine', index=i)

        for drivenXForm in self.drivenXforms:
            drivenXForm.jointOrient.set([0,0,0], lock=True)

        self.drivenXformsGroup.setParent(self.root)
        self.drivenXform_root.setParent(self.drivenXformsGroup)
        self.drivenXform_pelvis.setParent(self.drivenXform_root)
        self.drivenXform_pelvisEnd.setParent(self.drivenXform_pelvis)
        parent = self.drivenXform_root
        for lowerSpine in self.drivenXform_lowerSpines:
            lowerSpine.setParent(parent)
            parent = lowerSpine
        self.drivenXform_upperSpine.setParent(parent)
        self.drivenXform_upperSpineEnd.setParent(self.drivenXform_upperSpine)

        ka_transforms.snap(self.drivenXform_root, self.defaultXform_root, t=1, r=1)
        ka_transforms.snap(self.drivenXform_pelvis, self.defaultXform_pelvis, t=1, r=1)
        ka_transforms.snap(self.drivenXform_pelvisEnd, self.defaultXform_pelvisEnd, t=1, r=1)
        for i, lowerSpine in enumerate(self.drivenXform_lowerSpines):
            ka_transforms.snap(self.drivenXform_lowerSpines[i], self.defaultXform_lowerSpines[i], t=1, r=1)
        ka_transforms.snap(self.drivenXform_upperSpine, self.defaultXform_upperSpine, t=1, r=1)
        ka_transforms.snap(self.drivenXform_upperSpineEnd, self.defaultXform_upperSpineEnd, t=1, r=1)

        # change root size and draw to make it look less messy
        self.outputXform_root.radius.set(3)
        self.outputXform_root.drawStyle.set(1)
        self.drivenXform_root.radius.set(3)
        self.drivenXform_root.drawStyle.set(1)



        #self.createLimbXform('root', matrix=self.matrixDict['root'])
        #self.createLimbXform('pelvis', matrix=self.matrixDict['pelvis'])
        #self.createLimbXform('pelvisEnd', matrix=self.matrixDict['pelvisEnd'])
        #self.createLimbXforms('lowerSpine', self.lenLowerSpine, matrices=self.matrixDict['lowerSpines'],
                             #parentName=root)

        ##parentName='root'
        ##for i in range(self.lenLowerSpine-1):
            ##self.createLimbXform('lowerSpine', index=i, parentName=parentName, matrix=self.matrixDict['lowerSpines'][i])
            ##parentName=None
        #self.createLimbXform('upperSpine', matrix=self.matrixDict['upperSpine'])
        #self.createLimbXform('upperSpineEnd', matrix=self.matrixDict['upperSpineEnd'])


        lockAttrs = ('sx', 'sy', 'sz', 'v')

        # make COG ---------------------------------------------------------------------------
        size = [self.sizeDict['root'], self.sizeDict['root']*0.2, self.sizeDict['root']]
        self.cog_controlStack = ka_controls.createControlStack(self.baseName+'_pelvis',size=size, side=self.side, shape='cube')
        self.cog_controlStack[0].setParent(self.root)
        ka_transforms.snap(self.cog_controlStack[0], self.defaultXform_root, t=1, r=1)
        for attr in lockAttrs: self.cog_controlStack[-1].attr(attr).set(lock=True, keyable=False)
        ka_attr.addSeparatorAttr(node=self.cog_controlStack[-1])



        ## switch control --------------------------------------------------------------------------------------
        #self.switchControl.setParent(self.drivenXform_knee)
        #self.switchControl.t.set(0,0,2.5)
        #self.switchControl.r.set(0,0,0)
        #for attr in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v',]:
            #self.switchControl.attr(attr).set(lock=True, keyable=False)


        ## visibility
        #drivenLegIkHandle.v.set(0)
        #drivenKneeIkHandle.v.set(0)
        #self.drivenXform_legTwists[0].v.set(0)
        #self.drivenXform_kneeTwists[0].v.set(0)
        #self.drivenXform_ankle.v.set(0)

        ## switch attrs
        #self.switchControl.addAttr(BENDY_VIS_ATTRIBUTE_NAME, maxValue=1.0, minValue=0.0, defaultValue=0, keyable=True)
        #for controlStack in self.bendyLegControlStacks:
            #self.switchControl.attr(BENDY_VIS_ATTRIBUTE_NAME) >> controlStack[0].v

        #for controlStack in self.bendyKneeControlStacks:
            #self.switchControl.attr(BENDY_VIS_ATTRIBUTE_NAME) >> controlStack[0].v

        #self.switchControl.addAttr(KNEE_IK_VIS_ATTRIBUTE_NAME, maxValue=1.0, minValue=0.0, defaultValue=0, keyable=True)
