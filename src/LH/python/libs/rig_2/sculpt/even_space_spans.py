from maya import cmds

def even_space():
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

