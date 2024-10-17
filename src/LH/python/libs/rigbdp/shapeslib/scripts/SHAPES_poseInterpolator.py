import maya.cmds as cmds
import maya.mel as mel
import decorator
@decorator.sel_restore
def shapesPI_createPoseInterpolatorNode():
    """
    Create the pose interpolator and set up the control node and neutral poses.
    
    Returns:
        str: The shape node of the pose interpolator.
    """
    node = shapesUI_getDriverNodeNames()
    sel = cmds.ls(sl=True)
    cmds.select(node[0])

    solver = mel.eval('createPoseInterpolatorNode("newPoseInterpolator", 0, 0)')
    shape = shapesCommon_getShapeNode(solver)

    control = cmds.textField('shpUI_controlField', q=True, tx=True)
    items = control.split(",")
    
    if control != "" and items[0] != node[0]:
        cmds.select(items[0])
    else:
        cmds.select(node[0])

    mel.eval('createNeutralPoses {}'.format(shape))
    cmds.select(sel)
    
    return shape


def shapesPI_addNeutralPoses(solver):
    """
    Add neutral poses to the given solver.
    
    Args:
        solver (str): The solver to add neutral poses to.
    """
    mel.eval('createNeutralPoses {}'.format(solver))


def shapesPI_deleteNeutralPose(solver):
    """
    Delete neutral poses from the solver.
    
    Args:
        solver (str): The solver to delete neutral poses from.
    """
    cmds.catchQuiet(mel.eval('poseInterpolator -e -deletePose neutral {}'.format(solver)))
    cmds.catchQuiet(mel.eval('poseInterpolator -e -deletePose neutralSwing {}'.format(solver)))
    cmds.catchQuiet(mel.eval('poseInterpolator -e -deletePose neutralTwist {}'.format(solver)))


def shapesPI_addPose(solver, target):
    """
    Add a new pose to the pose interpolator.
    
    Args:
        solver (str): The pose interpolator solver.
        target (str): The target for the pose.
    
    Returns:
        int: The index of the added pose.
    """
    index = mel.eval('poseInterpolatorAddPose("{}", "{}")'.format(solver, target))
    cmds.setAttr('{}.pose[{}].poseType'.format(solver, index), cmds.optionVar(q="SHAPESDefaultPoseMode"))
    
    return index


def shapesPI_deletePose(solver, target):
    """
    Delete a pose from the pose interpolator.
    
    Args:
        solver (str): The pose interpolator solver.
        target (str): The target pose to delete.
    """
    mel.eval('poseInterpolator -e -deletePose "{}" "{}"'.format(target, solver))


def shapesPI_connectCustomControl(solver, control):
    """
    Connect custom control attributes to the pose interpolator.
    
    Args:
        solver (str): The pose interpolator solver.
        control (str): The control node to connect.
    """
    attr_list = ["rotateX", "rotateY", "rotateZ"]
    
    for i, attr in enumerate(attr_list):
        cmds.connectAttr('{}.{}'.format(control, attr), '{}.driver[0].driverController[{}]'.format(solver, i+1), force=True)


def shapesPI_mirrorConnectDriver(node, solver):
    """
    Connect the mirror driver to the mirrored pose interpolator.
    
    Args:
        node (str): The node to connect.
        solver (str): The pose interpolator solver.
    """
    cmds.connectAttr('{}.jointOrient'.format(node), '{}.driver[0].driverOrient'.format(solver), force=True)
    cmds.connectAttr('{}.matrix'.format(node), '{}.driver[0].driverMatrix'.format(solver), force=True)
    cmds.connectAttr('{}.rotateAxis'.format(node), '{}.driver[0].driverRotateAxis'.format(solver), force=True)
    cmds.connectAttr('{}.rotateOrder'.format(node), '{}.driver[0].driverRotateOrder'.format(solver), force=True)


