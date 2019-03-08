//Maya ASCII 2018ff09 scene
//Name: MID_LIP_CURVES.ma
//Last modified: Thu, Mar 07, 2019 08:15:03 PM
//Codeset: UTF-8
requires maya "2018ff09";
requires -nodeType "glimpseGlobals" "glimpseMaya" "03.22.05";
requires -nodeType "assetResolverConfig" "assetResolverMaya" "AssetResolverMaya 1.0";
requires -nodeType "decomposeMatrix" "matrixNodes" "1.0";
requires "AL_MayaExtensionAttributes" "1.0";
requires -nodeType "LHWeightNode" -nodeType "LHCurveWeightNode" -nodeType "LHGeometryConstraint"
		 -nodeType "nullTransform" "collision" "1.0";
requires "stereoCamera" "10.0";
requires -nodeType "ALF_globals" -dataType "ALF_data" "ALF" "ALF 0.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201811281902-7c8857228f";
fileInfo "osv" "Linux 3.10.0-693.21.1.el7.x86_64 #1 SMP Wed Mar 7 19:03:37 UTC 2018 x86_64";
createNode transform -s -n "persp";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C91E";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0.014106936861085134 1.0661980394171238 2.3551304012328065 ;
	setAttr ".r" -type "double3" 1.4616472703973644 1.799999999999929 -6.2150876328019078e-18 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C91F";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 2.4337521878629187;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C920";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C921";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C922";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C923";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C924";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C925";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "BASE";
	rename -uid "94BF1100-0001-EA12-5C7F-22890002CEEF";
	setAttr ".v" no;
createNode mesh -n "BASEShape" -p "BASE";
	rename -uid "94BF1100-0001-EA12-5C7F-22890002CEEE";
	addAttr -ci true -sn "membershipWeights" -ln "membershipWeights" -dt "doubleArray";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".membershipWeights" -type "doubleArray" 1111 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 ;
createNode transform -n "pPlane1";
	rename -uid "94BF1100-0001-EA12-5C7F-22890002CEF2";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 2 ;
createNode mesh -n "pPlaneShape1" -p "pPlane1";
	rename -uid "94BF1100-0001-EA12-5C7F-22890002CEF1";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "BASE1";
	rename -uid "94BF1100-0001-EA12-5C7F-22950002CF2C";
	setAttr ".v" no;
createNode mesh -n "BASE1Shape" -p "BASE1";
	rename -uid "94BF1100-0001-EA12-5C7F-22950002CF2B";
	addAttr -ci true -sn "membershipWeights" -ln "membershipWeights" -dt "doubleArray";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".membershipWeights" -type "doubleArray" 1111 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 ;
createNode transform -n "pPlane2";
	rename -uid "94BF1100-0001-EA12-5C7F-22950002CF2F";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 2 ;
createNode mesh -n "pPlaneShape2" -p "pPlane2";
	rename -uid "94BF1100-0001-EA12-5C7F-22950002CF2E";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "BASE2";
	rename -uid "94BF1100-0001-EA12-5C7F-237E0002D812";
	setAttr ".v" no;
createNode mesh -n "BASE2Shape" -p "BASE2";
	rename -uid "94BF1100-0001-EA12-5C7F-237E0002D811";
	addAttr -ci true -sn "membershipWeights" -ln "membershipWeights" -dt "doubleArray";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".membershipWeights" -type "doubleArray" 1111 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 ;
createNode transform -n "pPlane3";
	rename -uid "94BF1100-0001-EA12-5C7F-237E0002D815";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 2 ;
createNode mesh -n "pPlaneShape3" -p "pPlane3";
	rename -uid "94BF1100-0001-EA12-5C7F-237E0002D814";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "BASE3";
	rename -uid "3A48D100-0000-2490-5C81-B67F000636CA";
	setAttr ".v" no;
createNode mesh -n "BASE3Shape" -p "BASE3";
	rename -uid "3A48D100-0000-2490-5C81-B67F000636C9";
	addAttr -ci true -sn "membershipWeights" -ln "membershipWeights" -dt "doubleArray";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".membershipWeights" -type "doubleArray" 561 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 ;
createNode transform -n "pPlane4";
	rename -uid "3A48D100-0000-2490-5C81-B67F000636CD";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 2 ;
createNode mesh -n "pPlaneShape4" -p "pPlane4";
	rename -uid "3A48D100-0000-2490-5C81-B67F000636CC";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "Control";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC69";
	addAttr -ci true -k true -sn "C_falloff" -ln "C_falloff" -at "float";
	addAttr -ci true -k true -sn "C_lipSingle_LR" -ln "C_lipSingle_LR" -at "float";
	addAttr -ci true -k true -sn "C_lipSingle_UD" -ln "C_lipSingle_UD" -at "float";
	addAttr -ci true -k true -sn "L_falloff00" -ln "L_falloff00" -at "float";
	addAttr -ci true -k true -sn "R_falloff00" -ln "R_falloff00" -at "float";
	addAttr -ci true -k true -sn "L_lipPrime00_LR" -ln "L_lipPrime00_LR" -at "float";
	addAttr -ci true -k true -sn "C_lipPrime_LR" -ln "C_lipPrime_LR" -at "float";
	addAttr -ci true -k true -sn "R_lipPrime00_LR" -ln "R_lipPrime00_LR" -at "float";
	addAttr -ci true -k true -sn "L_lipPrime00_UD" -ln "L_lipPrime00_UD" -at "float";
	addAttr -ci true -k true -sn "C_lipPrime_UD" -ln "C_lipPrime_UD" -at "float";
	addAttr -ci true -k true -sn "R_lipPrime00_UD" -ln "R_lipPrime00_UD" -at "float";
	addAttr -ci true -k true -sn "L_falloff01" -ln "L_falloff01" -at "float";
	addAttr -ci true -k true -sn "L_falloff02" -ln "L_falloff02" -at "float";
	addAttr -ci true -k true -sn "L_falloff03" -ln "L_falloff03" -at "float";
	addAttr -ci true -k true -sn "L_falloff04" -ln "L_falloff04" -at "float";
	addAttr -ci true -k true -sn "R_falloff04" -ln "R_falloff04" -at "float";
	addAttr -ci true -k true -sn "R_falloff03" -ln "R_falloff03" -at "float";
	addAttr -ci true -k true -sn "R_falloff02" -ln "R_falloff02" -at "float";
	addAttr -ci true -k true -sn "R_falloff01" -ln "R_falloff01" -at "float";
	addAttr -ci true -k true -sn "L_lipSecondary00_LR" -ln "L_lipSecondary00_LR" -at "float";
	addAttr -ci true -k true -sn "L_lipSecondary01_LR" -ln "L_lipSecondary01_LR" -at "float";
	addAttr -ci true -k true -sn "L_lipSecondary02_LR" -ln "L_lipSecondary02_LR" -at "float";
	addAttr -ci true -k true -sn "L_lipSecondary03_LR" -ln "L_lipSecondary03_LR" -at "float";
	addAttr -ci true -k true -sn "L_lipSecondary04_LR" -ln "L_lipSecondary04_LR" -at "float";
	addAttr -ci true -k true -sn "C_lipSecondary_LR" -ln "C_lipSecondary_LR" -at "float";
	addAttr -ci true -k true -sn "R_lipSecondary04_LR" -ln "R_lipSecondary04_LR" -at "float";
	addAttr -ci true -k true -sn "R_lipSecondary03_LR" -ln "R_lipSecondary03_LR" -at "float";
	addAttr -ci true -k true -sn "R_lipSecondary02_LR" -ln "R_lipSecondary02_LR" -at "float";
	addAttr -ci true -k true -sn "R_lipSecondary01_LR" -ln "R_lipSecondary01_LR" -at "float";
	addAttr -ci true -k true -sn "R_lipSecondary00_LR" -ln "R_lipSecondary00_LR" -at "float";
	addAttr -ci true -k true -sn "L_lipSecondary00_UD" -ln "L_lipSecondary00_UD" -at "float";
	addAttr -ci true -k true -sn "L_lipSecondary01_UD" -ln "L_lipSecondary01_UD" -at "float";
	addAttr -ci true -k true -sn "L_lipSecondary02_UD" -ln "L_lipSecondary02_UD" -at "float";
	addAttr -ci true -k true -sn "L_lipSecondary03_UD" -ln "L_lipSecondary03_UD" -at "float";
	addAttr -ci true -k true -sn "L_lipSecondary04_UD" -ln "L_lipSecondary04_UD" -at "float";
	addAttr -ci true -k true -sn "C_lipSecondary_UD" -ln "C_lipSecondary_UD" -at "float";
	addAttr -ci true -k true -sn "R_lipSecondary04_UD" -ln "R_lipSecondary04_UD" -at "float";
	addAttr -ci true -k true -sn "R_lipSecondary03_UD" -ln "R_lipSecondary03_UD" -at "float";
	addAttr -ci true -k true -sn "R_lipSecondary02_UD" -ln "R_lipSecondary02_UD" -at "float";
	addAttr -ci true -k true -sn "R_lipSecondary01_UD" -ln "R_lipSecondary01_UD" -at "float";
	addAttr -ci true -k true -sn "R_lipSecondary00_UD" -ln "R_lipSecondary00_UD" -at "float";
	setAttr -k on ".C_falloff";
	setAttr -k on ".C_lipSingle_LR";
	setAttr -k on ".C_lipSingle_UD";
	setAttr -k on ".L_falloff00";
	setAttr -k on ".R_falloff00";
	setAttr -k on ".L_lipPrime00_LR";
	setAttr -k on ".C_lipPrime_LR";
	setAttr -k on ".R_lipPrime00_LR";
	setAttr -k on ".L_lipPrime00_UD";
	setAttr -k on ".C_lipPrime_UD";
	setAttr -k on ".R_lipPrime00_UD";
	setAttr -k on ".L_falloff01";
	setAttr -k on ".L_falloff02";
	setAttr -k on ".L_falloff03";
	setAttr -k on ".L_falloff04";
	setAttr -k on ".R_falloff04";
	setAttr -k on ".R_falloff03";
	setAttr -k on ".R_falloff02";
	setAttr -k on ".R_falloff01";
	setAttr -k on ".L_lipSecondary00_LR";
	setAttr -k on ".L_lipSecondary01_LR";
	setAttr -k on ".L_lipSecondary02_LR";
	setAttr -k on ".L_lipSecondary03_LR";
	setAttr -k on ".L_lipSecondary04_LR";
	setAttr -k on ".C_lipSecondary_LR";
	setAttr -k on ".R_lipSecondary04_LR";
	setAttr -k on ".R_lipSecondary03_LR";
	setAttr -k on ".R_lipSecondary02_LR";
	setAttr -k on ".R_lipSecondary01_LR";
	setAttr -k on ".R_lipSecondary00_LR";
	setAttr -k on ".L_lipSecondary00_UD";
	setAttr -k on ".L_lipSecondary01_UD";
	setAttr -k on ".L_lipSecondary02_UD";
	setAttr -k on ".L_lipSecondary03_UD";
	setAttr -k on ".L_lipSecondary04_UD";
	setAttr -k on ".C_lipSecondary_UD";
	setAttr -k on ".R_lipSecondary04_UD";
	setAttr -k on ".R_lipSecondary03_UD";
	setAttr -k on ".R_lipSecondary02_UD";
	setAttr -k on ".R_lipSecondary01_UD";
	setAttr -k on ".R_lipSecondary00_UD";
createNode nurbsCurve -n "ControlShape" -p "Control";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC68";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode transform -n "deformMesh";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC6C";
createNode mesh -n "deformMeshShape" -p "deformMesh";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC6B";
	setAttr -k off ".v";
	setAttr -s 6 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode mesh -n "deformMeshShapeOrig" -p "deformMesh";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC6E";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "cluster1Handle";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC76";
	setAttr ".t" -type "double3" 0 1 0 ;
createNode clusterHandle -n "cluster1HandleShape" -p "cluster1Handle";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC77";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
createNode transform -n "BASE4";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC7A";
	setAttr ".v" no;
createNode mesh -n "BASE4Shape" -p "BASE4";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC79";
	addAttr -ci true -sn "membershipWeights" -ln "membershipWeights" -dt "doubleArray";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".membershipWeights" -type "doubleArray" 341 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
		 1 ;
createNode transform -n "pPlane5";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC7D";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 2 ;
createNode mesh -n "pPlaneShape5" -p "pPlane5";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC7C";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "cluster2Handle";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC82";
	setAttr ".t" -type "double3" 1 0 0 ;
	setAttr ".rp" -type "double3" 0 1 0 ;
	setAttr ".sp" -type "double3" 0 1 0 ;
createNode clusterHandle -n "cluster2HandleShape" -p "cluster2Handle";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC83";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".or" -type "double3" 0 1 0 ;
createNode transform -n "C_lipSingle_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC8D";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "C_lipSingle_LOC" -p "C_lipSingle_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC8E";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "C_lipSingle_LOCShape" -p "C_lipSingle_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC8F";
	setAttr -k off ".v" no;
createNode transform -n "C_lipSingleBuffer2_GRP" -p "C_lipSingle_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC90";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr ".t" -type "double3" 8.9406967163085938e-08 -5.9604410296287824e-09 0 ;
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "C_lipSingleBuffer1_GRP" -p "C_lipSingleBuffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC91";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "C_lipSingle_CTL" -p "C_lipSingleBuffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC94";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr ".t" -type "double3" 0 -0.6 0 ;
	setAttr ".speedtyout" -0.6;
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape1" -p "C_lipSingle_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC92";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 1 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.070000000000000007 -8.5725275940314735e-18 0.099999999999999992
		-0.060621750000000002 -0.03500000000000001 0.099999999999999992
		-0.034999999999999996 -0.060621750000000016 0.099999999999999992
		8.5725275940314735e-18 -0.070000000000000007 0.10000000000000001
		0.03500000000000001 -0.060621750000000002 0.10000000000000002
		0.060621750000000016 -0.034999999999999996 0.10000000000000002
		0.070000000000000007 8.5725275940314735e-18 0.10000000000000002
		0.060621750000000002 0.03500000000000001 0.10000000000000002
		0.034999999999999996 0.060621750000000016 0.10000000000000002
		-8.5725275940314735e-18 0.070000000000000007 0.10000000000000001
		-0.03500000000000001 0.060621750000000002 0.099999999999999992
		-0.060621750000000016 0.034999999999999996 0.099999999999999992
		-0.070000000000000007 -8.5725275940314735e-18 0.099999999999999992
		-0.049497489999999991 -6.0616942694328134e-18 0.050502509999999987
		1.5543122344752193e-17 0 0.029999999999999999
		0.049497490000000019 6.0616942694328134e-18 0.050502510000000014
		0.070000000000000007 8.5725275940314735e-18 0.10000000000000002
		0.049497489999999991 6.0616942694328134e-18 0.14949749000000001
		-1.5543122344752193e-17 0 0.17000000000000001
		-9.1744687315982812e-18 -0.035000000000000003 0.16062175000000001
		-3.475379627549899e-19 -0.060621750000000009 0.13500000000000001
		8.5725275940314735e-18 -0.070000000000000007 0.10000000000000001
		1.5195584381997202e-17 -0.060621750000000009 0.065000000000000002
		1.7746996325629756e-17 -0.035000000000000003 0.039378249999999997
		1.5543122344752193e-17 0 0.029999999999999999
		9.1744687315982812e-18 0.035000000000000003 0.039378249999999997
		3.475379627549899e-19 0.060621750000000009 0.065000000000000002
		-8.5725275940314735e-18 0.070000000000000007 0.10000000000000001
		-1.5195584381997202e-17 0.060621750000000009 0.13500000000000001
		-1.7746996325629756e-17 0.035000000000000003 0.16062175000000001
		-1.5543122344752193e-17 0 0.17000000000000001
		-0.049497490000000019 -6.0616942694328134e-18 0.14949749000000001
		-0.070000000000000007 -8.5725275940314735e-18 0.099999999999999992
		;
createNode transform -n "C_lipSingleGimbal_CTL" -p "C_lipSingle_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC96";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape2" -p "C_lipSingleGimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC95";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 1 1 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.063000000000000014
		0 0.031500000000000007 0.054559575000000013
		0 0.054559575000000013 0.031500000000000007
		0 0.063000000000000014 0
		0 0.054559575000000013 -0.031500000000000007
		0 0.031500000000000007 -0.054559575000000013
		0 0 -0.063000000000000014
		0 -0.031500000000000007 -0.054559575000000013
		0 -0.054559575000000013 -0.031500000000000007
		0 -0.063000000000000014 0
		0 -0.054559575000000013 0.031500000000000007
		0 -0.031500000000000007 0.054559575000000013
		0 0 0.063000000000000014
		0.044547741000000016 0 0.044547741000000016
		0.063000000000000014 0 0
		0.044547741000000016 0 -0.044547741000000016
		0 0 -0.063000000000000014
		-0.044547741000000016 0 -0.044547741000000016
		-0.063000000000000014 0 0
		-0.054559575000000013 0.031500000000000007 0
		-0.031500000000000007 0.054559575000000013 0
		0 0.063000000000000014 0
		0.031500000000000007 0.054559575000000013 0
		0.054559575000000013 0.031500000000000007 0
		0.063000000000000014 0 0
		0.054559575000000013 -0.031500000000000007 0
		0.031500000000000007 -0.054559575000000013 0
		0 -0.063000000000000014 0
		-0.031500000000000007 -0.054559575000000013 0
		-0.054559575000000013 -0.031500000000000007 0
		-0.063000000000000014 0 0
		-0.044547741000000016 0 0.044547741000000016
		0 0 0.063000000000000014
		;
createNode transform -n "L_lipPrime00_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCA5";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "L_lipPrime00_LOC" -p "L_lipPrime00_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCA6";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "L_lipPrime00_LOCShape" -p "L_lipPrime00_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCA7";
	setAttr -k off ".v" no;
createNode transform -n "L_lipPrime00Buffer2_GRP" -p "L_lipPrime00_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCA8";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr ".t" -type "double3" 1.5894570992713852e-08 -1.2327226350805631e-08 0 ;
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "L_lipPrime00Buffer1_GRP" -p "L_lipPrime00Buffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCA9";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "L_lipPrime00_CTL" -p "L_lipPrime00Buffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCAC";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr ".t" -type "double3" 0 0.40060463949354463 0 ;
	setAttr ".speedtyout" 0.40060463949354463;
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape3" -p "L_lipPrime00_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCAA";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.050000000000000003 0.10000000000000001 0.099999999999999992
		-0.043301250000000006 0.074999999999999997 0.099999999999999992
		-0.024999999999999994 0.056698749999999999 0.10000000000000001
		6.1232339957367663e-18 0.050000000000000003 0.10000000000000001
		0.025000000000000008 0.056698749999999999 0.10000000000000001
		0.043301250000000006 0.075000000000000011 0.10000000000000002
		0.050000000000000003 0.10000000000000001 0.10000000000000002
		0.043301250000000006 0.125 0.10000000000000002
		0.024999999999999994 0.14330125000000002 0.10000000000000001
		-6.1232339957367663e-18 0.15000000000000002 0.10000000000000001
		-0.025000000000000008 0.14330125000000002 0.10000000000000001
		-0.043301250000000006 0.125 0.099999999999999992
		-0.050000000000000003 0.10000000000000001 0.099999999999999992
		-0.035355349999999994 0.10000000000000001 0.064644649999999998
		1.1102230246251566e-17 0.10000000000000001 0.050000000000000003
		0.035355350000000008 0.10000000000000001 0.064644650000000012
		0.050000000000000003 0.10000000000000001 0.10000000000000002
		0.035355349999999994 0.10000000000000001 0.13535535000000001
		-1.1102230246251566e-17 0.10000000000000001 0.15000000000000002
		-6.5531919511416302e-18 0.075000000000000011 0.14330125000000002
		-2.4824140196784905e-19 0.056698749999999999 0.125
		6.1232339957367663e-18 0.050000000000000003 0.10000000000000001
		1.0853988844283717e-17 0.056698749999999999 0.075000000000000011
		1.2676425946878397e-17 0.075000000000000011 0.056698749999999999
		1.1102230246251566e-17 0.10000000000000001 0.050000000000000003
		6.5531919511416302e-18 0.125 0.056698749999999999
		2.4824140196784905e-19 0.14330125000000002 0.075000000000000011
		-6.1232339957367663e-18 0.15000000000000002 0.10000000000000001
		-1.0853988844283717e-17 0.14330125000000002 0.125
		-1.2676425946878397e-17 0.125 0.14330125000000002
		-1.1102230246251566e-17 0.10000000000000001 0.15000000000000002
		-0.035355350000000008 0.10000000000000001 0.13535534999999999
		-0.050000000000000003 0.10000000000000001 0.099999999999999992
		;
createNode transform -n "L_lipPrime00Gimbal_CTL" -p "L_lipPrime00_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCAE";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape4" -p "L_lipPrime00Gimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCAD";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.045000000000000005
		0 0.022500000000000003 0.038971125000000009
		0 0.038971125000000009 0.022500000000000003
		0 0.045000000000000005 0
		0 0.038971125000000009 -0.022500000000000003
		0 0.022500000000000003 -0.038971125000000009
		0 0 -0.045000000000000005
		0 -0.022500000000000003 -0.038971125000000009
		0 -0.038971125000000009 -0.022500000000000003
		0 -0.045000000000000005 0
		0 -0.038971125000000009 0.022500000000000003
		0 -0.022500000000000003 0.038971125000000009
		0 0 0.045000000000000005
		0.031819815000000008 0 0.031819815000000008
		0.045000000000000005 0 0
		0.031819815000000008 0 -0.031819815000000008
		0 0 -0.045000000000000005
		-0.031819815000000008 0 -0.031819815000000008
		-0.045000000000000005 0 0
		-0.038971125000000009 0.022500000000000003 0
		-0.022500000000000003 0.038971125000000009 0
		0 0.045000000000000005 0
		0.022500000000000003 0.038971125000000009 0
		0.038971125000000009 0.022500000000000003 0
		0.045000000000000005 0 0
		0.038971125000000009 -0.022500000000000003 0
		0.022500000000000003 -0.038971125000000009 0
		0 -0.045000000000000005 0
		-0.022500000000000003 -0.038971125000000009 0
		-0.038971125000000009 -0.022500000000000003 0
		-0.045000000000000005 0 0
		-0.031819815000000008 0 0.031819815000000008
		0 0 0.045000000000000005
		;
createNode transform -n "C_lipPrime_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCB4";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "C_lipPrime_LOC" -p "C_lipPrime_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCB5";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "C_lipPrime_LOCShape" -p "C_lipPrime_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCB6";
	setAttr -k off ".v" no;
createNode transform -n "C_lipPrimeBuffer2_GRP" -p "C_lipPrime_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCB7";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr ".t" -type "double3" -4.9737991503207013e-14 -1.7603838387003634e-09 0 ;
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "C_lipPrimeBuffer1_GRP" -p "C_lipPrimeBuffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCB8";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "C_lipPrime_CTL" -p "C_lipPrimeBuffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCBB";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr ".t" -type "double3" 0 0.55292475304600597 0 ;
	setAttr ".speedtyout" 0.55292475304600597;
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape5" -p "C_lipPrime_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCB9";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 1 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.050000000000000003 0.10000000000000001 0.099999999999999992
		-0.043301250000000006 0.074999999999999997 0.099999999999999992
		-0.024999999999999994 0.056698749999999999 0.10000000000000001
		6.1232339957367663e-18 0.050000000000000003 0.10000000000000001
		0.025000000000000008 0.056698749999999999 0.10000000000000001
		0.043301250000000006 0.075000000000000011 0.10000000000000002
		0.050000000000000003 0.10000000000000001 0.10000000000000002
		0.043301250000000006 0.125 0.10000000000000002
		0.024999999999999994 0.14330125000000002 0.10000000000000001
		-6.1232339957367663e-18 0.15000000000000002 0.10000000000000001
		-0.025000000000000008 0.14330125000000002 0.10000000000000001
		-0.043301250000000006 0.125 0.099999999999999992
		-0.050000000000000003 0.10000000000000001 0.099999999999999992
		-0.035355349999999994 0.10000000000000001 0.064644649999999998
		1.1102230246251566e-17 0.10000000000000001 0.050000000000000003
		0.035355350000000008 0.10000000000000001 0.064644650000000012
		0.050000000000000003 0.10000000000000001 0.10000000000000002
		0.035355349999999994 0.10000000000000001 0.13535535000000001
		-1.1102230246251566e-17 0.10000000000000001 0.15000000000000002
		-6.5531919511416302e-18 0.075000000000000011 0.14330125000000002
		-2.4824140196784905e-19 0.056698749999999999 0.125
		6.1232339957367663e-18 0.050000000000000003 0.10000000000000001
		1.0853988844283717e-17 0.056698749999999999 0.075000000000000011
		1.2676425946878397e-17 0.075000000000000011 0.056698749999999999
		1.1102230246251566e-17 0.10000000000000001 0.050000000000000003
		6.5531919511416302e-18 0.125 0.056698749999999999
		2.4824140196784905e-19 0.14330125000000002 0.075000000000000011
		-6.1232339957367663e-18 0.15000000000000002 0.10000000000000001
		-1.0853988844283717e-17 0.14330125000000002 0.125
		-1.2676425946878397e-17 0.125 0.14330125000000002
		-1.1102230246251566e-17 0.10000000000000001 0.15000000000000002
		-0.035355350000000008 0.10000000000000001 0.13535534999999999
		-0.050000000000000003 0.10000000000000001 0.099999999999999992
		;
