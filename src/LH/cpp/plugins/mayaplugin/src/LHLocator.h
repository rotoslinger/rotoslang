#pragma once

#include <maya/MIOStream.h>
#include <maya/MPxNode.h>
#include <maya/MPxLocatorNode.h>
#include <maya/MString.h>
#include <maya/MTypeId.h>
#include <maya/MPlug.h>
#include <maya/MVector.h>
#include <maya/MDataBlock.h>
#include <maya/MDataHandle.h>
#include <maya/MColor.h>
#include <maya/M3dView.h>
#include <maya/MDistance.h>
#include <maya/MFnUnitAttribute.h>
#include <maya/MFnMessageAttribute.h>
#include <maya/MFnNumericAttribute.h>
#include <maya/MFn.h>
#include <maya/MPxNode.h>
#include <maya/MPxManipContainer.h>
#include <maya/MFnDistanceManip.h>
#include <maya/MPxContext.h>
#include <maya/MPxSelectionContext.h>
#include <maya/MFnNumericData.h>
#include <maya/MManipData.h>

class LHLocator : public MPxLocatorNode
{
public:
        LHLocator();
        virtual ~LHLocator();
        virtual void            draw(M3dView &view, const MDagPath &path,
                                                                 M3dView::DisplayStyle style,
                                                                 M3dView::DisplayStatus status);

//        virtual bool            isBounded() const;
//        virtual MBoundingBox    boundingBox() const;

        static  void *          creator();
        static  MStatus         initialize();

        static  MObject         aMessage;
        static  MObject         aDrawFaces;

        static  MObject         aSize;
        static  MObject         aType;
        static  MObject         aOrient;
        static  MObject         aColorR;
        static  MObject         aColorG;
        static  MObject         aColorB;
public:
        static  MTypeId         id;
};