def shapesPI_addRbfAttributes(solver, add):
    """
    Add default weight driver attributes to the given solver.
    
    Args:
        solver (str): The solver to add attributes to.
        add (int): If True, add attributes to the solver.
    
    Returns:
        str: The generated command string for adding attributes.
    """
    cmd = ''
    cmd += 'addAttr -ln "twistAxis" -at "long" {};\n'.format(solver)
    cmd += 'addAttr -ln "opposite" -at "bool" {};\n'.format(solver)
    cmd += 'addAttr -ln "driverList" -sn "dl" -at "compound" -nc 3 -m -h 1 {};\n'.format(solver)
    cmd += 'addAttr -ln "driverInput" -sn "di" -dt "matrix" -h 1 -p "driverList" {};\n'.format(solver)
    cmd += 'addAttr -ln "controlNode" -sn "cn" -at "message" -p "driverList" {};\n'.format(solver)
    cmd += 'addAttr -ln "poseList" -sn "p" -at "compound" -nc 6 -m -h 1 -p "driverList" {};\n'.format(solver)
    cmd += 'addAttr -ln "poseMatrix" -sn "pmat" -dt "matrix" -p "poseList" {};\n'.format(solver)
    cmd += 'addAttr -ln "poseParentMatrix" -sn "ppmat" -dt "matrix" -p "poseList" {};\n'.format(solver)
    cmd += 'addAttr -ln "poseMode" -sn "pmd" -at "long" -p "poseList" {};\n'.format(solver)
    cmd += 'addAttr -ln "controlPoseAttributes" -sn "cpa" -dt "stringArray" -p "poseList" {};\n'.format(solver)
    cmd += 'addAttr -ln "controlPoseValues" -sn "cpv" -dt "doubleArray" -p "poseList" {};\n'.format(solver)
    cmd += 'addAttr -ln "controlPoseRotateOrder" -sn "cpro" -at "long" -p "poseList" {};\n'.format(solver)

    if add:
        mel.eval(cmd)

    return cmd


def shapesPI_performRbfAttributeCheck(solver):
    """
    Check if the pose interpolator is RBF compatible and update it if necessary.
    
    Args:
        solver (str): The solver to check and update.
    """
    if shapesPI_hasLegacyRbf(solver):
        shapesPI_transferRbfAttributes(solver)
        br_displayMessage('info', 'Updated RBF attributes on {}.'.format(solver))
    elif not shapesPI_hasRbfAttributes(solver):
        shapesPI_addRbfAttributes(solver, 1)
        br_displayMessage('info', 'Added RBF attributes to {}.'.format(solver))


def shapesPI_hasLegacyRbf(solver):
    """
    Check if the solver contains legacy RBF attributes from version 4.0.
    
    Args:
        solver (str): The solver to check.
    
    Returns:
        bool: True if the solver contains legacy RBF attributes, False otherwise.
    """
    solver = shapesCommon_getShapeNode(solver)
    return cmds.attributeQuery("driveMatrix", exists=True, node=solver)


def shapesPI_hasRbfAttributes(solver):
    """
    Check if the solver contains RBF attributes.
    
    Args:
        solver (str): The solver to check.
    
    Returns:
        bool: True if the solver contains RBF attributes, False otherwise.
    """
    solver = shapesCommon_getShapeNode(solver)
    return cmds.attributeQuery("driverList", exists=True, node=solver)


def shapesPI_isRbfCompatible(solver):
    """
    Check if the solver is RBF compatible.
    
    Args:
        solver (str): The solver to check.
    
    Returns:
        bool: True if the solver is RBF compatible, False otherwise.
    """
    solver = shapesCommon_getShapeNode(solver)
    return cmds.attributeQuery("SHAPES_wd", exists=True, node=solver)