createNode transform -n "C_lipPrimeGimbal_CTL" -p "C_lipPrime_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCBD";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape6" -p "C_lipPrimeGimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCBC";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 1 1 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.045000000000000005
		0 0.022500000000000003 0.038971125000000009
		0 0.038971125000000009 0.022500000000000003
		0 0.045000000000000005 0
		0 0.038971125000000009 -0.022500000000000003
		0 0.022500000000000003 -0.038971125000000009
		0 0 -0.045000000000000005
		0 -0.022500000000000003 -0.038971125000000009
		0 -0.038971125000000009 -0.022500000000000003
		0 -0.045000000000000005 0
		0 -0.038971125000000009 0.022500000000000003
		0 -0.022500000000000003 0.038971125000000009
		0 0 0.045000000000000005
		0.031819815000000008 0 0.031819815000000008
		0.045000000000000005 0 0
		0.031819815000000008 0 -0.031819815000000008
		0 0 -0.045000000000000005
		-0.031819815000000008 0 -0.031819815000000008
		-0.045000000000000005 0 0
		-0.038971125000000009 0.022500000000000003 0
		-0.022500000000000003 0.038971125000000009 0
		0 0.045000000000000005 0
		0.022500000000000003 0.038971125000000009 0
		0.038971125000000009 0.022500000000000003 0
		0.045000000000000005 0 0
		0.038971125000000009 -0.022500000000000003 0
		0.022500000000000003 -0.038971125000000009 0
		0 -0.045000000000000005 0
		-0.022500000000000003 -0.038971125000000009 0
		-0.038971125000000009 -0.022500000000000003 0
		-0.045000000000000005 0 0
		-0.031819815000000008 0 0.031819815000000008
		0 0 0.045000000000000005
		;
createNode transform -n "R_lipPrime00_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCC3";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_lipPrime00_LOC" -p "R_lipPrime00_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCC4";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "R_lipPrime00_LOCShape" -p "R_lipPrime00_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCC5";
	setAttr -k off ".v" no;
createNode transform -n "R_lipPrime00Buffer2_GRP" -p "R_lipPrime00_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCC6";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr ".t" -type "double3" -1.5894574545427531e-08 1.8356146824771713e-08 0 ;
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_lipPrime00Buffer1_GRP" -p "R_lipPrime00Buffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCC7";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "R_lipPrime00_CTL" -p "R_lipPrime00Buffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCCA";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr ".t" -type "double3" 0 0.4047566189241486 0 ;
	setAttr ".speedtyout" 0.4047566189241486;
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape7" -p "R_lipPrime00_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCC8";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.050000000000000003 0.10000000000000001 0.099999999999999992
		-0.043301250000000006 0.074999999999999997 0.099999999999999992
		-0.024999999999999994 0.056698749999999999 0.10000000000000001
		6.1232339957367663e-18 0.050000000000000003 0.10000000000000001
		0.025000000000000008 0.056698749999999999 0.10000000000000001
		0.043301250000000006 0.075000000000000011 0.10000000000000002
		0.050000000000000003 0.10000000000000001 0.10000000000000002
		0.043301250000000006 0.125 0.10000000000000002
		0.024999999999999994 0.14330125000000002 0.10000000000000001
		-6.1232339957367663e-18 0.15000000000000002 0.10000000000000001
		-0.025000000000000008 0.14330125000000002 0.10000000000000001
		-0.043301250000000006 0.125 0.099999999999999992
		-0.050000000000000003 0.10000000000000001 0.099999999999999992
		-0.035355349999999994 0.10000000000000001 0.064644649999999998
		1.1102230246251566e-17 0.10000000000000001 0.050000000000000003
		0.035355350000000008 0.10000000000000001 0.064644650000000012
		0.050000000000000003 0.10000000000000001 0.10000000000000002
		0.035355349999999994 0.10000000000000001 0.13535535000000001
		-1.1102230246251566e-17 0.10000000000000001 0.15000000000000002
		-6.5531919511416302e-18 0.075000000000000011 0.14330125000000002
		-2.4824140196784905e-19 0.056698749999999999 0.125
		6.1232339957367663e-18 0.050000000000000003 0.10000000000000001
		1.0853988844283717e-17 0.056698749999999999 0.075000000000000011
		1.2676425946878397e-17 0.075000000000000011 0.056698749999999999
		1.1102230246251566e-17 0.10000000000000001 0.050000000000000003
		6.5531919511416302e-18 0.125 0.056698749999999999
		2.4824140196784905e-19 0.14330125000000002 0.075000000000000011
		-6.1232339957367663e-18 0.15000000000000002 0.10000000000000001
		-1.0853988844283717e-17 0.14330125000000002 0.125
		-1.2676425946878397e-17 0.125 0.14330125000000002
		-1.1102230246251566e-17 0.10000000000000001 0.15000000000000002
		-0.035355350000000008 0.10000000000000001 0.13535534999999999
		-0.050000000000000003 0.10000000000000001 0.099999999999999992
		;
createNode transform -n "R_lipPrime00Gimbal_CTL" -p "R_lipPrime00_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCCC";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape8" -p "R_lipPrime00Gimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCCB";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.045000000000000005
		0 0.022500000000000003 0.038971125000000009
		0 0.038971125000000009 0.022500000000000003
		0 0.045000000000000005 0
		0 0.038971125000000009 -0.022500000000000003
		0 0.022500000000000003 -0.038971125000000009
		0 0 -0.045000000000000005
		0 -0.022500000000000003 -0.038971125000000009
		0 -0.038971125000000009 -0.022500000000000003
		0 -0.045000000000000005 0
		0 -0.038971125000000009 0.022500000000000003
		0 -0.022500000000000003 0.038971125000000009
		0 0 0.045000000000000005
		0.031819815000000008 0 0.031819815000000008
		0.045000000000000005 0 0
		0.031819815000000008 0 -0.031819815000000008
		0 0 -0.045000000000000005
		-0.031819815000000008 0 -0.031819815000000008
		-0.045000000000000005 0 0
		-0.038971125000000009 0.022500000000000003 0
		-0.022500000000000003 0.038971125000000009 0
		0 0.045000000000000005 0
		0.022500000000000003 0.038971125000000009 0
		0.038971125000000009 0.022500000000000003 0
		0.045000000000000005 0 0
		0.038971125000000009 -0.022500000000000003 0
		0.022500000000000003 -0.038971125000000009 0
		0 -0.045000000000000005 0
		-0.022500000000000003 -0.038971125000000009 0
		-0.038971125000000009 -0.022500000000000003 0
		-0.045000000000000005 0 0
		-0.031819815000000008 0 0.031819815000000008
		0 0 0.045000000000000005
		;
createNode transform -n "L_lipSecondary00_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCEE";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "L_lipSecondary00_LOC" -p "L_lipSecondary00_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCEF";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "L_lipSecondary00_LOCShape" -p "L_lipSecondary00_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCF0";
	setAttr -k off ".v" no;
createNode transform -n "L_lipSecondary00Buffer2_GRP" -p "L_lipSecondary00_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCF1";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "L_lipSecondary00Buffer1_GRP" -p "L_lipSecondary00Buffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCF2";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "L_lipSecondary00_CTL" -p "L_lipSecondary00Buffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCF5";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape9" -p "L_lipSecondary00_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCF3";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.025980749999999997 0.035000000000000003 0.10000000000000001
		-0.014999999999999996 0.024019249999999999 0.10000000000000001
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		0.015000000000000003 0.024019250000000006 0.10000000000000001
		0.025980750000000004 0.035000000000000003 0.10000000000000001
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.025980749999999997 0.065000000000000002 0.10000000000000001
		0.014999999999999996 0.075980750000000014 0.10000000000000001
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-0.015000000000000003 0.07598075 0.10000000000000001
		-0.025980750000000004 0.065000000000000002 0.10000000000000001
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.021213209999999996 0.050000000000000003 0.078786789999999995
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		0.021213210000000003 0.050000000000000003 0.078786790000000009
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.021213209999999996 0.050000000000000003 0.12121321000000002
		-6.661338147750939e-18 0.050000000000000003 0.13
		-3.9319151706849776e-18 0.035000000000000003 0.12598075
		-1.4894484118070974e-19 0.024019250000000002 0.115
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		6.5123933065702293e-18 0.024019250000000002 0.085000000000000006
		7.6058555681270368e-18 0.035000000000000003 0.074019250000000009
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		3.9319151706849776e-18 0.065000000000000002 0.074019250000000009
		1.4894484118070974e-19 0.07598075 0.085000000000000006
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-6.5123933065702293e-18 0.07598075 0.115
		-7.6058555681270368e-18 0.065000000000000002 0.12598075
		-6.661338147750939e-18 0.050000000000000003 0.13
		-0.021213210000000003 0.050000000000000003 0.12121321
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		;
createNode transform -n "L_lipSecondary00Gimbal_CTL" -p "L_lipSecondary00_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCF7";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape10" -p "L_lipSecondary00Gimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCF6";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.027
		0 0.0135 0.023382675000000002
		0 0.023382675000000002 0.0135
		0 0.027 0
		0 0.023382675000000002 -0.0135
		0 0.0135 -0.023382675000000002
		0 0 -0.027
		0 -0.0135 -0.023382675000000002
		0 -0.023382675000000002 -0.0135
		0 -0.027 0
		0 -0.023382675000000002 0.0135
		0 -0.0135 0.023382675000000002
		0 0 0.027
		0.019091889000000001 0 0.019091889000000001
		0.027 0 0
		0.019091889000000001 0 -0.019091889000000001
		0 0 -0.027
		-0.019091889000000001 0 -0.019091889000000001
		-0.027 0 0
		-0.023382675000000002 0.0135 0
		-0.0135 0.023382675000000002 0
		0 0.027 0
		0.0135 0.023382675000000002 0
		0.023382675000000002 0.0135 0
		0.027 0 0
		0.023382675000000002 -0.0135 0
		0.0135 -0.023382675000000002 0
		0 -0.027 0
		-0.0135 -0.023382675000000002 0
		-0.023382675000000002 -0.0135 0
		-0.027 0 0
		-0.019091889000000001 0 0.019091889000000001
		0 0 0.027
		;
createNode transform -n "L_lipSecondary01_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCFD";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "L_lipSecondary01_LOC" -p "L_lipSecondary01_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCFE";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "L_lipSecondary01_LOCShape" -p "L_lipSecondary01_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCFF";
	setAttr -k off ".v" no;
createNode transform -n "L_lipSecondary01Buffer2_GRP" -p "L_lipSecondary01_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD00";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr ".t" -type "double3" 0 -3.2782544678866543e-08 0 ;
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "L_lipSecondary01Buffer1_GRP" -p "L_lipSecondary01Buffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD01";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "L_lipSecondary01_CTL" -p "L_lipSecondary01Buffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD04";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape11" -p "L_lipSecondary01_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD02";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.025980749999999997 0.035000000000000003 0.10000000000000001
		-0.014999999999999996 0.024019249999999999 0.10000000000000001
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		0.015000000000000003 0.024019250000000006 0.10000000000000001
		0.025980750000000004 0.035000000000000003 0.10000000000000001
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.025980749999999997 0.065000000000000002 0.10000000000000001
		0.014999999999999996 0.075980750000000014 0.10000000000000001
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-0.015000000000000003 0.07598075 0.10000000000000001
		-0.025980750000000004 0.065000000000000002 0.10000000000000001
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.021213209999999996 0.050000000000000003 0.078786789999999995
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		0.021213210000000003 0.050000000000000003 0.078786790000000009
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.021213209999999996 0.050000000000000003 0.12121321000000002
		-6.661338147750939e-18 0.050000000000000003 0.13
		-3.9319151706849776e-18 0.035000000000000003 0.12598075
		-1.4894484118070974e-19 0.024019250000000002 0.115
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		6.5123933065702293e-18 0.024019250000000002 0.085000000000000006
		7.6058555681270368e-18 0.035000000000000003 0.074019250000000009
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		3.9319151706849776e-18 0.065000000000000002 0.074019250000000009
		1.4894484118070974e-19 0.07598075 0.085000000000000006
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-6.5123933065702293e-18 0.07598075 0.115
		-7.6058555681270368e-18 0.065000000000000002 0.12598075
		-6.661338147750939e-18 0.050000000000000003 0.13
		-0.021213210000000003 0.050000000000000003 0.12121321
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		;
createNode transform -n "L_lipSecondary01Gimbal_CTL" -p "L_lipSecondary01_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD06";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape12" -p "L_lipSecondary01Gimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD05";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.027
		0 0.0135 0.023382675000000002
		0 0.023382675000000002 0.0135
		0 0.027 0
		0 0.023382675000000002 -0.0135
		0 0.0135 -0.023382675000000002
		0 0 -0.027
		0 -0.0135 -0.023382675000000002
		0 -0.023382675000000002 -0.0135
		0 -0.027 0
		0 -0.023382675000000002 0.0135
		0 -0.0135 0.023382675000000002
		0 0 0.027
		0.019091889000000001 0 0.019091889000000001
		0.027 0 0
		0.019091889000000001 0 -0.019091889000000001
		0 0 -0.027
		-0.019091889000000001 0 -0.019091889000000001
		-0.027 0 0
		-0.023382675000000002 0.0135 0
		-0.0135 0.023382675000000002 0
		0 0.027 0
		0.0135 0.023382675000000002 0
		0.023382675000000002 0.0135 0
		0.027 0 0
		0.023382675000000002 -0.0135 0
		0.0135 -0.023382675000000002 0
		0 -0.027 0
		-0.0135 -0.023382675000000002 0
		-0.023382675000000002 -0.0135 0
		-0.027 0 0
		-0.019091889000000001 0 0.019091889000000001
		0 0 0.027
		;
createNode transform -n "L_lipSecondary02_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD0C";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "L_lipSecondary02_LOC" -p "L_lipSecondary02_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD0D";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "L_lipSecondary02_LOCShape" -p "L_lipSecondary02_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD0E";
	setAttr -k off ".v" no;
createNode transform -n "L_lipSecondary02Buffer2_GRP" -p "L_lipSecondary02_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD0F";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr ".t" -type "double3" -2.9802320611338473e-08 -2.4076207694179175e-09 0 ;
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "L_lipSecondary02Buffer1_GRP" -p "L_lipSecondary02Buffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD10";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "L_lipSecondary02_CTL" -p "L_lipSecondary02Buffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD13";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape13" -p "L_lipSecondary02_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD11";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.025980749999999997 0.035000000000000003 0.10000000000000001
		-0.014999999999999996 0.024019249999999999 0.10000000000000001
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		0.015000000000000003 0.024019250000000006 0.10000000000000001
		0.025980750000000004 0.035000000000000003 0.10000000000000001
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.025980749999999997 0.065000000000000002 0.10000000000000001
		0.014999999999999996 0.075980750000000014 0.10000000000000001
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-0.015000000000000003 0.07598075 0.10000000000000001
		-0.025980750000000004 0.065000000000000002 0.10000000000000001
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.021213209999999996 0.050000000000000003 0.078786789999999995
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		0.021213210000000003 0.050000000000000003 0.078786790000000009
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.021213209999999996 0.050000000000000003 0.12121321000000002
		-6.661338147750939e-18 0.050000000000000003 0.13
		-3.9319151706849776e-18 0.035000000000000003 0.12598075
		-1.4894484118070974e-19 0.024019250000000002 0.115
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		6.5123933065702293e-18 0.024019250000000002 0.085000000000000006
		7.6058555681270368e-18 0.035000000000000003 0.074019250000000009
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		3.9319151706849776e-18 0.065000000000000002 0.074019250000000009
		1.4894484118070974e-19 0.07598075 0.085000000000000006
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-6.5123933065702293e-18 0.07598075 0.115
		-7.6058555681270368e-18 0.065000000000000002 0.12598075
		-6.661338147750939e-18 0.050000000000000003 0.13
		-0.021213210000000003 0.050000000000000003 0.12121321
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		;
createNode transform -n "L_lipSecondary02Gimbal_CTL" -p "L_lipSecondary02_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD15";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape14" -p "L_lipSecondary02Gimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD14";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.027
		0 0.0135 0.023382675000000002
		0 0.023382675000000002 0.0135
		0 0.027 0
		0 0.023382675000000002 -0.0135
		0 0.0135 -0.023382675000000002
		0 0 -0.027
		0 -0.0135 -0.023382675000000002
		0 -0.023382675000000002 -0.0135
		0 -0.027 0
		0 -0.023382675000000002 0.0135
		0 -0.0135 0.023382675000000002
		0 0 0.027
		0.019091889000000001 0 0.019091889000000001
		0.027 0 0
		0.019091889000000001 0 -0.019091889000000001
		0 0 -0.027
		-0.019091889000000001 0 -0.019091889000000001
		-0.027 0 0
		-0.023382675000000002 0.0135 0
		-0.0135 0.023382675000000002 0
		0 0.027 0
		0.0135 0.023382675000000002 0
		0.023382675000000002 0.0135 0
		0.027 0 0
		0.023382675000000002 -0.0135 0
		0.0135 -0.023382675000000002 0
		0 -0.027 0
		-0.0135 -0.023382675000000002 0
		-0.023382675000000002 -0.0135 0
		-0.027 0 0
		-0.019091889000000001 0 0.019091889000000001
		0 0 0.027
		;
createNode transform -n "L_lipSecondary03_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD1B";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "L_lipSecondary03_LOC" -p "L_lipSecondary03_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD1C";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "L_lipSecondary03_LOCShape" -p "L_lipSecondary03_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD1D";
	setAttr -k off ".v" no;
createNode transform -n "L_lipSecondary03Buffer2_GRP" -p "L_lipSecondary03_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD1E";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "L_lipSecondary03Buffer1_GRP" -p "L_lipSecondary03Buffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD1F";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "L_lipSecondary03_CTL" -p "L_lipSecondary03Buffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD22";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape15" -p "L_lipSecondary03_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD20";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.025980749999999997 0.035000000000000003 0.10000000000000001
		-0.014999999999999996 0.024019249999999999 0.10000000000000001
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		0.015000000000000003 0.024019250000000006 0.10000000000000001
		0.025980750000000004 0.035000000000000003 0.10000000000000001
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.025980749999999997 0.065000000000000002 0.10000000000000001
		0.014999999999999996 0.075980750000000014 0.10000000000000001
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-0.015000000000000003 0.07598075 0.10000000000000001
		-0.025980750000000004 0.065000000000000002 0.10000000000000001
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.021213209999999996 0.050000000000000003 0.078786789999999995
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		0.021213210000000003 0.050000000000000003 0.078786790000000009
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.021213209999999996 0.050000000000000003 0.12121321000000002
		-6.661338147750939e-18 0.050000000000000003 0.13
		-3.9319151706849776e-18 0.035000000000000003 0.12598075
		-1.4894484118070974e-19 0.024019250000000002 0.115
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		6.5123933065702293e-18 0.024019250000000002 0.085000000000000006
		7.6058555681270368e-18 0.035000000000000003 0.074019250000000009
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		3.9319151706849776e-18 0.065000000000000002 0.074019250000000009
		1.4894484118070974e-19 0.07598075 0.085000000000000006
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-6.5123933065702293e-18 0.07598075 0.115
		-7.6058555681270368e-18 0.065000000000000002 0.12598075
		-6.661338147750939e-18 0.050000000000000003 0.13
		-0.021213210000000003 0.050000000000000003 0.12121321
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		;
createNode transform -n "L_lipSecondary03Gimbal_CTL" -p "L_lipSecondary03_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD24";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape16" -p "L_lipSecondary03Gimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD23";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.027
		0 0.0135 0.023382675000000002
		0 0.023382675000000002 0.0135
		0 0.027 0
		0 0.023382675000000002 -0.0135
		0 0.0135 -0.023382675000000002
		0 0 -0.027
		0 -0.0135 -0.023382675000000002
		0 -0.023382675000000002 -0.0135
		0 -0.027 0
		0 -0.023382675000000002 0.0135
		0 -0.0135 0.023382675000000002
		0 0 0.027
		0.019091889000000001 0 0.019091889000000001
		0.027 0 0
		0.019091889000000001 0 -0.019091889000000001
		0 0 -0.027
		-0.019091889000000001 0 -0.019091889000000001
		-0.027 0 0
		-0.023382675000000002 0.0135 0
		-0.0135 0.023382675000000002 0
		0 0.027 0
		0.0135 0.023382675000000002 0
		0.023382675000000002 0.0135 0
		0.027 0 0
		0.023382675000000002 -0.0135 0
		0.0135 -0.023382675000000002 0
		0 -0.027 0
		-0.0135 -0.023382675000000002 0
		-0.023382675000000002 -0.0135 0
		-0.027 0 0
		-0.019091889000000001 0 0.019091889000000001
		0 0 0.027
		;
createNode transform -n "L_lipSecondary04_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD2A";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "L_lipSecondary04_LOC" -p "L_lipSecondary04_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD2B";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "L_lipSecondary04_LOCShape" -p "L_lipSecondary04_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD2C";
	setAttr -k off ".v" no;
createNode transform -n "L_lipSecondary04Buffer2_GRP" -p "L_lipSecondary04_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD2D";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "L_lipSecondary04Buffer1_GRP" -p "L_lipSecondary04Buffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD2E";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "L_lipSecondary04_CTL" -p "L_lipSecondary04Buffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD31";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape17" -p "L_lipSecondary04_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD2F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.025980749999999997 0.035000000000000003 0.10000000000000001
		-0.014999999999999996 0.024019249999999999 0.10000000000000001
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		0.015000000000000003 0.024019250000000006 0.10000000000000001
		0.025980750000000004 0.035000000000000003 0.10000000000000001
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.025980749999999997 0.065000000000000002 0.10000000000000001
		0.014999999999999996 0.075980750000000014 0.10000000000000001
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-0.015000000000000003 0.07598075 0.10000000000000001
		-0.025980750000000004 0.065000000000000002 0.10000000000000001
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.021213209999999996 0.050000000000000003 0.078786789999999995
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		0.021213210000000003 0.050000000000000003 0.078786790000000009
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.021213209999999996 0.050000000000000003 0.12121321000000002
		-6.661338147750939e-18 0.050000000000000003 0.13
		-3.9319151706849776e-18 0.035000000000000003 0.12598075
		-1.4894484118070974e-19 0.024019250000000002 0.115
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		6.5123933065702293e-18 0.024019250000000002 0.085000000000000006
		7.6058555681270368e-18 0.035000000000000003 0.074019250000000009
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		3.9319151706849776e-18 0.065000000000000002 0.074019250000000009
		1.4894484118070974e-19 0.07598075 0.085000000000000006
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-6.5123933065702293e-18 0.07598075 0.115
		-7.6058555681270368e-18 0.065000000000000002 0.12598075
		-6.661338147750939e-18 0.050000000000000003 0.13
		-0.021213210000000003 0.050000000000000003 0.12121321
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		;
createNode transform -n "L_lipSecondary04Gimbal_CTL" -p "L_lipSecondary04_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD33";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape18" -p "L_lipSecondary04Gimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD32";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 0 0 1 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.027
		0 0.0135 0.023382675000000002
		0 0.023382675000000002 0.0135
		0 0.027 0
		0 0.023382675000000002 -0.0135
		0 0.0135 -0.023382675000000002
		0 0 -0.027
		0 -0.0135 -0.023382675000000002
		0 -0.023382675000000002 -0.0135
		0 -0.027 0
		0 -0.023382675000000002 0.0135
		0 -0.0135 0.023382675000000002
		0 0 0.027
		0.019091889000000001 0 0.019091889000000001
		0.027 0 0
		0.019091889000000001 0 -0.019091889000000001
		0 0 -0.027
		-0.019091889000000001 0 -0.019091889000000001
		-0.027 0 0
		-0.023382675000000002 0.0135 0
		-0.0135 0.023382675000000002 0
		0 0.027 0
		0.0135 0.023382675000000002 0
		0.023382675000000002 0.0135 0
		0.027 0 0
		0.023382675000000002 -0.0135 0
		0.0135 -0.023382675000000002 0
		0 -0.027 0
		-0.0135 -0.023382675000000002 0
		-0.023382675000000002 -0.0135 0
		-0.027 0 0
		-0.019091889000000001 0 0.019091889000000001
		0 0 0.027
		;
