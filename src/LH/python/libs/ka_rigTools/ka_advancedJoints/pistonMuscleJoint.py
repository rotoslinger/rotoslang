
from .. import ka_advancedJoints as ka_advancedJoints #;reload(ka_advancedJoints)



class PistonMuscleJoint(ka_advancedJoints.AdvancedJoint):

    def __init__(self, **kwargs):
        ka_advancedJoints.AdvancedJoint.__init__(self, **kwargs)

        self.muscleJointGroup = kwargs.get('muscleJointGroup')


        #if not self.dagContainer:      #create new
            #self.baseName              = kwargs.get( 'baseName',             None )
            #self.numberOfJoints        = kwargs.get( 'numberOfJoints',       6 )
            #self.side                  = kwargs.get( 'side',                 '')
            #self.animationRig          = kwargs.get( 'animationRig',         None )
            #self.parent                = kwargs.get( 'parent',               None )
            #self.jointPositions        = kwargs.get( 'jointPositions',       None )
            #self.features              = kwargs.get( 'features',             None )
            #self.installedFeatures     = kwargs.get( 'installedFeatures',    None )
            #self.defaultSwitchesIndex  = kwargs.get( 'defaultSwitchesIndex', 0 )
            #self.mirrorObject          = kwargs.get( 'mirrorObject',         None )
            #self.jointRadius           = kwargs.get( 'jointRadius',         None )


    def getKwargs(self):
        pass


    def create(self):
        pass





