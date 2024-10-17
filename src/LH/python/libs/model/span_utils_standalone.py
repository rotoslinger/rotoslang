#######################################################################
##################   simplify_edges    ################################
#######################################################################

import maya.cmds as cmds
#TODO add even spacing option

def simplify_edges(even_spacing=True, select_all=False, select_handles=False):
    #get selection
    selection = cmds.ls(sl=True, fl=True);    
    selEdges = list()
    #find which are edges
    for idx, mayaObject in enumerate(selection):
        if ".e[" in mayaObject:
            maya_mesh = mayaObject.split(".e")[0]
            selEdges.append(mayaObject)
    #for ($a=0; $a <= `size selection`; $a++) {
    num_bez_tools= len(cmds.ls( 'EdgeBezierTool*', exactType="transform", s=False))
    counter_suffix= "{0:02d}".format(num_bez_tools)
    #if selection was edges, run edge bezier tool
    if (len(selEdges) > 0):
        selObj = selEdges[0].split(".")
        refCurve = "edgeBezier_ReferenceCurve" + counter_suffix
        cmds.select(selEdges,r=True)
        cmds.polyToCurve(form = 0, degree=1, n=refCurve)

        cmds.HideSelectedObjects()
        targetCurve = "edgeBezier_TargetCurve" + counter_suffix
        cmds.rebuildCurve(refCurve, ch=1,rpo=0, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=1, d=3, tol=0, n=targetCurve)
        cmds.select(targetCurve)
        cmds.nurbsCurveToBezier()
        # delete history
        cmds.delete([targetCurve, refCurve], ch=True)
        bez_wire= cmds.wire(selEdges,w= targetCurve, n="edgeBezierProject" + counter_suffix, gw=False, en=1.000000, ce=0.000000, dds=[0, 10000], li=0.000000)

        
        cmds.setAttr(bez_wire[0]+".scale[0]", 0)
        cmds.setAttr(bez_wire[0]+".rotation", 0)
       
        cmds.group(targetCurve, targetCurve+"BaseWire", refCurve, n="EdgeBezierTool" + counter_suffix)
        
        if not select_handles:
            cmds.select(maya_mesh, r=True)
            cmds.selectMode(component=True )
            cmds.selectType(edge=True)
            cmds.select(selEdges, r=True)

            return
            
                  
        cmds.select(targetCurve, r=True)
        cmds.selectMode(component=True )
        
        if select_all:
            all_target_curves = list()
            for idx in range(num_bez_tools+1):
                all_target_curves.append("edgeBezier_TargetCurve{0:02d}".format(idx))
                
            cmds.select(all_target_curves, r=True)
            cmds.selectMode(component=True )
            cmds.selectType(controlVertex=True)
############################## Usage ##############################
cmds.undoInfo(openChunk=True)	
simplify_edges()
cmds.undoInfo(closeChunk=True)
###################################################################


#######################################################################
################## equal_spacing_edges ################################
#######################################################################


def selectBezTools():
    num_bez_tools= len(cmds.ls( 'EdgeBezierTool*', exactType="transform", s=False))
    counter_suffix= "{0:02d}".format(num_bez_tools)
                  
        
    all_target_curves = list()
    for idx in range(num_bez_tools):
        all_target_curves.append("edgeBezier_TargetCurve{0:02d}".format(idx))
        
    cmds.select(all_target_curves, r=True)
    cmds.selectMode(component=True )
    cmds.selectType(controlVertex=True)
############################## Usage ##############################
cmds.undoInfo(openChunk=True)	
selectBezTools()
cmds.undoInfo(closeChunk=True)	
###################################################################


#######################################################################
################## selectCVTool #################################
#######################################################################

def selectCVTool():
    all_target_curves = cmds.ls(sl=True)
    cmds.select(all_target_curves, r=True)
    cmds.selectMode(component=True )
    cmds.selectType(controlVertex=True)
############################## Usage ##############################
cmds.undoInfo(openChunk=True)	
selectCVTool()
cmds.undoInfo(closeChunk=True)	
###################################################################