createNode transform -n "C_lipSecondary_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD39";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "C_lipSecondary_LOC" -p "C_lipSecondary_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD3A";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "C_lipSecondary_LOCShape" -p "C_lipSecondary_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD3B";
	setAttr -k off ".v" no;
createNode transform -n "C_lipSecondaryBuffer2_GRP" -p "C_lipSecondary_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD3C";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "C_lipSecondaryBuffer1_GRP" -p "C_lipSecondaryBuffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD3D";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "C_lipSecondary_CTL" -p "C_lipSecondaryBuffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD40";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape19" -p "C_lipSecondary_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD3E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 1 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.025980749999999997 0.035000000000000003 0.10000000000000001
		-0.014999999999999996 0.024019249999999999 0.10000000000000001
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		0.015000000000000003 0.024019250000000006 0.10000000000000001
		0.025980750000000004 0.035000000000000003 0.10000000000000001
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.025980749999999997 0.065000000000000002 0.10000000000000001
		0.014999999999999996 0.075980750000000014 0.10000000000000001
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-0.015000000000000003 0.07598075 0.10000000000000001
		-0.025980750000000004 0.065000000000000002 0.10000000000000001
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.021213209999999996 0.050000000000000003 0.078786789999999995
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		0.021213210000000003 0.050000000000000003 0.078786790000000009
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.021213209999999996 0.050000000000000003 0.12121321000000002
		-6.661338147750939e-18 0.050000000000000003 0.13
		-3.9319151706849776e-18 0.035000000000000003 0.12598075
		-1.4894484118070974e-19 0.024019250000000002 0.115
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		6.5123933065702293e-18 0.024019250000000002 0.085000000000000006
		7.6058555681270368e-18 0.035000000000000003 0.074019250000000009
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		3.9319151706849776e-18 0.065000000000000002 0.074019250000000009
		1.4894484118070974e-19 0.07598075 0.085000000000000006
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-6.5123933065702293e-18 0.07598075 0.115
		-7.6058555681270368e-18 0.065000000000000002 0.12598075
		-6.661338147750939e-18 0.050000000000000003 0.13
		-0.021213210000000003 0.050000000000000003 0.12121321
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		;
createNode transform -n "C_lipSecondaryGimbal_CTL" -p "C_lipSecondary_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD42";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape20" -p "C_lipSecondaryGimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD41";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 1 1 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.027
		0 0.0135 0.023382675000000002
		0 0.023382675000000002 0.0135
		0 0.027 0
		0 0.023382675000000002 -0.0135
		0 0.0135 -0.023382675000000002
		0 0 -0.027
		0 -0.0135 -0.023382675000000002
		0 -0.023382675000000002 -0.0135
		0 -0.027 0
		0 -0.023382675000000002 0.0135
		0 -0.0135 0.023382675000000002
		0 0 0.027
		0.019091889000000001 0 0.019091889000000001
		0.027 0 0
		0.019091889000000001 0 -0.019091889000000001
		0 0 -0.027
		-0.019091889000000001 0 -0.019091889000000001
		-0.027 0 0
		-0.023382675000000002 0.0135 0
		-0.0135 0.023382675000000002 0
		0 0.027 0
		0.0135 0.023382675000000002 0
		0.023382675000000002 0.0135 0
		0.027 0 0
		0.023382675000000002 -0.0135 0
		0.0135 -0.023382675000000002 0
		0 -0.027 0
		-0.0135 -0.023382675000000002 0
		-0.023382675000000002 -0.0135 0
		-0.027 0 0
		-0.019091889000000001 0 0.019091889000000001
		0 0 0.027
		;
createNode transform -n "R_lipSecondary04_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD48";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_lipSecondary04_LOC" -p "R_lipSecondary04_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD49";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "R_lipSecondary04_LOCShape" -p "R_lipSecondary04_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD4A";
	setAttr -k off ".v" no;
createNode transform -n "R_lipSecondary04Buffer2_GRP" -p "R_lipSecondary04_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD4B";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_lipSecondary04Buffer1_GRP" -p "R_lipSecondary04Buffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD4C";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "R_lipSecondary04_CTL" -p "R_lipSecondary04Buffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD4F";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape21" -p "R_lipSecondary04_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD4D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.025980749999999997 0.035000000000000003 0.10000000000000001
		-0.014999999999999996 0.024019249999999999 0.10000000000000001
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		0.015000000000000003 0.024019250000000006 0.10000000000000001
		0.025980750000000004 0.035000000000000003 0.10000000000000001
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.025980749999999997 0.065000000000000002 0.10000000000000001
		0.014999999999999996 0.075980750000000014 0.10000000000000001
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-0.015000000000000003 0.07598075 0.10000000000000001
		-0.025980750000000004 0.065000000000000002 0.10000000000000001
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.021213209999999996 0.050000000000000003 0.078786789999999995
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		0.021213210000000003 0.050000000000000003 0.078786790000000009
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.021213209999999996 0.050000000000000003 0.12121321000000002
		-6.661338147750939e-18 0.050000000000000003 0.13
		-3.9319151706849776e-18 0.035000000000000003 0.12598075
		-1.4894484118070974e-19 0.024019250000000002 0.115
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		6.5123933065702293e-18 0.024019250000000002 0.085000000000000006
		7.6058555681270368e-18 0.035000000000000003 0.074019250000000009
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		3.9319151706849776e-18 0.065000000000000002 0.074019250000000009
		1.4894484118070974e-19 0.07598075 0.085000000000000006
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-6.5123933065702293e-18 0.07598075 0.115
		-7.6058555681270368e-18 0.065000000000000002 0.12598075
		-6.661338147750939e-18 0.050000000000000003 0.13
		-0.021213210000000003 0.050000000000000003 0.12121321
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		;
createNode transform -n "R_lipSecondary04Gimbal_CTL" -p "R_lipSecondary04_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD51";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape22" -p "R_lipSecondary04Gimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD50";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.027
		0 0.0135 0.023382675000000002
		0 0.023382675000000002 0.0135
		0 0.027 0
		0 0.023382675000000002 -0.0135
		0 0.0135 -0.023382675000000002
		0 0 -0.027
		0 -0.0135 -0.023382675000000002
		0 -0.023382675000000002 -0.0135
		0 -0.027 0
		0 -0.023382675000000002 0.0135
		0 -0.0135 0.023382675000000002
		0 0 0.027
		0.019091889000000001 0 0.019091889000000001
		0.027 0 0
		0.019091889000000001 0 -0.019091889000000001
		0 0 -0.027
		-0.019091889000000001 0 -0.019091889000000001
		-0.027 0 0
		-0.023382675000000002 0.0135 0
		-0.0135 0.023382675000000002 0
		0 0.027 0
		0.0135 0.023382675000000002 0
		0.023382675000000002 0.0135 0
		0.027 0 0
		0.023382675000000002 -0.0135 0
		0.0135 -0.023382675000000002 0
		0 -0.027 0
		-0.0135 -0.023382675000000002 0
		-0.023382675000000002 -0.0135 0
		-0.027 0 0
		-0.019091889000000001 0 0.019091889000000001
		0 0 0.027
		;
createNode transform -n "R_lipSecondary03_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD57";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_lipSecondary03_LOC" -p "R_lipSecondary03_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD58";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "R_lipSecondary03_LOCShape" -p "R_lipSecondary03_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD59";
	setAttr -k off ".v" no;
createNode transform -n "R_lipSecondary03Buffer2_GRP" -p "R_lipSecondary03_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD5A";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_lipSecondary03Buffer1_GRP" -p "R_lipSecondary03Buffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD5B";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "R_lipSecondary03_CTL" -p "R_lipSecondary03Buffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD5E";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape23" -p "R_lipSecondary03_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD5C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.025980749999999997 0.035000000000000003 0.10000000000000001
		-0.014999999999999996 0.024019249999999999 0.10000000000000001
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		0.015000000000000003 0.024019250000000006 0.10000000000000001
		0.025980750000000004 0.035000000000000003 0.10000000000000001
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.025980749999999997 0.065000000000000002 0.10000000000000001
		0.014999999999999996 0.075980750000000014 0.10000000000000001
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-0.015000000000000003 0.07598075 0.10000000000000001
		-0.025980750000000004 0.065000000000000002 0.10000000000000001
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.021213209999999996 0.050000000000000003 0.078786789999999995
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		0.021213210000000003 0.050000000000000003 0.078786790000000009
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.021213209999999996 0.050000000000000003 0.12121321000000002
		-6.661338147750939e-18 0.050000000000000003 0.13
		-3.9319151706849776e-18 0.035000000000000003 0.12598075
		-1.4894484118070974e-19 0.024019250000000002 0.115
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		6.5123933065702293e-18 0.024019250000000002 0.085000000000000006
		7.6058555681270368e-18 0.035000000000000003 0.074019250000000009
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		3.9319151706849776e-18 0.065000000000000002 0.074019250000000009
		1.4894484118070974e-19 0.07598075 0.085000000000000006
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-6.5123933065702293e-18 0.07598075 0.115
		-7.6058555681270368e-18 0.065000000000000002 0.12598075
		-6.661338147750939e-18 0.050000000000000003 0.13
		-0.021213210000000003 0.050000000000000003 0.12121321
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		;
createNode transform -n "R_lipSecondary03Gimbal_CTL" -p "R_lipSecondary03_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD60";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape24" -p "R_lipSecondary03Gimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD5F";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.027
		0 0.0135 0.023382675000000002
		0 0.023382675000000002 0.0135
		0 0.027 0
		0 0.023382675000000002 -0.0135
		0 0.0135 -0.023382675000000002
		0 0 -0.027
		0 -0.0135 -0.023382675000000002
		0 -0.023382675000000002 -0.0135
		0 -0.027 0
		0 -0.023382675000000002 0.0135
		0 -0.0135 0.023382675000000002
		0 0 0.027
		0.019091889000000001 0 0.019091889000000001
		0.027 0 0
		0.019091889000000001 0 -0.019091889000000001
		0 0 -0.027
		-0.019091889000000001 0 -0.019091889000000001
		-0.027 0 0
		-0.023382675000000002 0.0135 0
		-0.0135 0.023382675000000002 0
		0 0.027 0
		0.0135 0.023382675000000002 0
		0.023382675000000002 0.0135 0
		0.027 0 0
		0.023382675000000002 -0.0135 0
		0.0135 -0.023382675000000002 0
		0 -0.027 0
		-0.0135 -0.023382675000000002 0
		-0.023382675000000002 -0.0135 0
		-0.027 0 0
		-0.019091889000000001 0 0.019091889000000001
		0 0 0.027
		;
createNode transform -n "R_lipSecondary02_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD66";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_lipSecondary02_LOC" -p "R_lipSecondary02_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD67";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "R_lipSecondary02_LOCShape" -p "R_lipSecondary02_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD68";
	setAttr -k off ".v" no;
createNode transform -n "R_lipSecondary02Buffer2_GRP" -p "R_lipSecondary02_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD69";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr ".t" -type "double3" -1.4901162970204496e-08 -1.4632406841741386e-08 0 ;
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_lipSecondary02Buffer1_GRP" -p "R_lipSecondary02Buffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD6A";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "R_lipSecondary02_CTL" -p "R_lipSecondary02Buffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD6D";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape25" -p "R_lipSecondary02_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD6B";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.025980749999999997 0.035000000000000003 0.10000000000000001
		-0.014999999999999996 0.024019249999999999 0.10000000000000001
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		0.015000000000000003 0.024019250000000006 0.10000000000000001
		0.025980750000000004 0.035000000000000003 0.10000000000000001
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.025980749999999997 0.065000000000000002 0.10000000000000001
		0.014999999999999996 0.075980750000000014 0.10000000000000001
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-0.015000000000000003 0.07598075 0.10000000000000001
		-0.025980750000000004 0.065000000000000002 0.10000000000000001
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.021213209999999996 0.050000000000000003 0.078786789999999995
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		0.021213210000000003 0.050000000000000003 0.078786790000000009
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.021213209999999996 0.050000000000000003 0.12121321000000002
		-6.661338147750939e-18 0.050000000000000003 0.13
		-3.9319151706849776e-18 0.035000000000000003 0.12598075
		-1.4894484118070974e-19 0.024019250000000002 0.115
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		6.5123933065702293e-18 0.024019250000000002 0.085000000000000006
		7.6058555681270368e-18 0.035000000000000003 0.074019250000000009
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		3.9319151706849776e-18 0.065000000000000002 0.074019250000000009
		1.4894484118070974e-19 0.07598075 0.085000000000000006
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-6.5123933065702293e-18 0.07598075 0.115
		-7.6058555681270368e-18 0.065000000000000002 0.12598075
		-6.661338147750939e-18 0.050000000000000003 0.13
		-0.021213210000000003 0.050000000000000003 0.12121321
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		;
createNode transform -n "R_lipSecondary02Gimbal_CTL" -p "R_lipSecondary02_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD6F";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape26" -p "R_lipSecondary02Gimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD6E";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.027
		0 0.0135 0.023382675000000002
		0 0.023382675000000002 0.0135
		0 0.027 0
		0 0.023382675000000002 -0.0135
		0 0.0135 -0.023382675000000002
		0 0 -0.027
		0 -0.0135 -0.023382675000000002
		0 -0.023382675000000002 -0.0135
		0 -0.027 0
		0 -0.023382675000000002 0.0135
		0 -0.0135 0.023382675000000002
		0 0 0.027
		0.019091889000000001 0 0.019091889000000001
		0.027 0 0
		0.019091889000000001 0 -0.019091889000000001
		0 0 -0.027
		-0.019091889000000001 0 -0.019091889000000001
		-0.027 0 0
		-0.023382675000000002 0.0135 0
		-0.0135 0.023382675000000002 0
		0 0.027 0
		0.0135 0.023382675000000002 0
		0.023382675000000002 0.0135 0
		0.027 0 0
		0.023382675000000002 -0.0135 0
		0.0135 -0.023382675000000002 0
		0 -0.027 0
		-0.0135 -0.023382675000000002 0
		-0.023382675000000002 -0.0135 0
		-0.027 0 0
		-0.019091889000000001 0 0.019091889000000001
		0 0 0.027
		;
createNode transform -n "R_lipSecondary01_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD75";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_lipSecondary01_LOC" -p "R_lipSecondary01_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD76";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "R_lipSecondary01_LOCShape" -p "R_lipSecondary01_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD77";
	setAttr -k off ".v" no;
createNode transform -n "R_lipSecondary01Buffer2_GRP" -p "R_lipSecondary01_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD78";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr ".t" -type "double3" -9.9341086468029971e-09 1.1140059985592643e-08 0 ;
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_lipSecondary01Buffer1_GRP" -p "R_lipSecondary01Buffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD79";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "R_lipSecondary01_CTL" -p "R_lipSecondary01Buffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD7C";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape27" -p "R_lipSecondary01_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD7A";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.025980749999999997 0.035000000000000003 0.10000000000000001
		-0.014999999999999996 0.024019249999999999 0.10000000000000001
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		0.015000000000000003 0.024019250000000006 0.10000000000000001
		0.025980750000000004 0.035000000000000003 0.10000000000000001
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.025980749999999997 0.065000000000000002 0.10000000000000001
		0.014999999999999996 0.075980750000000014 0.10000000000000001
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-0.015000000000000003 0.07598075 0.10000000000000001
		-0.025980750000000004 0.065000000000000002 0.10000000000000001
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.021213209999999996 0.050000000000000003 0.078786789999999995
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		0.021213210000000003 0.050000000000000003 0.078786790000000009
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.021213209999999996 0.050000000000000003 0.12121321000000002
		-6.661338147750939e-18 0.050000000000000003 0.13
		-3.9319151706849776e-18 0.035000000000000003 0.12598075
		-1.4894484118070974e-19 0.024019250000000002 0.115
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		6.5123933065702293e-18 0.024019250000000002 0.085000000000000006
		7.6058555681270368e-18 0.035000000000000003 0.074019250000000009
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		3.9319151706849776e-18 0.065000000000000002 0.074019250000000009
		1.4894484118070974e-19 0.07598075 0.085000000000000006
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-6.5123933065702293e-18 0.07598075 0.115
		-7.6058555681270368e-18 0.065000000000000002 0.12598075
		-6.661338147750939e-18 0.050000000000000003 0.13
		-0.021213210000000003 0.050000000000000003 0.12121321
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		;
createNode transform -n "R_lipSecondary01Gimbal_CTL" -p "R_lipSecondary01_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD7E";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape28" -p "R_lipSecondary01Gimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD7D";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.027
		0 0.0135 0.023382675000000002
		0 0.023382675000000002 0.0135
		0 0.027 0
		0 0.023382675000000002 -0.0135
		0 0.0135 -0.023382675000000002
		0 0 -0.027
		0 -0.0135 -0.023382675000000002
		0 -0.023382675000000002 -0.0135
		0 -0.027 0
		0 -0.023382675000000002 0.0135
		0 -0.0135 0.023382675000000002
		0 0 0.027
		0.019091889000000001 0 0.019091889000000001
		0.027 0 0
		0.019091889000000001 0 -0.019091889000000001
		0 0 -0.027
		-0.019091889000000001 0 -0.019091889000000001
		-0.027 0 0
		-0.023382675000000002 0.0135 0
		-0.0135 0.023382675000000002 0
		0 0.027 0
		0.0135 0.023382675000000002 0
		0.023382675000000002 0.0135 0
		0.027 0 0
		0.023382675000000002 -0.0135 0
		0.0135 -0.023382675000000002 0
		0 -0.027 0
		-0.0135 -0.023382675000000002 0
		-0.023382675000000002 -0.0135 0
		-0.027 0 0
		-0.019091889000000001 0 0.019091889000000001
		0 0 0.027
		;
createNode transform -n "R_lipSecondary00_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD84";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_lipSecondary00_LOC" -p "R_lipSecondary00_CPT";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD85";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "R_lipSecondary00_LOCShape" -p "R_lipSecondary00_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD86";
	setAttr -k off ".v" no;
createNode transform -n "R_lipSecondary00Buffer2_GRP" -p "R_lipSecondary00_LOC";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD87";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "geoConstraint" -ln "geoConstraint" -at "message";
	setAttr ".t" -type "double3" 1.1920930020892229e-08 8.4740863215415629e-09 0 ;
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_lipSecondary00Buffer1_GRP" -p "R_lipSecondary00Buffer2_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD88";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "R_lipSecondary00_CTL" -p "R_lipSecondary00Buffer1_GRP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD8B";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape29" -p "R_lipSecondary00_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD89";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.025980749999999997 0.035000000000000003 0.10000000000000001
		-0.014999999999999996 0.024019249999999999 0.10000000000000001
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		0.015000000000000003 0.024019250000000006 0.10000000000000001
		0.025980750000000004 0.035000000000000003 0.10000000000000001
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.025980749999999997 0.065000000000000002 0.10000000000000001
		0.014999999999999996 0.075980750000000014 0.10000000000000001
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-0.015000000000000003 0.07598075 0.10000000000000001
		-0.025980750000000004 0.065000000000000002 0.10000000000000001
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		-0.021213209999999996 0.050000000000000003 0.078786789999999995
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		0.021213210000000003 0.050000000000000003 0.078786790000000009
		0.029999999999999999 0.05000000000000001 0.10000000000000001
		0.021213209999999996 0.050000000000000003 0.12121321000000002
		-6.661338147750939e-18 0.050000000000000003 0.13
		-3.9319151706849776e-18 0.035000000000000003 0.12598075
		-1.4894484118070974e-19 0.024019250000000002 0.115
		3.6739403974420592e-18 0.020000000000000004 0.10000000000000001
		6.5123933065702293e-18 0.024019250000000002 0.085000000000000006
		7.6058555681270368e-18 0.035000000000000003 0.074019250000000009
		6.661338147750939e-18 0.050000000000000003 0.070000000000000007
		3.9319151706849776e-18 0.065000000000000002 0.074019250000000009
		1.4894484118070974e-19 0.07598075 0.085000000000000006
		-3.6739403974420592e-18 0.080000000000000002 0.10000000000000001
		-6.5123933065702293e-18 0.07598075 0.115
		-7.6058555681270368e-18 0.065000000000000002 0.12598075
		-6.661338147750939e-18 0.050000000000000003 0.13
		-0.021213210000000003 0.050000000000000003 0.12121321
		-0.029999999999999999 0.049999999999999996 0.10000000000000001
		;
createNode transform -n "R_lipSecondary00Gimbal_CTL" -p "R_lipSecondary00_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD8D";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape30" -p "R_lipSecondary00Gimbal_CTL";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD8C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovrgbf" yes;
	setAttr ".ovc" 19;
	setAttr ".ovrgb" -type "float3" 1 0 0 ;
	setAttr ".cc" -type "nurbsCurve" 
		1 32 0 no 3
		33 0 1 2 3 4 5 6 7 8 9 10
		 11 12 13 14 15 16 17 18 19 20 21 22
		 23 24 25 26 27 28 29 30 31 32
		33
		0 0 0.027
		0 0.0135 0.023382675000000002
		0 0.023382675000000002 0.0135
		0 0.027 0
		0 0.023382675000000002 -0.0135
		0 0.0135 -0.023382675000000002
		0 0 -0.027
		0 -0.0135 -0.023382675000000002
		0 -0.023382675000000002 -0.0135
		0 -0.027 0
		0 -0.023382675000000002 0.0135
		0 -0.0135 0.023382675000000002
		0 0 0.027
		0.019091889000000001 0 0.019091889000000001
		0.027 0 0
		0.019091889000000001 0 -0.019091889000000001
		0 0 -0.027
		-0.019091889000000001 0 -0.019091889000000001
		-0.027 0 0
		-0.023382675000000002 0.0135 0
		-0.0135 0.023382675000000002 0
		0 0.027 0
		0.0135 0.023382675000000002 0
		0.023382675000000002 0.0135 0
		0.027 0 0
		0.023382675000000002 -0.0135 0
		0.0135 -0.023382675000000002 0
		0 -0.027 0
		-0.0135 -0.023382675000000002 0
		-0.023382675000000002 -0.0135 0
		-0.027 0 0
		-0.019091889000000001 0 0.019091889000000001
		0 0 0.027
		;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "3A48D100-0000-2490-5C81-EBD30011DC53";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode assetResolverConfig -n "assetResolverConfig";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C927";
