#include <maya/MIOStream.h>
#include <stdio.h>
#include <stdlib.h>

#include <maya/MPxToolCommand.h>
#include <maya/MFnPlugin.h>
#include <maya/MArgList.h>
#include <maya/MGlobal.h>
#include <maya/MItSelectionList.h>
#include <maya/MPoint.h>
#include <maya/MVector.h>
#include <maya/MDagPath.h>

#include <maya/MFnTransform.h>
#include <maya/MItCurveCV.h>
#include <maya/MItSurfaceCV.h>
#include <maya/MItMeshVertex.h>

#include <maya/MPxSelectionContext.h>
#include <maya/MPxContextCommand.h>
#include <maya/M3dView.h>
#include <maya/MFnCamera.h>
#include <string>
#include <vector>

#define CHECKRESULT(stat,msg)     \
        if ( MS::kSuccess != stat ) { \
                cerr << msg << endl;      \
        }

#define kVectorEpsilon 1.0e-3

//
// The move command
//
// - this is a tool command which can be used in tool
//   contexts or in the MEL command window.
//
#define         MOVENAME        "weightSlideCmd"
#define         DOIT            0
#define         UNDOIT          1
#define         REDOIT          2

class weightSlideCmd : public MPxToolCommand
{
public:
        weightSlideCmd();
        virtual ~weightSlideCmd();

        MStatus     doIt( const MArgList& args );
        MStatus     redoIt();
        MStatus     undoIt();
        bool        isUndoable() const;
        MStatus         finalize();


public:
        static void* creator();

        void            setVector( double x, double y, double z);
        void            setWeight( double w);
private:
        MVector         delta;
        double         weight;
        MStatus         action( int flag );


};

weightSlideCmd::weightSlideCmd( )
{
        setCommandString( MOVENAME );
}

weightSlideCmd::~weightSlideCmd()
{}

void* weightSlideCmd::creator()
{
        return new weightSlideCmd;
}

bool weightSlideCmd::isUndoable() const
//
// Description
//     Set this command to be undoable.
//
{
        return true;
}

void weightSlideCmd::setVector( double x, double y, double z)
{
        delta.x = x;
        delta.y = y;
        delta.z = z;
}

void weightSlideCmd::setWeight( double w)
{
        weight = w;
}



MStatus weightSlideCmd::finalize()
//
// Description
//     Command is finished, construct a string for the command
//     for journalling.
//
{
    MArgList command;
    command.addArg( commandString() );
    command.addArg( delta.x );
    command.addArg( delta.y );
    command.addArg( delta.z );
    command.addArg( weight );

        // This call adds the command to the undo queue and sets
        // the journal string for the command.
        //
    return MPxToolCommand::doFinalize( command );
}

MStatus weightSlideCmd::doIt( const MArgList& args )
//
// Description
//              Test MItSelectionList class
//
{
        MStatus stat;
        MVector vector( 1.0, 0.0, 0.0 );        // default delta
        unsigned i = 0;

        switch ( args.length() )         // set arguments to vector
        {
                case 1:
                        vector.x = args.asDouble( 0, &stat );
                        break;
                case 2:
                        vector.x = args.asDouble( 0, &stat );
                        vector.y = args.asDouble( 1, &stat );
                        break;
                case 3:
                        vector = args.asVector(i,3);
                        break;
                case 0:
                default:
                        break;
        }
        delta = vector;

        return action( DOIT );
}

MStatus weightSlideCmd::undoIt( )
//
// Description
//              Undo last delta translation
//
{
        return action( UNDOIT );
}

MStatus weightSlideCmd::redoIt( )
//
// Description
//              Redo last delta translation
//
{
        return action( REDOIT );
}