#######################################################################
################## cleanupBezTools #################################
#######################################################################


def cleanupBezTools():
    #geo_to_cleanup = cmds.ls(sl=True, type="transform")
    geo_to_cleanup = cmds.ls(sl=True, type="transform", long=True)
    if not geo_to_cleanup:
        cmds.warning("Please select the mesh that the bez tools are deforming")
        return
        
    cmds.delete(geo_to_cleanup, ch=True)
    num_bez_tools= len(cmds.ls( 'EdgeBezierTool*', exactType="transform", s=False))

    for idx in range(num_bez_tools):
        tool = "EdgeBezierTool{0:02d}".format(idx)
        cmds.delete(tool)
############################## Usage ##############################
cmds.undoInfo(openChunk=True)	
cleanupBezTools()
cmds.undoInfo(closeChunk=True)	
###################################################################


#######################################################################
################## equal_spacing_edges #################################
#######################################################################
import maya.cmds as cmds

def equal_spacing_edges():
    cmds.undoInfo(openChunk=True)  # Start undo chunk

    try:
        # Get selection
        selection = cmds.ls(sl=True, fl=True)
        sel_edges = []

        # Find which are edges
        for maya_object in selection:
            if "e[" in maya_object:
                sel_edges.append(maya_object)
                maya_mesh = maya_object.split(".e")[0]

        num_bez_tools = len(cmds.ls('EdgeBezierTool*', exactType="transform", s=False))
        counter_suffix = "{0:02d}".format(num_bez_tools)

        # If selection was edges, run edge bezier tool
        if sel_edges:
            sel_obj = sel_edges[0].split(".")
            init_curve = cmds.polyToCurve(form=0, degree=1)
            num_spans = cmds.getAttr(init_curve[0] + ".spans")
            uniform_curve = cmds.rebuildCurve(
                init_curve[0],
                ch=1,
                rpo=0,
                rt=0,
                end=1,
                kr=0,
                kcp=0,
                kep=1,
                kt=0,
                s=num_spans,
                d=1,
                tol=0
            )

            # Delete history
            cmds.delete(uniform_curve[0], init_curve[0], ch=True)

            bez_wire = cmds.wire(
                uniform_curve[0],
                w=init_curve[0],
                gw=False,
                en=1.0,
                ce=0.0,
                dds=[0, 10000],
                li=0.0
            )

            cmds.setAttr(bez_wire[0] + ".scale[0]", 0)
            cmds.setAttr(bez_wire[0] + ".rotation", 0)
            cmds.delete(uniform_curve[0], init_curve[0], ch=True)

            crv_blend = cmds.blendShape(uniform_curve[0], init_curve[0], parallel=True)

            cmds.wire(sel_obj[0], gw=False, dds=[0, 0.1], en=1.0, ce=0.0, li=0.0, w=init_curve[0])
            cmds.setAttr(crv_blend[0] + "." + uniform_curve[0], 1)

            cmds.delete(sel_edges, ch=True)

            cmds.select(maya_mesh, r=True)
            cmds.selectMode(component=True)
            cmds.selectType(edge=True)
            cmds.select(sel_edges, r=True)

    except Exception as e:
        cmds.undoInfo(closeChunk=True)  # Close undo chunk if an error occurs
        raise e  # Re-raise the error for debugging

    cmds.undoInfo(closeChunk=True)  # Close undo chunk

############################## Usage ##############################
equal_spacing_edges()
###################################################################

#######################################################################
#################### simplify_edges ###################################
#######################################################################