createNode glimpseGlobals -s -n "glimpseGlobals";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C928";
	addAttr -ci true -sn "filesystemresolver" -ln "filesystemresolver" -at "compound" 
		-nc 2;
	addAttr -ci true -sn "filesystemresolver_active" -ln "filesystemresolver_active" 
		-dv 1 -at "long" -p "filesystemresolver";
	addAttr -ci true -sn "filesystemresolver_order" -ln "filesystemresolver_order" -dv 
		10 -at "long" -p "filesystemresolver";
	addAttr -ci true -sn "lookuptablerecorder" -ln "lookuptablerecorder" -at "compound" 
		-nc 4;
	addAttr -ci true -sn "lookuptablerecorder_active" -ln "lookuptablerecorder_active" 
		-dv 1 -at "long" -p "lookuptablerecorder";
	addAttr -ci true -sn "lookuptablerecorder_filepath" -ln "lookuptablerecorder_filepath" 
		-dt "string" -p "lookuptablerecorder";
	addAttr -ci true -sn "lookuptablerecorder_urionly" -ln "lookuptablerecorder_urionly" 
		-dv 1 -at "long" -p "lookuptablerecorder";
	addAttr -ci true -sn "lookuptablerecorder_order" -ln "lookuptablerecorder_order" 
		-dv 9 -at "long" -p "lookuptablerecorder";
	addAttr -ci true -sn "lookuptableresolver" -ln "lookuptableresolver" -at "compound" 
		-nc 5;
	addAttr -ci true -sn "lookuptableresolver_active" -ln "lookuptableresolver_active" 
		-dv 1 -at "long" -p "lookuptableresolver";
	addAttr -ci true -sn "lookuptableresolver_filepath" -ln "lookuptableresolver_filepath" 
		-dt "string" -p "lookuptableresolver";
	addAttr -ci true -sn "lookuptableresolver_urionly" -ln "lookuptableresolver_urionly" 
		-dv 1 -at "long" -p "lookuptableresolver";
	addAttr -ci true -sn "lookuptableresolver_order" -ln "lookuptableresolver_order" 
		-dv 19 -at "long" -p "lookuptableresolver";
	addAttr -ci true -sn "lookuptableresolver_cachefixedversionsonly" -ln "lookuptableresolver_cachefixedversionsonly" 
		-at "long" -p "lookuptableresolver";
	addAttr -ci true -sn "diagnosticrecorder" -ln "diagnosticrecorder" -at "compound" 
		-nc 2;
	addAttr -ci true -sn "diagnosticrecorder_active" -ln "diagnosticrecorder_active" 
		-dv 1 -at "long" -p "diagnosticrecorder";
	addAttr -ci true -sn "diagnosticrecorder_order" -ln "diagnosticrecorder_order" -dv 
		5 -at "long" -p "diagnosticrecorder";
	addAttr -ci true -sn "archiverecorder" -ln "archiverecorder" -at "compound" -nc 
		3;
	addAttr -ci true -sn "archiverecorder_active" -ln "archiverecorder_active" -at "long" 
		-p "archiverecorder";
	addAttr -ci true -sn "archiverecorder_basefolder" -ln "archiverecorder_basefolder" 
		-dt "string" -p "archiverecorder";
	addAttr -ci true -sn "archiverecorder_order" -ln "archiverecorder_order" -dv 10 
		-at "long" -p "archiverecorder";
	addAttr -ci true -sn "testresolver" -ln "testresolver" -at "compound" -nc 3;
	addAttr -ci true -sn "testresolver_active" -ln "testresolver_active" -at "long" 
		-p "testresolver";
	addAttr -ci true -sn "testresolver_prefix" -ln "testresolver_prefix" -dt "string" 
		-p "testresolver";
	addAttr -ci true -sn "testresolver_order" -ln "testresolver_order" -dv 1 -at "long" 
		-p "testresolver";
	addAttr -ci true -sn "arkuriresolver" -ln "arkuriresolver" -at "compound" -nc 8;
	addAttr -ci true -sn "arkuriresolver_active" -ln "arkuriresolver_active" -dv 1 -at "long" 
		-p "arkuriresolver";
	addAttr -ci true -sn "arkuriresolver_order" -ln "arkuriresolver_order" -dv 25 -at "long" 
		-p "arkuriresolver";
	addAttr -ci true -sn "arkuriresolver_fallbackToLatest" -ln "arkuriresolver_fallbackToLatest" 
		-dv 1 -at "long" -p "arkuriresolver";
	addAttr -ci true -sn "arkuriresolver_numRetries" -ln "arkuriresolver_numRetries" 
		-dv 3 -at "long" -p "arkuriresolver";
	addAttr -ci true -sn "arkuriresolver_connectTimeout" -ln "arkuriresolver_connectTimeout" 
		-at "long" -p "arkuriresolver";
	addAttr -ci true -sn "arkuriresolver_transferTimeout" -ln "arkuriresolver_transferTimeout" 
		-dv 1800 -at "long" -p "arkuriresolver";
	addAttr -ci true -sn "arkuriresolver_verbose" -ln "arkuriresolver_verbose" -at "long" 
		-p "arkuriresolver";
	addAttr -ci true -sn "arkuriresolver_cacheEnabled" -ln "arkuriresolver_cacheEnabled" 
		-dv 1 -at "long" -p "arkuriresolver";
	addAttr -ci true -sn "repositorypathresolver" -ln "repositorypathresolver" -at "compound" 
		-nc 2;
	addAttr -ci true -sn "repositorypathresolver_active" -ln "repositorypathresolver_active" 
		-dv 1 -at "long" -p "repositorypathresolver";
	addAttr -ci true -sn "repositorypathresolver_order" -ln "repositorypathresolver_order" 
		-dv 9 -at "long" -p "repositorypathresolver";
	setAttr ".acc" -type "string" "compact";
	setAttr ".spp" 128;
	setAttr ".var" 0.5;
	setAttr ".mb" 4;
	setAttr ".sho[0]"  0.5 1 1;
createNode ALF_globals -n "ALF_globals";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C929";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "3A48D100-0000-2490-5C81-EBD30011DC57";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "3A48D100-0000-2490-5C81-EBD30011DC58";
createNode displayLayerManager -n "layerManager";
	rename -uid "3A48D100-0000-2490-5C81-EBD30011DC59";
createNode displayLayer -n "defaultLayer";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C92D";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "3A48D100-0000-2490-5C81-EBD30011DC5B";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "94BF1100-0001-EA12-5C7F-214E0002C92F";
	setAttr ".g" yes;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "94BF1100-0001-EA12-5C7F-21630002C930";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"ALFShapeDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n"
		+ "            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n"
		+ "            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 0\n            -height 1003\n"
		+ "            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"ALFShapeDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n"
		+ "            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n"
		+ "            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n"
		+ "            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 790\n            -height 1003\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"ALFShapeDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n"
		+ "            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n"
		+ "            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n"
		+ "            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 789\n            -height 1003\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"ALFShapeDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 0\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n"
		+ "            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n"
		+ "            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n"
		+ "            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n"
		+ "            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n"
		+ "                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n"
		+ "                -alwaysToggleSelect 0\n                -directSelect 0\n                -isSet 0\n                -isSetMember 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                -selectionOrder \"display\" \n                -expandAttribute 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n"
		+ "                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -clipTime \"on\" \n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 0\n"
		+ "                -outliner \"graphEditor1OutlineEd\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n"
		+ "                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n"
		+ "                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n"
		+ "                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n"
		+ "                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n"
		+ "                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n"
		+ "                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n"
		+ "                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit 2\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -enableOpenGL 0\n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 0\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit 2\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -enableOpenGL 0\n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 0\n                -syncedSelection 1\n"
		+ "                -extendToShapes 1\n                -editorMode \"default\" \n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n"
		+ "                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n"
		+ "                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n"
		+ "                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n"
		+ "                -pluginObjects \"ALFShapeDisplayFilter\" 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"vertical2\\\" -ps 1 50 100 -ps 2 50 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Graph Editor\")) \n\t\t\t\t\t\"scriptedPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `scriptedPanel -unParent  -type \\\"graphEditor\\\" -l (localizedPanelLabel(\\\"Graph Editor\\\")) -mbv $menusOkayInPanels `;\\n\\n\\t\\t\\t$editorName = ($panelName+\\\"OutlineEd\\\");\\n            outlinerEditor -e \\n                -showShapes 1\\n                -showAssignedMaterials 0\\n                -showTimeEditor 1\\n                -showReferenceNodes 0\\n                -showReferenceMembers 0\\n                -showAttributes 1\\n                -showConnected 1\\n                -showAnimCurvesOnly 1\\n                -showMuteInfo 0\\n                -organizeByLayer 1\\n                -organizeByClip 1\\n                -showAnimLayerWeight 1\\n                -autoExpandLayers 1\\n                -autoExpand 1\\n                -showDagOnly 0\\n                -showAssets 1\\n                -showContainedOnly 0\\n                -showPublishedAsConnected 0\\n                -showParentContainers 1\\n                -showContainerContents 0\\n                -ignoreDagHierarchy 0\\n                -expandConnections 1\\n                -showUpstreamCurves 1\\n                -showUnitlessCurves 1\\n                -showCompounds 0\\n                -showLeafs 1\\n                -showNumericAttrsOnly 1\\n                -highlightActive 0\\n                -autoSelectNewObjects 1\\n                -doNotSelectNewObjects 0\\n                -dropIsParent 1\\n                -transmitFilters 1\\n                -setFilter \\\"0\\\" \\n                -showSetMembers 0\\n                -allowMultiSelection 1\\n                -alwaysToggleSelect 0\\n                -directSelect 0\\n                -isSet 0\\n                -isSetMember 0\\n                -displayMode \\\"DAG\\\" \\n                -expandObjects 0\\n                -setsIgnoreFilters 1\\n                -containersIgnoreFilters 0\\n                -editAttrName 0\\n                -showAttrValues 0\\n                -highlightSecondary 0\\n                -showUVAttrsOnly 0\\n                -showTextureNodesOnly 0\\n                -attrAlphaOrder \\\"default\\\" \\n                -animLayerFilterOptions \\\"allAffecting\\\" \\n                -sortOrder \\\"none\\\" \\n                -longNames 0\\n                -niceNames 1\\n                -showNamespace 1\\n                -showPinIcons 1\\n                -mapMotionTrails 1\\n                -ignoreHiddenAttribute 0\\n                -ignoreOutlinerColor 0\\n                -renderFilterVisible 0\\n                -selectionOrder \\\"display\\\" \\n                -expandAttribute 1\\n                $editorName;\\n\\n\\t\\t\\t$editorName = ($panelName+\\\"GraphEd\\\");\\n            animCurveEditor -e \\n                -displayKeys 1\\n                -displayTangents 0\\n                -displayActiveKeys 0\\n                -displayActiveKeyTangents 1\\n                -displayInfinities 0\\n                -displayValues 0\\n                -autoFit 1\\n                -autoFitTime 0\\n                -snapTime \\\"integer\\\" \\n                -snapValue \\\"none\\\" \\n                -showResults \\\"off\\\" \\n                -showBufferCurves \\\"off\\\" \\n                -smoothness \\\"fine\\\" \\n                -resultSamples 1\\n                -resultScreenSamples 0\\n                -resultUpdate \\\"delayed\\\" \\n                -showUpstreamCurves 1\\n                -showCurveNames 0\\n                -showActiveCurveNames 0\\n                -clipTime \\\"on\\\" \\n                -stackedCurves 0\\n                -stackedCurvesMin -1\\n                -stackedCurvesMax 1\\n                -stackedCurvesSpace 0.2\\n                -displayNormalized 0\\n                -preSelectionHighlight 0\\n                -constrainDrag 0\\n                -classicMode 1\\n                -valueLinesToggle 0\\n                -outliner \\\"graphEditor1OutlineEd\\\" \\n                $editorName\"\n"
		+ "\t\t\t\t\t\"scriptedPanel -edit -l (localizedPanelLabel(\\\"Graph Editor\\\")) -mbv $menusOkayInPanels  $panelName;\\n\\n\\t\\t\\t$editorName = ($panelName+\\\"OutlineEd\\\");\\n            outlinerEditor -e \\n                -showShapes 1\\n                -showAssignedMaterials 0\\n                -showTimeEditor 1\\n                -showReferenceNodes 0\\n                -showReferenceMembers 0\\n                -showAttributes 1\\n                -showConnected 1\\n                -showAnimCurvesOnly 1\\n                -showMuteInfo 0\\n                -organizeByLayer 1\\n                -organizeByClip 1\\n                -showAnimLayerWeight 1\\n                -autoExpandLayers 1\\n                -autoExpand 1\\n                -showDagOnly 0\\n                -showAssets 1\\n                -showContainedOnly 0\\n                -showPublishedAsConnected 0\\n                -showParentContainers 1\\n                -showContainerContents 0\\n                -ignoreDagHierarchy 0\\n                -expandConnections 1\\n                -showUpstreamCurves 1\\n                -showUnitlessCurves 1\\n                -showCompounds 0\\n                -showLeafs 1\\n                -showNumericAttrsOnly 1\\n                -highlightActive 0\\n                -autoSelectNewObjects 1\\n                -doNotSelectNewObjects 0\\n                -dropIsParent 1\\n                -transmitFilters 1\\n                -setFilter \\\"0\\\" \\n                -showSetMembers 0\\n                -allowMultiSelection 1\\n                -alwaysToggleSelect 0\\n                -directSelect 0\\n                -isSet 0\\n                -isSetMember 0\\n                -displayMode \\\"DAG\\\" \\n                -expandObjects 0\\n                -setsIgnoreFilters 1\\n                -containersIgnoreFilters 0\\n                -editAttrName 0\\n                -showAttrValues 0\\n                -highlightSecondary 0\\n                -showUVAttrsOnly 0\\n                -showTextureNodesOnly 0\\n                -attrAlphaOrder \\\"default\\\" \\n                -animLayerFilterOptions \\\"allAffecting\\\" \\n                -sortOrder \\\"none\\\" \\n                -longNames 0\\n                -niceNames 1\\n                -showNamespace 1\\n                -showPinIcons 1\\n                -mapMotionTrails 1\\n                -ignoreHiddenAttribute 0\\n                -ignoreOutlinerColor 0\\n                -renderFilterVisible 0\\n                -selectionOrder \\\"display\\\" \\n                -expandAttribute 1\\n                $editorName;\\n\\n\\t\\t\\t$editorName = ($panelName+\\\"GraphEd\\\");\\n            animCurveEditor -e \\n                -displayKeys 1\\n                -displayTangents 0\\n                -displayActiveKeys 0\\n                -displayActiveKeyTangents 1\\n                -displayInfinities 0\\n                -displayValues 0\\n                -autoFit 1\\n                -autoFitTime 0\\n                -snapTime \\\"integer\\\" \\n                -snapValue \\\"none\\\" \\n                -showResults \\\"off\\\" \\n                -showBufferCurves \\\"off\\\" \\n                -smoothness \\\"fine\\\" \\n                -resultSamples 1\\n                -resultScreenSamples 0\\n                -resultUpdate \\\"delayed\\\" \\n                -showUpstreamCurves 1\\n                -showCurveNames 0\\n                -showActiveCurveNames 0\\n                -clipTime \\\"on\\\" \\n                -stackedCurves 0\\n                -stackedCurvesMin -1\\n                -stackedCurvesMax 1\\n                -stackedCurvesSpace 0.2\\n                -displayNormalized 0\\n                -preSelectionHighlight 0\\n                -constrainDrag 0\\n                -classicMode 1\\n                -valueLinesToggle 0\\n                -outliner \\\"graphEditor1OutlineEd\\\" \\n                $editorName\"\n"
		+ "\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 789\\n    -height 1003\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"ALFShapeDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 789\\n    -height 1003\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"ALFShapeDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "94BF1100-0001-EA12-5C7F-21630002C931";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode polyPlane -n "polyPlane2";
	rename -uid "94BF1100-0001-EA12-5C7F-22890002CEED";
	setAttr ".ax" -type "double3" 0 0 1 ;
	setAttr ".w" 2;
	setAttr ".h" 2;
	setAttr ".sw" 100;
createNode polyPlane -n "polyPlane3";
	rename -uid "94BF1100-0001-EA12-5C7F-22890002CEF0";
	setAttr ".ax" -type "double3" 0 0 1 ;
	setAttr ".w" 2;
	setAttr ".h" 2;
createNode polyPlane -n "polyPlane5";
	rename -uid "94BF1100-0001-EA12-5C7F-22950002CF2A";
	setAttr ".ax" -type "double3" 0 0 1 ;
	setAttr ".w" 2;
	setAttr ".h" 2;
	setAttr ".sw" 100;
createNode polyPlane -n "polyPlane6";
	rename -uid "94BF1100-0001-EA12-5C7F-22950002CF2D";
	setAttr ".ax" -type "double3" 0 0 1 ;
	setAttr ".w" 2;
	setAttr ".h" 2;
createNode polyPlane -n "polyPlane8";
	rename -uid "94BF1100-0001-EA12-5C7F-237E0002D810";
	setAttr ".ax" -type "double3" 0 0 1 ;
	setAttr ".w" 2;
	setAttr ".h" 2;
	setAttr ".sw" 100;
createNode polyPlane -n "polyPlane9";
	rename -uid "94BF1100-0001-EA12-5C7F-237E0002D813";
	setAttr ".ax" -type "double3" 0 0 1 ;
	setAttr ".w" 2;
	setAttr ".h" 2;
createNode polyPlane -n "polyPlane11";
	rename -uid "3A48D100-0000-2490-5C81-B67F000636C8";
	setAttr ".ax" -type "double3" 0 0 1 ;
	setAttr ".w" 2;
	setAttr ".h" 2;
	setAttr ".sw" 50;
createNode polyPlane -n "polyPlane12";
	rename -uid "3A48D100-0000-2490-5C81-B67F000636CB";
	setAttr ".ax" -type "double3" 0 0 1 ;
	setAttr ".w" 2;
	setAttr ".h" 2;
createNode makeNurbCircle -n "makeNurbCircle1";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC67";
	setAttr ".nr" -type "double3" 0 1 0 ;
createNode polyPlane -n "polyPlane13";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC6A";
	setAttr ".ax" -type "double3" 0 0 1 ;
	setAttr ".w" 2;
	setAttr ".h" 2;
	setAttr ".sw" 30;
createNode cluster -n "cluster1";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC6D";
	setAttr -s 341 ".wl[0].w[0:340]"  0 0 0 -5.9374037e-19 -1.1713819e-18
		 -2.4027256e-18 -4.8084472e-18 -2.5080346e-17 0 0 0 0 0 -9.8575105e-18 -1.004905e-17
		 0 -1.0107525e-17 -9.9013288e-18 0 0 0 0 0 -2.1544336e-17 -3.9665138e-18 0 -5.2564143e-19
		 0 0 0 0 0 -9.6237483e-05 -0.00016394001 -0.00028465799 -0.0005615977 -0.001151943
		 -0.002305323 -0.0030060783 -0.002651107 -0.0032516725 -0.0041842372 -0.0046494277
		 -0.0047097611 -0.0047260029 -0.0048178332 -0.0048958259 -0.0048458683 -0.0047470108
		 -0.0046843002 -0.0045384304 -0.0039607962 -0.0029175319 -0.0022437011 -0.0025822597
		 -0.0019016725 -0.00078921037 -0.00025200914 -3.8279843e-05 1.0128656e-05 -3.6697336e-06
		 0 0 -0.00032572687 -0.00055487402 -0.00096345786 -0.0019007924 -0.0038988842 -0.0078026312
		 -0.010174419 -0.0089729773 -0.011005661 -0.014162035 -0.015736526 -0.015940731 -0.015995702
		 -0.016306512 -0.016570488 -0.016401397 -0.016066805 -0.015854554 -0.015360842 -0.013405772
		 -0.0098747239 -0.0075940657 -0.0087399548 -0.0064364304 -0.0026711738 -0.00085295399
		 -0.00012956254 3.4281606e-05 -1.2420637e-05 0 0 -0.00059963379 -0.0010214726 -0.0017736384
		 -0.0034991871 -0.0071774963 -0.014363935 -0.018730178 -0.016518436 -0.020260422 -0.026071019
		 -0.028969513 -0.029345436 -0.029446635 -0.030018806 -0.030504761 -0.030193482 -0.029577529
		 -0.029186793 -0.028277913 -0.02467881 -0.018178469 -0.013979985 -0.016089464 -0.011848883
		 -0.0049173879 -0.0015702109 -0.00023851165 6.3109321e-05 -2.2865264e-05 0 0 -0.00082912296
		 -0.0014124062 -0.0024524382 -0.0048383805 -0.0099244323 -0.019861244 -0.02589852
		 -0.022840306 -0.028014408 -0.036048815 -0.040056609 -0.040576406 -0.040716331 -0.041507486
		 -0.042179421 -0.041749012 -0.040897325 -0.040357046 -0.039100323 -0.034123782 -0.025135661
		 -0.019330349 -0.022247158 -0.01638364 -0.006799351 -0.0021711558 -0.00032979387 8.726227e-05
		 -3.1616168e-05 0 0 -0.00092536042 -0.0015763466 -0.002737096 -0.0053999801 -0.011076375
		 -0.022166569 -0.028904596 -0.025491413 -0.031266082 -0.04023305 -0.044706035 -0.045286164
		 -0.045442335 -0.046325319 -0.047075246 -0.046594881 -0.045644332 -0.045041345 -0.043638751
		 -0.038084578 -0.028053192 -0.02157405 -0.024829416 -0.018285312 -0.0075885612 -0.0024231649
		 -0.00036807542 9.7390919e-05 -3.5285902e-05 0 0 -0.00092536077 -0.0015763466 -0.002737096
		 -0.0053999801 -0.011076383 -0.022166569 -0.028904596 -0.025491413 -0.031266082 -0.04023305
		 -0.044706035 -0.045286164 -0.045442335 -0.046325319 -0.047075246 -0.046594881 -0.045644332
		 -0.045041345 -0.043638751 -0.038084578 -0.028053192 -0.02157405 -0.024829416 -0.018285312
		 -0.0075885612 -0.0024231649 -0.00036807352 9.7390919e-05 -3.5285902e-05 0 0 -0.00092536042
		 -0.0015763466 -0.002737096 -0.0053999801 -0.011076375 -0.022166569 -0.028904596 -0.025491413
		 -0.031266082 -0.04023305 -0.044706035 -0.045286164 -0.045442335 -0.046325319 -0.047075246
		 -0.046594881 -0.045644332 -0.045041345 -0.043638751 -0.038084578 -0.028053192 -0.02157405
		 -0.024829416 -0.018285312 -0.0075885612 -0.0024231649 -0.00036807542 9.7390919e-05
		 -3.5285902e-05 0 0 -0.00092536077 -0.0015763466 -0.002737096 -0.0053999801 -0.011076383
		 -0.022166569 -0.028904596 -0.025491413 -0.031266082 -0.04023305 -0.044706035 -0.045286164
		 -0.045442335 -0.046325319 -0.047075246 -0.046594881 -0.045644332 -0.045041345 -0.043638751
		 -0.038084578 -0.028053192 -0.02157405 -0.024829416 -0.018285312 -0.0075885612 -0.0024231649
		 -0.00036807542 9.7390919e-05 -3.5285902e-05 0 0 -0.00092536077 -0.0015763466 -0.002737096
		 -0.0053999801 -0.011076383 -0.022166569 -0.028904596 -0.025491413 -0.031266082 -0.04023305
		 -0.044706035 -0.045286164 -0.045442335 -0.046325319 -0.047075246 -0.046594881 -0.045644332
		 -0.045041345 -0.043638751 -0.038084578 -0.028053192 -0.02157405 -0.024829416 -0.018285312
		 -0.0075885612 -0.0024231649 -0.00036807352 9.7390919e-05 -3.5285902e-05 0 0 -0.00092536042
		 -0.0015763466 -0.002737096 -0.0053999801 -0.011076375 -0.022166569 -0.028904596 -0.025491413
		 -0.031266082 -0.04023305 -0.044706035 -0.045286164 -0.045442335 -0.046325319 -0.047075246
		 -0.046594881 -0.045644332 -0.045041345 -0.043638751 -0.038084578 -0.028053192 -0.02157405
		 -0.024829416 -0.018285312 -0.0075885612 -0.0024231649 -0.00036807542 9.7390919e-05
		 -3.5285902e-05 0;
	setAttr ".gm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
createNode tweak -n "tweak1";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC6F";
createNode objectSet -n "cluster1Set";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC70";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "cluster1GroupId";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC71";
	setAttr ".ihi" 0;
createNode groupParts -n "cluster1GroupParts";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC72";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode objectSet -n "tweakSet1";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC73";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId2";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC74";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts2";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC75";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode polyPlane -n "polyPlane14";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC78";
	setAttr ".ax" -type "double3" 0 0 1 ;
	setAttr ".w" 2;
	setAttr ".h" 2;
	setAttr ".sw" 30;
createNode polyPlane -n "polyPlane15";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC7B";
	setAttr ".ax" -type "double3" 0 0 1 ;
	setAttr ".w" 2;
	setAttr ".h" 2;
	setAttr ".sw" 3;
createNode cluster -n "cluster2";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC7E";
	setAttr -s 341 ".wl[0].w[0:340]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;
	setAttr ".gm[0]" -type "matrix" 1 0 0 0 0 1 0 0
		 0 0 1 0 0 0 0 1;
createNode objectSet -n "cluster2Set";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC7F";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "cluster2GroupId";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC80";
	setAttr ".ihi" 0;