MStatus weightSlideCmd::action( int flag )
{
        MStatus stat;
        double wt = weight;
        switch( flag )
        {
                case UNDOIT:
                        wt = -wt;
                        break;
                case REDOIT:
                        break;
                case DOIT:
                        break;
                default:
                        break;
        }
        int exists;

        MGlobal::executeCommand(MString(" optionVar -exists weightName "),exists, false, false);
        if ( exists == 1)
        {

//            if (weightAttrSplit.length()>0)
//                weightAttrSplit.clear();
//
//            if (geo.length()>0)
//                geo.clear();
//
//            if (selected.length()>0)
//                selected.clear();
//
//            if (vtx.length()>0)
//                vtx.clear();
//
//            if (cv.length()>0)
//                cv.clear();
//
//            if (points.length()>0)
//                points.clear();
//
//            if (finalPoints.length()>0)
//                finalPoints.clear();
//
//            if (weightAttrs.length()>0)
//                weightAttrs.clear();
//
//            if (allWeightValues.length()>0)
//                allWeightValues.clear();
//
//            if (finalPointsIndexes.length()>0)
//                finalPointsIndexes.clear();
//
//            if (initialValues.length()>0)
//                initialValues.clear();



            MString weightAttr;
            MStringArray weightAttrSplit;
            MString deformer;
            MStringArray geo;
            MStringArray tmpGeoTransform;
            MStringArray geoTransform;
            MStringArray selected;
            MStringArray points;
            MString tmpWeights;
//            std::vector < MStringArray > finalPoints;
            MStringArray finalPoints;

            MStringArray weightAttrs;
            std::vector < MDoubleArray > allWeightValues;
            MDoubleArray tmpAllWeightValues;
            std::vector < MIntArray > finalPointsIndexes;
            MIntArray tmpFinalPointsIndexes;
            std::vector < MDoubleArray > initialValues;
            MDoubleArray tmpInitialValues;
            MString strIdx;
            int idx;
            unsigned int i;
            unsigned int j;


            MGlobal::executeCommand(MString(" optionVar -q weightName "), weightAttr, false, false);
            weightAttr.split('.',weightAttrSplit);
            deformer = weightAttrSplit[0];
            MGlobal::executeCommand(MString(" deformer -q -g "), geo, false, false);
            for (i = 0; i < geo.length();++i)
            {
                if (tmpGeoTransform.length()>0)
                    tmpGeoTransform.clear();
                MGlobal::executeCommand(MString("listRelatives ") +  MString("-parent ") + MString(geo[i]) , tmpGeoTransform, false, false);
                geoTransform.append(tmpGeoTransform[0]);
                MGlobal::executeCommand(MString("ls -sl -fl"), selected, false, false);
            }
            std::string something;
            for (i = 0; i < selected.length();++i)
                {
                    //checks if vertex
                    if (std::string(selected[i].asChar()).find(std::string(".vtx")) != std::string::npos)
                    {
                        points.append(selected[i]);
//                        MGlobal::displayInfo(MString()+selected[i]);
                    }
                    //checks if cv
                    if (std::string(selected[i].asChar()).find(std::string(".cv")) != std::string::npos)
                    {
                        points.append(selected[i]);
//                        MGlobal::displayInfo(MString()+selected[i]);
                    }
                }



            for (i = 0; i < geoTransform.length();++i)
            {
//                MString stringer;
//                stringer += i;
                if (tmpAllWeightValues.length()>0)
                    tmpAllWeightValues.clear();

                weightAttrs.append(weightAttrSplit[1] + "." + weightAttrSplit[2] + "s[" + i +"]" + weightAttrSplit[2]);
                MGlobal::executeCommand(MString("getAttr ") +  MString(weightAttrs[i]), tmpAllWeightValues, false, false);
                allWeightValues.push_back(tmpAllWeightValues);

                if (tmpFinalPointsIndexes.length()>0)
                    tmpFinalPointsIndexes.clear();
                if (tmpInitialValues.length()>0)
                    tmpInitialValues.clear();
                int len = points.length();
                tmpFinalPointsIndexes.setLength(len);
                tmpInitialValues.setLength(len);
                for (j = 0; j < len;++j)
                {

                    //                                    if geoTransform[i] in points[j]:


                    std::string tmp1 = geoTransform[i].asChar();
                    std::string tmp2 = points[j].asChar();
//                    MGlobal::displayInfo(MString(" ")+geoTransform[i].asChar());
//                    MGlobal::displayInfo(MString(" ")+(tmp2.find(tmp1) != std::string::npos));
                    if (tmp2.find(tmp1) != std::string::npos)
                    {
//                        MGlobal::displayInfo(MString("stuff"));
                        finalPoints.append(points[j]);
                        MStringArray tmpIdx;
                        points[j].split('[',tmpIdx);
                        if (tmpIdx.length() > 0 )
                        {
                            strIdx = tmpIdx[1];
                            tmpIdx.clear();
                        }
                        strIdx.split(']',tmpIdx);
                        if (tmpIdx.length() > 0 )
                        {
                            strIdx = tmpIdx[0];
                        }
                        idx = strIdx.asInt();
                        tmpFinalPointsIndexes[j] = idx;
                        tmpInitialValues[j]=allWeightValues[i][idx];
//                        MGlobal::displayInfo(MString()+idx);
//                        MGlobal::displayInfo(MString()+allWeightValues[i][idx);
                    }
                }
                finalPointsIndexes.push_back(tmpFinalPointsIndexes);
                initialValues.push_back(tmpInitialValues);
//            MGlobal::displayInfo(MString()+cv.length());
            }
            for (i = 0; i < geoTransform.length();++i)
            {
//                MGlobal::displayInfo(MString()+finalPointsIndexes[i].length());
                for (j = 0; j < finalPointsIndexes[i].length();++j)
                {
                    allWeightValues[i][finalPointsIndexes[i][j]] = initialValues[i][j]+wt;
                }
            }
            for (i = 0; i < allWeightValues.size();++i)
            {
                MString cmd;
                cmd = "setAttr ";
                cmd += weightAttrs[i];
                cmd += " -typ doubleArray ";
                cmd += allWeightValues[i].length();
                cmd += " ";
                for (j = 0; j < allWeightValues[i].length();++j)
                {
                    cmd += allWeightValues[i][j];
                    cmd += " ";
                }
//                cmd += " ) ";
//                cmd += weightAttrs[i];
//                MGlobal::displayInfo(MString()+wt);
                MGlobal::executeCommand(MString(cmd ), tmpAllWeightValues, false, false);
//                cmds.setAttr(weightAttrs[i],allWeightValues[i], typ='doubleArray')

            }
        }
//            MGlobal::displayInfo(MString()+weightName);

//        MString sCmd = "evalDeferred \"source \\\"cgfxShader_initUI.mel\\\"\"";
//        if()
//
//        if cmds.optionVar(exists='weightName') == 1:
//                            weightAttr = cmds.optionVar(q='weightName')
//                            weightAttrSplit = weightAttr.split(".")
//                            #---get deformer
//                            deformer = weightAttr.split(".")[1]
//                            geo = cmds.deformer(deformer, q = True, g = True)
//                            geoTransform = [cmds.listRelatives(i,parent = True)[0] for i in geo]
//                            #---make sure selected are points, and are in the deformer
//                            selected = cmds.ls(sl = True, fl = True)
//                            vtx = [i for i in selected if ".vtx[" in i]
//                            cv = [i for i in selected if ".cv[" in i]
//                            points = vtx + cv
//                            finalPoints = []
//
//                            weightAttrs = []
//                            allWeightValues = []
//                            for i in range(len(geoTransform)):
//                                weightAttrs.append(weightAttrSplit[1]+"."+weightAttrSplit[2] + "s["+str(i)+"]." + weightAttrSplit[2])
//                                allWeightValues.append(cmds.getAttr(weightAttrs[i]))
//
//                            final_points_indexes = []
//                            initial_values = []
//                            for i in range(len(geoTransform)):
//                                tmp_final_idx = []
//                                tmp_value = []
//                                for j in range(len(points)):
//                                    if geoTransform[i] in points[j]:
//                                        finalPoints.append(points[j])
//                                        idx = points[j].split("[")[1]
//                                        idx = int(idx.split("]")[0])
//                                        tmp_final_idx.append(idx)
//                                        tmp_value.append(allWeightValues[i][idx])
//                                final_points_indexes.append(tmp_final_idx)
//                                initial_values.append(tmp_value)
//                            for i in range(len(geoTransform)):
//                                for j in range(len(final_points_indexes[i])):
//                                    allWeightValues[i][final_points_indexes[i][j]] = initial_values[i][j]+wt
//                            for i in range(len(allWeightValues)):
//                                cmds.setAttr(weightAttrs[i],allWeightValues[i], typ='doubleArray')

        return MS::kSuccess;
}


