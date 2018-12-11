#include <maya/MCppCompat.h>

#include "LHNurbsBlendshape.h"
#include <maya/MFnPlugin.h>

MTypeId LHNurbsBlend::id(0x00003652);
MObject LHNurbsBlend::aBlendOldMesh;
MObject LHNurbsBlend::aBlendWeight;
MObject LHNurbsBlend::aSurface;
MObject LHNurbsBlend::aSurfaceBase;
MObject LHNurbsBlend::aCacheParams;
MObject LHNurbsBlend::aCacheBase;

// baseGeoAttrs
MObject LHNurbsBlend::aTargetGeo;
MObject LHNurbsBlend::aTargetGeoParent;
MObject LHNurbsBlend::aUseBaseGeo;

MObject LHNurbsBlend::aBaseMesh;
MObject LHNurbsBlend::aBaseMeshParent;

MObject LHNurbsBlend::aBlendAttr;
MObject LHNurbsBlend::aBlendAttrParent;

MStatus LHNurbsBlend::pushbackNurbsParams(MObject &oSurfaceBase,
                                          int &numIndex,
										  MArrayDataHandle &geomArrayHandle,
										  std::vector <MPointArray> &UVBasePt,
										  int &cacheParamsAmt,
										  std::vector < std::vector < double > > &UBasePtParam,
										  std::vector < std::vector < double > > &VBasePtParam,
										  MObject &childGeom)


{
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	////////   get closest param infos (cache if specified)    ////////////
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// Caches out closest point functions for sliding """
    MStatus status;

	if (UVBasePt.size() < numIndex or cacheParamsAmt == 0)
	{
	    MNurbsIntersector fnBaseIntersector;
	    fnBaseIntersector.create(oSurfaceBase);
	    // dump existing infos
	    if (UVBasePt.size() > 0)
	        UVBasePt.clear();
	    if (UBasePtParam.size() > 0)
	        UBasePtParam.clear();
	    if (VBasePtParam.size() > 0)
	        VBasePtParam.clear();

	    for(i = 0; i < numIndex; i++ )
	    {
	        status = geomArrayHandle.jumpToElement( i );
	//                CheckStatusReturn( status, "Unable to jump to element" );
	        if (status == MS::kSuccess)
	        {
	            success = 1;
	        }
	        else
	        {
	            success = 0;
	        }
	        // if you find a connection, get the geometry
	        if (success == 1)
	        {
	            MPointArray tmpPoint;
	            std::vector < double > tmpUParam, tmpVParam;
	            MDataHandle dhInput = geomArrayHandle.inputValue();
	            MDataHandle dhWeightChild = dhInput.child( childGeom );
	            MItGeometry iter(dhWeightChild, true );
	            unsigned int iterGeoCount = iter.count();
	            if (iterGeoCount > 0)
	            {
	                for (; !iter.isDone();)
	                {
	                    pt = iter.position();

	                    MPointOnNurbs ptON;
	                    fnBaseIntersector.getClosestPoint(pt, ptON);
	                    tmpSlideUVPoint = ptON.getPoint();
	                    MPoint UV = ptON.getUV();
	                    fnUParam = UV.x;
	                    fnVParam = UV.y;

	                    tmpPoint.append(tmpSlideUVPoint);
	                    tmpUParam.push_back(fnUParam);
	                    tmpVParam.push_back(fnVParam);
	                    iter.next();
	                }
	                iter.reset();
	                UVBasePt.push_back(tmpPoint);
	                UBasePtParam.push_back(tmpUParam);
	                VBasePtParam.push_back(tmpVParam);
	            }
	            else
	            {
	                tmpPoint.append( 0.0, 0.0, 0.0 );
	                tmpUParam.push_back(0.0);
	                tmpVParam.push_back(0.0);

	                UVBasePt.push_back(tmpPoint);
	                UBasePtParam.push_back(tmpUParam);
	                VBasePtParam.push_back(tmpVParam);
	            }
	        }
	        else if (success == 0)
	        {
	            MPointArray tmpPoint;
	            std::vector < double > tmpUParam, tmpVParam;
	            tmpPoint.append( 0.0, 0.0, 0.0 );
	            tmpUParam.push_back(0.0);
	            tmpVParam.push_back(0.0);

	            UVBasePt.push_back(tmpPoint);
	            UBasePtParam.push_back(tmpUParam);
	            VBasePtParam.push_back(tmpVParam);
	        }
	    }
	}
    return MS::kSuccess;
}