createNode groupParts -n "cluster2GroupParts";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC81";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode LHCurveWeightNode -n "TestCurveWeights";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC84";
	setAttr -s 15 ".inputs[0:14]"  0.99076682 0.57475001 1 0.50000006 0
		 0.57475001 1 0.23333335 0.9499464 0.57475001 1 0.50000006 0.057097286 0.57475001
		 1 0.76666671 0 0.57475001 1 0.10000002 0 0.57475001 1 0.16666669 0 0.57475001 1 0.25000003
		 0 0.57475001 1 0.33333334 0 0.57475001 1 0.41666672 0.55546504 0.57475001 1 0.5 0.76631218
		 0.57475001 1 0.58333337 0 0.57475001 1 0 0 0.57475001 1 0 0 0.57475001 1 0 0 0.57475001
		 1 0;
	setAttr -s 15 ".inputs";
	setAttr -s 15 ".outDoubleweights";
	setAttr ".outDoubleweights[0].owd" -type "doubleArray" 341 0 0 0
		 8.3628550524725787e-17 1.057930786373083e-16 1.2567012327884413e-16 1.4340335235070486e-16 6.3637272792667576e-16 0 0 0 0 0 2.1336102031961342e-16 2.1603370238563854e-16
		 0 2.1603370102318263e-16 2.1336101031191402e-16 0 0 0 0 0 6.3637268294424962e-16 1.4340332253381765e-16 0 1.0579309470260846e-16
		 0 0 0 0 0 0.015046097401724906 0.028264987703849914 0.040094179347855682 0.05072055601013796 0.06025024064982365 0.068752110891200785 0.076274331138056303
		 0.082851893088285264 0.088510992522378443 0.093271385182387118 0.09714803411402459 0.10015217428019668 0.10229203245722272 0.10357340178166864 0.10400000000000001 0.1035734165170865 0.10229203071249328 0.10015216706609137 0.097148027973325959
		 0.09327138187904474 0.08851098322435004 0.082851886848922404 0.076274318557888354 0.068752095866099455 0.060250224567027999 0.050720557163741457 0.040094179347855675 0.028264971783095894 0.015046086672481491 0 0
		 0.050925254515818211 0.095666137110568095 0.13570338097494553 0.17166958015996725 0.20392389852399972 0.23269944622790617 0.25815927001573186 0.2804218017460518 0.29957567742005076 0.31568777621441207 0.3288087422856194 0.33897659278439563
		 0.34621919882209518 0.35055614130185664 0.35200001224489796 0.35055608736453703 0.34621918258268242 0.33897657724631947 0.32880872150171564 0.31568776503386831 0.29957564594979968 0.2804217806282075 0.25815920049522806 0.23269940948778273
		 0.20392384408992023 0.17166957365208774 0.1357033809749455 0.095666061670687003 0.050925218201454618 0 0 0.093748810616005429 0.17611266535634296 0.24981759317555641 0.31602812966471172 0.37540542413066053
		 0.42837853833668593 0.47524770788680903 0.51623105543026671 0.55149160005697495 0.58115250985079414 0.60530701610183824 0.62402510493001662 0.63735808451871889 0.64534199610471321 0.64800003673469342 0.64534190667205349 0.63735805462343575
		 0.62402507632583037 0.60530697784055998 0.58115248926842888 0.55149154212310247 0.51623101655423431 0.47524762950269356 0.4283784677578808 0.37540526666065066 0.31602812966471161 0.24981746849731459 0.17611252647837702 0.093748699196936403
		 0 0 0.12962791725741152 0.24351374243638568 0.34542677906709718 0.43697710191470152 0.51907900109692962 0.59232589256133261 0.65713264377098113 0.71380093157159197 0.76255625021720941 0.80356886427709517
		 0.83696768614626138 0.86284948675133633 0.88128521073758215 0.89232470040261769 0.89600000816326519 0.89232463036307186 0.88128519570606667 0.86284944719987078 0.83696763324178047 0.80356883581752991 0.76255617011111787 0.71380087781708068
		 0.65713249347905123 0.59232575439679513 0.51907886253745805 0.43697711828461561 0.34542660667249941 0.24351360527296517 0.12962782482085203 0 0 0.14467401347812409 0.27177878915529702 0.38552095526784308
		 0.48769770331679957 0.57932923701753503 0.6610780412284244 0.73340691503909083 0.79665281815658895 0.85106723579210031 0.89684024213833757 0.93411571263485171 0.96300165054698494 0.98357723516560303 0.99589809405450602 1
		 0.99589807939928332 0.9835771890309094 0.96300160640472465 0.93411565358967263 0.89684021037543016 0.85106714638798109 0.7966527581627153 0.73340679407595655 0.6610778448663408 0.57932908237526914 0.4876977033167994 0.38552095526784302
		 0.27177857483746048 0.14467391031232202 0 0 0.14467408225532002 0.27177878915529702 0.38552095526784308 0.48769770331679957 0.57932932538452986 0.6610780412284244 0.73340691503909083 0.79665281815658895
		 0.85106723579210031 0.89684024213833757 0.93411571263485171 0.96300167577112183 0.98357723516560303 0.99589809405450602 1 0.99589807939928332 0.9835771890309094 0.96300160640472465 0.93411565358967263 0.89684021037543016
		 0.85106714638798109 0.7966527581627153 0.73340679407595655 0.6610778448663408 0.57932908237526914 0.4876977033167994 0.38552076286315984 0.27177857483746048 0.14467391031232202 0 0 0.14467401347812409
		 0.27177878915529702 0.38552095526784308 0.48769770331679957 0.57932923701753503 0.6610780412284244 0.73340691503909083 0.79665281815658895 0.85106723579210031 0.89684024213833757 0.93411571263485171 0.96300165054698494 0.98357723516560303
		 0.99589809405450602 1 0.99589807939928332 0.9835771890309094 0.96300160640472465 0.93411565358967263 0.89684021037543016 0.85106714638798109 0.7966527581627153 0.73340679407595655 0.6610778448663408 0.57932908237526914
		 0.4876977033167994 0.38552095526784302 0.27177857483746048 0.14467391031232202 0 0 0.14467408225532002 0.27177878915529702 0.38552095526784308 0.48769770331679957 0.57932932538452986 0.6610780412284244
		 0.73340691503909083 0.79665281815658895 0.85106723579210031 0.89684024213833757 0.93411571263485171 0.96300165054698494 0.98357723516560303 0.99589809405450602 1 0.99589807939928332 0.9835771890309094 0.96300160640472465
		 0.93411565358967263 0.89684021037543016 0.85106714638798109 0.7966527581627153 0.73340679407595655 0.6610778448663408 0.57932908237526914 0.4876977033167994 0.38552095526784302 0.27177857483746048 0.14467391031232202 0
		 0 0.14467408225532002 0.27177878915529702 0.38552095526784308 0.48769770331679957 0.57932932538452986 0.6610780412284244 0.73340691503909083 0.79665281815658895 0.85106723579210031 0.89684024213833757 0.93411571263485171
		 0.96300167577112183 0.98357723516560303 0.99589809405450602 1 0.99589807939928332 0.9835771890309094 0.96300160640472465 0.93411565358967263 0.89684021037543016 0.85106714638798109 0.7966527581627153 0.73340679407595655
		 0.6610778448663408 0.57932908237526914 0.4876977033167994 0.38552076286315984 0.27177857483746048 0.14467391031232202 0 0 0.14467401347812409 0.27177878915529702 0.38552095526784308 0.48769770331679957
		 0.57932923701753503 0.6610780412284244 0.73340691503909083 0.79665281815658895 0.85106723579210031 0.89684024213833757 0.93411571263485171 0.96300167577112183 0.98357723516560303 0.99589809405450602 1 0.99589807939928332
		 0.9835771890309094 0.96300160640472465 0.93411565358967263 0.89684021037543016 0.85106714638798109 0.7966527581627153 0.73340679407595655 0.6610778448663408 0.57932908237526914 0.4876977033167994 0.38552095526784302 0.27177857483746048
		 0.14467391031232202 0 ;
	setAttr ".outDoubleweights[1].owd" -type "doubleArray" 341 0 0 0
		 1.2377138217106264e-16 1.5552607013865542e-16 1.8222292293103034e-16 2.0277739234044723e-16 8.6034073551840592e-16 0 0 0 0 0 2.2466633907946396e-17 5.3860201319931811e-18
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0.022294851522748429 0.041924258876533553 0.059339925880805729 0.074564128708322269 0.087363445027821132 0.097217904485294118 0.10311867129922958
		 0.10229814036942289 0.089485998120452451 0.068141158668668961 0.044911951948480133 0.025010314203056619 0.010771216042525332 0.0025822232933158632 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0.075459500086592579 0.1418975284548481 0.20084283304475917 0.25237090594576522 0.29569167038028371 0.32904520666958542 0.34901703509424825 0.34623987175641485 0.30287569648217477 0.23063162197839429 0.15200968880583918 0.084650356754342723
		 0.036456424796743825 0.0087398329890985057 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0.13891414896124482 0.26122045583149417 0.36973340529419318 0.46459194994440944 0.54434156878923989
		 0.60574232970781261 0.64250857980766529 0.63739614151227741 0.55756663528167205 0.42457185885040438 0.27983602415809528 0.15583361471094398 0.067112965300324359 0.016089271926821892 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0.19207872256135938 0.36119361822704715 0.51123628916932196 0.64239865318599521 0.75266968709710291 0.83756965860031762 0.8884069395556331 0.88133783275086297 0.77095629852330116 0.58706229541713206
		 0.38693374338909969 0.21547362984222096 0.092798169827221055 0.022246847037407567 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0.21437357233411949 0.40311796454178905 0.57057621039236273
		 0.7169628450725295 0.84003312526751084 0.93478761650205111 0.99152552991401077 0.98363596509060458 0.86044228961973501 0.65520344873720149 0.43184569181230892 0.24048395968648062 0.10356938502428203 0.024829070128037145 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0.21437367451588518 0.40311796454178905 0.57057621039236273 0.7169628450725295 0.8400332375476488 0.93478761650205111 0.99152552991401077 0.98363596509060458
		 0.86044228961973501 0.65520344873720149 0.43184569181230892 0.24048379041400592 0.10356938502428203 0.024829070128037145 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0.21437357233411949
		 0.40311796454178905 0.57057621039236273 0.7169628450725295 0.84003312526751084 0.93478761650205111 0.99152552991401077 0.98363596509060458 0.86044228961973501 0.65520344873720149 0.43184569181230892 0.24048395968648062 0.10356938502428203
		 0.024829070128037145 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0.21437367451588518 0.40311796454178905 0.57057621039236273 0.7169628450725295 0.8400332375476488 0.93478761650205111
		 0.99152552991401077 0.98363596509060458 0.86044228961973501 0.65520344873720149 0.43184569181230892 0.24048395968648062 0.10356938502428203 0.024829070128037145 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0.21437367451588518 0.40311796454178905 0.57057621039236273 0.7169628450725295 0.8400332375476488 0.93478761650205111 0.99152552991401077 0.98363596509060458 0.86044228961973501 0.65520344873720149 0.43184569181230892
		 0.24048379041400592 0.10356938502428203 0.024829070128037145 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.21437357233411949 0.40311796454178905 0.57057621039236273 0.7169628450725295
		 0.84003312526751084 0.93478761650205111 0.99152552991401077 0.98363596509060458 0.86044228961973501 0.65520344873720149 0.43184569181230892 0.24048379041400592 0.10356938502428203 0.024829070128037145 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 ;
	setAttr ".outDoubleweights[2].owd" -type "doubleArray" 341 0 0 0
		 0 0 0 0 2.185975779651843e-17 0 0 0 0 0 1.974208303240709e-16 2.123498834414081e-16
		 0 2.1220367556166535e-16 1.9717281946327782e-16 0 0 0 0 0 2.1794421721208375e-17 0 0 0
		 0 0 0 0 0 0 0 0 0 0 6.4270125710327558e-16 0.0026200710231456589
		 0.010994116729338184 0.025331506640478965 0.044275336444086662 0.064470718935157323 0.082040630745898652 0.094649800385236141 0.10180726605346412 0.10400000000000001 0.10173718068666758 0.094530913780163484 0.081898830257051941 0.064334180181505662
		 0.044167747073651412 0.025263826226181185 0.010962755164254439 0.0026122344809920797 0 0 0 0 0 0 0 0
		 0 0 0 0 0 2.1752965062350149e-15 0.0088679325355260213 0.037210857916816137 0.085737410073368353 0.14985499010062961 0.21820859475589183 0.27767593779583832
		 0.3203531816786564 0.34457845093691297 0.35200001224489796 0.34434113694737056 0.31995073646446343 0.27719605051274132 0.21774646357361022 0.14949084144956587 0.085508337893930295 0.037104711077455589 0.0088414079321753325 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 4.0045232289775188e-15 0.016325056276099544 0.068501808119967797 0.15783478109207211 0.27586941963662559 0.4017021945989811 0.51117616941120347 0.5897410973708116 0.63433758779015159 0.64800003673469342 0.63390074762033299 0.58900023230118392
		 0.51029274052978912 0.40085145308569275 0.27519905505975734 0.15741308002523383 0.068306401434137756 0.016276228595270645 0 0 0 0 0 0
		 0 0 0 0 0 0 0 5.5371186546755255e-15 0.02257291768565119 0.094718544992643289 0.21824067458323998 0.38144905591666306
		 0.55544004511723588 0.70681145987778193 0.81544444151752871 0.87710876168253415 0.89600000816326519 0.876504755787749 0.81442018767987878 0.70558992864308079 0.55426371122890428 0.3805221321013913 0.21765758177782357 0.094448353044844766
		 0.022505401431328155 0 0 0 0 0 0 0 0 0 0 0
		 0 0 6.1798202649114151e-15 0.025192986652226704 0.10571266085902099 0.24357217923537464 0.42572438888544861 0.61991075899189729 0.78885206856938983 0.9100942344734243 0.97891601974484721 1
		 0.97824196841701538 0.90895092424560253 0.78748875247165318 0.61859788636063129 0.42468987570818661 0.2429214060209729 0.10541110734860037 0.025117635297194463 0 0 0 0
		 0 0 0 0 0 0 0 0 0 6.1798202649114151e-15 0.025192986652226704 0.10571266085902099
		 0.24357217923537464 0.42572438888544861 0.61991075899189729 0.78885221871056388 0.9100942344734243 0.97891601974484721 1 0.97824196841701538 0.90895092424560253 0.78748875247165318 0.61859788636063129 0.42468987570818661
		 0.2429214060209729 0.10541110734860037 0.025117635297194463 0 0 0 0 0 0 0 0 0
		 0 0 0 0 6.1798202649114151e-15 0.025192986652226704 0.10571266085902099 0.24357217923537464 0.42572438888544861 0.61991075899189729 0.78885206856938983 0.9100942344734243
		 0.97891601974484721 1 0.97824196841701538 0.90895092424560253 0.78748875247165318 0.61859788636063129 0.42468987570818661 0.2429214060209729 0.10541110734860037 0.025117635297194463 0 0
		 0 0 0 0 0 0 0 0 0 0 0 6.1798202649114151e-15
		 0.025192986652226704 0.10571266085902099 0.24357217923537464 0.42572438888544861 0.61991075899189729 0.78885206856938983 0.9100942344734243 0.97891601974484721 1 0.97824196841701538 0.90895092424560253 0.78748875247165318
		 0.61859788636063129 0.42468987570818661 0.2429214060209729 0.10541110734860037 0.025117635297194463 0 0 0 0 0 0 0
		 0 0 0 0 0 0 6.1798202649114151e-15 0.025192986652226704 0.10571266085902099 0.24357217923537464 0.42572438888544861 0.61991075899189729
		 0.78885221871056388 0.9100942344734243 0.97891601974484721 1 0.97824196841701538 0.90895092424560253 0.78748875247165318 0.61859788636063129 0.42468987570818661 0.2429214060209729 0.10541110734860037 0.025117635297194463
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 6.1798202649114151e-15 0.025192986652226704 0.10571266085902099 0.24357217923537464 0.42572438888544861 0.61991075899189729 0.78885221871056388 0.9100942344734243 0.97891601974484721 1 0.97824196841701538
		 0.90895092424560253 0.78748875247165318 0.61859788636063129 0.42468987570818661 0.2429214060209729 0.10541110734860037 0.025117635297194463 0 0 0 0 0
		 0 0 ;
	setAttr ".outDoubleweights[3].owd" -type "doubleArray" 341 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 5.3860285608260242e-18 2.2466699350181703e-17 0 0 0 0 0 8.6034071401298814e-16 2.0277736214894622e-16 0 1.5552609260031545e-16
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.0025822331278002536 0.010771227451640069 0.025010362614998956 0.044911991562709815
		 0.068141176565324924 0.089486030470402045 0.10229814727334108 0.10311866528484644 0.097217891437985579 0.087363424592828726 0.074564130034785236 0.059339925880805715 0.041924235286999685 0.022294835582391773 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0.0087398636868893272 0.036456530989328786 0.084650461026240104 0.15200982288477508 0.23063168255169353 0.30287580597431568 0.34623989512352338 0.34901697831448952 0.32904518246725079
		 0.29569160121569166 0.25237089512812005 0.20084283304475911 0.14189741667674877 0.075459446134614333 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0.016089294977456366 0.067113160791223675
		 0.15583380666603197 0.27983627098523267 0.42457197036034405 0.55756683684675401 0.63739618452900082 0.64250854233343568 0.60574228099119309 0.54434136870597727 0.46459194994440944 0.36973322350267562 0.2612202500581704 0.13891398342676747
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0.022246926854011022 0.092798268121133537 0.21547389526158928 0.38693408468092777 0.5870624496037079 0.77095657723056177 0.88133789223077408
		 0.88840683108082319 0.83756953386587019 0.75266951104178215 0.64239867406843565 0.51123603780328486 0.36119341499413815 0.19207858522905463 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0.024829160792559483 0.10356968670775153 0.24048425591345149 0.43184607271836356 0.65520362082043193 0.86044260067694267 0.98363603147443335 0.99152547208341268 0.93478741767293816 0.84003292877719926 0.7169628450725295 0.57057621039236261
		 0.40311764699038155 0.21437341906145935 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0.024829160792559483 0.10356968670775153 0.24048425591345149 0.43184607271836356 0.65520362082043193
		 0.86044260067694267 0.98363603147443335 0.99152547208341268 0.93478741767293816 0.84003292877719926 0.7169628450725295 0.57057592984991323 0.40311764699038155 0.21437341906145935 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0.024829160792559483 0.10356968670775153 0.24048425591345149 0.43184607271836356 0.65520362082043193 0.86044260067694267 0.98363603147443335 0.99152547208341268 0.93478741767293816 0.84003292877719926
		 0.7169628450725295 0.57057621039236261 0.40311764699038155 0.21437341906145935 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0.024829160792559483 0.10356968670775153 0.24048425591345149
		 0.43184607271836356 0.65520362082043193 0.86044260067694267 0.98363603147443335 0.99152547208341268 0.93478741767293816 0.84003292877719926 0.7169628450725295 0.57057621039236261 0.40311764699038155 0.21437341906145935 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0.024829160792559483 0.10356968670775153 0.24048425591345149 0.43184607271836356 0.65520362082043193 0.86044260067694267 0.98363603147443335 0.99152547208341268
		 0.93478741767293816 0.84003292877719926 0.7169628450725295 0.57057592984991323 0.40311764699038155 0.21437341906145935 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0.024829160792559483
		 0.10356968670775153 0.24048425591345149 0.43184607271836356 0.65520362082043193 0.86044260067694267 0.98363603147443335 0.99152547208341268 0.93478741767293816 0.84003292877719926 0.7169628450725295 0.57057621039236261 0.40311764699038155
		 0.21437341906145935 0 ;
	setAttr ".outDoubleweights[4].owd" -type "doubleArray" 341 0 0 0
		 2.1562208128614409e-16 1.7839749270424248e-16 8.4516225999589053e-17 7.7727256886593851e-18 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0.050341838486989567 0.084394524942878524 0.10337605844576118 0.085529390686729601 0.040519744673238732 0.0037264753743535949 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0.1703877669601058 0.28564306422041669 0.34988820998785791 0.28948410162526422 0.13714375597250167 0.012612685556175304 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0.31366852072182849 0.52584292519587339 0.64411240067635633 0.53291380776307884 0.25246890454013715
		 0.023218808169242044 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0.43371430476246564 0.72709129843994269 0.89062451164700185 0.73686860339912319 0.34909318805764733 0.032105019374820659 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0.48405613929797658 0.81148594967003984 0.99400056197847286
		 0.82239780486504255 0.38961292955037241 0.035831496796688511 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0.48405633169778944 0.81148594967003984 0.99400056197847286 0.82239780486504255 0.38961248491950917 0.035831496796688511 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0.48405613929797658
		 0.81148594967003984 0.99400056197847286 0.82239780486504255 0.38961292955037241 0.035831496796688511 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0.48405633169778944 0.81148594967003984 0.99400056197847286 0.82239780486504255 0.38961248491950917 0.035831496796688511
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0.48405633169778944 0.81148594967003984 0.99400056197847286 0.82239780486504255 0.38961248491950917 0.035831496796688511 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.48405613929797658 0.81148594967003984 0.99400056197847286 0.82239780486504255
		 0.38961292955037241 0.035831496796688511 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 ;
	setAttr ".outDoubleweights[5].owd" -type "doubleArray" 341 0 0 0
		 7.2839806552427209e-17 1.6623101155995628e-16 2.1692350401306879e-16 1.6623111411774278e-16 2.9135916210874813e-16 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0.0019716326180934524 0.034921722108588418 0.079696423486617263 0.10399999999999097 0.079696425136312671 0.034921663760705039
		 0.0019716288516903177 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0.0066732443125203248 0.11819660201765429 0.26974175041503701 0.35200001224486738 0.2697417396378044 0.11819639831230629 0.0066732055763210176 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.01228483638984712 0.21758920393465431 0.496570179966701 0.64800003673418738
		 0.49657003498524094 0.21758880622406779 0.012284765080024107 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0.016986373479872047 0.3008640701381779 0.68661534706338567 0.89600000816318737 0.68661537138135353 0.30086353940511462 0.016986341030860129 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0.018958079773808444 0.33578578950565785
		 0.76631196267973145 0.99999999999991318 0.76631184030691757 0.3357851757547875 0.018957969727791513 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0.018958079773808444 0.33578578950565785 0.76631196267973145 0.99999999999921907 0.76631184030691757 0.3357851757547875 0.018957969727791513
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0.018958079773808444 0.33578578950565785 0.76631196267973145 0.99999999999991318 0.76631184030691757 0.3357851757547875 0.018957969727791513 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0.018958079773808444 0.33578578950565785 0.76631196267973145 0.99999999999921907 0.76631184030691757
		 0.3357851757547875 0.018957969727791513 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0.018958079773808444 0.33578578950565785 0.76631196267973145 0.99999999999921907 0.76631184030691757 0.3357851757547875 0.018957969727791513 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0.018958079773808444 0.33578578950565785 0.76631196267973145
		 0.99999999999991318 0.76631184030691757 0.3357851757547875 0.018957969727791513 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 ;
	setAttr ".outDoubleweights[6].owd" -type "doubleArray" 341 0 0 0
		 0 0 3.1032041063490231e-17 1.2049342880779021e-16 8.0753940911834559e-16 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0.014877752411321339 0.057768397691266418 0.096790036517125436
		 0.096789994015215819 0.057768361808143098 0.01487771837468297 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0.050355471451554529 0.19552380251282736 0.32759704082924429 0.3275969142167266 0.19552369292148139 0.05035535625062066 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0.092700067143076048
		 0.3599415558919849 0.6030763208894736 0.60307615074433274 0.35994135167095948 0.092699635128105654 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0.12817756040379766 0.49769697658398371 0.83388332140291854 0.83388303295918997 0.49769666011225644 0.12817726716506445
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0.14305531164732055 0.55546540601613292 0.93067328194672205 0.93067301937707514 0.5554650173859913 0.14305498437195163 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.14305565106168297 0.55546540601613292 0.93067328194672205 0.93067301937707514
		 0.5554650173859913 0.14305498437195163 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0.14305531164732055 0.55546540601613292 0.93067328194672205 0.93067301937707514 0.5554650173859913 0.14305498437195163 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0.14305565106168297 0.55546540601613292
		 0.93067328194672205 0.93067301937707514 0.5554650173859913 0.14305498437195163 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0.14305565106168297 0.55546540601613292 0.93067328194672205 0.93067301937707514 0.5554650173859913 0.14305498437195163 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0.14305531164732055 0.55546540601613292 0.93067328194672205 0.93067301937707514 0.5554650173859913 0.14305498437195163 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 ;
	setAttr ".outDoubleweights[7].owd" -type "doubleArray" 341 0 0 0
		 0 0 0 0 1.6449780251122792e-17 0 0 0 0 0 4.1124130549643885e-18 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0.0019716521235968467
		 0.034921722108588377 0.079696475066794906 0.10399999999999097 0.0796964338026553 0.034921586880502078 0.0019716211005448283 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0.0066732839915887359 0.11819660201765415 0.26974192499410582 0.35200001224486738 0.26974178533085924 0.11819629688756378
		 0.0066731793416738346 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0.012284908153354394 0.21758920393465406 0.49657037279719873 0.64800003673463713 0.49657011568985282 0.21758864221788449 0.012284716784422552 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.016986539943965765 0.30086407013817751 0.68661579144645857 0.89600000816318737
		 0.68661543594002183 0.300863293443422 0.016986274251759925 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0.018958190519955367 0.33578578950565746 0.76631226025764321 0.99999999999991318 0.76631186348707014 0.33578492265883997 0.018957895197546426 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0.018958190519955367 0.33578578950565746
		 0.76631226025764321 0.99999999999991318 0.76631186348707014 0.33578448923559689 0.018957895197546426 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0.018958190519955367 0.33578578950565746 0.76631226025764321 0.99999999999991318 0.76631186348707014 0.33578492265883997 0.018957895197546426
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0.018958190519955367 0.33578578950565746 0.76631226025764321 0.99999999999991318 0.76631186348707014 0.33578492265883997 0.018957895197546426 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0.018958190519955367 0.33578578950565746 0.76631226025764321 0.99999999999991318 0.76631186348707014
		 0.33578448923559689 0.018957895197546426 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0.018958190519955367 0.33578578950565746 0.76631226025764321 0.99999999999991318 0.76631186348707014 0.33578448923559689 0.018957895197546426 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 ;
	setAttr ".outDoubleweights[8].owd" -type "doubleArray" 341 0 0 0
		 0 0 0 0 0 0 0 0 0 0 2.0188481143362447e-16 1.2049342880779031e-16
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0.014877752411321339 0.057768402225677841 0.096790068295903878 0.096789974348891042 0.057768320088973014 0.014877725937020135 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0.050355471451554529 0.19552382971929605 0.32759707477860345
		 0.32759684765377889 0.1955235517181316 0.050355381846224262 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0.092699847202556737 0.35994160350330562 0.60307644632415802 0.60307602820799444 0.3599413841712219 0.09269968224728603 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0.12817756040379766
		 0.49769700832486663 0.83388344166213879 0.83388286352623653 0.49769630068555709 0.12817733231750827 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0.14305531164732055 0.55546540601613303 0.9306734755187549 0.93067283027779846 0.55546461624012511 0.14305505708673205
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0.14305531164732055 0.55546540601613303 0.93067373361446026 0.93067283027779846 0.55546461624012511 0.14305505708673205 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.14305531164732055 0.55546540601613303 0.9306734755187549 0.93067283027779846
		 0.55546461624012511 0.14305505708673205 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0.14305531164732055 0.55546540601613303 0.9306734755187549 0.93067283027779846 0.55546461624012511 0.14305505708673205 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0.14305531164732055 0.55546540601613303
		 0.93067373361446026 0.93067283027779846 0.55546461624012511 0.14305505708673205 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0.14305531164732055 0.55546540601613303 0.93067373361446026 0.93067283027779846 0.55546461624012511 0.14305505708673205 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 ;
	setAttr ".outDoubleweights[9].owd" -type "doubleArray" 341 0 0 0
		 0 0 0 0 0 0 0 0 0 0 7.2839877067240745e-17 1.6623111914605436e-16
		 0 1.6623100653163099e-16 7.2839555890814112e-17 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0.0019716748493651946 0.034921744646612789 0.079696506014886634 0.10399999999999776 0.079696423271050518 0.034921669547506931 0.0019716211733275613 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0.006673309283652667
		 0.11819667830020097 0.26974202974149686 0.35200001224489036 0.26974166980615699 0.11819615712981595 0.0066731795880153998 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0.012284955995797915 0.21758934436389105 0.49657030852037365 0.64800003673467943 0.4965699064315226 0.21758838493657034
		 0.012284717237914989 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0.016986605013152096 0.30086426431192809 0.68661605807617432 0.89600000816324576 0.68661519362806023 0.30086361730424094 0.016986274878811165 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.018958264350882541 0.33578600621743065 0.76631255783544827 0.99999999999997835
		 0.76631164192153478 0.33578452561979744 0.018957895897380395 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0.018958412013126869 0.33578600621743065 0.76631255783544827 0.99999999999997835 0.76631164192153478 0.33578452561979744 0.018957895897380395 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0.018958264350882541 0.33578600621743065
		 0.76631255783544827 0.99999999999997835 0.76631164192153478 0.33578452561979744 0.018957895897380395 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0.018958264350882541 0.33578600621743065 0.76631255783544827 0.99999999999997835 0.76631164192153478 0.33578452561979744 0.018957895897380395
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0.018958412013126869 0.33578600621743065 0.76631255783544827 0.99999999999997835 0.76631164192153478 0.33578452561979744 0.018957895897380395 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0.018958412013126869 0.33578600621743065 0.76631255783544827 0.99999999999997835 0.76631164192153478
		 0.33578452561979744 0.018957895897380395 0 0 0 0 0 0 0 0 0 0
		 0 0 ;
	setAttr ".outDoubleweights[10].owd" -type "doubleArray" 341 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 1.2049355117991081e-16 2.0188499339183021e-16 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0.014877743586552437 0.057768434762132587 0.096790014611956923 0.096789980594187627 0.057768291405241166
		 0.014877700725159634 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0.050355441583104898 0.19552388194171322 0.32759714291588493 0.32759686879170652 0.19552345463472809 0.050355296513770367 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0.092699792217455071 0.3599417021133472 0.60307657175870155
		 0.60307606712099848 0.35994091300669945 0.092699525157992471 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0.12817748437501875 0.49769717876661235 0.83388321040803803 0.83388291733186914 0.49769605356417268 0.12817711510763125 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0.14305522679377342
		 0.55546563166640039 0.93067366909057048 0.93067289032872713 0.55546434043501114 0.14305481466499648 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0.14305522679377342 0.55546563166640039 0.93067366909057048 0.93067289032872713 0.55546434043501114 0.14305481466499648
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0.14305522679377342 0.55546563166640039 0.93067366909057048 0.93067289032872713 0.55546434043501114 0.14305481466499648 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.14305522679377342 0.55546563166640039 0.93067366909057048 0.93067289032872713
		 0.55546434043501114 0.14305481466499648 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0.14305522679377342 0.55546563166640039 0.93067366909057048 0.93067289032872713 0.55546434043501114 0.14305481466499648 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0.14305522679377342 0.55546563166640039
		 0.93067366909057048 0.93067289032872713 0.55546434043501114 0.14305481466499648 0 0 0 0 0 0 0 0
		 0 0 ;
	setAttr ".outDoubleweights[11].owd" -type "doubleArray" 341 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 4.1125251644110268e-18 0 0 0 0 0 1.6449588064515977e-17 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0.0019716479748722103 0.034921744646612789 0.079696536962967218
		 0.10399999999996391 0.079696371906408825 0.034921643225525434 0.001971613731711435 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0.0066733612607644786 0.11819667830020096 0.2697421344888502 0.35200001224477578 0.26974157583586394 0.11819633502881645 0.0066731533534152686 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0.012285051680937664
		 0.21758934436389102 0.49657075845798654 0.64800003673446849 0.49656973002860294 0.21758871243246478 0.012284668942400054 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0.016986505784428708 0.30086426431192803 0.68661632470579403 0.89600000816295422 0.68661490268004732 0.30086339053024441
		 0.01698620809983073 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0.018958412013126869 0.3357860062174306 0.7663128554131462 0.99999999999965294 0.76631126833085406 0.33578503101466761 0.018957821367268979 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.018958412013126869 0.3357860062174306 0.7663128554131462 0.99999999999965294
		 0.76631126833085406 0.33578503101466761 0.018957821367268979 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0.018958412013126869 0.3357860062174306 0.7663128554131462 0.99999999999965294 0.76631126833085406 0.33578503101466761 0.018957821367268979 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0.018958412013126869 0.3357860062174306
		 0.7663128554131462 0.99999999999965294 0.76631126833085406 0.33578503101466761 0.018957821367268979 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0.018958412013126869 0.3357860062174306 0.7663128554131462 0.99999999999965294 0.76631126833085406 0.33578503101466761 0.018957821367268979
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0.018958412013126869 0.3357860062174306 0.7663128554131462 0.99999999999965294 0.76631126833085406 0.33578503101466761 0.018957821367268979 0 0 0 0 0
		 0 0 ;
	setAttr ".outDoubleweights[12].owd" -type "doubleArray" 341 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 8.0753912918201648e-16 1.204932085379426e-16 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0.014877770060864522 0.057768472628558463 0.096790034743455919 0.096789976122505811 0.057768261419891123 0.014877672988466983 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0.050355531188471997 0.19552406800597721 0.32759705206615941 0.32759680222871179 0.19552335314584751
		 0.050355202635730435 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0.092699957172793571 0.35994204216743281 0.60307640451261235 0.6030759445845737 0.35994072617489248 0.092699352337051538 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0.12817771246140186 0.49769761487276676 0.83388338384864635
		 0.83388274789879602 0.49769579522884694 0.12817687614535392 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0.14305548135446655 0.55546608296690825 0.93067341099476841 0.93067270122931689 0.55546405211433769 0.14305454796602868 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0.14305548135446655
		 0.55546608296690825 0.93067341099476841 0.93067270122931689 0.55546405211433769 0.14305454796602868 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0.14305548135446655 0.55546608296690825 0.93067341099476841 0.93067270122931689 0.55546405211433769 0.14305454796602868
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0.14305548135446655 0.55546608296690825 0.93067341099476841 0.93067270122931689 0.55546405211433769 0.14305454796602868 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.14305548135446655 0.55546608296690825 0.93067341099476841 0.93067270122931689
		 0.55546405211433769 0.14305454796602868 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0.14305548135446655 0.55546608296690825 0.93067341099476841 0.93067270122931689 0.55546405211433769 0.14305454796602868 0 0 0
		 0 0 ;
	setAttr ".outDoubleweights[13].owd" -type "doubleArray" 341 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 2.9135969465679686e-16 1.6623131280086849e-16 0 1.6623102804885848e-16
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0.0019716556532818927 0.034921772666864317 0.079696557595014747 0.10399999999988946 0.079696414820274189 0.034921692085527117 0.0019716019774797646 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0.0066732962894033507 0.11819675458275754 0.26974220432039814
		 0.35200001224452382 0.26974170472198283 0.11819650040113559 0.006673114617451366 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0.012284932074565694 0.21758948479314599 0.4965708870115208 0.64800003673400464 0.49657003639224934 0.21758852536571818 0.012284597633010399 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0.016986571936881956
		 0.30086445848570348 0.68661650245882067 0.89600000816231284 0.68661528250471227 0.30086313187006392 0.016986109499197873 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0.018958227435402812 0.33578622292923155 0.76631305379821868 0.99999999999893707 0.76631174111423217 0.33578550082237613
		 0.018957711321920812 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0.018958227435402812 0.33578622292923155 0.76631305379821868 0.99999999999893707 0.76631174111423217 0.33578474233143307 0.018957711321920812 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.018958227435402812 0.33578622292923155 0.76631305379821868 0.99999999999893707
		 0.76631174111423217 0.33578550082237613 0.018957711321920812 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0.018958227435402812 0.33578622292923155 0.76631305379821868 0.99999999999893707 0.76631174111423217 0.33578550082237613 0.018957711321920812 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0.018958227435402812 0.33578622292923155
		 0.76631305379821868 0.99999999999893707 0.76631174111423217 0.33578474233143307 0.018957711321920812 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0.018958227435402812 0.33578622292923155 0.76631305379821868 0.99999999999893707 0.76631174111423217 0.33578550082237613 0.018957711321920812
		 0 0 ;
	setAttr ".outDoubleweights[14].owd" -type "doubleArray" 341 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 7.7728420901852629e-18 0 1.7839745662976315e-16
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0.0037265467430885151 0.040519855773199387 0.085529385658787135 0.1033760549693169 0.084394467801648901 0.050341781788750407 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0.012612927876907131
		 0.13714413200315079 0.28948406704935109 0.34988819822143069 0.28564282403444285 0.17038757505836657 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0.023219254100143361 0.25246988489920846 0.53291393652988084 0.64411230354462468 0.525842483035321 0.31366804277307864
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0.032105633771424023 0.34909414522654786 0.73686857092626956 0.89062437734140409 0.72709080614626764 0.43371381628532379 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0.035832180222004947 0.38961399781922484 0.82239800357923198 0.99400052855112397
		 0.81148526732354709 0.48405559412260002 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0.035832180222004947 0.38961399781922484 0.82239800357923198 0.99400041208383383 0.81148526732354709 0.48405559412260002 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0.035832180222004947 0.38961399781922484
		 0.82239800357923198 0.99400052855112397 0.81148526732354709 0.48405559412260002 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0.035832180222004947 0.38961399781922484 0.82239800357923198 0.99400052855112397 0.81148526732354709 0.48405559412260002 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0.035832180222004947 0.38961399781922484 0.82239800357923198 0.99400041208383383 0.81148526732354709 0.48405559412260002 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0.035832180222004947 0.38961399781922484 0.82239800357923198 0.99400052855112397 0.81148526732354709
		 0.48405559412260002 0 ;