//
// The weightSlide Context
//
// - tool contexts are custom event handlers. The selection
//   context class defaults to maya's selection mode and
//   allows you to override press/drag/release events.
//
#define     MOVEHELPSTR        "drag to move selected object"
#define     MOVETITLESTR       "weightSlide"
#define         TOP             0
#define         FRONT           1
#define         SIDE            2
#define         PERSP           3

class weightSlideContext : public MPxSelectionContext
{
public:
    weightSlideContext();
    virtual void    toolOnSetup( MEvent & event );
    virtual MStatus doPress( MEvent & event );
    virtual MStatus doDrag( MEvent & event );
    virtual MStatus doRelease( MEvent & event );
    virtual MStatus doEnterRegion( MEvent & event );

private:
        int currWin;
        MEvent::MouseButtonType downButton;
        MEvent::ModifierType shiftButton;
        M3dView view;
        short startPos_x, endPos_x, start_x, last_x;
        short startPos_y, endPos_y, start_y, last_y;
        weightSlideCmd * cmd;
};


weightSlideContext::weightSlideContext()
{
        MString str( MOVETITLESTR );
    setTitleString( str );

        // Tell the context which XPM to use so the tool can properly
        // be a candidate for the 6th position on the mini-bar.
        setImage("weightSlide.xpm", MPxContext::kImage1 );
}

