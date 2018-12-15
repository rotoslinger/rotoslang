from maya import cmds
from utils import elements, misc


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
        self.createAttrs()
        self.createNodes()

    def createHier(self):
        self.cmptMasterParent = cmds.createNode("transform",
                                                n=misc.formatName(self.side,
                                                             self.name,
                                                             self.suffix),
                                                p=self.parent,
                                                ss=False)

    def createHelperGeo(self):
        if type(self.helperGeo) is str and cmds.objExists(self.helperGeo):
            return
        self.helperGeo = misc.createGeoFromData(self.helperGeo,
                                                name=misc.formatName(self.side,
                                                                     self.name,
                                                                     "EX"),
                                                parent=self.cmptMasterParent).fullPathName()

    def createCtrl(self):
        return

    def createAttrs(self):
        return

    def createNodes(self):
        return


