
#include <maya/MSimple.h>
#include <maya/MObject.h>
#include <maya/MGlobal.h>
//#include <maya/MItSelectionList.h>
//#include <maya/MItSurfaceCV.h>
#include <maya/MMeshIntersector.h>
#include <maya/MPointArray.h>
#include <maya/MSelectionList.h>
#include <maya/MDagPath.h>

#include <maya/MIOStream.h>

DeclareSimpleCommand( getSymPoints, "Levi Harrison", "1.0");

MStatus getSymPoints::doIt( const MArgList& args )
{
        MStatus stat;
        MSelectionList list;
//        if args
        MString node = args.asString( 0, &stat );
        if (stat == MS::kSuccess)
            list.add(node);
        else
            MGlobal::getActiveSelectionList( list );

        MDagPath path;
        MObject  component;
        MDoubleArray returnArray;

        list.getDagPath(0,path);
        MMeshIntersector fnMesh (path);

        // get points
        MPointArray points;

        for ( i = 0; i < args.length(); i++ )
        {
                if ( args.asString(i) == MString("-node") ||
                        args.asString(i) == MString("-n") )
                        shadow = 1;
                if ( args.asString(i) == MString("-mirror") ||
                        args.asString(i) == MString("-m") )
                        shadow = 1;
                else
                        break;
        }

        // Make expanded Selection List
        //
//        for ( MItSelectionList iter( list ); !iter.isDone(); iter.next() ) {
//                iter.getDagPath( path, component );
//
//                if ( path.hasFn( MFn::kNurbsSurfaceGeom ) &&
//                         !component.isNull() ) {
//                        for ( MItSurfaceCV cvIter( path, component );
//                                  !cvIter.isDone(); cvIter.next() ) {
//                                newList.add( path, cvIter.cv() );
//                        }
//                } else {
//                        newList.add( path, component );
//                }
//        }

        // Return expanded selection list as an array of strings
        //
//        newList.getSelectionStrings( returnArray );

        MPxCommand::setResult( returnArray );

        return MS::kSuccess;
}