def shapesPI_transferRbfAttributes(solver):
    """
    Transfer pose data from version 4.0 to 4.1 for compatibility with multiple drivers.
    
    Args:
        solver (str): The solver to transfer data for.
    """
    cmds.addAttr(solver, ln="controlPoseTemp", sn="cpt", at="compound", nc=3, m=True, h=True)
    cmds.addAttr(solver, ln="controlPoseAttributesTemp", sn="cpat", dt="stringArray", p="controlPoseTemp")
    cmds.addAttr(solver, ln="controlPoseValuesTemp", sn="cpvt", dt="doubleArray", p="controlPoseTemp")
    cmds.addAttr(solver, ln="controlPoseRotateOrderTemp", sn="cprot", at="long", p="controlPoseTemp")
    cmds.addAttr(solver, ln="poseMatrixTemp", dt="matrix", m=True, h=True)

    axis = cmds.getAttr("{}.twistAxis".format(solver))
    loc = cmds.listConnections("{}.driveMatrix".format(solver), s=1, d=0)
    driver = cmds.listConnections("{}.twistNode".format(solver), s=1, d=0)
    control_node = cmds.listConnections("{}.controlNode".format(solver), s=1, d=0)

    for pose in cmds.getAttr("{}.pose".format(solver), mi=True):
        attrs = cmds.getAttr("{}.pose[{}].controlPoseAttributes".format(solver, pose))
        vals = cmds.getAttr("{}.pose[{}].controlPoseValues".format(solver, pose))
        rotate = cmds.getAttr("{}.pose[{}].controlPoseRotateOrder".format(solver, pose))
        matrix = cmds.getAttr("{}.pose[{}].poseMatrix".format(solver, pose))
        
        cmds.setAttr("{}.controlPoseAttributesTemp[{}]".format(solver, pose), len(attrs), *attrs, type="stringArray")
        cmds.setAttr("{}.controlPoseValuesTemp[{}]".format(solver, pose), len(vals), *vals, type="doubleArray")
        cmds.setAttr("{}.controlPoseRotateOrderTemp[{}]".format(solver, pose), rotate)
        cmds.setAttr("{}.poseMatrixTemp[{}]".format(solver, pose), matrix, type="matrix")

    cmds.deleteAttr("{}.pose".format(solver))

    cmds.connectAttr("{}.matrix".format(loc), "{}.driver[0].driverMatrix".format(solver), f=True)
    cmds.connectAttr("{}.jointOrient".format(loc), "{}.driver[0].driverOrient".format(solver), f=True)
    cmds.setAttr("{}.twistAxis".format(solver), axis)

    for i in range(len(control_node)):
        cmds.connectAttr("{}.message".format(control_node[i]), "{}.driver[{}].driverNode".format(solver, i), f=True)
        cmds.connectAttr("{}.rotateX".format(driver[i]), "{}.driver[{}].driverController[1]".format(solver, i), f=True)
        cmds.connectAttr("{}.rotateY".format(driver[i]), "{}.driver[{}].driverController[2]".format(solver, i), f=True)
        cmds.connectAttr("{}.rotateZ".format(driver[i]), "{}.driver[{}].driverController[3]".format(solver, i), f=True)

    for pose in cmds.getAttr("{}.controlPoseTemp".format(solver), mi=True):
        attrs = cmds.getAttr("{}.controlPoseAttributesTemp[{}]".format(solver, pose))
        vals = cmds.getAttr("{}.controlPoseValuesTemp[{}]".format(solver, pose))
        rotate = cmds.getAttr("{}.controlPoseRotateOrderTemp[{}]".format(solver, pose))
        matrix = cmds.getAttr("{}.poseMatrixTemp[{}]".format(solver, pose))

        cmds.setAttr("{}.pose[{}].controlPoseAttributes".format(solver, pose), len(attrs), *attrs, type="stringArray")
        cmds.setAttr("{}.pose[{}].controlPoseValues".format(solver, pose), len(vals), *vals, type="doubleArray")
        cmds.setAttr("{}.pose[{}].controlPoseRotateOrder".format(solver, pose), rotate)
        cmds.setAttr("{}.pose[{}].poseMatrix".format(solver, pose), matrix, type="matrix")

    cmds.deleteAttr("{}.controlPoseTemp".format(solver))
    cmds.deleteAttr("{}.poseMatrixTemp".format(solver))