createNode animCurveTU -n "C_lipSingle_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC85";
	setAttr ".tan" 1;
	setAttr -s 3 ".ktv[0:2]"  -10 0 0 1 10 0;
	setAttr -s 3 ".ktl[0:2]" no yes no;
	setAttr -s 3 ".kix[0:2]"  0.0062499998603016138 0.75000002980232239 0.0040174224707444795;
	setAttr -s 3 ".kiy[0:2]"  0 0 -0.011490666389948256;
	setAttr -s 3 ".kox[0:2]"  0.0040174224707444795 0.75000002980232239 0.0062499998603016138;
	setAttr -s 3 ".koy[0:2]"  0.011490666389948256 0 0;
createNode animCurveTU -n "C_lipSingleFalloff_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC86";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode LHWeightNode -n "TestWeights_UD";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC88";
	setAttr -s 15 ".inputs";
	setAttr -s 341 ".wlf[0].outflw[3:340]"  -5.9374037e-19 -1.1713819e-18
		 -2.4027256e-18 -4.8084472e-18 -2.5080346e-17 0 0 0 0 0 -9.8575105e-18 -1.004905e-17
		 0 -1.0107525e-17 -9.9013288e-18 0 0 0 0 0 -2.1544336e-17 -3.9665138e-18 0 -5.2564143e-19
		 0 0 0 0 0 -9.6237483e-05 -0.00016394001 -0.00028465799 -0.0005615977 -0.001151943
		 -0.002305323 -0.0030060783 -0.002651107 -0.0032516725 -0.0041842372 -0.0046494277
		 -0.0047097611 -0.0047260029 -0.0048178332 -0.0048958259 -0.0048458683 -0.0047470108
		 -0.0046843002 -0.0045384304 -0.0039607962 -0.0029175319 -0.0022437011 -0.0025822597
		 -0.0019016725 -0.00078921037 -0.00025200914 -3.8279843e-05 1.0128656e-05 -3.6697336e-06
		 0 0 -0.00032572687 -0.00055487402 -0.00096345786 -0.0019007924 -0.0038988842 -0.0078026312
		 -0.010174419 -0.0089729773 -0.011005661 -0.014162035 -0.015736526 -0.015940731 -0.015995702
		 -0.016306512 -0.016570488 -0.016401397 -0.016066805 -0.015854554 -0.015360842 -0.013405772
		 -0.0098747239 -0.0075940657 -0.0087399548 -0.0064364304 -0.0026711738 -0.00085295399
		 -0.00012956254 3.4281606e-05 -1.2420637e-05 0 0 -0.00059963379 -0.0010214726 -0.0017736384
		 -0.0034991871 -0.0071774963 -0.014363935 -0.018730178 -0.016518436 -0.020260422 -0.026071019
		 -0.028969513 -0.029345436 -0.029446635 -0.030018806 -0.030504761 -0.030193482 -0.029577529
		 -0.029186793 -0.028277913 -0.02467881 -0.018178469 -0.013979985 -0.016089464 -0.011848883
		 -0.0049173879 -0.0015702109 -0.00023851165 6.3109321e-05 -2.2865264e-05 0 0 -0.00082912296
		 -0.0014124062 -0.0024524382 -0.0048383805 -0.0099244323 -0.019861244 -0.02589852
		 -0.022840306 -0.028014408 -0.036048815 -0.040056609 -0.040576406 -0.040716331 -0.041507486
		 -0.042179421 -0.041749012 -0.040897325 -0.040357046 -0.039100323 -0.034123782 -0.025135661
		 -0.019330349 -0.022247158 -0.01638364 -0.006799351 -0.0021711558 -0.00032979387 8.726227e-05
		 -3.1616168e-05 0 0 -0.00092536042 -0.0015763466 -0.002737096 -0.0053999801 -0.011076375
		 -0.022166569 -0.028904596 -0.025491413 -0.031266082 -0.04023305 -0.044706035 -0.045286164
		 -0.045442335 -0.046325319 -0.047075246 -0.046594881 -0.045644332 -0.045041345 -0.043638751
		 -0.038084578 -0.028053192 -0.02157405 -0.024829416 -0.018285312 -0.0075885612 -0.0024231649
		 -0.00036807542 9.7390919e-05 -3.5285902e-05 0 0 -0.00092536077 -0.0015763466 -0.002737096
		 -0.0053999801 -0.011076383 -0.022166569 -0.028904596 -0.025491413 -0.031266082 -0.04023305
		 -0.044706035 -0.045286164 -0.045442335 -0.046325319 -0.047075246 -0.046594881 -0.045644332
		 -0.045041345 -0.043638751 -0.038084578 -0.028053192 -0.02157405 -0.024829416 -0.018285312
		 -0.0075885612 -0.0024231649 -0.00036807352 9.7390919e-05 -3.5285902e-05 0 0 -0.00092536042
		 -0.0015763466 -0.002737096 -0.0053999801 -0.011076375 -0.022166569 -0.028904596 -0.025491413
		 -0.031266082 -0.04023305 -0.044706035 -0.045286164 -0.045442335 -0.046325319 -0.047075246
		 -0.046594881 -0.045644332 -0.045041345 -0.043638751 -0.038084578 -0.028053192 -0.02157405
		 -0.024829416 -0.018285312 -0.0075885612 -0.0024231649 -0.00036807542 9.7390919e-05
		 -3.5285902e-05 0 0 -0.00092536077 -0.0015763466 -0.002737096 -0.0053999801 -0.011076383
		 -0.022166569 -0.028904596 -0.025491413 -0.031266082 -0.04023305 -0.044706035 -0.045286164
		 -0.045442335 -0.046325319 -0.047075246 -0.046594881 -0.045644332 -0.045041345 -0.043638751
		 -0.038084578 -0.028053192 -0.02157405 -0.024829416 -0.018285312 -0.0075885612 -0.0024231649
		 -0.00036807542 9.7390919e-05 -3.5285902e-05 0 0 -0.00092536077 -0.0015763466 -0.002737096
		 -0.0053999801 -0.011076383 -0.022166569 -0.028904596 -0.025491413 -0.031266082 -0.04023305
		 -0.044706035 -0.045286164 -0.045442335 -0.046325319 -0.047075246 -0.046594881 -0.045644332
		 -0.045041345 -0.043638751 -0.038084578 -0.028053192 -0.02157405 -0.024829416 -0.018285312
		 -0.0075885612 -0.0024231649 -0.00036807352 9.7390919e-05 -3.5285902e-05 0 0 -0.00092536042
		 -0.0015763466 -0.002737096 -0.0053999801 -0.011076375 -0.022166569 -0.028904596 -0.025491413
		 -0.031266082 -0.04023305 -0.044706035 -0.045286164 -0.045442335 -0.046325319 -0.047075246
		 -0.046594881 -0.045644332 -0.045041345 -0.043638751 -0.038084578 -0.028053192 -0.02157405
		 -0.024829416 -0.018285312 -0.0075885612 -0.0024231649 -0.00036807542 9.7390919e-05
		 -3.5285902e-05 0;
createNode LHWeightNode -n "TestWeights_LR";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC89";
	setAttr -s 15 ".inputs";
createNode LHGeometryConstraint -n "C_lipSingle_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC97";
	setAttr ".outmatrix" -type "matrix" 0.99993673380656367 -0.011248483642759982 0 0 0.011248483642759982 0.99993673380656378 0 0
		 0 0 1 0 0 0.85292480132205739 0 1;
	setAttr ".bweights" -type "float3" -0.25000015 0.74999982 0.5000003 ;
	setAttr ".apointidx" 293;
	setAttr ".bpointidx" 294;
	setAttr ".cpointidx" 325;
	setAttr ".dpointidx" 324;
createNode decomposeMatrix -n "C_lipSingle_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC98";
createNode animCurveTU -n "L_lipPrime00_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC9D";
	setAttr ".tan" 1;
	setAttr -s 4 ".ktv[0:3]"  -10 0 -5 1 0 0 10 0;
	setAttr -s 4 ".kit[3]"  18;
	setAttr -s 4 ".kot[3]"  18;
	setAttr -s 4 ".ktl[0:3]" no yes no yes;
	setAttr -s 4 ".kix[0:3]"  0.3125 0.1875000074505806 0.3125 0.41666666666666669;
	setAttr -s 4 ".kiy[0:3]"  0 0 0 0;
	setAttr -s 4 ".kox[0:3]"  0.15625000000000003 0.1875000074505806 0.3125 0.41666666666666669;
	setAttr -s 4 ".koy[0:3]"  1.299038105676658 0 0 0;