void* LHNurbsBlend::creator() { return new LHNurbsBlend; }

MStatus LHNurbsBlend::deform(MDataBlock& data, MItGeometry& itGeo,
                          const MMatrix &localToWorldMatrix, unsigned int mIndex) {
  MObject thisMObj( thisMObject() );
  MStatus status;

  // Get the envelope and blend weight
  float env = data.inputValue(envelope).asFloat();

  if (env == 0.0)
  {
      return MS::kSuccess;
  }



  float blendWeight = data.inputValue(aBlendWeight).asFloat();
  int cacheParamsAmt = data.inputValue(aCacheParams).asInt();
  int cacheBaseAmt = data.inputValue(aCacheBase).asInt();

  //////////////////////////////////////////////////////////////////////////////////////////
  ////////   get all attrVals (can't cache)    ////////
  //////////////////////////////////////////////////////////////////////////////////////////

  int len = sizeof(aBlendAttrParent);
  MArrayDataHandle arrayHandle(data.inputArrayValue( aBlendAttrParent ));
  unsigned int attrCount = arrayHandle.elementCount();
  std::vector <float> attrValArray;

  for (j= 0; j < attrCount; ++j)
  {
	  arrayHandle.jumpToElement(j);
	  attrValArray.push_back(arrayHandle.inputValue().child( aBlendAttr ).asFloat());
  }



  blendWeight *= env;
  // Get the blend mesh
  MObject oBlendMesh = data.inputValue(aBlendOldMesh).asMesh();
//  if (oBlendMesh.isNull()) {
//    // No blend mesh attached so exit node.
//    return MS::kSuccess;
//  }

  //make sure num index is equal to the highest index of connected geometry
  //to avoid index scrambling
  MPlug geomPlug( thisMObj, input );
  MIntArray geomIndices;
  geomPlug.getExistingArrayAttributeIndices(geomIndices);
  len = geomIndices.length();

  //loop to put indices into std vector

  if (indexIntArray.size() > 0)
  {
      indexIntArray.clear();
  }

  for (i= 0; i < len; ++i)
  {
      indexIntArray.push_back(geomIndices[i]);
  }

  if (len == 1)
     numIndex = geomIndices[0]+1;
  if (len == 2)
     numIndex = std::max(geomIndices[0], geomIndices[1])+1;
  if (len >= 3)
     numIndex = *(std::max_element(indexIntArray.begin(), indexIntArray.end()))+1;


  // surfaces
  MObject oSurface = data.inputValue(aSurface).asNurbsSurfaceTransformed();
  MObject oSurfaceBase = data.inputValue(aSurfaceBase).asNurbsSurfaceTransformed();

  if (oSurface.isNull() or oSurfaceBase.isNull())
  {
      return MS::kSuccess;
  }


  //Surface Base
  MFnNurbsSurface fnSurfaceBase( oSurfaceBase );

  // get Surface
  MFnNurbsSurface fnSurface( oSurface );


  //Make sure attributes and target geo have the same count, otherwise you will crash
  //Target

//  MString string1;
//  string1 += (int)targetCount;
//  MString string2;
//  string2 += (int)attrCount;
//  MGlobal::displayInfo( "targetCount" + string1 + "attrCount" +string2);//print in script editor
//
//  if (attrCount != targetCount) {
//    // mismatch so exit node.
//    return MS::kSuccess;
//  }
//  MGlobal::displayInfo( "made it past" );//print in script editor
//
  //Base
  MArrayDataHandle geomArrayHandle = data.inputArrayValue(geomPlug);
  geomArrayHandle = data.inputArrayValue(aBaseMeshParent, &status);
  int baseCount = geomArrayHandle.elementCount();

  //Target
  MArrayDataHandle geomTargetArrayHandle = data.inputArrayValue(geomPlug);
  geomTargetArrayHandle = data.inputArrayValue(aBlendAttrParent, &status);
  int targetCount = geomTargetArrayHandle.elementCount();

//  MObject LHNurbsBlend::aTargetGeo;
//  MObject LHNurbsBlend::aTargetGeoParent;
//  MObject LHNurbsBlend::aUseBaseGeo;
//
//  MObject LHNurbsBlend::aBaseMesh;

//	MString string1;
//	string1 += (int)baseCount;
//	MString string2;
//	string2 += (int)targetCount;
//	MGlobal::displayInfo( "baseCount" + string1 + "targetCount" +string2);//print in script editor
//



  //Get info from base Mesh.  This is the default mesh.
  status = LHNurbsBlend::pushbackNurbsParams(oSurfaceBase, baseCount, geomArrayHandle,
		                                     slideUVBasePt, cacheParamsAmt, slideUBasePtParam,
											 slideVBasePtParam, aBaseMesh);
//  MGlobal::displayInfo("WORKING");

  //Get info from the target meshes.
  status = LHNurbsBlend::pushbackNurbsParams(oSurfaceBase, targetCount, geomTargetArrayHandle,
		                                     slideUVTargetPt, cacheParamsAmt, slideUTargetPtParam,
											 slideVTargetPtParam,
											 aTargetGeo);


//
//


  	// Need to cache
  	std::vector <MPointArray> targetPoints;

    for(i = 0; i < targetCount; i++ )
    {
		status = geomTargetArrayHandle.jumpToElement( i );
		MDataHandle dhInput = geomTargetArrayHandle.inputValue();
		MDataHandle dhWeightChild = dhInput.child( aTargetGeo );
		MItGeometry iter(dhWeightChild, true );
		MPointArray tmpTargetPoints;
		iter.allPositions(tmpTargetPoints, MSpace::kObject);
		targetPoints.push_back(tmpTargetPoints);
    }

//	MString string1;
//	string1 += (int)targetCount;
//	MString string2;
//	string2 += (int)baseCount;
//	MGlobal::displayInfo( "targetCount" + string1 + "baseCount" +string2);//print in script editor



//  MGlobal::displayInfo( "made it past" );//print in script editor
//
//
//  return MS::kSuccess;

  MPoint pt;
//  float w = 0.0f;
  for (; !itGeo.isDone(); itGeo.next()) {
    // Get the input point
    pt = itGeo.position();



    float uBaseParameter = slideUBasePtParam[0][itGeo.index()];
	float vBaseParameter = slideVBasePtParam[0][itGeo.index()];

//	MPoint finalAverage;
//	MPoint finalPatchPoint;
//
//    for(i = 0; i < targetCount; i++ )
//    {
//        float uTargetParameter = slideUTargetPtParam[i][itGeo.index()];
//    	float vTargetParameter = slideVTargetPtParam[i][itGeo.index()];
//
//
//    	float finalU = uBaseParameter + (uTargetParameter - uBaseParameter) * attrValArray[i];
//    	float finalV = vBaseParameter + (vTargetParameter - vBaseParameter) * attrValArray[i];
//
//    	MPoint startPoint;
//        fnSurface.getPointAtParam( uBaseParameter,vBaseParameter, startPoint, MSpace::kObject );
//
//		MPoint endPoint;
//		fnSurfaceBase.getPointAtParam( uTargetParameter,vTargetParameter, endPoint, MSpace::kObject );
//
//
//		MPoint finalPatchPointTemp;
//        fnSurface.getPointAtParam( finalU,finalV, finalPatchPointTemp, MSpace::kObject );
//
//    	MPoint averagePoint = startPoint + (endPoint - startPoint) * attrValArray[i];
//
//    	finalAverage += averagePoint;
//		finalPatchPoint += finalPatchPointTemp;
//
//    }
	pt = pt + (targetPoints[i][itGeo.index()] - pt) * attrValArray[i];
//	pt =  pt - (finalAverage - finalPatchPoint) * blendWeight;

    // Set the new output point
    itGeo.setPosition(pt);
  }

  return MS::kSuccess;
}

