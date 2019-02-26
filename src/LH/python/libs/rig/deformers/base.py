class newNode(object):
    def __init__(self):
        pass

class weightStack(newNode):
    def __init__(self):
        pass

class curveWeights(newNode):
    def __init__(self):
        pass

class deformer(object):
    def __init__(self,
                 type="",
                 driverSurface = '',
                 weightGeo = '',
                 weightBase = [],
                 geoms = [],
                 control = "",
                 ihi = 0,
                 side='C',
                 name='',
                 lockAttrs = 1,
                 uNames = [],
                 vNames = [],
                 nNames = [],
                 animCurveSuffix = "ACV",
                 deformerSuffix="SLD"
                 ):