def simplify_edges(even_spacing=True, select_all_handles=False, select_handles=False, redo=False):
    #get selection
    selection = cmds.ls(sl=True, fl=True);    
    selEdges = list()
    #find which are edges
    for idx, mayaObject in enumerate(selection):
        if ".e[" in mayaObject:
            maya_mesh = mayaObject.split(".e")[0]
            selEdges.append(mayaObject)

    num_bez_tools= len(cmds.ls( 'EdgeBezierTool*', exactType="transform", s=False))
    counter_suffix= "{0:02d}".format(num_bez_tools)
    if redo:
        counter_suffix = "{0:02d}".format(0)
    #if selection was edges, run edge bezier tool
    if (len(selEdges) > 0):
        selObj = selEdges[0].split(".")
        if redo and cmds.objExists("EdgeBezierTool" + counter_suffix):
            cmds.delete(maya_mesh, ch=True)
            cmds.delete("EdgeBezierTool" + counter_suffix)
        refCurve = "edgeBezier_ReferenceCurve" + counter_suffix
        cmds.select(selEdges,r=True)
        cmds.polyToCurve(form = 0, degree=1, n=refCurve)
        cmds.HideSelectedObjects()
        targetCurve = "edgeBezier_TargetCurve" + counter_suffix
        cmds.rebuildCurve(refCurve, ch=1,rpo=0, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=1, d=3, tol=0, n=targetCurve)
        cmds.select(targetCurve)
        cmds.nurbsCurveToBezier()
        # delete history
        cmds.delete([targetCurve, refCurve], ch=True)
        bez_wire= cmds.wire(selEdges,w= targetCurve, n="edgeBezierProject" + counter_suffix, gw=False, en=1.000000, ce=0.000000, dds=[0, 10000], li=0.000000)
        cmds.setAttr(bez_wire[0]+".scale[0]", 0)
        cmds.setAttr(bez_wire[0]+".rotation", 0)
       
        cmds.group(targetCurve, targetCurve+"BaseWire", refCurve, n="EdgeBezierTool" + counter_suffix)
        
        if not select_handles:
            cmds.select(maya_mesh, r=True)
            cmds.selectMode(component=True )
            cmds.selectType(edge=True)
            cmds.select(selEdges, r=True)
            return
   
        cmds.select(targetCurve, r=True)
        cmds.selectMode(component=True )
        
        if select_all_handles:
            all_target_curves = list()
            for idx in range(num_bez_tools+1):
                all_target_curves.append("edgeBezier_TargetCurve{0:02d}".format(idx))
                
            cmds.select(all_target_curves, r=True)
            cmds.selectMode(component=True )
            cmds.selectType(controlVertex=True)
############################## Usage ##############################
cmds.undoInfo(openChunk=True)	
simplify_edges(redo=True)
cmds.undoInfo(closeChunk=True)	
###################################################################






















#######################################################################
#################### junk code ########################################
#######################################################################

def equal_spacing_edges():
    cmds.undoInfo(openChunk=True)  # Start undo chunk
    try:
        # Get selection
        selection = cmds.ls(sl=True, fl=True)
        sel_edges = []

        # Find which are edges
        for maya_object in selection:
            if "e[" in maya_object:
                sel_edges.append(maya_object)
                maya_mesh = maya_object.split(".e")[0]

        num_bez_tools = len(cmds.ls('EdgeBezierTool*', exactType="transform", s=False))
        counter_suffix = "{0:02d}".format(num_bez_tools)

        # If selection was edges, run edge bezier tool
        if sel_edges:
            sel_obj = sel_edges[0].split(".")
            init_curve = cmds.polyToCurve(form=0, degree=1)
            num_spans = cmds.getAttr(init_curve[0] + ".spans")
            uniform_curve = cmds.rebuildCurve(
                init_curve[0],
                ch=1,
                rpo=0,
                rt=0,
                end=1,
                kr=0,
                kcp=0,
                kep=1,
                kt=0,
                s=num_spans,
                d=1,
                tol=0
            )

            # Delete history
            cmds.delete(uniform_curve[0], init_curve[0], ch=True)
            bez_wire = cmds.wire(
                uniform_curve[0],
                w=init_curve[0],
                gw=False,
                en=1.0,
                ce=0.0,
                dds=[0, 10000],
                li=0.0
            )
            cmds.setAttr(bez_wire[0] + ".scale[0]", 0)
            cmds.setAttr(bez_wire[0] + ".rotation", 0)
            cmds.delete(uniform_curve[0], init_curve[0], ch=True)

            crv_blend = cmds.blendShape(uniform_curve[0], init_curve[0], parallel=True)

            cmds.wire(sel_obj[0], gw=False, dds=[0, 0.1], en=1.0, ce=0.0, li=0.0, w=init_curve[0])
            cmds.setAttr(crv_blend[0] + "." + uniform_curve[0], 1)

            cmds.delete(sel_edges, ch=True)

            cmds.select(maya_mesh, r=True)
            cmds.selectMode(component=True)
            cmds.selectType(edge=True)
            cmds.select(sel_edges, r=True)
    except Exception as e:
        cmds.undoInfo(closeChunk=True)  # Close undo chunk if an error occurs
        raise e  # Re-raise the error for debugging
    cmds.undoInfo(closeChunk=True)  # Close undo chunk




