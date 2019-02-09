from maya import cmds
from rig.utils import elements, misc


class component(object):
    def __init__(self,
                 side="C",
                 name="component",
                 suffix="CPT",
                 parent=None,
                 helperGeo=elements.componentNurbs
                 ):
        """
        @param side:
        @param name:
        @param suffix:
        @param parent:
        @param helperGeo: If it already exists in scene, just give the object as an arg
                          To create, give a dictionary created from export utils
                          By default a dictionary will be selected from elements

        """

        self.side = side
        self.name = name
        self.suffix = suffix
        self.parent = parent
        self.helperGeo = helperGeo

        self.createHier()
        self.createHelperGeo()
        self.createCtrl()
        self.createGuide()
        self.createAttrs()
        self.preConnect()
        self.createNodes()
        self.postConnect()
        self.componentName = "component"

    def createHier(self):
        self.cmptMasterParent = cmds.createNode("transform",
                                                n=misc.formatName(self.side,
                                                             self.name,
                                                             self.suffix),
                                                ss=False)
        if self.parent and cmds.objExists(self.parent):
            cmds.parent(self.cmptMasterParent, self.parent)

    def createHelperGeo(self):
        if type(self.helperGeo) is unicode:
            self.helperGeo = str(self.helperGeo)
        if type(self.helperGeo) is str and cmds.objExists(self.helperGeo):
            return

        self.helperGeo = misc.createGeoFromData(self.helperGeo,
                                                name=misc.formatName(self.side,
                                                                     self.name,
                                                                     "EX"),
                                                parent=self.cmptMasterParent).fullPathName()
    def addComponentTypeAttr(self, node):
        cmds.addAttr(node, ln = "componentType", dt = "string", k=False)
        cmds.setAttr(node + ".componentType", self.componentName, typ = "string", l=True)

    def createCtrl(self):
        return

    def createGuide(self):
        pass

    def createAttrs(self):
        return

    def preConnect(self):
        return

    def createNodes(self):
        return

    def postConnect(self):
        return


