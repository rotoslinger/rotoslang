from maya import cmds
from rig.utils import misc
import importlib
importlib.reload(misc)

#===============================================================================
#CLASS:         returnDeformerCmd
#DESCRIPTION:   Creates an lhCurveDeformer
#USAGE:         Select driver curve, aim curve, and geometry[] or set args
#RETURN:        lhCurveDeformer
#AUTHOR:        Levi Harrison
#DATE:          June 26th, 2014
#Version        1.0.0
#===============================================================================

class curveDeformerCmd():
    def __init__(self,
                 driverCurve = '',
                 aimCurve = '',
                 geom = [''],
                 ihi = 0,
                 lockAttrs = 1,
                 side='C',
                 aimCurveBase=None,
                 driverCurveBase=None,
                 
                 name=''):
        """
        type  driverCurve:          string
        param driverCurve:          the name of the curve that will drive the
                                     geometry, or the first selection

        type  aimCurve:             string
        param aimCurve:             the name of the curve that the geometry
                                     will aim at, or the second selection

        type  geom:                 string array
        param geom:                 the names of the geometry the will be deformed,
                                     or the third selection and beyond

        type  ihi:                  int
        param ihi:                  sets the deformer isHistoricallyIntersting to 0

        type  lockAttrs:            int
        param lockAttrs:            if set to 1 all attributes in return 
                                     deformer are locked and hidden

        type  side:                 string
        param side:                 defaults to C but L and R are also acceptable
        
        type  name:                 string
        param name:                 description
        """

        #----args
        self.lockAttrs               = lockAttrs
        self.ihi                     = ihi
        self.side                    = side
        self.name                    = name
        self.driverCurve             = driverCurve
        self.aimCurve                = aimCurve
        self.geom                    = geom
        self.aimCurveBase            = aimCurveBase
        self.driverCurveBase         = driverCurveBase

        #----vars
        self.driverCurveShape        = ''
        self.aimCurveShape           = ''
        self.driverBaseName          = ''
        self.aimBaseName             = ''
        # self.driverCurveBase         = ''
        # self.aimCurveBase            = ''
        self.driverCurveBaseShape    = ''
        self.aimCurveBaseShape       = ''
        
        self.geomShapes              = []
        self.returnDeformer          = ''
        self.attrs                   = ['en', 'cacheweights','cparams','cbase',
                                        'cContinuouss','ramount','revamount',
                                        'falloff','scale','vol','slide', 
                                        'length']
        #----functions
        self.__create()

    def __getArgs(self):
        """if no arguments are defined tries to get selection, if not, warn, quit"""
        if not (self.driverCurve and self.aimCurve and self.geom):
            try:
                sel = cmds.ls(sl=True)
                self.driverCurve = sel[0]
                self.aimCurve = sel[1]
                self.geom = sel[2:]
            except:
                raise Exception('please give arguments (driverCurve, aimCurve, geom) or select 2 curves and at least 1 piece of geometry')
                quit()

    def __getShapes(self):
        """gets shape"""

        self.driverCurveShape = cmds.listRelatives(self.driverCurve, shapes = True)[0]
        self.aimCurveShape = cmds.listRelatives(self.aimCurve, shapes = True)[0]
        for i in range(len(self.geom)):
            self.geomShapes.append(cmds.listRelatives(self.geom[i], shapes = True)[0])
        if not (self.driverCurveShape or self.aimCurveShape or self.geomShaps):
            print('one or more argument did not have a shape')
            quit()

    def __checkDriverArgs(self):
        """checks to make sure the right args are curves"""

        if (cmds.objectType(self.driverCurveShape, isType='nurbsCurve') == True
            and cmds.objectType(self.aimCurveShape, isType='nurbsCurve') == True):
            pass
        else:
            raise Exception('arguments are not of required type nurbsCurve, nurbsCurve, geometry ')
            quit()

    def __checkGeomArgs(self):
        """checks the args to make sure they are geometry"""

        for i in self.geomShapes:
            if ((cmds.objectType(i, isType='nurbsSurface') == True) or
                (cmds.objectType(i, isType='nurbsCurve') == True) or
                (cmds.objectType(i, isType='mesh') == True)) :
                continue
            else:
                raise Exception(i + ' is not geometry')
                quit()

    def __createBaseCurves(self):
        """creates base curves based on the names of the driver curves"""
        if  self.driverCurveBase and self.aimCurveBase:
            self.driverCurveBaseShape = misc.getShape(self.driverCurveBase)
            self.aimCurveBaseShape = misc.getShape(self.aimCurveBase)
            return 
        # If you don't get the base and aim as args then create them here
        self.driverBaseName = self.__nameBase(self.driverCurve)
        self.aimBaseName = self.__nameBase(self.aimCurve)
        if not cmds.objExists(self.driverBaseName):
            tmpDriveBase = self.__duplicateCurveClean(curve = self.driverCurve, 
                                    name = self.driverBaseName)
        else:
            tmpDriveBase = (self.driverBaseName, misc.getShape(self.driverBaseName))


        if not cmds.objExists(self.aimBaseName):
            tmpAimBase = self.__duplicateCurveClean(curve = self.aimCurve, 
                                    name = self.aimBaseName)
        else:
            tmpAimBase = (self.aimBaseName, misc.getShape(self.aimBaseName))

        self.driverCurveBase = tmpDriveBase[0]
        self.driverCurveBaseShape = tmpDriveBase[1]
        
        self.aimCurveBase = tmpAimBase[0]
        self.aimCurveBaseShape = tmpAimBase[1]

    def __createCurveDeformer(self):
        """creates the spline deformer creates base curves"""

        self.returnDeformer = cmds.deformer(self.geom, 
                                            type = 'LHCurveDeformer',
                                            name= self.side + "_" +
                                                  self.name + "_LCD")[0]

    def __connectCurveDeformer(self):
        """makes all connections into the spline deformer"""

        cmds.connectAttr(self.driverCurveShape + '.worldSpace',
                         self.returnDeformer + '.curve',
                         force=True)
        cmds.connectAttr(self.driverCurveBaseShape + '.worldSpace',
                         self.returnDeformer + '.curveBase',
                         force=True)
        cmds.connectAttr(self.aimCurveShape + '.worldSpace',
                         self.returnDeformer + '.aimCurve',
                         force=True)
        cmds.connectAttr(self.aimCurveBaseShape + '.worldSpace',
                         self.returnDeformer + '.aimCurveBase',
                         force=True)

    def __nameBase(self, name):
        """assuming name is side_description_Type, returns description"""

        try:
            name = name.split("_")
            return name[0] + '_' + name[1] + 'Base_' + name[2]
        except:
            return name[0] + 'Base'

    def __duplicateCurveClean(self, curve, name):
        "duplicates a nurbs curve cleanly"
        parent = ""
        try:
            parent = cmds.listRelatives(curve,p=True)
        except:
            pass
        nurbscurveShape = cmds.ls(curve, dag = 1, g = 1)[0]
        newTransform = cmds.createNode("transform", n = name)
        newCurve = cmds.createNode("nurbsCurve", n = name+"Shape", p = newTransform)
        cmds.connectAttr(nurbscurveShape + ".worldSpace", newCurve + ".create")
        cmds.refresh()
        cmds.disconnectAttr(nurbscurveShape + ".worldSpace", newCurve + ".create")
        if parent:
            cmds.parent(newTransform, parent)
        return newTransform, newCurve

    def __cleanup(self):
        """hides base curves"""

        try:
            cmds.setAttr(self.driverCurveBase +'.v', 0)
            cmds.setAttr(self.aimCurveBase +'.v', 0)
        except:
            pass
        if self.lockAttrs == 1:
            for i in self.attrs:
                cmds.setAttr(self.returnDeformer + "." + i, lock =True)
        if self.ihi == 0:
            cmds.setAttr(self.returnDeformer+".ihi",0)
            connections = cmds.listConnections(self.returnDeformer)
            if connections:
                for i in connections:
                    cmds.setAttr(i+".ihi",0)
        
    def __create(self):
        """ This method creates the curveDeformer setup """

        self.__getArgs()
        self.__getShapes()
        self.__checkDriverArgs()
        self.__checkGeomArgs()
        self.__createBaseCurves()
        self.__createCurveDeformer()
        self.__connectCurveDeformer()
        self.__cleanup()