void weightSlideContext::toolOnSetup( MEvent & )
{
        MString str( MOVEHELPSTR );
    setHelpString( str );
}

MStatus weightSlideContext::doPress( MEvent & event )
{
        MStatus stat = MPxSelectionContext::doPress( event );
        MSpace::Space spc = MSpace::kWorld;

        // If we are not in selecting mode (i.e. an object has been selected)
        // then set up for the translation.
        //
        if ( !isSelecting() ) {
                event.getPosition( startPos_x, startPos_y );
                view = M3dView::active3dView();

                MDagPath camera;
                stat = view.getCamera( camera );
                if ( stat != MS::kSuccess ) {
                        cerr << "Error: M3dView::getCamera" << endl;
                        return stat;
                }
                MFnCamera fnCamera( camera );
                MVector upDir = fnCamera.upDirection( spc );
                MVector rightDir = fnCamera.rightDirection( spc );

                // Determine the camera used in the current view
                //
                if ( fnCamera.isOrtho() ) {
                        if ( upDir.isEquivalent(MVector::zNegAxis,kVectorEpsilon) ) {
                                currWin = TOP;
                        } else if ( rightDir.isEquivalent(MVector::xAxis,kVectorEpsilon) ) {
                                currWin = FRONT;
                        } else  {
                                currWin = SIDE;
                        }
                }
                else {
                        currWin = PERSP;
                }

                // Create an instance of the move tool command.
                //
                cmd = (weightSlideCmd*)newToolCommand();

                cmd->setWeight( 0.0);
        }
        return stat;
}