MStatus LHNurbsBlend::initialize() {
  MFnTypedAttribute tAttr;
  MFnNumericAttribute nAttr;
  MFnCompoundAttribute cAttr;
  MFnMatrixAttribute mAttr;
  MFnGenericAttribute gAttr;

  aBlendOldMesh = tAttr.create("blendMesh", "blendMesh", MFnData::kMesh);
  addAttribute(aBlendOldMesh);
  attributeAffects(aBlendOldMesh, outputGeom);


  MObject outputGeom = MPxDeformerNode::outputGeom;


  ////////// typed attributes ////////////

  // surface
  aSurface = tAttr.create("surface", "s", MFnData::kNurbsSurface);
  addAttribute( aSurface );
  attributeAffects(aSurface, outputGeom);

  // base
  aSurfaceBase = tAttr.create("surfaceBase", "sb", MFnData::kNurbsSurface);
  addAttribute( aSurfaceBase );
  attributeAffects(aSurfaceBase, outputGeom);

  aCacheParams = nAttr.create("cacheParams", "cpar", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setMin(0.0);
  nAttr.setMax(1.0);
  nAttr.setDefault(1.0);
  addAttribute(aCacheParams);
  attributeAffects(aCacheParams, outputGeom);

  aCacheBase = nAttr.create("cacheBase", "cb", MFnNumericData::kInt);
  nAttr.setKeyable(true);
  nAttr.setMin(0.0);
  nAttr.setMax(1.0);
  nAttr.setDefault(1.0);
  addAttribute(aCacheBase);
  attributeAffects(aCacheBase, outputGeom);

  //base geoms
  aTargetGeo = gAttr.create("targetGeo", "tGeo");
  gAttr.addAccept(MFnData::kMesh);
  gAttr.addAccept(MFnData::kNurbsSurface);
  gAttr.addAccept(MFnData::kNurbsCurve);
  attributeAffects(aTargetGeo, outputGeom);

//  aTargetGeoParent = cAttr.create("targetGeoArray", "tGeoArray");
//  cAttr.setKeyable(true);
//  cAttr.setArray(true);
//  cAttr.addChild( aTargetGeo );
//  cAttr.setReadable(true);
//  cAttr.setWritable(true);
//  cAttr.setConnectable(true);
//  cAttr.setChannelBox(true);
//  cAttr.setUsesArrayDataBuilder(true);
//  addAttribute(aTargetGeoParent);
//  attributeAffects(aTargetGeoParent, outputGeom);

  //  //blend geoms
    aBaseMesh = gAttr.create("baseMesh", "bMesh");
    gAttr.addAccept(MFnData::kMesh);
    gAttr.addAccept(MFnData::kNurbsSurface);
    gAttr.addAccept(MFnData::kNurbsCurve);
    addAttribute(aBaseMesh);
    attributeAffects(aBaseMesh, outputGeom);

    aBaseMeshParent = cAttr.create("baseMeshArray", "bMeshArray");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aBaseMesh );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aBaseMeshParent);
    attributeAffects(aBaseMeshParent, outputGeom);



    aBlendWeight = nAttr.create("blendWeight", "bw", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    nAttr.setMin(0.0);
    nAttr.setMax(1.0);
    nAttr.setDefault(1.0);
    addAttribute(aBlendWeight);
    attributeAffects(aBlendWeight, outputGeom);



    aBlendAttr = nAttr.create("blendAttr", "bv", MFnNumericData::kFloat);
    nAttr.setKeyable(true);
    cAttr.setIndexMatters( false );
    nAttr.setDefault(0.0);
    attributeAffects(aBlendAttr, outputGeom);

    aBlendAttrParent = cAttr.create("blendCompoundAttrs", "bca");
    cAttr.setKeyable(true);
    cAttr.setArray(true);
    cAttr.addChild( aBlendAttr );
//    cAttr.addChild( aBaseMesh );
    cAttr.addChild( aTargetGeo );
    cAttr.setReadable(true);
    cAttr.setWritable(true);
    cAttr.setIndexMatters( false );
    cAttr.setConnectable(true);
    cAttr.setChannelBox(true);
    cAttr.setUsesArrayDataBuilder(true);
    addAttribute(aBlendAttrParent);
    attributeAffects(aBlendAttrParent, outputGeom);


  // Make the deformer weights paintable
  MGlobal::executeCommand("makePaintable -attrType multiFloat -sm deformer blendNode weights;");

  return MS::kSuccess;
}

MStatus initializePlugin(MObject obj) {
  MStatus status;
  MFnPlugin plugin(obj, "Levi Harrison", "1.0", "Any");

  // Specify we are making a deformer node
  status = plugin.registerNode("nurbsBlend", LHNurbsBlend::id, LHNurbsBlend::creator,
                               LHNurbsBlend::initialize, MPxNode::kDeformerNode);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}

MStatus uninitializePlugin(MObject obj) {
  MStatus     status;
  MFnPlugin plugin(obj);

  status = plugin.deregisterNode(LHNurbsBlend::id);
  CHECK_MSTATUS_AND_RETURN_IT(status);

  return status;
}