def simplify_edges(even_spacing=True, select_all_handles=False, select_handles=False, redo=False):
    #get selection
    selection = cmds.ls(sl=True, fl=True);    
    selEdges = list()
    #find which are edges
    for idx, mayaObject in enumerate(selection):
        if ".e[" in mayaObject:
            maya_mesh = mayaObject.split(".e")[0]
            selEdges.append(mayaObject)
    #for ($a=0; $a <= `size selection`; $a++) {aq
    num_bez_tools= len(cmds.ls( 'EdgeBezierTool*', exactType="transform", s=False))
    counter_suffix= "{0:02d}".format(num_bez_tools)
    if redo:
        counter_suffix = "{0:02d}".format(0)
    #if selection was edges, run edge bezier tool
    if (len(selEdges) > 0):
        selObj = selEdges[0].split(".")
        if redo and cmds.objExists("EdgeBezierTool" + counter_suffix):
            cmds.delete(maya_mesh, ch=True)
            cmds.delete("EdgeBezierTool" + counter_suffix)

        refCurve = "edgeBezier_ReferenceCurve" + counter_suffix
        cmds.select(selEdges,r=True)
        cmds.polyToCurve(form = 0, degree=1, n=refCurve)

        cmds.HideSelectedObjects()
        targetCurve = "edgeBezier_TargetCurve" + counter_suffix
        cmds.rebuildCurve(refCurve, ch=1,rpo=0, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=1, d=3, tol=0, n=targetCurve)
        cmds.select(targetCurve)
        cmds.nurbsCurveToBezier()
        # delete history
        cmds.delete([targetCurve, refCurve], ch=True)
        bez_wire= cmds.wire(selEdges,w= targetCurve, n="edgeBezierProject" + counter_suffix, gw=False, en=1.000000, ce=0.000000, dds=[0, 10000], li=0.000000)

        cmds.setAttr(bez_wire[0]+".scale[0]", 0)
        cmds.setAttr(bez_wire[0]+".rotation", 0)
    
        cmds.group(targetCurve, targetCurve+"BaseWire", refCurve, n="EdgeBezierTool" + counter_suffix)
        
        if not select_handles:
            cmds.select(maya_mesh, r=True)
            cmds.selectMode(component=True )
            cmds.selectType(edge=True)
            cmds.select(selEdges, r=True)
            return
             
        cmds.select(targetCurve, r=True)
        cmds.selectMode(component=True )
        
        if select_all_handles:
            all_target_curves = list()
            for idx in range(num_bez_tools+1):
                all_target_curves.append("edgeBezier_TargetCurve{0:02d}".format(idx))
                
            cmds.select(all_target_curves, r=True)
            cmds.selectMode(component=True )
            cmds.selectType(controlVertex=True)

# # delete history every time so you can continually simplify:
# cmds.undoInfo(openChunk=True)	
# simplify_edges(redo=True)
# cmds.undoInfo(closeChunk=True)	

# # keeps history, creates numbered bezier tools to allow for interactive modeling:
# cmds.undoInfo(openChunk=True)	
# simplify_edges(redo=False)
# cmds.undoInfo(closeChunk=True)