createNode animCurveTU -n "L_lipPrimeFalloff0_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC9E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode animCurveTU -n "C_lipPrime_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DC9F";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  -10 0 -6 0 0 1 6 0 10 0;
	setAttr -s 5 ".kit[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".kot[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".ktl[1:4]" no yes no yes;
	setAttr -s 5 ".kix[1:4]"  0.3125 0.33880435675445919 0.3125 0.16666666666666669;
	setAttr -s 5 ".kiy[1:4]"  0 -0.0046439626837641839 0 0;
	setAttr -s 5 ".kox[1:4]"  0.3125 0.33880435675382614 0.3125 0.16666666666666669;
	setAttr -s 5 ".koy[1:4]"  0 -0.0046439627185463905 0 0;
createNode animCurveTU -n "C_lipPrimeFalloff_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCA0";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode animCurveTU -n "R_lipPrime00_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCA1";
	setAttr ".tan" 1;
	setAttr -s 4 ".ktv[0:3]"  -10 0 0 0 5 1 10 0;
	setAttr -s 4 ".kit[0:3]"  18 1 1 1;
	setAttr -s 4 ".kot[0:3]"  18 1 1 1;
	setAttr -s 4 ".ktl[1:3]" no yes no;
	setAttr -s 4 ".kix[1:3]"  0.3125 0.1875000074505806 0.15625000000000003;
	setAttr -s 4 ".kiy[1:3]"  0 0 -1.299038105676658;
	setAttr -s 4 ".kox[1:3]"  0.3125 0.1875000074505806 0.3125;
	setAttr -s 4 ".koy[1:3]"  0 0 0;
createNode animCurveTU -n "R_lipPrimeFalloff0_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCA2";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode LHGeometryConstraint -n "L_lipPrime00_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCAF";
	setAttr ".outmatrix" -type "matrix" 0.99493112818698703 -0.10055869014943135 0 0 0.10055869014943136 0.99493112818698703 0 0
		 0 0 1 0 -0.53333331743876045 0.87382031495562096 0 1;
	setAttr ".bweights" -type "float3" -0.25681219 0.74318784 0.51362437 ;
	setAttr ".apointidx" 285;
	setAttr ".bpointidx" 286;
	setAttr ".cpointidx" 317;
	setAttr ".dpointidx" 316;
createNode decomposeMatrix -n "L_lipPrime00_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCB0";
createNode LHGeometryConstraint -n "C_lipPrime_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCBE";
	setAttr ".outmatrix" -type "matrix" 0.99997403638411853 0.0072060084411336035 0 0 -0.0072060084411336026 0.99997403638411853 0 0
		 0 0 1 0 5.9604694513382128e-08 0.85415536164180139 0 1;
	setAttr ".bweights" -type "float3" 0.74692261 -0.2530756 0.50615299 ;
	setAttr ".apointidx" 294;
	setAttr ".bpointidx" 295;
	setAttr ".cpointidx" 326;
	setAttr ".dpointidx" 325;
createNode decomposeMatrix -n "C_lipPrime_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCBF";
createNode LHGeometryConstraint -n "R_lipPrime00_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCCD";
	setAttr ".outmatrix" -type "matrix" 0.99880992048592987 -0.04877235629832178 0 0 0.04877235629832178 0.99880992048592976 0 0
		 0 0 1 0 0.53333343664805355 0.8778955204031611 0 1;
	setAttr ".bweights" -type "float3" -0.25681213 0.7431879 0.51362425 ;
	setAttr ".apointidx" 301;
	setAttr ".bpointidx" 302;
	setAttr ".cpointidx" 333;
	setAttr ".dpointidx" 332;
createNode decomposeMatrix -n "R_lipPrime00_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCCE";
createNode animCurveTU -n "L_lipSecondary00_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCD6";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  -10.5 0 -10 0.37559766722021753 -8.3333333333333339 1 -6.1666668367346942 0 10 0;
	setAttr -s 5 ".kit[4]"  18;
	setAttr -s 5 ".kot[4]"  18;
	setAttr -s 5 ".ktl[0:4]" no yes yes no yes;
	setAttr -s 5 ".kix[0:4]"  0.083333334657880925 0.027374968030668634 0.057906307661639289 0.083333334657880925 0.67361111819727892;
	setAttr -s 5 ".kiy[0:4]"  0 0.40680792898433393 0 0 0;
	setAttr -s 5 ".kox[0:4]"  0.012713513498120776 0.062342456365257926 0.083333334657880925 0.083333334657880925 0.67361111819727892;
	setAttr -s 5 ".koy[0:4]"  0.31709450658911731 0.92644512071517637 0 0 0;
createNode animCurveTU -n "L_lipSecondaryFalloff0_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCD7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode animCurveTU -n "L_lipSecondary01_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCD8";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  -10 0 -8.8333333333333339 0 -6.666666666666667 1 -4.5000001700680272 0 10 0;
	setAttr -s 5 ".kit[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".kot[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".ktl[1:4]" no yes no yes;
	setAttr -s 5 ".kix[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.6041666737528345;
	setAttr -s 5 ".kiy[1:4]"  0 0 0 0;
	setAttr -s 5 ".kox[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.6041666737528345;
	setAttr -s 5 ".koy[1:4]"  0 0 0 0;
createNode animCurveTU -n "L_lipSecondaryFalloff1_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCD9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode animCurveTU -n "L_lipSecondary02_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCDA";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  -10 0 -7.166666666666667 0 -5 1 -2.8333335034013607 0 10 0;
	setAttr -s 5 ".kit[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".kot[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".ktl[1:4]" no yes no yes;
	setAttr -s 5 ".kix[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.53472222930839008;
	setAttr -s 5 ".kiy[1:4]"  0 0 0 0;
	setAttr -s 5 ".kox[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.53472222930839008;
	setAttr -s 5 ".koy[1:4]"  0 0 0 0;
createNode animCurveTU -n "L_lipSecondaryFalloff2_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCDB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode animCurveTU -n "L_lipSecondary03_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCDC";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  -10 0 -5.5000001700680272 0 -3.3333335034013607 1 -1.166666836734694 0 10 0;
	setAttr -s 5 ".kit[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".kot[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".ktl[1:4]" no yes no yes;
	setAttr -s 5 ".kix[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.46527778486394561;
	setAttr -s 5 ".kiy[1:4]"  0 0 0 0;
	setAttr -s 5 ".kox[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.46527778486394561;
	setAttr -s 5 ".koy[1:4]"  0 0 0 0;
createNode animCurveTU -n "L_lipSecondaryFalloff3_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCDD";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode animCurveTU -n "L_lipSecondary04_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCDE";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  -10 0 -3.8333335034013607 0 -1.666666836734694 1 0.49999982993197278 0 10 0;
	setAttr -s 5 ".kit[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".kot[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".ktl[1:4]" no yes no yes;
	setAttr -s 5 ".kix[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.39583334041950113;
	setAttr -s 5 ".kiy[1:4]"  0 0 0 0;
	setAttr -s 5 ".kox[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.39583334041950113;
	setAttr -s 5 ".koy[1:4]"  0 0 0 0;
createNode animCurveTU -n "L_lipSecondaryFalloff4_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCDF";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode animCurveTU -n "C_lipSecondary_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCE0";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  -10 0 -2.1666668367346937 0 -1.7006802721088437e-07 1 2.1666663265306121 0 10 0;
	setAttr -s 5 ".kit[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".kot[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".ktl[1:4]" no yes no yes;
	setAttr -s 5 ".kix[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.32638890306122448;
	setAttr -s 5 ".kiy[1:4]"  0 0 0 0;
	setAttr -s 5 ".kox[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.32638890306122448;
	setAttr -s 5 ".koy[1:4]"  0 0 0 0;
createNode animCurveTU -n "C_lipSecondaryFalloff_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCE1";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode animCurveTU -n "R_lipSecondary04_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCE2";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  -10 0 -0.50000017006802722 0 1.6666664965986395 1 3.833332993197279 0 10 0;
	setAttr -s 5 ".kit[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".kot[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".ktl[1:4]" no yes no yes;
	setAttr -s 5 ".kix[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.25694445861678006;
	setAttr -s 5 ".kiy[1:4]"  0 0 0 0;
	setAttr -s 5 ".kox[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.25694445861678006;
	setAttr -s 5 ".koy[1:4]"  0 0 0 0;
createNode animCurveTU -n "R_lipSecondaryFalloff4_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCE3";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode animCurveTU -n "R_lipSecondary03_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCE4";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  -10 0 1.1666663265306123 0 3.333332993197279 1 5.4999996598639456 0 10 0;
	setAttr -s 5 ".kit[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".kot[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".ktl[1:4]" no yes no yes;
	setAttr -s 5 ".kix[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.18750001417233561;
	setAttr -s 5 ".kiy[1:4]"  0 0 0 0;
	setAttr -s 5 ".kox[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.18750001417233561;
	setAttr -s 5 ".koy[1:4]"  0 0 0 0;
createNode animCurveTU -n "R_lipSecondaryFalloff3_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCE5";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode animCurveTU -n "R_lipSecondary02_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCE6";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  -10 0 2.833332993197279 0 4.9999996598639456 1 7.1666663265306125 0 10 0;
	setAttr -s 5 ".kit[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".kot[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".ktl[1:4]" no yes no yes;
	setAttr -s 5 ".kix[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.11805556972789116;
	setAttr -s 5 ".kiy[1:4]"  0 0 0 0;
	setAttr -s 5 ".kox[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.11805556972789116;
	setAttr -s 5 ".koy[1:4]"  0 0 0 0;
createNode animCurveTU -n "R_lipSecondaryFalloff2_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCE7";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode animCurveTU -n "R_lipSecondary01_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCE8";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  -10 0 4.4999996598639456 0 6.6666663265306125 1 8.8333328231292523 0 10 0;
	setAttr -s 5 ".kit[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".kot[0:4]"  18 1 1 1 18;
	setAttr -s 5 ".ktl[1:4]" no yes no yes;
	setAttr -s 5 ".kix[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.048611132369614507;
	setAttr -s 5 ".kiy[1:4]"  0 0 0 0;
	setAttr -s 5 ".kox[1:4]"  0.083333334657880925 0.083333334657880925 0.083333334657880925 0.048611132369614507;
	setAttr -s 5 ".koy[1:4]"  0 0 0 0;
createNode animCurveTU -n "R_lipSecondaryFalloff1_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCE9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode animCurveTU -n "R_lipSecondary00_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCEA";
	setAttr ".tan" 1;
	setAttr -s 5 ".ktv[0:4]"  -10 0 6.1666663265306125 0 8.3333329931972795 1 10 0.37559737473543175 10.499999489795918 0;
	setAttr -s 5 ".kit[0:4]"  18 1 1 1 1;
	setAttr -s 5 ".kot[0:4]"  18 1 1 1 1;
	setAttr -s 5 ".ktl[1:4]" no yes yes no;
	setAttr -s 5 ".kix[1:4]"  0.083333334657880925 0.083333334657880925 0.06234245352923351 0.012713504357420746;
	setAttr -s 5 ".kiy[1:4]"  0 0 -0.92644540037159717 -0.31709427860605;
	setAttr -s 5 ".kox[1:4]"  0.083333334657880925 0.057906325943039683 0.027374938460984433 0.083333334657880925;
	setAttr -s 5 ".koy[1:4]"  0 0 -0.40680763086653499 0;
createNode animCurveTU -n "R_lipSecondaryFalloff0_ACV";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCEB";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode LHGeometryConstraint -n "L_lipSecondary00_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCF8";
	setAttr ".outmatrix" -type "matrix" 0.99984846128168914 -0.017408459800872619 0 0 0.017408459800872619 0.99984846128168903 0 0
		 0 0 1 0 -0.79999995231628418 0.89726293087005615 0 1;
	setAttr ".bweights" -type "float3" -0.25 0.75 0.5 ;
	setAttr ".apointidx" 281;
	setAttr ".bpointidx" 282;
	setAttr ".cpointidx" 313;
	setAttr ".dpointidx" 312;
createNode decomposeMatrix -n "L_lipSecondary00_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DCF9";
createNode LHGeometryConstraint -n "L_lipSecondary01_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD07";
	setAttr ".outmatrix" -type "matrix" 0.99639469129805314 -0.084838783307267157 0 0 0.084838783307267171 0.99639469129805325 0 0
		 0 0 1 0 -0.66666662693023682 0.88892369270323002 0 1;
	setAttr ".bweights" -type "float3" -0.25000012 0.74999988 0.50000024 ;
	setAttr ".apointidx" 283;
	setAttr ".bpointidx" 284;
	setAttr ".cpointidx" 315;
	setAttr ".dpointidx" 314;
createNode decomposeMatrix -n "L_lipSecondary01_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD08";
createNode LHGeometryConstraint -n "L_lipSecondary02_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD16";
	setAttr ".outmatrix" -type "matrix" 0.99869195291534574 0.051131039321852013 0 0 -0.051131039321852013 0.99869195291534585 0 0
		 0 0 1 0 -0.499999940395357 0.87280203256600686 0 1;
	setAttr ".bweights" -type "float3" 0.24999952 0.25000042 0.50000006 ;
	setAttr ".apointidx" 286;
	setAttr ".bpointidx" 287;
	setAttr ".cpointidx" 318;
	setAttr ".dpointidx" 317;
createNode decomposeMatrix -n "L_lipSecondary02_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD17";
createNode LHGeometryConstraint -n "L_lipSecondary03_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD25";
	setAttr ".outmatrix" -type "matrix" 0.99107515411327363 -0.1333043093802711 0 0 0.1333043093802711 0.99107515411327363 0 0
		 0 0 1 0 -0.33333331346511841 0.85976696014404297 0 1;
	setAttr ".bweights" -type "float3" -0.25 0.75 0.5 ;
	setAttr ".apointidx" 288;
	setAttr ".bpointidx" 289;
	setAttr ".cpointidx" 320;
	setAttr ".dpointidx" 319;
createNode decomposeMatrix -n "L_lipSecondary03_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD26";
createNode LHGeometryConstraint -n "L_lipSecondary04_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD34";
	setAttr ".outmatrix" -type "matrix" 0.99999725644558868 -0.0023424562526206906 0 0 0.0023424562526206906 0.99999725644558879 0 0
		 0 0 1 0 -0.16666659712791443 0.85463577508926392 0 1;
	setAttr ".bweights" -type "float3" 0.25 0.25 0.5 ;
	setAttr ".apointidx" 291;
	setAttr ".bpointidx" 292;
	setAttr ".cpointidx" 323;
	setAttr ".dpointidx" 322;
createNode decomposeMatrix -n "L_lipSecondary04_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD35";
createNode LHGeometryConstraint -n "C_lipSecondary_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD43";
	setAttr ".outmatrix" -type "matrix" 0.99993673380656367 -0.011248483642759982 0 0 0.011248483642759982 0.99993673380656378 0 0
		 0 0 1 0 0 0.85292476415634155 0 1;
	setAttr ".bweights" -type "float3" -0.25 0.75 0.5 ;
	setAttr ".apointidx" 293;
	setAttr ".bpointidx" 294;
	setAttr ".cpointidx" 325;
	setAttr ".dpointidx" 324;
createNode decomposeMatrix -n "C_lipSecondary_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD44";
createNode LHGeometryConstraint -n "R_lipSecondary04_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD52";
	setAttr ".outmatrix" -type "matrix" 0.99995909368011415 0.0090449414837652127 0 0 -0.0090449414837652127 0.99995909368011415 0 0
		 0 0 1 0 0.16666674613952637 0.85465720295906067 0 1;
	setAttr ".bweights" -type "float3" 0.25 0.25 0.5 ;
	setAttr ".apointidx" 296;
	setAttr ".bpointidx" 297;
	setAttr ".cpointidx" 328;
	setAttr ".dpointidx" 327;
createNode decomposeMatrix -n "R_lipSecondary04_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD53";
createNode LHGeometryConstraint -n "R_lipSecondary03_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD61";
	setAttr ".outmatrix" -type "matrix" 0.99654742940554819 0.083025423486988242 0 0 -0.083025423486988242 0.99654742940554819 0 0
		 0 0 1 0 0.33333337306976318 0.8619154691696167 0 1;
	setAttr ".bweights" -type "float3" -0.25 0.75 0.5 ;
	setAttr ".apointidx" 298;
	setAttr ".bpointidx" 299;
	setAttr ".cpointidx" 330;
	setAttr ".dpointidx" 329;
createNode decomposeMatrix -n "R_lipSecondary03_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD62";
createNode LHGeometryConstraint -n "R_lipSecondary02_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD70";
	setAttr ".outmatrix" -type "matrix" 0.99880992048592987 -0.04877235629832178 0 0 0.04877235629832178 0.99880992048592976 0 0
		 0 0 1 0 0.50000007450580775 0.87679836680883838 0 1;
	setAttr ".bweights" -type "float3" 0.24999999 0.24999999 0.50000006 ;
	setAttr ".apointidx" 301;
	setAttr ".bpointidx" 302;
	setAttr ".cpointidx" 333;
	setAttr ".dpointidx" 332;
createNode decomposeMatrix -n "R_lipSecondary02_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD71";
createNode LHGeometryConstraint -n "R_lipSecondary01_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD7F";
	setAttr ".outmatrix" -type "matrix" 0.98737096049095896 0.15842533376692342 0 0 -0.15842533376692344 0.98737096049095907 0 0
		 0 0 1 0 0.66666675607363501 0.89241146433967256 0 1;
	setAttr ".bweights" -type "float3" -0.24999996 0.75000006 0.49999991 ;
	setAttr ".apointidx" 303;
	setAttr ".bpointidx" 304;
	setAttr ".cpointidx" 335;
	setAttr ".dpointidx" 334;
createNode decomposeMatrix -n "R_lipSecondary01_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD80";
createNode LHGeometryConstraint -n "R_lipSecondary00_GCS";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD8E";
	setAttr ".outmatrix" -type "matrix" 0.99952519696149034 0.030812021016053237 0 0 -0.030812021016053244 0.99952519696149056 0 0
		 0 0 1 0 0.80000005960464371 0.89963193536354158 0 1;
	setAttr ".bweights" -type "float3" -0.24999993 0.75000006 0.49999985 ;
	setAttr ".apointidx" 305;
	setAttr ".bpointidx" 306;
	setAttr ".cpointidx" 337;
	setAttr ".dpointidx" 336;
createNode decomposeMatrix -n "R_lipSecondary00_GCS_DCP";
	rename -uid "3A48D100-0000-2490-5C81-EBD40011DD8F";
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 11 ".dsm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "glimpse";
	setAttr ".an" yes;
	setAttr ".ufe" yes;
	setAttr ".pff" yes;
select -ne :defaultResolution;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr -av ".w" 1920;
	setAttr -av ".h" 1080;
	setAttr ".pa" 1;
	setAttr -k on ".al";
	setAttr -av ".dar" 1.7779999971389771;
	setAttr -k on ".ldar";
	setAttr -k on ".off";
	setAttr -k on ".fld";
	setAttr -k on ".zsl";
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "/film/tools/packages/ALColour_banzai/0.1.0/config.ocio";
	setAttr ".vtn" -type "string" "Output Transform (P3-D60)";
	setAttr ".wsn" -type "string" "acescg";
	setAttr ".otn" -type "string" "Output Transform (P3-D60)";
	setAttr ".potn" -type "string" "Output Transform (P3-D60)";
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
	setAttr -k off ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off ".eeaa";
	setAttr -k off ".engm";
	setAttr -k off ".mes";
	setAttr -k off ".emb";
	setAttr -k off ".mbbf";
	setAttr -k off ".mbs";
	setAttr -k off ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".enpt";
	setAttr -k off ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off ".twa";
	setAttr -k off ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
connectAttr "polyPlane2.out" "BASEShape.i";
connectAttr "polyPlane3.out" "pPlaneShape1.i";
connectAttr "polyPlane5.out" "BASE1Shape.i";
connectAttr "polyPlane6.out" "pPlaneShape2.i";
connectAttr "polyPlane8.out" "BASE2Shape.i";
connectAttr "polyPlane9.out" "pPlaneShape3.i";
connectAttr "polyPlane11.out" "BASE3Shape.i";
connectAttr "polyPlane12.out" "pPlaneShape4.i";
connectAttr "makeNurbCircle1.oc" "ControlShape.cr";
connectAttr "cluster1GroupId.id" "deformMeshShape.iog.og[0].gid";
connectAttr "cluster1Set.mwc" "deformMeshShape.iog.og[0].gco";
connectAttr "groupId2.id" "deformMeshShape.iog.og[1].gid";
connectAttr "tweakSet1.mwc" "deformMeshShape.iog.og[1].gco";
connectAttr "cluster2GroupId.id" "deformMeshShape.iog.og[2].gid";
connectAttr "cluster2Set.mwc" "deformMeshShape.iog.og[2].gco";
connectAttr "cluster2.og[0]" "deformMeshShape.i";
connectAttr "tweak1.vl[0].vt[0]" "deformMeshShape.twl";
connectAttr "polyPlane13.out" "deformMeshShapeOrig.i";
connectAttr "polyPlane14.out" "BASE4Shape.i";
connectAttr "polyPlane15.out" "pPlaneShape5.i";
connectAttr "C_lipSingle_CPT.msg" "C_lipSingle_CPT.root";
connectAttr "C_lipSingle_CTL.msg" "C_lipSingle_CPT.control";
connectAttr "C_lipSingleBuffer2_GRP.msg" "C_lipSingle_CPT.transform";
connectAttr "C_lipSingle_CPT.msg" "C_lipSingle_LOC.root";
connectAttr "C_lipSingle_GCS_DCP.ot" "C_lipSingle_LOC.t";
connectAttr "C_lipSingle_CPT.msg" "C_lipSingleBuffer2_GRP.root";
connectAttr "C_lipSingle_GCS.msg" "C_lipSingleBuffer2_GRP.geoConstraint";
connectAttr "C_lipSingle_CPT.msg" "C_lipSingleBuffer1_GRP.root";
connectAttr "C_lipSingle_CPT.msg" "C_lipSingle_CTL.root";
connectAttr "C_lipSingle_CTL.gimbal_vis" "curveShape2.v" -l on;
connectAttr "L_lipPrime00_CPT.msg" "L_lipPrime00_CPT.root";
connectAttr "L_lipPrime00_CTL.msg" "L_lipPrime00_CPT.control";
connectAttr "L_lipPrime00Buffer2_GRP.msg" "L_lipPrime00_CPT.transform";
connectAttr "L_lipPrime00_CPT.msg" "L_lipPrime00_LOC.root";
connectAttr "L_lipPrime00_GCS_DCP.ot" "L_lipPrime00_LOC.t";
connectAttr "L_lipPrime00_CPT.msg" "L_lipPrime00Buffer2_GRP.root";
connectAttr "L_lipPrime00_GCS.msg" "L_lipPrime00Buffer2_GRP.geoConstraint";
connectAttr "L_lipPrime00_CPT.msg" "L_lipPrime00Buffer1_GRP.root";
connectAttr "L_lipPrime00_CPT.msg" "L_lipPrime00_CTL.root";
connectAttr "L_lipPrime00_CTL.gimbal_vis" "curveShape4.v" -l on;
connectAttr "C_lipPrime_CPT.msg" "C_lipPrime_CPT.root";
connectAttr "C_lipPrime_CTL.msg" "C_lipPrime_CPT.control";
connectAttr "C_lipPrimeBuffer2_GRP.msg" "C_lipPrime_CPT.transform";
connectAttr "C_lipPrime_CPT.msg" "C_lipPrime_LOC.root";
connectAttr "C_lipPrime_GCS_DCP.ot" "C_lipPrime_LOC.t";
connectAttr "C_lipPrime_CPT.msg" "C_lipPrimeBuffer2_GRP.root";
connectAttr "C_lipPrime_GCS.msg" "C_lipPrimeBuffer2_GRP.geoConstraint";
connectAttr "C_lipPrime_CPT.msg" "C_lipPrimeBuffer1_GRP.root";
connectAttr "C_lipPrime_CPT.msg" "C_lipPrime_CTL.root";
connectAttr "C_lipPrime_CTL.gimbal_vis" "curveShape6.v" -l on;
connectAttr "R_lipPrime00_CPT.msg" "R_lipPrime00_CPT.root";
connectAttr "R_lipPrime00_CTL.msg" "R_lipPrime00_CPT.control";
connectAttr "R_lipPrime00Buffer2_GRP.msg" "R_lipPrime00_CPT.transform";
connectAttr "R_lipPrime00_CPT.msg" "R_lipPrime00_LOC.root";
connectAttr "R_lipPrime00_GCS_DCP.ot" "R_lipPrime00_LOC.t";
connectAttr "R_lipPrime00_CPT.msg" "R_lipPrime00Buffer2_GRP.root";
connectAttr "R_lipPrime00_GCS.msg" "R_lipPrime00Buffer2_GRP.geoConstraint";
connectAttr "R_lipPrime00_CPT.msg" "R_lipPrime00Buffer1_GRP.root";
connectAttr "R_lipPrime00_CPT.msg" "R_lipPrime00_CTL.root";
connectAttr "R_lipPrime00_CTL.gimbal_vis" "curveShape8.v" -l on;
connectAttr "L_lipSecondary00_CPT.msg" "L_lipSecondary00_CPT.root";
connectAttr "L_lipSecondary00_CTL.msg" "L_lipSecondary00_CPT.control";
connectAttr "L_lipSecondary00Buffer2_GRP.msg" "L_lipSecondary00_CPT.transform";
connectAttr "L_lipSecondary00_CPT.msg" "L_lipSecondary00_LOC.root";
connectAttr "L_lipSecondary00_GCS_DCP.ot" "L_lipSecondary00_LOC.t";
connectAttr "L_lipSecondary00_CPT.msg" "L_lipSecondary00Buffer2_GRP.root";
connectAttr "L_lipSecondary00_GCS.msg" "L_lipSecondary00Buffer2_GRP.geoConstraint"
		;
connectAttr "L_lipSecondary00_CPT.msg" "L_lipSecondary00Buffer1_GRP.root";
connectAttr "L_lipSecondary00_CPT.msg" "L_lipSecondary00_CTL.root";
connectAttr "L_lipSecondary00_CTL.gimbal_vis" "curveShape10.v" -l on;
connectAttr "L_lipSecondary01_CPT.msg" "L_lipSecondary01_CPT.root";
connectAttr "L_lipSecondary01_CTL.msg" "L_lipSecondary01_CPT.control";
connectAttr "L_lipSecondary01Buffer2_GRP.msg" "L_lipSecondary01_CPT.transform";
connectAttr "L_lipSecondary01_CPT.msg" "L_lipSecondary01_LOC.root";
connectAttr "L_lipSecondary01_GCS_DCP.ot" "L_lipSecondary01_LOC.t";
connectAttr "L_lipSecondary01_CPT.msg" "L_lipSecondary01Buffer2_GRP.root";
connectAttr "L_lipSecondary01_GCS.msg" "L_lipSecondary01Buffer2_GRP.geoConstraint"
		;
connectAttr "L_lipSecondary01_CPT.msg" "L_lipSecondary01Buffer1_GRP.root";
connectAttr "L_lipSecondary01_CPT.msg" "L_lipSecondary01_CTL.root";
connectAttr "L_lipSecondary01_CTL.gimbal_vis" "curveShape12.v" -l on;
connectAttr "L_lipSecondary02_CPT.msg" "L_lipSecondary02_CPT.root";
connectAttr "L_lipSecondary02_CTL.msg" "L_lipSecondary02_CPT.control";
connectAttr "L_lipSecondary02Buffer2_GRP.msg" "L_lipSecondary02_CPT.transform";
connectAttr "L_lipSecondary02_CPT.msg" "L_lipSecondary02_LOC.root";
connectAttr "L_lipSecondary02_GCS_DCP.ot" "L_lipSecondary02_LOC.t";
connectAttr "L_lipSecondary02_CPT.msg" "L_lipSecondary02Buffer2_GRP.root";
connectAttr "L_lipSecondary02_GCS.msg" "L_lipSecondary02Buffer2_GRP.geoConstraint"
		;
connectAttr "L_lipSecondary02_CPT.msg" "L_lipSecondary02Buffer1_GRP.root";
connectAttr "L_lipSecondary02_CPT.msg" "L_lipSecondary02_CTL.root";
connectAttr "L_lipSecondary02_CTL.gimbal_vis" "curveShape14.v" -l on;
connectAttr "L_lipSecondary03_CPT.msg" "L_lipSecondary03_CPT.root";
connectAttr "L_lipSecondary03_CTL.msg" "L_lipSecondary03_CPT.control";
connectAttr "L_lipSecondary03Buffer2_GRP.msg" "L_lipSecondary03_CPT.transform";
connectAttr "L_lipSecondary03_CPT.msg" "L_lipSecondary03_LOC.root";
connectAttr "L_lipSecondary03_GCS_DCP.ot" "L_lipSecondary03_LOC.t";
connectAttr "L_lipSecondary03_CPT.msg" "L_lipSecondary03Buffer2_GRP.root";
connectAttr "L_lipSecondary03_GCS.msg" "L_lipSecondary03Buffer2_GRP.geoConstraint"
		;
connectAttr "L_lipSecondary03_CPT.msg" "L_lipSecondary03Buffer1_GRP.root";
connectAttr "L_lipSecondary03_CPT.msg" "L_lipSecondary03_CTL.root";
connectAttr "L_lipSecondary03_CTL.gimbal_vis" "curveShape16.v" -l on;
connectAttr "L_lipSecondary04_CPT.msg" "L_lipSecondary04_CPT.root";
connectAttr "L_lipSecondary04_CTL.msg" "L_lipSecondary04_CPT.control";
connectAttr "L_lipSecondary04Buffer2_GRP.msg" "L_lipSecondary04_CPT.transform";
connectAttr "L_lipSecondary04_CPT.msg" "L_lipSecondary04_LOC.root";
connectAttr "L_lipSecondary04_GCS_DCP.ot" "L_lipSecondary04_LOC.t";
connectAttr "L_lipSecondary04_CPT.msg" "L_lipSecondary04Buffer2_GRP.root";
connectAttr "L_lipSecondary04_GCS.msg" "L_lipSecondary04Buffer2_GRP.geoConstraint"
		;
connectAttr "L_lipSecondary04_CPT.msg" "L_lipSecondary04Buffer1_GRP.root";
connectAttr "L_lipSecondary04_CPT.msg" "L_lipSecondary04_CTL.root";
connectAttr "L_lipSecondary04_CTL.gimbal_vis" "curveShape18.v" -l on;
connectAttr "C_lipSecondary_CPT.msg" "C_lipSecondary_CPT.root";
connectAttr "C_lipSecondary_CTL.msg" "C_lipSecondary_CPT.control";
connectAttr "C_lipSecondaryBuffer2_GRP.msg" "C_lipSecondary_CPT.transform";
connectAttr "C_lipSecondary_CPT.msg" "C_lipSecondary_LOC.root";
connectAttr "C_lipSecondary_GCS_DCP.ot" "C_lipSecondary_LOC.t";
connectAttr "C_lipSecondary_CPT.msg" "C_lipSecondaryBuffer2_GRP.root";
connectAttr "C_lipSecondary_GCS.msg" "C_lipSecondaryBuffer2_GRP.geoConstraint";
connectAttr "C_lipSecondary_CPT.msg" "C_lipSecondaryBuffer1_GRP.root";
connectAttr "C_lipSecondary_CPT.msg" "C_lipSecondary_CTL.root";
connectAttr "C_lipSecondary_CTL.gimbal_vis" "curveShape20.v" -l on;
connectAttr "R_lipSecondary04_CPT.msg" "R_lipSecondary04_CPT.root";
connectAttr "R_lipSecondary04_CTL.msg" "R_lipSecondary04_CPT.control";
connectAttr "R_lipSecondary04Buffer2_GRP.msg" "R_lipSecondary04_CPT.transform";
connectAttr "R_lipSecondary04_CPT.msg" "R_lipSecondary04_LOC.root";
connectAttr "R_lipSecondary04_GCS_DCP.ot" "R_lipSecondary04_LOC.t";
connectAttr "R_lipSecondary04_CPT.msg" "R_lipSecondary04Buffer2_GRP.root";
connectAttr "R_lipSecondary04_GCS.msg" "R_lipSecondary04Buffer2_GRP.geoConstraint"
		;
connectAttr "R_lipSecondary04_CPT.msg" "R_lipSecondary04Buffer1_GRP.root";
connectAttr "R_lipSecondary04_CPT.msg" "R_lipSecondary04_CTL.root";
connectAttr "R_lipSecondary04_CTL.gimbal_vis" "curveShape22.v" -l on;
connectAttr "R_lipSecondary03_CPT.msg" "R_lipSecondary03_CPT.root";
connectAttr "R_lipSecondary03_CTL.msg" "R_lipSecondary03_CPT.control";
connectAttr "R_lipSecondary03Buffer2_GRP.msg" "R_lipSecondary03_CPT.transform";
connectAttr "R_lipSecondary03_CPT.msg" "R_lipSecondary03_LOC.root";
connectAttr "R_lipSecondary03_GCS_DCP.ot" "R_lipSecondary03_LOC.t";
connectAttr "R_lipSecondary03_CPT.msg" "R_lipSecondary03Buffer2_GRP.root";
connectAttr "R_lipSecondary03_GCS.msg" "R_lipSecondary03Buffer2_GRP.geoConstraint"
		;
connectAttr "R_lipSecondary03_CPT.msg" "R_lipSecondary03Buffer1_GRP.root";
connectAttr "R_lipSecondary03_CPT.msg" "R_lipSecondary03_CTL.root";
connectAttr "R_lipSecondary03_CTL.gimbal_vis" "curveShape24.v" -l on;
connectAttr "R_lipSecondary02_CPT.msg" "R_lipSecondary02_CPT.root";
connectAttr "R_lipSecondary02_CTL.msg" "R_lipSecondary02_CPT.control";
connectAttr "R_lipSecondary02Buffer2_GRP.msg" "R_lipSecondary02_CPT.transform";
connectAttr "R_lipSecondary02_CPT.msg" "R_lipSecondary02_LOC.root";
connectAttr "R_lipSecondary02_GCS_DCP.ot" "R_lipSecondary02_LOC.t";
connectAttr "R_lipSecondary02_CPT.msg" "R_lipSecondary02Buffer2_GRP.root";
connectAttr "R_lipSecondary02_GCS.msg" "R_lipSecondary02Buffer2_GRP.geoConstraint"
		;
connectAttr "R_lipSecondary02_CPT.msg" "R_lipSecondary02Buffer1_GRP.root";
connectAttr "R_lipSecondary02_CPT.msg" "R_lipSecondary02_CTL.root";
connectAttr "R_lipSecondary02_CTL.gimbal_vis" "curveShape26.v" -l on;
connectAttr "R_lipSecondary01_CPT.msg" "R_lipSecondary01_CPT.root";
connectAttr "R_lipSecondary01_CTL.msg" "R_lipSecondary01_CPT.control";
connectAttr "R_lipSecondary01Buffer2_GRP.msg" "R_lipSecondary01_CPT.transform";
connectAttr "R_lipSecondary01_CPT.msg" "R_lipSecondary01_LOC.root";
connectAttr "R_lipSecondary01_GCS_DCP.ot" "R_lipSecondary01_LOC.t";
connectAttr "R_lipSecondary01_CPT.msg" "R_lipSecondary01Buffer2_GRP.root";
connectAttr "R_lipSecondary01_GCS.msg" "R_lipSecondary01Buffer2_GRP.geoConstraint"
		;
connectAttr "R_lipSecondary01_CPT.msg" "R_lipSecondary01Buffer1_GRP.root";
connectAttr "R_lipSecondary01_CPT.msg" "R_lipSecondary01_CTL.root";
connectAttr "R_lipSecondary01_CTL.gimbal_vis" "curveShape28.v" -l on;
connectAttr "R_lipSecondary00_CPT.msg" "R_lipSecondary00_CPT.root";
connectAttr "R_lipSecondary00_CTL.msg" "R_lipSecondary00_CPT.control";
connectAttr "R_lipSecondary00Buffer2_GRP.msg" "R_lipSecondary00_CPT.transform";
connectAttr "R_lipSecondary00_CPT.msg" "R_lipSecondary00_LOC.root";
connectAttr "R_lipSecondary00_GCS_DCP.ot" "R_lipSecondary00_LOC.t";
connectAttr "R_lipSecondary00_CPT.msg" "R_lipSecondary00Buffer2_GRP.root";
connectAttr "R_lipSecondary00_GCS.msg" "R_lipSecondary00Buffer2_GRP.geoConstraint"
		;
connectAttr "R_lipSecondary00_CPT.msg" "R_lipSecondary00Buffer1_GRP.root";
connectAttr "R_lipSecondary00_CPT.msg" "R_lipSecondary00_CTL.root";
connectAttr "R_lipSecondary00_CTL.gimbal_vis" "curveShape30.v" -l on;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "cluster1GroupParts.og" "cluster1.ip[0].ig";
connectAttr "cluster1GroupId.id" "cluster1.ip[0].gi";
connectAttr "cluster1Handle.wm" "cluster1.ma";
connectAttr "cluster1HandleShape.x" "cluster1.x";
connectAttr "TestWeights_UD.wlf[0]" "cluster1.wl[0]";
connectAttr "groupParts2.og" "tweak1.ip[0].ig";
connectAttr "groupId2.id" "tweak1.ip[0].gi";
connectAttr "cluster1GroupId.msg" "cluster1Set.gn" -na;
connectAttr "deformMeshShape.iog.og[0]" "cluster1Set.dsm" -na;
connectAttr "cluster1.msg" "cluster1Set.ub[0]";
connectAttr "tweak1.og[0]" "cluster1GroupParts.ig";
connectAttr "cluster1GroupId.id" "cluster1GroupParts.gi";
connectAttr "groupId2.msg" "tweakSet1.gn" -na;
connectAttr "deformMeshShape.iog.og[1]" "tweakSet1.dsm" -na;
connectAttr "tweak1.msg" "tweakSet1.ub[0]";
connectAttr "deformMeshShapeOrig.w" "groupParts2.ig";
connectAttr "groupId2.id" "groupParts2.gi";
connectAttr "cluster2GroupParts.og" "cluster2.ip[0].ig";
connectAttr "cluster2GroupId.id" "cluster2.ip[0].gi";
connectAttr "cluster2Handle.wm" "cluster2.ma";
connectAttr "cluster2HandleShape.x" "cluster2.x";
connectAttr "TestWeights_LR.wlf[0]" "cluster2.wl[0]";
connectAttr "cluster2GroupId.msg" "cluster2Set.gn" -na;
connectAttr "deformMeshShape.iog.og[2]" "cluster2Set.dsm" -na;
connectAttr "cluster2.msg" "cluster2Set.ub[0]";
connectAttr "cluster1.og[0]" "cluster2GroupParts.ig";
connectAttr "cluster2GroupId.id" "cluster2GroupParts.gi";
connectAttr "BASE4Shape.membershipWeights" "TestCurveWeights.mweights";
connectAttr "pPlaneShape5.w" "TestCurveWeights.pmesh";
connectAttr "BASE4Shape.w" "TestCurveWeights.inmesh";
connectAttr "C_lipSingle_ACV.o" "TestCurveWeights.inputs[0].acu";
connectAttr "C_lipSingleFalloff_ACV.o" "TestCurveWeights.inputs[0].acv";
connectAttr "C_lipSingle_CTL.sx" "TestCurveWeights.inputs[0].falloffu";
connectAttr "L_lipPrime00_ACV.o" "TestCurveWeights.inputs[1].acu";
connectAttr "L_lipPrimeFalloff0_ACV.o" "TestCurveWeights.inputs[1].acv";
connectAttr "L_lipPrime00_CTL.sx" "TestCurveWeights.inputs[1].falloffu";
connectAttr "C_lipPrime_ACV.o" "TestCurveWeights.inputs[2].acu";
connectAttr "C_lipPrimeFalloff_ACV.o" "TestCurveWeights.inputs[2].acv";
connectAttr "C_lipPrime_CTL.sx" "TestCurveWeights.inputs[2].falloffu";
connectAttr "R_lipPrime00_ACV.o" "TestCurveWeights.inputs[3].acu";
connectAttr "R_lipPrimeFalloff0_ACV.o" "TestCurveWeights.inputs[3].acv";
connectAttr "R_lipPrime00_CTL.sx" "TestCurveWeights.inputs[3].falloffu";
connectAttr "L_lipSecondary00_ACV.o" "TestCurveWeights.inputs[4].acu";
connectAttr "L_lipSecondaryFalloff0_ACV.o" "TestCurveWeights.inputs[4].acv";
connectAttr "L_lipSecondary00_CTL.sx" "TestCurveWeights.inputs[4].falloffu";
connectAttr "L_lipSecondary01_ACV.o" "TestCurveWeights.inputs[5].acu";
connectAttr "L_lipSecondaryFalloff1_ACV.o" "TestCurveWeights.inputs[5].acv";
connectAttr "L_lipSecondary01_CTL.sx" "TestCurveWeights.inputs[5].falloffu";
connectAttr "L_lipSecondary02_ACV.o" "TestCurveWeights.inputs[6].acu";
connectAttr "L_lipSecondaryFalloff2_ACV.o" "TestCurveWeights.inputs[6].acv";
connectAttr "L_lipSecondary02_CTL.sx" "TestCurveWeights.inputs[6].falloffu";
connectAttr "L_lipSecondary03_ACV.o" "TestCurveWeights.inputs[7].acu";
connectAttr "L_lipSecondaryFalloff3_ACV.o" "TestCurveWeights.inputs[7].acv";
connectAttr "L_lipSecondary03_CTL.sx" "TestCurveWeights.inputs[7].falloffu";
connectAttr "L_lipSecondary04_ACV.o" "TestCurveWeights.inputs[8].acu";
connectAttr "L_lipSecondaryFalloff4_ACV.o" "TestCurveWeights.inputs[8].acv";
connectAttr "L_lipSecondary04_CTL.sx" "TestCurveWeights.inputs[8].falloffu";
connectAttr "C_lipSecondary_ACV.o" "TestCurveWeights.inputs[9].acu";
connectAttr "C_lipSecondaryFalloff_ACV.o" "TestCurveWeights.inputs[9].acv";
connectAttr "C_lipSecondary_CTL.sx" "TestCurveWeights.inputs[9].falloffu";
connectAttr "R_lipSecondary04_ACV.o" "TestCurveWeights.inputs[10].acu";
connectAttr "R_lipSecondaryFalloff4_ACV.o" "TestCurveWeights.inputs[10].acv";
connectAttr "R_lipSecondary04_CTL.sx" "TestCurveWeights.inputs[10].falloffu";
connectAttr "R_lipSecondary03_ACV.o" "TestCurveWeights.inputs[11].acu";
connectAttr "R_lipSecondaryFalloff3_ACV.o" "TestCurveWeights.inputs[11].acv";
connectAttr "R_lipSecondary03_CTL.sx" "TestCurveWeights.inputs[11].falloffu";
connectAttr "R_lipSecondary02_ACV.o" "TestCurveWeights.inputs[12].acu";
connectAttr "R_lipSecondaryFalloff2_ACV.o" "TestCurveWeights.inputs[12].acv";
connectAttr "R_lipSecondary02_CTL.sx" "TestCurveWeights.inputs[12].falloffu";
connectAttr "R_lipSecondary01_ACV.o" "TestCurveWeights.inputs[13].acu";
connectAttr "R_lipSecondaryFalloff1_ACV.o" "TestCurveWeights.inputs[13].acv";
connectAttr "R_lipSecondary01_CTL.sx" "TestCurveWeights.inputs[13].falloffu";
connectAttr "R_lipSecondary00_ACV.o" "TestCurveWeights.inputs[14].acu";
connectAttr "R_lipSecondaryFalloff0_ACV.o" "TestCurveWeights.inputs[14].acv";
connectAttr "R_lipSecondary00_CTL.sx" "TestCurveWeights.inputs[14].falloffu";
connectAttr "TestCurveWeights.outDoubleweights[0].owd" "TestWeights_UD.inputs[0].iw"
		;
connectAttr "C_lipSingle_CTL.speedtyout" "TestWeights_UD.inputs[0].f";
connectAttr "TestCurveWeights.outDoubleweights[1].owd" "TestWeights_UD.inputs[1].iw"
		;
connectAttr "L_lipPrime00_CTL.speedtyout" "TestWeights_UD.inputs[1].f";
connectAttr "TestCurveWeights.outDoubleweights[2].owd" "TestWeights_UD.inputs[2].iw"
		;
connectAttr "C_lipPrime_CTL.speedtyout" "TestWeights_UD.inputs[2].f";
connectAttr "TestCurveWeights.outDoubleweights[3].owd" "TestWeights_UD.inputs[3].iw"
		;
connectAttr "R_lipPrime00_CTL.speedtyout" "TestWeights_UD.inputs[3].f";
connectAttr "TestCurveWeights.outDoubleweights[4].owd" "TestWeights_UD.inputs[4].iw"
		;
connectAttr "L_lipSecondary00_CTL.speedtyout" "TestWeights_UD.inputs[4].f";
connectAttr "TestCurveWeights.outDoubleweights[5].owd" "TestWeights_UD.inputs[5].iw"
		;
connectAttr "L_lipSecondary01_CTL.speedtyout" "TestWeights_UD.inputs[5].f";
connectAttr "TestCurveWeights.outDoubleweights[6].owd" "TestWeights_UD.inputs[6].iw"
		;
connectAttr "L_lipSecondary02_CTL.speedtyout" "TestWeights_UD.inputs[6].f";
connectAttr "TestCurveWeights.outDoubleweights[7].owd" "TestWeights_UD.inputs[7].iw"
		;
connectAttr "L_lipSecondary03_CTL.speedtyout" "TestWeights_UD.inputs[7].f";
connectAttr "TestCurveWeights.outDoubleweights[8].owd" "TestWeights_UD.inputs[8].iw"
		;
connectAttr "L_lipSecondary04_CTL.speedtyout" "TestWeights_UD.inputs[8].f";
connectAttr "TestCurveWeights.outDoubleweights[9].owd" "TestWeights_UD.inputs[9].iw"
		;
connectAttr "C_lipSecondary_CTL.speedtyout" "TestWeights_UD.inputs[9].f";
connectAttr "TestCurveWeights.outDoubleweights[10].owd" "TestWeights_UD.inputs[10].iw"
		;
connectAttr "R_lipSecondary04_CTL.speedtyout" "TestWeights_UD.inputs[10].f";
connectAttr "TestCurveWeights.outDoubleweights[11].owd" "TestWeights_UD.inputs[11].iw"
		;
connectAttr "R_lipSecondary03_CTL.speedtyout" "TestWeights_UD.inputs[11].f";
connectAttr "TestCurveWeights.outDoubleweights[12].owd" "TestWeights_UD.inputs[12].iw"
		;
connectAttr "R_lipSecondary02_CTL.speedtyout" "TestWeights_UD.inputs[12].f";
connectAttr "TestCurveWeights.outDoubleweights[13].owd" "TestWeights_UD.inputs[13].iw"
		;
connectAttr "R_lipSecondary01_CTL.speedtyout" "TestWeights_UD.inputs[13].f";
connectAttr "TestCurveWeights.outDoubleweights[14].owd" "TestWeights_UD.inputs[14].iw"
		;
connectAttr "R_lipSecondary00_CTL.speedtyout" "TestWeights_UD.inputs[14].f";
connectAttr "TestCurveWeights.outDoubleweights[0].owd" "TestWeights_LR.inputs[0].iw"
		;
connectAttr "C_lipSingle_CTL.speedtxout" "TestWeights_LR.inputs[0].f";
connectAttr "TestCurveWeights.outDoubleweights[1].owd" "TestWeights_LR.inputs[1].iw"
		;
connectAttr "L_lipPrime00_CTL.speedtxout" "TestWeights_LR.inputs[1].f";
connectAttr "TestCurveWeights.outDoubleweights[2].owd" "TestWeights_LR.inputs[2].iw"
		;
connectAttr "C_lipPrime_CTL.speedtxout" "TestWeights_LR.inputs[2].f";
connectAttr "TestCurveWeights.outDoubleweights[3].owd" "TestWeights_LR.inputs[3].iw"
		;
connectAttr "R_lipPrime00_CTL.speedtxout" "TestWeights_LR.inputs[3].f";
connectAttr "TestCurveWeights.outDoubleweights[4].owd" "TestWeights_LR.inputs[4].iw"
		;
connectAttr "L_lipSecondary00_CTL.speedtxout" "TestWeights_LR.inputs[4].f";
connectAttr "TestCurveWeights.outDoubleweights[5].owd" "TestWeights_LR.inputs[5].iw"
		;
connectAttr "L_lipSecondary01_CTL.speedtxout" "TestWeights_LR.inputs[5].f";
connectAttr "TestCurveWeights.outDoubleweights[6].owd" "TestWeights_LR.inputs[6].iw"
		;
connectAttr "L_lipSecondary02_CTL.speedtxout" "TestWeights_LR.inputs[6].f";
connectAttr "TestCurveWeights.outDoubleweights[7].owd" "TestWeights_LR.inputs[7].iw"
		;
connectAttr "L_lipSecondary03_CTL.speedtxout" "TestWeights_LR.inputs[7].f";
connectAttr "TestCurveWeights.outDoubleweights[8].owd" "TestWeights_LR.inputs[8].iw"
		;
connectAttr "L_lipSecondary04_CTL.speedtxout" "TestWeights_LR.inputs[8].f";
connectAttr "TestCurveWeights.outDoubleweights[9].owd" "TestWeights_LR.inputs[9].iw"
		;
connectAttr "C_lipSecondary_CTL.speedtxout" "TestWeights_LR.inputs[9].f";
connectAttr "TestCurveWeights.outDoubleweights[10].owd" "TestWeights_LR.inputs[10].iw"
		;
connectAttr "R_lipSecondary04_CTL.speedtxout" "TestWeights_LR.inputs[10].f";
connectAttr "TestCurveWeights.outDoubleweights[11].owd" "TestWeights_LR.inputs[11].iw"
		;
connectAttr "R_lipSecondary03_CTL.speedtxout" "TestWeights_LR.inputs[11].f";
connectAttr "TestCurveWeights.outDoubleweights[12].owd" "TestWeights_LR.inputs[12].iw"
		;
connectAttr "R_lipSecondary02_CTL.speedtxout" "TestWeights_LR.inputs[12].f";
connectAttr "TestCurveWeights.outDoubleweights[13].owd" "TestWeights_LR.inputs[13].iw"
		;
connectAttr "R_lipSecondary01_CTL.speedtxout" "TestWeights_LR.inputs[13].f";
connectAttr "TestCurveWeights.outDoubleweights[14].owd" "TestWeights_LR.inputs[14].iw"
		;
connectAttr "R_lipSecondary00_CTL.speedtxout" "TestWeights_LR.inputs[14].f";
connectAttr "deformMeshShape.w" "C_lipSingle_GCS.inmesh";
connectAttr "C_lipSingle_GCS.outmatrix" "C_lipSingle_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "L_lipPrime00_GCS.inmesh";
connectAttr "L_lipPrime00_GCS.outmatrix" "L_lipPrime00_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "C_lipPrime_GCS.inmesh";
connectAttr "C_lipPrime_GCS.outmatrix" "C_lipPrime_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "R_lipPrime00_GCS.inmesh";
connectAttr "R_lipPrime00_GCS.outmatrix" "R_lipPrime00_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "L_lipSecondary00_GCS.inmesh";
connectAttr "L_lipSecondary00_GCS.outmatrix" "L_lipSecondary00_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "L_lipSecondary01_GCS.inmesh";
connectAttr "L_lipSecondary01_GCS.outmatrix" "L_lipSecondary01_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "L_lipSecondary02_GCS.inmesh";
connectAttr "L_lipSecondary02_GCS.outmatrix" "L_lipSecondary02_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "L_lipSecondary03_GCS.inmesh";
connectAttr "L_lipSecondary03_GCS.outmatrix" "L_lipSecondary03_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "L_lipSecondary04_GCS.inmesh";
connectAttr "L_lipSecondary04_GCS.outmatrix" "L_lipSecondary04_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "C_lipSecondary_GCS.inmesh";
connectAttr "C_lipSecondary_GCS.outmatrix" "C_lipSecondary_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "R_lipSecondary04_GCS.inmesh";
connectAttr "R_lipSecondary04_GCS.outmatrix" "R_lipSecondary04_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "R_lipSecondary03_GCS.inmesh";
connectAttr "R_lipSecondary03_GCS.outmatrix" "R_lipSecondary03_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "R_lipSecondary02_GCS.inmesh";
connectAttr "R_lipSecondary02_GCS.outmatrix" "R_lipSecondary02_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "R_lipSecondary01_GCS.inmesh";
connectAttr "R_lipSecondary01_GCS.outmatrix" "R_lipSecondary01_GCS_DCP.imat";
connectAttr "deformMeshShape.w" "R_lipSecondary00_GCS.inmesh";
connectAttr "R_lipSecondary00_GCS.outmatrix" "R_lipSecondary00_GCS_DCP.imat";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "BASEShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "pPlaneShape1.iog" ":initialShadingGroup.dsm" -na;
connectAttr "BASE1Shape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "pPlaneShape2.iog" ":initialShadingGroup.dsm" -na;
connectAttr "BASE2Shape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "pPlaneShape3.iog" ":initialShadingGroup.dsm" -na;
connectAttr "BASE3Shape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "pPlaneShape4.iog" ":initialShadingGroup.dsm" -na;
connectAttr "deformMeshShape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "BASE4Shape.iog" ":initialShadingGroup.dsm" -na;
connectAttr "pPlaneShape5.iog" ":initialShadingGroup.dsm" -na;
// End of MID_LIP_CURVES.ma
