import maya.cmds as cmds

def assembleCmd():
    srcAttr = cmds.optionVar(q="PENCsrcAttr")
    destAttr = cmds.optionVar(q="PENCdest")
    cmd = "connectAttr {} {}".format(srcAttr, destAttr)
    return cmd

def PoseEditorNewConnectionCallback(parent, doIt):
    cmds.setParent(parent)
    bsd = cmds.optionMenuGrp('pencBlendShapeDeformerMenuGrp', q=True, value=True) if cmds.optionMenuGrp('pencBlendShapeDeformerMenuGrp', q=True, ni=True) else ""
    cmds.optionVar(sv=("PENCbsd", bsd))
    tgt = cmds.optionMenuGrp('pencTargetMenuGrp', q=True, value=True) if cmds.optionMenuGrp('pencTargetMenuGrp', q=True, ni=True) else ""
    cmds.optionVar(sv=("PENCtgt", tgt))
    dest = cmds.textFieldGrp('pencConnDestFieldGrp', q=True, text=True)
    cmds.optionVar(sv=("PENCdest", dest))
    
    if doIt:
        cmd = assembleCmd()
        cmds.eval(cmd)

def PoseEditorNewConnectionSetup(parent, forceFactorySettings):
    cmds.setParent(parent)
    
    cmds.optionVar(init=forceFactorySettings, category="Pose Editor.Add Connection",
                   sv=("PENCbsd", ""),
                   sv=("PENCtgt", ""),
                   sv=("PENCdest", ""))
    
    bsdL = cmds.ls(type="blendShape")
    bsd = cmds.optionVar(q="PENCbsd")
    
    if cmds.optionMenuGrp('pencBlendShapeDeformerMenuGrp', q=True, ni=True) != 0:
        if bsd == "":
            cmds.optionMenuGrp('pencBlendShapeDeformerMenuGrp', e=True, select=1)
        elif bsd in bsdL:
            cmds.optionMenuGrp('pencBlendShapeDeformerMenuGrp', e=True, value=bsd)
    
    pencBsdChanged(1)

def pencBsdChanged(init):
    # Update target menu
    items = cmds.optionMenuGrp('pencTargetMenuGrp', q=True, ill=True)
    for item in items:
        cmds.deleteUI(item)
    
    bsd = cmds.optionMenuGrp('pencBlendShapeDeformerMenuGrp', q=True, value=True) if cmds.optionMenuGrp('pencBlendShapeDeformerMenuGrp', q=True, ni=True) else ""
    if not bsd:
        return
    
    tgts = cmds.listAttr(bsd + ".weight", m=True) or []
    tgts = sorted(tgts)
    
    cmds.setParent('pencTargetMenuGrp')
    for tgt in tgts:
        cmds.menuItem(label=tgt)
    
    if init:
        if cmds.optionMenuGrp('pencTargetMenuGrp', q=True, ni=True) != 0:
            tgt = cmds.optionVar(q="PENCtgt")
            if not tgt:
                cmds.optionMenuGrp('pencTargetMenuGrp', e=True, select=1)
            elif tgt in tgts:
                cmds.optionMenuGrp('pencTargetMenuGrp', e=True, value=tgt)
    
    pencTgtChanged()

def pencTgtChanged():
    cmds.textFieldGrp('pencConnDestFieldGrp', e=True, text="")
    
    if cmds.optionMenuGrp('pencBlendShapeDeformerMenuGrp', q=True, ni=True) == 0 or cmds.optionMenuGrp('pencTargetMenuGrp', q=True, ni=True) == 0:
        return
    
    bsd = cmds.optionMenuGrp('pencBlendShapeDeformerMenuGrp', q=True, value=True)
    tgt = cmds.optionMenuGrp('pencTargetMenuGrp', q=True, value=True)
    
    if not bsd or not tgt:
        return
    
    cmds.textFieldGrp('pencConnDestFieldGrp', e=True, text="{}.{}".format(bsd, tgt))

def poseEditorNewConnectionOptions():
    commandName = "PoseEditorNewConnection"
    callback = "{}Callback".format(commandName)
    setup = "{}Setup".format(commandName)

    layout = getOptionBox()
    cmds.setParent(layout)

    setOptionBoxCommandName(commandName)
    cmds.setUITemplate('DefaultTemplate', push=True)

    cmds.waitCursor(state=True)
    parent = cmds.columnLayout(adjustableColumn=True)
    cmds.formLayout()
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.optionMenuGrp(label=uiRes("m_poseEditorNewConnectionWindow.kBlendShapeDeformer"), changeCommand="pencBsdChanged(0)", name='pencBlendShapeDeformerMenuGrp')
    bsdL = cmds.ls(type="blendShape")
    bsdL.sort()
    for bsd in bsdL:
        cmds.menuItem(label=bsd)
    
    cmds.optionMenuGrp(label=uiRes("m_poseEditorNewConnectionWindow.kTarget"), changeCommand="pencTgtChanged", name='pencTargetMenuGrp')
    cmds.formLayout(height=5)
    cmds.setParent('..')
    cmds.textFieldGrp(label=uiRes("m_poseEditorNewConnectionWindow.kConnection"), name='pencConnDestFieldGrp')

    cmds.waitCursor(state=False)
    cmds.setUITemplate('DefaultTemplate', pop=True)

    applyBtn = getOptionBoxApplyBtn()
    cmds.button(applyBtn, e=True,
                label=uiRes("m_poseEditorNewConnectionWindow.kAddConnection"),
                command="{} {} 1".format(callback, parent))
    
    saveBtn = getOptionBoxSaveBtn()
    cmds.button(saveBtn, e=True,
                command="{} {} 0; hideOptionBox".format(callback, parent))
    
    resetBtn = getOptionBoxResetBtn()
    cmds.button(resetBtn, e=True,
                command="{} {} 1".format(setup, parent))
    
    setOptionBoxTitle(uiRes("m_poseEditorNewConnectionWindow.kAddPoseShapeConnection"))
    setOptionBoxHelpTag(commandName)
    eval("{} {} 0".format(setup, parent))
    showOptionBox()

def poseEditorNewConnectionWindow(sourceAttr):
    cmds.optionVar(sv=("PENCsrcAttr", sourceAttr))
    poseEditorNewConnectionOptions()