MStatus weightSlideContext::doDrag( MEvent & event )
{
        MStatus stat;
        stat = MPxSelectionContext::doDrag( event );

        // If we are not in selecting mode (i.e. an object has been selected)
        // then do the translation.
        //
        if ( !isSelecting() ) {
                event.getPosition( endPos_x, endPos_y );
                MPoint endW, startW;
                MVector vec;
                view.viewToWorld( startPos_x, startPos_y, startW, vec );
                view.viewToWorld( endPos_x, endPos_y, endW, vec );
                downButton = event.mouseButton();
                shiftButton = event.modifiers();
                // We reset the the move vector each time a drag event occurs
                // and then recalculate it based on the start position.
                //
                cmd->undoIt();

                if (currWin == PERSP)
                {
                    if (downButton == MEvent::kMiddleMouse and shiftButton != MEvent::shiftKey and shiftButton != MEvent::controlKey)
                    {

                        double all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z;
                        if (all != 0)
                            all = all/3;
                        cmd->setWeight(all*40);

                    }
                    else if (downButton == MEvent::kMiddleMouse and shiftButton == MEvent::shiftKey and shiftButton != MEvent::controlKey)
                    {

                        double all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z;
                        if (all != 0)
                            all = all/3;
                        cmd->setWeight(all*60);

                    }
                    else if (downButton == MEvent::kMiddleMouse and shiftButton != MEvent::shiftKey and shiftButton != MEvent::controlKey)
                    {

                        double all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z;
                        if (all != 0)
                            all = all/3;
                        cmd->setWeight(all);

                    }
                    else
                    {

                        double all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z;
                        if (all != 0)
                            all = all/3;
                        cmd->setWeight(all);

                    }

                }
                else
                {
                    if (downButton == MEvent::kMiddleMouse and shiftButton != MEvent::shiftKey and shiftButton != MEvent::controlKey)
                    {

                        double all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z;
                        if (all != 0)
                            all = all/3;
                        cmd->setWeight(all*40);
//                                MGlobal::displayInfo(MString("THIS IS WORKING"));

                    }
                    else if (downButton == MEvent::kMiddleMouse and shiftButton == MEvent::shiftKey and shiftButton != MEvent::controlKey)
                    {

                        double all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z;
                        if (all != 0)
                            all = all/3;
                        cmd->setWeight(all * 0.1);

                    }
                    else if (downButton == MEvent::kMiddleMouse and shiftButton != MEvent::shiftKey and shiftButton != MEvent::controlKey)
                    {

                        double all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z;
                        if (all != 0)
                            all = all/3;
                        cmd->setWeight(all);

                    }
                    else
                    {

                        double all = endW.x - startW.x + endW.y - startW.y + endW.z - startW.z;
                        if (all != 0)
                            all = all/3;
                        cmd->setWeight(all * 0.01);

                    }

                }
                stat = cmd->redoIt();
                view.refresh( true );
        }
        return stat;
}

MStatus weightSlideContext::doRelease( MEvent & event )
{
        MStatus stat = MPxSelectionContext::doRelease( event );
        if ( !isSelecting() ) {
                event.getPosition( endPos_x, endPos_y );

                // Delete the move command if we have moved less then 2 pixels
                // otherwise call finalize to set up the journal and add the
                // command to the undo queue.
                //
                if ( abs(startPos_x - endPos_x) < 2 && abs(startPos_y - endPos_y) < 2 ) {
                        delete cmd;
                        view.refresh( true );
                }
                else {
                        stat = cmd->finalize();
                        view.refresh( true );
                }
        }
        return stat;
}

MStatus weightSlideContext::doEnterRegion( MEvent & /*event*/ )
//
// Print the tool description in the help line.
//
{
        MString str( MOVEHELPSTR );
    return setHelpString( str );
}


//
// Context creation command
//
#define     CREATE_CTX_NAME     "weightSlideContext"

class weightSlideContextCommand : public MPxContextCommand
{
public:
    weightSlideContextCommand() {};
    virtual MPxContext * makeObj();

public:
    static void* creator();
};

MPxContext * weightSlideContextCommand::makeObj()
{
    return new weightSlideContext();
}

void * weightSlideContextCommand::creator()
{
    return new weightSlideContextCommand;
}


MStatus initializePlugin( MObject obj )
{
        MStatus         status;
        MFnPlugin       plugin( obj, "Levi Harrison", "1.0", "Any" );

        status = plugin.registerContextCommand( CREATE_CTX_NAME,
                                                                        &weightSlideContextCommand::creator,
                                                                        MOVENAME, &weightSlideCmd::creator );
        if (!status) {
                status.perror("registerContextCommand");
                return status;
        }

        return status;
}

MStatus uninitializePlugin( MObject obj )
{
        MStatus         status;
        MFnPlugin       plugin( obj );

        status = plugin.deregisterContextCommand( CREATE_CTX_NAME, MOVENAME );
        if (!status) {
                status.perror("deregisterContextCommand");
                return status;
        }

        return status;
}

