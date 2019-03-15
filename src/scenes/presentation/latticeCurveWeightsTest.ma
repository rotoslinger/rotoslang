//Maya ASCII 2018ff09 scene
//Name: latticeCurveWeightsTest.ma
//Last modified: Thu, Mar 14, 2019 07:58:59 PM
//Codeset: UTF-8
requires maya "2018ff09";
requires -nodeType "glimpseGlobals" "glimpseMaya" "03.22.05";
requires -nodeType "assetResolverConfig" "assetResolverMaya" "AssetResolverMaya 1.0";
requires "AL_MayaExtensionAttributes" "1.0";
requires -nodeType "ALF_globals" -dataType "ALF_data" "ALF" "ALF 0.0";
requires -nodeType "LHCurveWeightNode" "collision" "1.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201811281902-7c8857228f";
fileInfo "osv" "Linux 3.10.0-693.21.1.el7.x86_64 #1 SMP Wed Mar 7 19:03:37 UTC 2018 x86_64";
createNode transform -s -n "persp";
	rename -uid "5D2FB100-0001-F410-5C8B-11AB0000026D";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -3.152987883968482 2.763947278265471 8.7577607568205611 ;
	setAttr ".r" -type "double3" -16.53835272954872 -19.800000000001038 -8.4510035341637258e-16 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "5D2FB100-0001-F410-5C8B-11AB0000026E";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 9.7097430773005104;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "5D2FB100-0001-F410-5C8B-11AB0000026F";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "5D2FB100-0001-F410-5C8B-11AB00000270";
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
	rename -uid "5D2FB100-0001-F410-5C8B-11AB00000271";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "5D2FB100-0001-F410-5C8B-11AB00000272";
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
	rename -uid "5D2FB100-0001-F410-5C8B-11AB00000273";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "5D2FB100-0001-F410-5C8B-11AB00000274";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "pSphere1";
	rename -uid "5D2FB100-0001-F410-5C8B-11B50000028B";
createNode mesh -n "pSphereShape1" -p "pSphere1";
	rename -uid "5D2FB100-0001-F410-5C8B-11B50000028A";
	setAttr -k off ".v";
	setAttr -s 4 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode mesh -n "pSphereShape1Orig" -p "pSphere1";
	rename -uid "5D2FB100-0001-F410-5C8B-11B900000291";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "ffd1Lattice";
	rename -uid "5D2FB100-0001-F410-5C8B-11B90000028E";
	setAttr ".t" -type "double3" -1.1920928955078125e-07 0 -1.7881393432617188e-07 ;
	setAttr ".s" -type "double3" 2.0000002384185791 2 2.0000005960464478 ;
createNode lattice -n "ffd1LatticeShape" -p "ffd1Lattice";
	rename -uid "5D2FB100-0001-F410-5C8B-11B900000290";
	addAttr -ci true -sn "wireMembership" -ln "wireMembership" -dt "doubleArray";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr -s 4 ".iog[0].og";
	setAttr ".tw" yes;
	setAttr ".sd" 5;
	setAttr ".ud" 5;
	setAttr ".wireMembership" -type "doubleArray" 125 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
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
createNode lattice -n "ffd1LatticeShapeOrig" -p "ffd1Lattice";
	rename -uid "06C2F100-0002-8846-5C8B-148A00000289";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".sd" 5;
	setAttr ".ud" 5;
	setAttr ".cc" -type "lattice" 5 5 5 125 -0.5 -0.5 -0.5 -0.25
		 -0.5 -0.5 0 -0.5 -0.5 0.25 -0.5 -0.5 0.5 -0.5 -0.5 -0.5
		 -0.25 -0.5 -0.25 -0.25 -0.5 0 -0.25 -0.5 0.25 -0.25 -0.5 0.5
		 -0.25 -0.5 -0.5 0 -0.5 -0.25 0 -0.5 0 0 -0.5 0.25
		 0 -0.5 0.5 0 -0.5 -0.5 0.25 -0.5 -0.25 0.25 -0.5 0
		 0.25 -0.5 0.25 0.25 -0.5 0.5 0.25 -0.5 -0.5 0.5 -0.5 -0.25
		 0.5 -0.5 0 0.5 -0.5 0.25 0.5 -0.5 0.5 0.5 -0.5 -0.5
		 -0.5 -0.25 -0.25 -0.5 -0.25 0 -0.5 -0.25 0.25 -0.5 -0.25 0.5
		 -0.5 -0.25 -0.5 -0.25 -0.25 -0.25 -0.25 -0.25 0 -0.25 -0.25 0.25
		 -0.25 -0.25 0.5 -0.25 -0.25 -0.5 0 -0.25 -0.25 0 -0.25 0
		 0 -0.25 0.25 0 -0.25 0.5 0 -0.25 -0.5 0.25 -0.25 -0.25
		 0.25 -0.25 0 0.25 -0.25 0.25 0.25 -0.25 0.5 0.25 -0.25 -0.5
		 0.5 -0.25 -0.25 0.5 -0.25 0 0.5 -0.25 0.25 0.5 -0.25 0.5
		 0.5 -0.25 -0.5 -0.5 0 -0.25 -0.5 0 0 -0.5 0 0.25
		 -0.5 0 0.5 -0.5 0 -0.5 -0.25 0 -0.25 -0.25 0 0
		 -0.25 0 0.25 -0.25 0 0.5 -0.25 0 -0.5 0 0 -0.25
		 0 0 0 0 0 0.25 0 0 0.5 0 0 -0.5
		 0.25 0 -0.25 0.25 0 0 0.25 0 0.25 0.25 0 0.5
		 0.25 0 -0.5 0.5 0 -0.25 0.5 0 0 0.5 0 0.25
		 0.5 0 0.5 0.5 0 -0.5 -0.5 0.25 -0.25 -0.5 0.25 0
		 -0.5 0.25 0.25 -0.5 0.25 0.5 -0.5 0.25 -0.5 -0.25 0.25 -0.25
		 -0.25 0.25 0 -0.25 0.25 0.25 -0.25 0.25 0.5 -0.25 0.25 -0.5
		 0 0.25 -0.25 0 0.25 0 0 0.25 0.25 0 0.25 0.5
		 0 0.25 -0.5 0.25 0.25 -0.25 0.25 0.25 0 0.25 0.25 0.25
		 0.25 0.25 0.5 0.25 0.25 -0.5 0.5 0.25 -0.25 0.5 0.25 0
		 0.5 0.25 0.25 0.5 0.25 0.5 0.5 0.25 -0.5 -0.5 0.5 -0.25
		 -0.5 0.5 0 -0.5 0.5 0.25 -0.5 0.5 0.5 -0.5 0.5 -0.5
		 -0.25 0.5 -0.25 -0.25 0.5 0 -0.25 0.5 0.25 -0.25 0.5 0.5
		 -0.25 0.5 -0.5 0 0.5 -0.25 0 0.5 0 0 0.5 0.25
		 0 0.5 0.5 0 0.5 -0.5 0.25 0.5 -0.25 0.25 0.5 0
		 0.25 0.5 0.25 0.25 0.5 0.5 0.25 0.5 -0.5 0.5 0.5 -0.25
		 0.5 0.5 0 0.5 0.5 0.25 0.5 0.5 0.5 0.5 0.5 ;
createNode transform -n "ffd1Base";
	rename -uid "5D2FB100-0001-F410-5C8B-11B90000028D";
	setAttr ".t" -type "double3" -1.1920928955078125e-07 0 -1.7881393432617188e-07 ;
	setAttr ".s" -type "double3" 2.0000002384185791 2 2.0000005960464478 ;
createNode baseLattice -n "ffd1BaseShape" -p "ffd1Base";
	rename -uid "5D2FB100-0001-F410-5C8B-11B90000028F";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
createNode transform -n "pPlane1";
	rename -uid "5D2FB100-0001-F410-5C8B-11D00000029B";
	setAttr ".rp" -type "double3" 0 0 1.4034363292323482 ;
	setAttr ".sp" -type "double3" 0 0 1.4034363292323482 ;
createNode mesh -n "pPlaneShape1" -p "pPlane1";
	rename -uid "5D2FB100-0001-F410-5C8B-11D00000029A";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "ffd1LatticeWEIGHTBASE";
	rename -uid "06C2F100-0002-8846-5C8B-14A4000002AA";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -1.1920928955078125e-07 0 -1.7881393432617188e-07 ;
	setAttr ".s" -type "double3" 2.0000002384185791 2 2.0000005960464478 ;
createNode lattice -n "ffd1LatticeWEIGHTBASEShape" -p "ffd1LatticeWEIGHTBASE";
	rename -uid "06C2F100-0002-8846-5C8B-14A4000002AB";
	addAttr -ci true -sn "wireMembership" -ln "wireMembership" -dt "doubleArray";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".sd" 5;
	setAttr ".ud" 5;
	setAttr ".cc" -type "lattice" 5 5 5 125 -0.5 -0.5 -0.5 -0.25
		 -0.5 -0.5 0 -0.5 -0.5 0.25 -0.5 -0.5 0.5 -0.5 -0.5 -0.5
		 -0.25 -0.5 -0.25 -0.25 -0.5 0 -0.25 -0.5 0.25 -0.25 -0.5 0.5
		 -0.25 -0.5 -0.5 0 -0.5 -0.25 0 -0.5 0 0 -0.5 0.25
		 0 -0.5 0.5 0 -0.5 -0.5 0.25 -0.5 -0.25 0.25 -0.5 0
		 0.25 -0.5 0.25 0.25 -0.5 0.5 0.25 -0.5 -0.5 0.5 -0.5 -0.25
		 0.5 -0.5 0 0.5 -0.5 0.25 0.5 -0.5 0.5 0.5 -0.5 -0.5
		 -0.5 -0.25 -0.25 -0.5 -0.25 0 -0.5 -0.25 0.25 -0.5 -0.25 0.5
		 -0.5 -0.25 -0.5 -0.25 -0.25 -0.25 -0.25 -0.25 0 -0.25 -0.25 0.25
		 -0.25 -0.25 0.5 -0.25 -0.25 -0.5 0 -0.25 -0.25 0 -0.25 0
		 0 -0.25 0.25 0 -0.25 0.5 0 -0.25 -0.5 0.25 -0.25 -0.25
		 0.25 -0.25 0 0.25 -0.25 0.25 0.25 -0.25 0.5 0.25 -0.25 -0.5
		 0.5 -0.25 -0.25 0.5 -0.25 0 0.5 -0.25 0.25 0.5 -0.25 0.5
		 0.5 -0.25 -0.5 -0.5 0 -0.25 -0.5 0 0 -0.5 0 0.25
		 -0.5 0 0.5 -0.5 0 -0.5 -0.25 0 -0.25 -0.25 0 0
		 -0.25 0 0.25 -0.25 0 0.5 -0.25 0 -0.5 0 0 -0.25
		 0 0 0 0 0 0.25 0 0 0.5 0 0 -0.5
		 0.25 0 -0.25 0.25 0 0 0.25 0 0.25 0.25 0 0.5
		 0.25 0 -0.5 0.5 0 -0.25 0.5 0 0 0.5 0 0.25
		 0.5 0 0.5 0.5 0 -0.5 -0.5 0.25 -0.25 -0.5 0.25 0
		 -0.5 0.25 0.25 -0.5 0.25 0.5 -0.5 0.25 -0.5 -0.25 0.25 -0.25
		 -0.25 0.25 0 -0.25 0.25 0.25 -0.25 0.25 0.5 -0.25 0.25 -0.5
		 0 0.25 -0.25 0 0.25 0 0 0.25 0.25 0 0.25 0.5
		 0 0.25 -0.5 0.25 0.25 -0.25 0.25 0.25 0 0.25 0.25 0.25
		 0.25 0.25 0.5 0.25 0.25 -0.5 0.5 0.25 -0.25 0.5 0.25 0
		 0.5 0.25 0.25 0.5 0.25 0.5 0.5 0.25 -0.5 -0.5 0.5 -0.25
		 -0.5 0.5 0 -0.5 0.5 0.25 -0.5 0.5 0.5 -0.5 0.5 -0.5
		 -0.25 0.5 -0.25 -0.25 0.5 0 -0.25 0.5 0.25 -0.25 0.5 0.5
		 -0.25 0.5 -0.5 0 0.5 -0.25 0 0.5 0 0 0.5 0.25
		 0 0.5 0.5 0 0.5 -0.5 0.25 0.5 -0.25 0.25 0.5 0
		 0.25 0.5 0.25 0.25 0.5 0.5 0.25 0.5 -0.5 0.5 0.5 -0.25
		 0.5 0.5 0 0.5 0.5 0.25 0.5 0.5 0.5 0.5 0.5 ;
	setAttr ".wireMembership" -type "doubleArray" 125 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1
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
createNode lattice -n "ffd1LatticeWEIGHTBASEShapeOrig" -p "ffd1LatticeWEIGHTBASE";
	rename -uid "06C2F100-0002-8846-5C8B-14A4000002B0";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".sd" 5;
	setAttr ".ud" 5;
	setAttr ".cc" -type "lattice" 5 5 5 125 -0.5 -0.5 -0.5 -0.25
		 -0.5 -0.5 0 -0.5 -0.5 0.25 -0.5 -0.5 0.5 -0.5 -0.5 -0.5
		 -0.25 -0.5 -0.25 -0.25 -0.5 0 -0.25 -0.5 0.25 -0.25 -0.5 0.5
		 -0.25 -0.5 -0.5 0 -0.5 -0.25 0 -0.5 0 0 -0.5 0.25
		 0 -0.5 0.5 0 -0.5 -0.5 0.25 -0.5 -0.25 0.25 -0.5 0
		 0.25 -0.5 0.25 0.25 -0.5 0.5 0.25 -0.5 -0.5 0.5 -0.5 -0.25
		 0.5 -0.5 0 0.5 -0.5 0.25 0.5 -0.5 0.5 0.5 -0.5 -0.5
		 -0.5 -0.25 -0.25 -0.5 -0.25 0 -0.5 -0.25 0.25 -0.5 -0.25 0.5
		 -0.5 -0.25 -0.5 -0.25 -0.25 -0.25 -0.25 -0.25 0 -0.25 -0.25 0.25
		 -0.25 -0.25 0.5 -0.25 -0.25 -0.5 0 -0.25 -0.25 0 -0.25 0
		 0 -0.25 0.25 0 -0.25 0.5 0 -0.25 -0.5 0.25 -0.25 -0.25
		 0.25 -0.25 0 0.25 -0.25 0.25 0.25 -0.25 0.5 0.25 -0.25 -0.5
		 0.5 -0.25 -0.25 0.5 -0.25 0 0.5 -0.25 0.25 0.5 -0.25 0.5
		 0.5 -0.25 -0.5 -0.5 0 -0.25 -0.5 0 0 -0.5 0 0.25
		 -0.5 0 0.5 -0.5 0 -0.5 -0.25 0 -0.25 -0.25 0 0
		 -0.25 0 0.25 -0.25 0 0.5 -0.25 0 -0.5 0 0 -0.25
		 0 0 0 0 0 0.25 0 0 0.5 0 0 -0.5
		 0.25 0 -0.25 0.25 0 0 0.25 0 0.25 0.25 0 0.5
		 0.25 0 -0.5 0.5 0 -0.25 0.5 0 0 0.5 0 0.25
		 0.5 0 0.5 0.5 0 -0.5 -0.5 0.25 -0.25 -0.5 0.25 0
		 -0.5 0.25 0.25 -0.5 0.25 0.5 -0.5 0.25 -0.5 -0.25 0.25 -0.25
		 -0.25 0.25 0 -0.25 0.25 0.25 -0.25 0.25 0.5 -0.25 0.25 -0.5
		 0 0.25 -0.25 0 0.25 0 0 0.25 0.25 0 0.25 0.5
		 0 0.25 -0.5 0.25 0.25 -0.25 0.25 0.25 0 0.25 0.25 0.25
		 0.25 0.25 0.5 0.25 0.25 -0.5 0.5 0.25 -0.25 0.5 0.25 0
		 0.5 0.25 0.25 0.5 0.25 0.5 0.5 0.25 -0.5 -0.5 0.5 -0.25
		 -0.5 0.5 0 -0.5 0.5 0.25 -0.5 0.5 0.5 -0.5 0.5 -0.5
		 -0.25 0.5 -0.25 -0.25 0.5 0 -0.25 0.5 0.25 -0.25 0.5 0.5
		 -0.25 0.5 -0.5 0 0.5 -0.25 0 0.5 0 0 0.5 0.25
		 0 0.5 0.5 0 0.5 -0.5 0.25 0.5 -0.25 0.25 0.5 0
		 0.25 0.5 0.25 0.25 0.5 0.5 0.25 0.5 -0.5 0.5 0.5 -0.25
		 0.5 0.5 0 0.5 0.5 0.25 0.5 0.5 0.5 0.5 0.5 ;
createNode transform -n "ffd1Base1";
	rename -uid "06C2F100-0002-8846-5C8B-14A4000002AE";
	setAttr ".t" -type "double3" -1.1920928955078125e-07 0 -1.7881393432617188e-07 ;
	setAttr ".s" -type "double3" 2.0000002384185791 2 2.0000005960464478 ;
createNode baseLattice -n "ffd1Base1Shape" -p "ffd1Base1";
	rename -uid "06C2F100-0002-8846-5C8B-14A4000002AF";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
createNode transform -n "cluster1Handle";
	rename -uid "06C2F100-0002-8846-5C8B-14F2000002C9";
	setAttr ".rp" -type "double3" -1.1920928955078125e-07 0 -1.7881393432617188e-07 ;
	setAttr ".sp" -type "double3" -1.1920928955078125e-07 0 -1.7881393432617188e-07 ;
createNode clusterHandle -n "cluster1HandleShape" -p "cluster1Handle";
	rename -uid "06C2F100-0002-8846-5C8B-14F2000002CA";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".or" -type "double3" -1.1920928955078125e-07 0 -1.7881393432617188e-07 ;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "06C2F100-0002-8846-5C8B-14350000026D";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode assetResolverConfig -n "assetResolverConfig";
	rename -uid "5D2FB100-0001-F410-5C8B-11AB00000276";
createNode glimpseGlobals -s -n "glimpseGlobals";
	rename -uid "5D2FB100-0001-F410-5C8B-11AB00000277";
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
	rename -uid "5D2FB100-0001-F410-5C8B-11AB00000278";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "06C2F100-0002-8846-5C8B-143500000271";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "06C2F100-0002-8846-5C8B-143500000272";
createNode displayLayerManager -n "layerManager";
	rename -uid "06C2F100-0002-8846-5C8B-143500000273";
createNode displayLayer -n "defaultLayer";
	rename -uid "5D2FB100-0001-F410-5C8B-11AB0000027C";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "06C2F100-0002-8846-5C8B-143500000275";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "5D2FB100-0001-F410-5C8B-11AB0000027E";
	setAttr ".g" yes;
createNode polySphere -n "polySphere1";
	rename -uid "5D2FB100-0001-F410-5C8B-11B500000289";
createNode ffd -n "ffd1";
	rename -uid "5D2FB100-0001-F410-5C8B-11B90000028C";
	setAttr ".lo" yes;
createNode tweak -n "tweak1";
	rename -uid "5D2FB100-0001-F410-5C8B-11B900000292";
createNode objectSet -n "ffd1Set";
	rename -uid "5D2FB100-0001-F410-5C8B-11B900000293";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "ffd1GroupId";
	rename -uid "5D2FB100-0001-F410-5C8B-11B900000294";
	setAttr ".ihi" 0;
createNode groupParts -n "ffd1GroupParts";
	rename -uid "5D2FB100-0001-F410-5C8B-11B900000295";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode objectSet -n "tweakSet1";
	rename -uid "5D2FB100-0001-F410-5C8B-11B900000296";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId2";
	rename -uid "5D2FB100-0001-F410-5C8B-11B900000297";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts2";
	rename -uid "5D2FB100-0001-F410-5C8B-11B900000298";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode polyPlane -n "polyPlane1";
	rename -uid "5D2FB100-0001-F410-5C8B-11D000000299";
	setAttr ".sw" 1;
	setAttr ".sh" 1;
	setAttr ".cuv" 2;
createNode transformGeometry -n "transformGeometry1";
	rename -uid "5D2FB100-0001-F410-5C8B-11F0000002B2";
	setAttr ".txf" -type "matrix" 2.0320278321884828 0 0 0 0 4.5120081719495948e-16 2.0320278321884828 0
		 0 -2.0320278321884828 4.5120081719495948e-16 0 0 0 1.4034363292323482 1;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "5D2FB100-0001-F410-5C8B-11F8000002B3";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"ALFShapeDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n"
		+ "            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n"
		+ "            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n"
		+ "            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"ALFShapeDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n"
		+ "            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n"
		+ "            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n"
		+ "            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"ALFShapeDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n"
		+ "            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n"
		+ "            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n"
		+ "            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 757\n            -height 1003\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"ALFShapeDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 1\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 0\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n"
		+ "            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n"
		+ "            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n"
		+ "            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n"
		+ "            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n"
		+ "                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -isSet 0\n                -isSetMember 0\n                -displayMode \"DAG\" \n"
		+ "                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                -selectionOrder \"display\" \n                -expandAttribute 1\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n"
		+ "                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -clipTime \"on\" \n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 0\n                -outliner \"graphEditor1OutlineEd\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n"
		+ "                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n"
		+ "                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n"
		+ "                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n"
		+ "                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -connectionMinSegment 0.03\n"
		+ "                -connectionOffset 0.03\n                -connectionRoundness 0.8\n                -connectionTension -100\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -enableOpenGL 0\n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 0\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -connectionMinSegment 0.03\n                -connectionOffset 0.03\n                -connectionRoundness 0.8\n                -connectionTension -100\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -enableOpenGL 0\n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n"
		+ "                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 0\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n"
		+ "\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"vertical2\\\" -ps 1 50 100 -ps 2 50 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Graph Editor\")) \n\t\t\t\t\t\"scriptedPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `scriptedPanel -unParent  -type \\\"graphEditor\\\" -l (localizedPanelLabel(\\\"Graph Editor\\\")) -mbv $menusOkayInPanels `;\\n\\n\\t\\t\\t$editorName = ($panelName+\\\"OutlineEd\\\");\\n            outlinerEditor -e \\n                -showShapes 1\\n                -showAssignedMaterials 0\\n                -showTimeEditor 1\\n                -showReferenceNodes 0\\n                -showReferenceMembers 0\\n                -showAttributes 1\\n                -showConnected 1\\n                -showAnimCurvesOnly 1\\n                -showMuteInfo 0\\n                -organizeByLayer 1\\n                -organizeByClip 1\\n                -showAnimLayerWeight 1\\n                -autoExpandLayers 1\\n                -autoExpand 1\\n                -showDagOnly 0\\n                -showAssets 1\\n                -showContainedOnly 0\\n                -showPublishedAsConnected 0\\n                -showParentContainers 1\\n                -showContainerContents 0\\n                -ignoreDagHierarchy 0\\n                -expandConnections 1\\n                -showUpstreamCurves 1\\n                -showUnitlessCurves 1\\n                -showCompounds 0\\n                -showLeafs 1\\n                -showNumericAttrsOnly 1\\n                -highlightActive 0\\n                -autoSelectNewObjects 1\\n                -doNotSelectNewObjects 0\\n                -dropIsParent 1\\n                -transmitFilters 1\\n                -setFilter \\\"0\\\" \\n                -showSetMembers 0\\n                -allowMultiSelection 1\\n                -alwaysToggleSelect 0\\n                -directSelect 0\\n                -isSet 0\\n                -isSetMember 0\\n                -displayMode \\\"DAG\\\" \\n                -expandObjects 0\\n                -setsIgnoreFilters 1\\n                -containersIgnoreFilters 0\\n                -editAttrName 0\\n                -showAttrValues 0\\n                -highlightSecondary 0\\n                -showUVAttrsOnly 0\\n                -showTextureNodesOnly 0\\n                -attrAlphaOrder \\\"default\\\" \\n                -animLayerFilterOptions \\\"allAffecting\\\" \\n                -sortOrder \\\"none\\\" \\n                -longNames 0\\n                -niceNames 1\\n                -showNamespace 1\\n                -showPinIcons 1\\n                -mapMotionTrails 1\\n                -ignoreHiddenAttribute 0\\n                -ignoreOutlinerColor 0\\n                -renderFilterVisible 0\\n                -selectionOrder \\\"display\\\" \\n                -expandAttribute 1\\n                $editorName;\\n\\n\\t\\t\\t$editorName = ($panelName+\\\"GraphEd\\\");\\n            animCurveEditor -e \\n                -displayKeys 1\\n                -displayTangents 0\\n                -displayActiveKeys 0\\n                -displayActiveKeyTangents 1\\n                -displayInfinities 0\\n                -displayValues 0\\n                -autoFit 1\\n                -autoFitTime 0\\n                -snapTime \\\"integer\\\" \\n                -snapValue \\\"none\\\" \\n                -showResults \\\"off\\\" \\n                -showBufferCurves \\\"off\\\" \\n                -smoothness \\\"fine\\\" \\n                -resultSamples 1\\n                -resultScreenSamples 0\\n                -resultUpdate \\\"delayed\\\" \\n                -showUpstreamCurves 1\\n                -showCurveNames 0\\n                -showActiveCurveNames 0\\n                -clipTime \\\"on\\\" \\n                -stackedCurves 0\\n                -stackedCurvesMin -1\\n                -stackedCurvesMax 1\\n                -stackedCurvesSpace 0.2\\n                -displayNormalized 0\\n                -preSelectionHighlight 0\\n                -constrainDrag 0\\n                -classicMode 1\\n                -valueLinesToggle 0\\n                -outliner \\\"graphEditor1OutlineEd\\\" \\n                $editorName\"\n"
		+ "\t\t\t\t\t\"scriptedPanel -edit -l (localizedPanelLabel(\\\"Graph Editor\\\")) -mbv $menusOkayInPanels  $panelName;\\n\\n\\t\\t\\t$editorName = ($panelName+\\\"OutlineEd\\\");\\n            outlinerEditor -e \\n                -showShapes 1\\n                -showAssignedMaterials 0\\n                -showTimeEditor 1\\n                -showReferenceNodes 0\\n                -showReferenceMembers 0\\n                -showAttributes 1\\n                -showConnected 1\\n                -showAnimCurvesOnly 1\\n                -showMuteInfo 0\\n                -organizeByLayer 1\\n                -organizeByClip 1\\n                -showAnimLayerWeight 1\\n                -autoExpandLayers 1\\n                -autoExpand 1\\n                -showDagOnly 0\\n                -showAssets 1\\n                -showContainedOnly 0\\n                -showPublishedAsConnected 0\\n                -showParentContainers 1\\n                -showContainerContents 0\\n                -ignoreDagHierarchy 0\\n                -expandConnections 1\\n                -showUpstreamCurves 1\\n                -showUnitlessCurves 1\\n                -showCompounds 0\\n                -showLeafs 1\\n                -showNumericAttrsOnly 1\\n                -highlightActive 0\\n                -autoSelectNewObjects 1\\n                -doNotSelectNewObjects 0\\n                -dropIsParent 1\\n                -transmitFilters 1\\n                -setFilter \\\"0\\\" \\n                -showSetMembers 0\\n                -allowMultiSelection 1\\n                -alwaysToggleSelect 0\\n                -directSelect 0\\n                -isSet 0\\n                -isSetMember 0\\n                -displayMode \\\"DAG\\\" \\n                -expandObjects 0\\n                -setsIgnoreFilters 1\\n                -containersIgnoreFilters 0\\n                -editAttrName 0\\n                -showAttrValues 0\\n                -highlightSecondary 0\\n                -showUVAttrsOnly 0\\n                -showTextureNodesOnly 0\\n                -attrAlphaOrder \\\"default\\\" \\n                -animLayerFilterOptions \\\"allAffecting\\\" \\n                -sortOrder \\\"none\\\" \\n                -longNames 0\\n                -niceNames 1\\n                -showNamespace 1\\n                -showPinIcons 1\\n                -mapMotionTrails 1\\n                -ignoreHiddenAttribute 0\\n                -ignoreOutlinerColor 0\\n                -renderFilterVisible 0\\n                -selectionOrder \\\"display\\\" \\n                -expandAttribute 1\\n                $editorName;\\n\\n\\t\\t\\t$editorName = ($panelName+\\\"GraphEd\\\");\\n            animCurveEditor -e \\n                -displayKeys 1\\n                -displayTangents 0\\n                -displayActiveKeys 0\\n                -displayActiveKeyTangents 1\\n                -displayInfinities 0\\n                -displayValues 0\\n                -autoFit 1\\n                -autoFitTime 0\\n                -snapTime \\\"integer\\\" \\n                -snapValue \\\"none\\\" \\n                -showResults \\\"off\\\" \\n                -showBufferCurves \\\"off\\\" \\n                -smoothness \\\"fine\\\" \\n                -resultSamples 1\\n                -resultScreenSamples 0\\n                -resultUpdate \\\"delayed\\\" \\n                -showUpstreamCurves 1\\n                -showCurveNames 0\\n                -showActiveCurveNames 0\\n                -clipTime \\\"on\\\" \\n                -stackedCurves 0\\n                -stackedCurvesMin -1\\n                -stackedCurvesMax 1\\n                -stackedCurvesSpace 0.2\\n                -displayNormalized 0\\n                -preSelectionHighlight 0\\n                -constrainDrag 0\\n                -classicMode 1\\n                -valueLinesToggle 0\\n                -outliner \\\"graphEditor1OutlineEd\\\" \\n                $editorName\"\n"
		+ "\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 757\\n    -height 1003\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"ALFShapeDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 757\\n    -height 1003\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"ALFShapeDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "5D2FB100-0001-F410-5C8B-11F8000002B4";
	setAttr ".b" -type "string" "playbackOptions -min -10 -max 120 -ast -10 -aet 200 ";
	setAttr ".st" 6;
createNode LHCurveWeightNode -n "LHCurveWeightNode1";
	rename -uid "5D2FB100-0001-F410-5C8B-1210000002B5";
	setAttr ".inputs[0]" 1;
createNode animCurveTU -n "LHCurveWeightNode1_Inputs_0__AnimCurveU";
	rename -uid "5D2FB100-0001-F410-5C8B-12A70000030D";
	setAttr ".tan" 1;
	setAttr ".wgt" no;
	setAttr -s 3 ".ktv[0:2]"  -10 0 0 1 10 0;
	setAttr -s 3 ".kix[0:2]"  1 0.99990710008941197 1;
	setAttr -s 3 ".kiy[0:2]"  0 0.013630524229926404 0;
	setAttr -s 3 ".kox[0:2]"  1 0.99990710008714689 1;
	setAttr -s 3 ".koy[0:2]"  0 0.013630524396090343 0;
createNode animCurveTU -n "LHCurveWeightNode1_Inputs_0__AnimCurveV";
	rename -uid "5D2FB100-0001-F410-5C8B-12A90000030E";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  -10 0 10 1;
createNode ffd -n "ffd2";
	rename -uid "06C2F100-0002-8846-5C8B-14A4000002AC";
	setAttr ".ip[0].ig" -type "mesh" 


		"v"	382
		0.14877813	-0.98768836	-0.048340943
		0.12655823	-0.98768836	-0.091949932
		0.091949932	-0.98768836	-0.12655823
		0.048340935	-0.98768836	-0.14877811
		-1.6940659e-21	-0.98768836	-0.15643455
		-0.048340935	-0.98768836	-0.1487781
		-0.091949917	-0.98768836	-0.1265582
		-0.12655818	-0.98768836	-0.091949902
		-0.14877807	-0.98768836	-0.048340924
		-0.15643452	-0.98768836	-3.5527306e-15
		-0.14877807	-0.98768836	0.048340924
		-0.12655818	-0.98768836	0.091949895
		-0.091949895	-0.98768836	0.12655817
		-0.048340924	-0.98768836	0.14877805
		-4.6621129e-09	-0.98768836	0.15643449
		0.048340909	-0.98768836	0.14877804
		0.09194988	-0.98768836	0.12655815
		0.12655815	-0.98768836	0.091949888
		0.14877804	-0.98768836	0.048340913
		0.15643448	-0.98768836	-3.5527306e-15
		0.29389283	-0.95105654	-0.095491566
		0.25000018	-0.95105654	-0.18163574
		0.18163574	-0.95105654	-0.25000015
		0.095491551	-0.95105654	-0.2938928
		-1.6940659e-21	-0.95105654	-0.30901715
		-0.095491551	-0.95105654	-0.29389277
		-0.18163571	-0.95105654	-0.25000009
		-0.25000009	-0.95105654	-0.18163569
		-0.29389271	-0.95105654	-0.095491529
		-0.30901706	-0.95105654	-3.5527306e-15
		-0.29389271	-0.95105654	0.095491529
		-0.25000006	-0.95105654	0.18163568
		-0.18163568	-0.95105654	0.25000006
		-0.095491529	-0.95105654	0.29389268
		-9.2094234e-09	-0.95105654	0.30901703
		0.095491499	-0.95105654	0.29389265
		0.18163563	-0.95105654	0.25000003
		0.25	-0.95105654	0.18163565
		0.29389265	-0.95105654	0.095491506
		0.309017	-0.95105654	-3.5527306e-15
		0.43177092	-0.89100653	-0.14029087
		0.36728629	-0.89100653	-0.2668491
		0.2668491	-0.89100653	-0.36728626
		0.14029086	-0.89100653	-0.43177086
		-1.6940659e-21	-0.89100653	-0.45399073
		-0.14029086	-0.89100653	-0.43177083
		-0.26684904	-0.89100653	-0.36728618
		-0.36728615	-0.89100653	-0.26684901
		-0.43177077	-0.89100653	-0.14029081
		-0.45399064	-0.89100653	-3.5527306e-15
		-0.43177077	-0.89100653	0.14029081
		-0.36728612	-0.89100653	0.26684898
		-0.26684898	-0.89100653	0.36728612
		-0.14029081	-0.89100653	0.43177071
		-1.3529972e-08	-0.89100653	0.45399058
		0.14029078	-0.89100653	0.43177068
		0.26684892	-0.89100653	0.36728609
		0.36728606	-0.89100653	0.26684895
		0.43177065	-0.89100653	0.1402908
		0.45399052	-0.89100653	-3.5527306e-15
		0.55901736	-0.809017	-0.18163574
		0.47552857	-0.809017	-0.34549171
		0.34549171	-0.809017	-0.47552854
		0.18163572	-0.809017	-0.5590173
		-1.6940659e-21	-0.809017	-0.58778554
		-0.18163572	-0.809017	-0.55901724
		-0.34549165	-0.809017	-0.47552842
		-0.47552839	-0.809017	-0.34549159
		-0.55901712	-0.809017	-0.18163566
		-0.58778536	-0.809017	-3.5527306e-15
		-0.55901712	-0.809017	0.18163566
		-0.47552836	-0.809017	0.34549156
		-0.34549156	-0.809017	0.47552833
		-0.18163566	-0.809017	0.55901706
		-1.7517367e-08	-0.809017	0.5877853
		0.18163562	-0.809017	0.55901706
		0.3454915	-0.809017	0.4755283
		0.47552827	-0.809017	0.34549153
		0.559017	-0.809017	0.18163563
		0.58778524	-0.809017	-3.5527306e-15
		0.67249894	-0.70710677	-0.21850814
		0.57206178	-0.70710677	-0.41562718
		0.41562718	-0.70710677	-0.57206172
		0.21850812	-0.70710677	-0.67249888
		-1.6940659e-21	-0.70710677	-0.70710713
		-0.21850812	-0.70710677	-0.67249882
		-0.41562709	-0.70710677	-0.5720616
		-0.57206154	-0.70710677	-0.41562706
		-0.6724987	-0.70710677	-0.21850805
		-0.70710695	-0.70710677	-3.5527306e-15
		-0.6724987	-0.70710677	0.21850805
		-0.57206154	-0.70710677	0.415627
		-0.415627	-0.70710677	0.57206148
		-0.21850805	-0.70710677	0.67249858
		-2.107342e-08	-0.70710677	0.70710683
		0.21850799	-0.70710677	0.67249858
		0.41562691	-0.70710677	0.57206142
		0.57206142	-0.70710677	0.41562697
		0.67249852	-0.70710677	0.21850802
		0.70710677	-0.70710677	-3.5527306e-15
		0.7694214	-0.58778524	-0.25000015
		0.65450895	-0.58778524	-0.47552854
		0.47552854	-0.58778524	-0.65450889
		0.25000012	-0.58778524	-0.76942128
		-1.6940659e-21	-0.58778524	-0.80901736
		-0.25000012	-0.58778524	-0.76942122
		-0.47552845	-0.58778524	-0.65450877
		-0.65450871	-0.58778524	-0.47552839
		-0.7694211	-0.58778524	-0.25000006
		-0.80901718	-0.58778524	-3.5527306e-15
		-0.7694211	-0.58778524	0.25000006
		-0.65450865	-0.58778524	0.47552836
		-0.47552836	-0.58778524	0.65450859
		-0.25000006	-0.58778524	0.76942098
		-2.4110587e-08	-0.58778524	0.80901712
		0.24999997	-0.58778524	0.76942098
		0.47552827	-0.58778524	0.65450853
		0.65450853	-0.58778524	0.4755283
		0.76942092	-0.58778524	0.24999999
		0.809017	-0.58778524	-3.5527306e-15
		0.8473981	-0.45399052	-0.27533633
		0.72083992	-0.45399052	-0.5237208
		0.5237208	-0.45399052	-0.72083986
		0.2753363	-0.45399052	-0.84739798
		-1.6940659e-21	-0.45399052	-0.89100695
		-0.2753363	-0.45399052	-0.84739798
		-0.52372068	-0.45399052	-0.72083968
		-0.72083962	-0.45399052	-0.52372062
		-0.8473978	-0.45399052	-0.27533621
		-0.89100677	-0.45399052	-3.5527306e-15
		-0.8473978	-0.45399052	0.27533621
		-0.72083962	-0.45399052	0.52372062
		-0.52372062	-0.45399052	0.72083956
		-0.27533621	-0.45399052	0.84739769
		-2.6554066e-08	-0.45399052	0.89100665
		0.27533615	-0.45399052	0.84739763
		0.5237205	-0.45399052	0.7208395
		0.72083944	-0.45399052	0.52372056
		0.84739757	-0.45399052	0.27533618
		0.89100653	-0.45399052	-3.5527306e-15
		0.90450913	-0.30901697	-0.2938928
		0.7694214	-0.30901697	-0.55901736
		0.55901736	-0.30901697	-0.76942134
		0.29389277	-0.30901697	-0.90450901
		-1.6940659e-21	-0.30901697	-0.95105702
		-0.29389277	-0.30901697	-0.90450895
		-0.55901724	-0.30901697	-0.76942122
		-0.76942116	-0.30901697	-0.55901718
		-0.90450877	-0.30901697	-0.29389271
		-0.95105678	-0.30901697	-3.5527306e-15
		-0.90450877	-0.30901697	0.29389271
		-0.7694211	-0.30901697	0.55901712
		-0.55901712	-0.30901697	0.76942104
		-0.29389271	-0.30901697	0.90450865
		-2.8343695e-08	-0.30901697	0.95105666
		0.29389262	-0.30901697	0.90450859
		0.559017	-0.30901697	0.76942098
		0.76942092	-0.30901697	0.55901706
		0.90450853	-0.30901697	0.29389265
		0.95105654	-0.30901697	-3.5527306e-15
		0.93934804	-0.15643437	-0.30521268
		0.79905719	-0.15643437	-0.580549
		0.580549	-0.15643437	-0.79905713
		0.30521265	-0.15643437	-0.93934792
		-1.6940659e-21	-0.15643437	-0.98768884
		-0.30521265	-0.15643437	-0.93934786
		-0.58054888	-0.15643437	-0.79905695
		-0.79905689	-0.15643437	-0.58054882
		-0.93934768	-0.15643437	-0.30521256
		-0.9876886	-0.15643437	-3.5527306e-15
		-0.93934768	-0.15643437	0.30521256
		-0.79905683	-0.15643437	0.58054876
		-0.58054876	-0.15643437	0.79905677
		-0.30521256	-0.15643437	0.93934757
		-2.9435409e-08	-0.15643437	0.98768848
		0.30521247	-0.15643437	0.93934757
		0.58054864	-0.15643437	0.79905671
		0.79905665	-0.15643437	0.5805487
		0.93934751	-0.15643437	0.3052125
		0.98768836	-0.15643437	-3.5527306e-15
		0.95105714	0	-0.30901718
		0.80901754	0	-0.5877856
		0.5877856	0	-0.80901748
		0.30901715	0	-0.95105702
		-1.6940659e-21	0	-1.0000005
		-0.30901715	0	-0.95105696
		-0.58778548	0	-0.8090173
		-0.80901724	0	-0.58778542
		-0.95105678	0	-0.30901706
		-1.0000002	0	-3.5527306e-15
		-0.95105678	0	0.30901706
		-0.80901718	0	0.58778536
		-0.58778536	0	0.80901712
		-0.30901706	0	0.95105666
		-2.9802326e-08	0	1.0000001
		0.30901697	0	0.9510566
		0.58778524	0	0.80901706
		0.809017	0	0.5877853
		0.95105654	0	0.309017
		1	0	-3.5527306e-15
		0.93934804	0.15643437	-0.30521268
		0.79905719	0.15643437	-0.580549
		0.580549	0.15643437	-0.79905713
		0.30521265	0.15643437	-0.93934792
		-1.6940659e-21	0.15643437	-0.98768884
		-0.30521265	0.15643437	-0.93934786
		-0.58054888	0.15643437	-0.79905695
		-0.79905689	0.15643437	-0.58054882
		-0.93934768	0.15643437	-0.30521256
		-0.9876886	0.15643437	-3.5527306e-15
		-0.93934768	0.15643437	0.30521256
		-0.79905683	0.15643437	0.58054876
		-0.58054876	0.15643437	0.79905677
		-0.30521256	0.15643437	0.93934757
		-2.9435409e-08	0.15643437	0.98768848
		0.30521247	0.15643437	0.93934757
		0.58054864	0.15643437	0.79905671
		0.79905665	0.15643437	0.5805487
		0.93934751	0.15643437	0.3052125
		0.98768836	0.15643437	-3.5527306e-15
		0.90450913	0.30901697	-0.2938928
		0.7694214	0.30901697	-0.55901736
		0.55901736	0.30901697	-0.76942134
		0.29389277	0.30901697	-0.90450901
		-1.6940659e-21	0.30901697	-0.95105702
		-0.29389277	0.30901697	-0.90450895
		-0.55901724	0.30901697	-0.76942122
		-0.76942116	0.30901697	-0.55901718
		-0.90450877	0.30901697	-0.29389271
		-0.95105678	0.30901697	-3.5527306e-15
		-0.90450877	0.30901697	0.29389271
		-0.7694211	0.30901697	0.55901712
		-0.55901712	0.30901697	0.76942104
		-0.29389271	0.30901697	0.90450865
		-2.8343695e-08	0.30901697	0.95105666
		0.29389262	0.30901697	0.90450859
		0.559017	0.30901697	0.76942098
		0.76942092	0.30901697	0.55901706
		0.90450853	0.30901697	0.29389265
		0.95105654	0.30901697	-3.5527306e-15
		0.8473981	0.45399052	-0.27533633
		0.72083992	0.45399052	-0.5237208
		0.5237208	0.45399052	-0.72083986
		0.2753363	0.45399052	-0.84739798
		-1.6940659e-21	0.45399052	-0.89100695
		-0.2753363	0.45399052	-0.84739798
		-0.52372068	0.45399052	-0.72083968
		-0.72083962	0.45399052	-0.52372062
		-0.8473978	0.45399052	-0.27533621
		-0.89100677	0.45399052	-3.5527306e-15
		-0.8473978	0.45399052	0.27533621
		-0.72083962	0.45399052	0.52372062
		-0.52372062	0.45399052	0.72083956
		-0.27533621	0.45399052	0.84739769
		-2.6554066e-08	0.45399052	0.89100665
		0.27533615	0.45399052	0.84739763
		0.5237205	0.45399052	0.7208395
		0.72083944	0.45399052	0.52372056
		0.84739757	0.45399052	0.27533618
		0.89100653	0.45399052	-3.5527306e-15
		0.7694214	0.58778524	-0.25000015
		0.65450895	0.58778524	-0.47552854
		0.47552854	0.58778524	-0.65450889
		0.25000012	0.58778524	-0.76942128
		-1.6940659e-21	0.58778524	-0.80901736
		-0.25000012	0.58778524	-0.76942122
		-0.47552845	0.58778524	-0.65450877
		-0.65450871	0.58778524	-0.47552839
		-0.7694211	0.58778524	-0.25000006
		-0.80901718	0.58778524	-3.5527306e-15
		-0.7694211	0.58778524	0.25000006
		-0.65450865	0.58778524	0.47552836
		-0.47552836	0.58778524	0.65450859
		-0.25000006	0.58778524	0.76942098
		-2.4110587e-08	0.58778524	0.80901712
		0.24999997	0.58778524	0.76942098
		0.47552827	0.58778524	0.65450853
		0.65450853	0.58778524	0.4755283
		0.76942092	0.58778524	0.24999999
		0.809017	0.58778524	-3.5527306e-15
		0.67249894	0.70710677	-0.21850814
		0.57206178	0.70710677	-0.41562718
		0.41562718	0.70710677	-0.57206172
		0.21850812	0.70710677	-0.67249888
		-1.6940659e-21	0.70710677	-0.70710713
		-0.21850812	0.70710677	-0.67249882
		-0.41562709	0.70710677	-0.5720616
		-0.57206154	0.70710677	-0.41562706
		-0.6724987	0.70710677	-0.21850805
		-0.70710695	0.70710677	-3.5527306e-15
		-0.6724987	0.70710677	0.21850805
		-0.57206154	0.70710677	0.415627
		-0.415627	0.70710677	0.57206148
		-0.21850805	0.70710677	0.67249858
		-2.107342e-08	0.70710677	0.70710683
		0.21850799	0.70710677	0.67249858
		0.41562691	0.70710677	0.57206142
		0.57206142	0.70710677	0.41562697
		0.67249852	0.70710677	0.21850802
		0.70710677	0.70710677	-3.5527306e-15
		0.55901736	0.809017	-0.18163574
		0.47552857	0.809017	-0.34549171
		0.34549171	0.809017	-0.47552854
		0.18163572	0.809017	-0.5590173
		-1.6940659e-21	0.809017	-0.58778554
		-0.18163572	0.809017	-0.55901724
		-0.34549165	0.809017	-0.47552842
		-0.47552839	0.809017	-0.34549159
		-0.55901712	0.809017	-0.18163566
		-0.58778536	0.809017	-3.5527306e-15
		-0.55901712	0.809017	0.18163566
		-0.47552836	0.809017	0.34549156
		-0.34549156	0.809017	0.47552833
		-0.18163566	0.809017	0.55901706
		-1.7517367e-08	0.809017	0.5877853
		0.18163562	0.809017	0.55901706
		0.3454915	0.809017	0.4755283
		0.47552827	0.809017	0.34549153
		0.559017	0.809017	0.18163563
		0.58778524	0.809017	-3.5527306e-15
		0.43177092	0.89100653	-0.14029087
		0.36728629	0.89100653	-0.2668491
		0.2668491	0.89100653	-0.36728626
		0.14029086	0.89100653	-0.43177086
		-1.6940659e-21	0.89100653	-0.45399073
		-0.14029086	0.89100653	-0.43177083
		-0.26684904	0.89100653	-0.36728618
		-0.36728615	0.89100653	-0.26684901
		-0.43177077	0.89100653	-0.14029081
		-0.45399064	0.89100653	-3.5527306e-15
		-0.43177077	0.89100653	0.14029081
		-0.36728612	0.89100653	0.26684898
		-0.26684898	0.89100653	0.36728612
		-0.14029081	0.89100653	0.43177071
		-1.3529972e-08	0.89100653	0.45399058
		0.14029078	0.89100653	0.43177068
		0.26684892	0.89100653	0.36728609
		0.36728606	0.89100653	0.26684895
		0.43177065	0.89100653	0.1402908
		0.45399052	0.89100653	-3.5527306e-15
		0.29389283	0.95105654	-0.095491566
		0.25000018	0.95105654	-0.18163574
		0.18163574	0.95105654	-0.25000015
		0.095491551	0.95105654	-0.2938928
		-1.6940659e-21	0.95105654	-0.30901715
		-0.095491551	0.95105654	-0.29389277
		-0.18163571	0.95105654	-0.25000009
		-0.25000009	0.95105654	-0.18163569
		-0.29389271	0.95105654	-0.095491529
		-0.30901706	0.95105654	-3.5527306e-15
		-0.29389271	0.95105654	0.095491529
		-0.25000006	0.95105654	0.18163568
		-0.18163568	0.95105654	0.25000006
		-0.095491529	0.95105654	0.29389268
		-9.2094234e-09	0.95105654	0.30901703
		0.095491499	0.95105654	0.29389265
		0.18163563	0.95105654	0.25000003
		0.25	0.95105654	0.18163565
		0.29389265	0.95105654	0.095491506
		0.309017	0.95105654	-3.5527306e-15
		0.14877813	0.98768836	-0.048340943
		0.12655823	0.98768836	-0.091949932
		0.091949932	0.98768836	-0.12655823
		0.048340935	0.98768836	-0.14877811
		-1.6940659e-21	0.98768836	-0.15643455
		-0.048340935	0.98768836	-0.1487781
		-0.091949917	0.98768836	-0.1265582
		-0.12655818	0.98768836	-0.091949902
		-0.14877807	0.98768836	-0.048340924
		-0.15643452	0.98768836	-3.5527306e-15
		-0.14877807	0.98768836	0.048340924
		-0.12655818	0.98768836	0.091949895
		-0.091949895	0.98768836	0.12655817
		-0.048340924	0.98768836	0.14877805
		-4.6621129e-09	0.98768836	0.15643449
		0.048340909	0.98768836	0.14877804
		0.09194988	0.98768836	0.12655815
		0.12655815	0.98768836	0.091949888
		0.14877804	0.98768836	0.048340913
		0.15643448	0.98768836	-3.5527306e-15
		-1.6940659e-21	-1	-3.5527306e-15
		-1.6940659e-21	1	-3.5527306e-15

		"vt"	439
		0	0.050000001
		0.050000001	0.050000001
		0.1	0.050000001
		0.15000001	0.050000001
		0.2	0.050000001
		0.25	0.050000001
		0.30000001	0.050000001
		0.35000002	0.050000001
		0.40000004	0.050000001
		0.45000005	0.050000001
		0.50000006	0.050000001
		0.55000007	0.050000001
		0.60000008	0.050000001
		0.6500001	0.050000001
		0.70000011	0.050000001
		0.75000012	0.050000001
		0.80000013	0.050000001
		0.85000014	0.050000001
		0.90000015	0.050000001
		0.95000017	0.050000001
		1.0000001	0.050000001
		0	0.1
		0.050000001	0.1
		0.1	0.1
		0.15000001	0.1
		0.2	0.1
		0.25	0.1
		0.30000001	0.1
		0.35000002	0.1
		0.40000004	0.1
		0.45000005	0.1
		0.50000006	0.1
		0.55000007	0.1
		0.60000008	0.1
		0.6500001	0.1
		0.70000011	0.1
		0.75000012	0.1
		0.80000013	0.1
		0.85000014	0.1
		0.90000015	0.1
		0.95000017	0.1
		1.0000001	0.1
		0	0.15000001
		0.050000001	0.15000001
		0.1	0.15000001
		0.15000001	0.15000001
		0.2	0.15000001
		0.25	0.15000001
		0.30000001	0.15000001
		0.35000002	0.15000001
		0.40000004	0.15000001
		0.45000005	0.15000001
		0.50000006	0.15000001
		0.55000007	0.15000001
		0.60000008	0.15000001
		0.6500001	0.15000001
		0.70000011	0.15000001
		0.75000012	0.15000001
		0.80000013	0.15000001
		0.85000014	0.15000001
		0.90000015	0.15000001
		0.95000017	0.15000001
		1.0000001	0.15000001
		0	0.2
		0.050000001	0.2
		0.1	0.2
		0.15000001	0.2
		0.2	0.2
		0.25	0.2
		0.30000001	0.2
		0.35000002	0.2
		0.40000004	0.2
		0.45000005	0.2
		0.50000006	0.2
		0.55000007	0.2
		0.60000008	0.2
		0.6500001	0.2
		0.70000011	0.2
		0.75000012	0.2
		0.80000013	0.2
		0.85000014	0.2
		0.90000015	0.2
		0.95000017	0.2
		1.0000001	0.2
		0	0.25
		0.050000001	0.25
		0.1	0.25
		0.15000001	0.25
		0.2	0.25
		0.25	0.25
		0.30000001	0.25
		0.35000002	0.25
		0.40000004	0.25
		0.45000005	0.25
		0.50000006	0.25
		0.55000007	0.25
		0.60000008	0.25
		0.6500001	0.25
		0.70000011	0.25
		0.75000012	0.25
		0.80000013	0.25
		0.85000014	0.25
		0.90000015	0.25
		0.95000017	0.25
		1.0000001	0.25
		0	0.30000001
		0.050000001	0.30000001
		0.1	0.30000001
		0.15000001	0.30000001
		0.2	0.30000001
		0.25	0.30000001
		0.30000001	0.30000001
		0.35000002	0.30000001
		0.40000004	0.30000001
		0.45000005	0.30000001
		0.50000006	0.30000001
		0.55000007	0.30000001
		0.60000008	0.30000001
		0.6500001	0.30000001
		0.70000011	0.30000001
		0.75000012	0.30000001
		0.80000013	0.30000001
		0.85000014	0.30000001
		0.90000015	0.30000001
		0.95000017	0.30000001
		1.0000001	0.30000001
		0	0.35000002
		0.050000001	0.35000002
		0.1	0.35000002
		0.15000001	0.35000002
		0.2	0.35000002
		0.25	0.35000002
		0.30000001	0.35000002
		0.35000002	0.35000002
		0.40000004	0.35000002
		0.45000005	0.35000002
		0.50000006	0.35000002
		0.55000007	0.35000002
		0.60000008	0.35000002
		0.6500001	0.35000002
		0.70000011	0.35000002
		0.75000012	0.35000002
		0.80000013	0.35000002
		0.85000014	0.35000002
		0.90000015	0.35000002
		0.95000017	0.35000002
		1.0000001	0.35000002
		0	0.40000004
		0.050000001	0.40000004
		0.1	0.40000004
		0.15000001	0.40000004
		0.2	0.40000004
		0.25	0.40000004
		0.30000001	0.40000004
		0.35000002	0.40000004
		0.40000004	0.40000004
		0.45000005	0.40000004
		0.50000006	0.40000004
		0.55000007	0.40000004
		0.60000008	0.40000004
		0.6500001	0.40000004
		0.70000011	0.40000004
		0.75000012	0.40000004
		0.80000013	0.40000004
		0.85000014	0.40000004
		0.90000015	0.40000004
		0.95000017	0.40000004
		1.0000001	0.40000004
		0	0.45000005
		0.050000001	0.45000005
		0.1	0.45000005
		0.15000001	0.45000005
		0.2	0.45000005
		0.25	0.45000005
		0.30000001	0.45000005
		0.35000002	0.45000005
		0.40000004	0.45000005
		0.45000005	0.45000005
		0.50000006	0.45000005
		0.55000007	0.45000005
		0.60000008	0.45000005
		0.6500001	0.45000005
		0.70000011	0.45000005
		0.75000012	0.45000005
		0.80000013	0.45000005
		0.85000014	0.45000005
		0.90000015	0.45000005
		0.95000017	0.45000005
		1.0000001	0.45000005
		0	0.50000006
		0.050000001	0.50000006
		0.1	0.50000006
		0.15000001	0.50000006
		0.2	0.50000006
		0.25	0.50000006
		0.30000001	0.50000006
		0.35000002	0.50000006
		0.40000004	0.50000006
		0.45000005	0.50000006
		0.50000006	0.50000006
		0.55000007	0.50000006
		0.60000008	0.50000006
		0.6500001	0.50000006
		0.70000011	0.50000006
		0.75000012	0.50000006
		0.80000013	0.50000006
		0.85000014	0.50000006
		0.90000015	0.50000006
		0.95000017	0.50000006
		1.0000001	0.50000006
		0	0.55000007
		0.050000001	0.55000007
		0.1	0.55000007
		0.15000001	0.55000007
		0.2	0.55000007
		0.25	0.55000007
		0.30000001	0.55000007
		0.35000002	0.55000007
		0.40000004	0.55000007
		0.45000005	0.55000007
		0.50000006	0.55000007
		0.55000007	0.55000007
		0.60000008	0.55000007
		0.6500001	0.55000007
		0.70000011	0.55000007
		0.75000012	0.55000007
		0.80000013	0.55000007
		0.85000014	0.55000007
		0.90000015	0.55000007
		0.95000017	0.55000007
		1.0000001	0.55000007
		0	0.60000008
		0.050000001	0.60000008
		0.1	0.60000008
		0.15000001	0.60000008
		0.2	0.60000008
		0.25	0.60000008
		0.30000001	0.60000008
		0.35000002	0.60000008
		0.40000004	0.60000008
		0.45000005	0.60000008
		0.50000006	0.60000008
		0.55000007	0.60000008
		0.60000008	0.60000008
		0.6500001	0.60000008
		0.70000011	0.60000008
		0.75000012	0.60000008
		0.80000013	0.60000008
		0.85000014	0.60000008
		0.90000015	0.60000008
		0.95000017	0.60000008
		1.0000001	0.60000008
		0	0.6500001
		0.050000001	0.6500001
		0.1	0.6500001
		0.15000001	0.6500001
		0.2	0.6500001
		0.25	0.6500001
		0.30000001	0.6500001
		0.35000002	0.6500001
		0.40000004	0.6500001
		0.45000005	0.6500001
		0.50000006	0.6500001
		0.55000007	0.6500001
		0.60000008	0.6500001
		0.6500001	0.6500001
		0.70000011	0.6500001
		0.75000012	0.6500001
		0.80000013	0.6500001
		0.85000014	0.6500001
		0.90000015	0.6500001
		0.95000017	0.6500001
		1.0000001	0.6500001
		0	0.70000011
		0.050000001	0.70000011
		0.1	0.70000011
		0.15000001	0.70000011
		0.2	0.70000011
		0.25	0.70000011
		0.30000001	0.70000011
		0.35000002	0.70000011
		0.40000004	0.70000011
		0.45000005	0.70000011
		0.50000006	0.70000011
		0.55000007	0.70000011
		0.60000008	0.70000011
		0.6500001	0.70000011
		0.70000011	0.70000011
		0.75000012	0.70000011
		0.80000013	0.70000011
		0.85000014	0.70000011
		0.90000015	0.70000011
		0.95000017	0.70000011
		1.0000001	0.70000011
		0	0.75000012
		0.050000001	0.75000012
		0.1	0.75000012
		0.15000001	0.75000012
		0.2	0.75000012
		0.25	0.75000012
		0.30000001	0.75000012
		0.35000002	0.75000012
		0.40000004	0.75000012
		0.45000005	0.75000012
		0.50000006	0.75000012
		0.55000007	0.75000012
		0.60000008	0.75000012
		0.6500001	0.75000012
		0.70000011	0.75000012
		0.75000012	0.75000012
		0.80000013	0.75000012
		0.85000014	0.75000012
		0.90000015	0.75000012
		0.95000017	0.75000012
		1.0000001	0.75000012
		0	0.80000013
		0.050000001	0.80000013
		0.1	0.80000013
		0.15000001	0.80000013
		0.2	0.80000013
		0.25	0.80000013
		0.30000001	0.80000013
		0.35000002	0.80000013
		0.40000004	0.80000013
		0.45000005	0.80000013
		0.50000006	0.80000013
		0.55000007	0.80000013
		0.60000008	0.80000013
		0.6500001	0.80000013
		0.70000011	0.80000013
		0.75000012	0.80000013
		0.80000013	0.80000013
		0.85000014	0.80000013
		0.90000015	0.80000013
		0.95000017	0.80000013
		1.0000001	0.80000013
		0	0.85000014
		0.050000001	0.85000014
		0.1	0.85000014
		0.15000001	0.85000014
		0.2	0.85000014
		0.25	0.85000014
		0.30000001	0.85000014
		0.35000002	0.85000014
		0.40000004	0.85000014
		0.45000005	0.85000014
		0.50000006	0.85000014
		0.55000007	0.85000014
		0.60000008	0.85000014
		0.6500001	0.85000014
		0.70000011	0.85000014
		0.75000012	0.85000014
		0.80000013	0.85000014
		0.85000014	0.85000014
		0.90000015	0.85000014
		0.95000017	0.85000014
		1.0000001	0.85000014
		0	0.90000015
		0.050000001	0.90000015
		0.1	0.90000015
		0.15000001	0.90000015
		0.2	0.90000015
		0.25	0.90000015
		0.30000001	0.90000015
		0.35000002	0.90000015
		0.40000004	0.90000015
		0.45000005	0.90000015
		0.50000006	0.90000015
		0.55000007	0.90000015
		0.60000008	0.90000015
		0.6500001	0.90000015
		0.70000011	0.90000015
		0.75000012	0.90000015
		0.80000013	0.90000015
		0.85000014	0.90000015
		0.90000015	0.90000015
		0.95000017	0.90000015
		1.0000001	0.90000015
		0	0.95000017
		0.050000001	0.95000017
		0.1	0.95000017
		0.15000001	0.95000017
		0.2	0.95000017
		0.25	0.95000017
		0.30000001	0.95000017
		0.35000002	0.95000017
		0.40000004	0.95000017
		0.45000005	0.95000017
		0.50000006	0.95000017
		0.55000007	0.95000017
		0.60000008	0.95000017
		0.6500001	0.95000017
		0.70000011	0.95000017
		0.75000012	0.95000017
		0.80000013	0.95000017
		0.85000014	0.95000017
		0.90000015	0.95000017
		0.95000017	0.95000017
		1.0000001	0.95000017
		0.025	0
		0.075000003	0
		0.125	0
		0.175	0
		0.22500001	0
		0.27500001	0
		0.32500002	0
		0.375	0
		0.42500001	0
		0.47499999	0
		0.52500004	0
		0.57499999	0
		0.625	0
		0.67500001	0
		0.72500002	0
		0.77500004	0
		0.82499999	0
		0.875	0
		0.92500001	0
		0.97500002	0
		0.025	1
		0.075000003	1
		0.125	1
		0.175	1
		0.22500001	1
		0.27500001	1
		0.32500002	1
		0.375	1
		0.42500001	1
		0.47499999	1
		0.52500004	1
		0.57499999	1
		0.625	1
		0.67500001	1
		0.72500002	1
		0.77500004	1
		0.82499999	1
		0.875	1
		0.92500001	1
		0.97500002	1

		"e"	780
		0	1	"smooth"
		1	2	"smooth"
		2	3	"smooth"
		3	4	"smooth"
		4	5	"smooth"
		5	6	"smooth"
		6	7	"smooth"
		7	8	"smooth"
		8	9	"smooth"
		9	10	"smooth"
		10	11	"smooth"
		11	12	"smooth"
		12	13	"smooth"
		13	14	"smooth"
		14	15	"smooth"
		15	16	"smooth"
		16	17	"smooth"
		17	18	"smooth"
		18	19	"smooth"
		19	0	"smooth"
		20	21	"smooth"
		21	22	"smooth"
		22	23	"smooth"
		23	24	"smooth"
		24	25	"smooth"
		25	26	"smooth"
		26	27	"smooth"
		27	28	"smooth"
		28	29	"smooth"
		29	30	"smooth"
		30	31	"smooth"
		31	32	"smooth"
		32	33	"smooth"
		33	34	"smooth"
		34	35	"smooth"
		35	36	"smooth"
		36	37	"smooth"
		37	38	"smooth"
		38	39	"smooth"
		39	20	"smooth"
		40	41	"smooth"
		41	42	"smooth"
		42	43	"smooth"
		43	44	"smooth"
		44	45	"smooth"
		45	46	"smooth"
		46	47	"smooth"
		47	48	"smooth"
		48	49	"smooth"
		49	50	"smooth"
		50	51	"smooth"
		51	52	"smooth"
		52	53	"smooth"
		53	54	"smooth"
		54	55	"smooth"
		55	56	"smooth"
		56	57	"smooth"
		57	58	"smooth"
		58	59	"smooth"
		59	40	"smooth"
		60	61	"smooth"
		61	62	"smooth"
		62	63	"smooth"
		63	64	"smooth"
		64	65	"smooth"
		65	66	"smooth"
		66	67	"smooth"
		67	68	"smooth"
		68	69	"smooth"
		69	70	"smooth"
		70	71	"smooth"
		71	72	"smooth"
		72	73	"smooth"
		73	74	"smooth"
		74	75	"smooth"
		75	76	"smooth"
		76	77	"smooth"
		77	78	"smooth"
		78	79	"smooth"
		79	60	"smooth"
		80	81	"smooth"
		81	82	"smooth"
		82	83	"smooth"
		83	84	"smooth"
		84	85	"smooth"
		85	86	"smooth"
		86	87	"smooth"
		87	88	"smooth"
		88	89	"smooth"
		89	90	"smooth"
		90	91	"smooth"
		91	92	"smooth"
		92	93	"smooth"
		93	94	"smooth"
		94	95	"smooth"
		95	96	"smooth"
		96	97	"smooth"
		97	98	"smooth"
		98	99	"smooth"
		99	80	"smooth"
		100	101	"smooth"
		101	102	"smooth"
		102	103	"smooth"
		103	104	"smooth"
		104	105	"smooth"
		105	106	"smooth"
		106	107	"smooth"
		107	108	"smooth"
		108	109	"smooth"
		109	110	"smooth"
		110	111	"smooth"
		111	112	"smooth"
		112	113	"smooth"
		113	114	"smooth"
		114	115	"smooth"
		115	116	"smooth"
		116	117	"smooth"
		117	118	"smooth"
		118	119	"smooth"
		119	100	"smooth"
		120	121	"smooth"
		121	122	"smooth"
		122	123	"smooth"
		123	124	"smooth"
		124	125	"smooth"
		125	126	"smooth"
		126	127	"smooth"
		127	128	"smooth"
		128	129	"smooth"
		129	130	"smooth"
		130	131	"smooth"
		131	132	"smooth"
		132	133	"smooth"
		133	134	"smooth"
		134	135	"smooth"
		135	136	"smooth"
		136	137	"smooth"
		137	138	"smooth"
		138	139	"smooth"
		139	120	"smooth"
		140	141	"smooth"
		141	142	"smooth"
		142	143	"smooth"
		143	144	"smooth"
		144	145	"smooth"
		145	146	"smooth"
		146	147	"smooth"
		147	148	"smooth"
		148	149	"smooth"
		149	150	"smooth"
		150	151	"smooth"
		151	152	"smooth"
		152	153	"smooth"
		153	154	"smooth"
		154	155	"smooth"
		155	156	"smooth"
		156	157	"smooth"
		157	158	"smooth"
		158	159	"smooth"
		159	140	"smooth"
		160	161	"smooth"
		161	162	"smooth"
		162	163	"smooth"
		163	164	"smooth"
		164	165	"smooth"
		165	166	"smooth"
		166	167	"smooth"
		167	168	"smooth"
		168	169	"smooth"
		169	170	"smooth"
		170	171	"smooth"
		171	172	"smooth"
		172	173	"smooth"
		173	174	"smooth"
		174	175	"smooth"
		175	176	"smooth"
		176	177	"smooth"
		177	178	"smooth"
		178	179	"smooth"
		179	160	"smooth"
		180	181	"smooth"
		181	182	"smooth"
		182	183	"smooth"
		183	184	"smooth"
		184	185	"smooth"
		185	186	"smooth"
		186	187	"smooth"
		187	188	"smooth"
		188	189	"smooth"
		189	190	"smooth"
		190	191	"smooth"
		191	192	"smooth"
		192	193	"smooth"
		193	194	"smooth"
		194	195	"smooth"
		195	196	"smooth"
		196	197	"smooth"
		197	198	"smooth"
		198	199	"smooth"
		199	180	"smooth"
		200	201	"smooth"
		201	202	"smooth"
		202	203	"smooth"
		203	204	"smooth"
		204	205	"smooth"
		205	206	"smooth"
		206	207	"smooth"
		207	208	"smooth"
		208	209	"smooth"
		209	210	"smooth"
		210	211	"smooth"
		211	212	"smooth"
		212	213	"smooth"
		213	214	"smooth"
		214	215	"smooth"
		215	216	"smooth"
		216	217	"smooth"
		217	218	"smooth"
		218	219	"smooth"
		219	200	"smooth"
		220	221	"smooth"
		221	222	"smooth"
		222	223	"smooth"
		223	224	"smooth"
		224	225	"smooth"
		225	226	"smooth"
		226	227	"smooth"
		227	228	"smooth"
		228	229	"smooth"
		229	230	"smooth"
		230	231	"smooth"
		231	232	"smooth"
		232	233	"smooth"
		233	234	"smooth"
		234	235	"smooth"
		235	236	"smooth"
		236	237	"smooth"
		237	238	"smooth"
		238	239	"smooth"
		239	220	"smooth"
		240	241	"smooth"
		241	242	"smooth"
		242	243	"smooth"
		243	244	"smooth"
		244	245	"smooth"
		245	246	"smooth"
		246	247	"smooth"
		247	248	"smooth"
		248	249	"smooth"
		249	250	"smooth"
		250	251	"smooth"
		251	252	"smooth"
		252	253	"smooth"
		253	254	"smooth"
		254	255	"smooth"
		255	256	"smooth"
		256	257	"smooth"
		257	258	"smooth"
		258	259	"smooth"
		259	240	"smooth"
		260	261	"smooth"
		261	262	"smooth"
		262	263	"smooth"
		263	264	"smooth"
		264	265	"smooth"
		265	266	"smooth"
		266	267	"smooth"
		267	268	"smooth"
		268	269	"smooth"
		269	270	"smooth"
		270	271	"smooth"
		271	272	"smooth"
		272	273	"smooth"
		273	274	"smooth"
		274	275	"smooth"
		275	276	"smooth"
		276	277	"smooth"
		277	278	"smooth"
		278	279	"smooth"
		279	260	"smooth"
		280	281	"smooth"
		281	282	"smooth"
		282	283	"smooth"
		283	284	"smooth"
		284	285	"smooth"
		285	286	"smooth"
		286	287	"smooth"
		287	288	"smooth"
		288	289	"smooth"
		289	290	"smooth"
		290	291	"smooth"
		291	292	"smooth"
		292	293	"smooth"
		293	294	"smooth"
		294	295	"smooth"
		295	296	"smooth"
		296	297	"smooth"
		297	298	"smooth"
		298	299	"smooth"
		299	280	"smooth"
		300	301	"smooth"
		301	302	"smooth"
		302	303	"smooth"
		303	304	"smooth"
		304	305	"smooth"
		305	306	"smooth"
		306	307	"smooth"
		307	308	"smooth"
		308	309	"smooth"
		309	310	"smooth"
		310	311	"smooth"
		311	312	"smooth"
		312	313	"smooth"
		313	314	"smooth"
		314	315	"smooth"
		315	316	"smooth"
		316	317	"smooth"
		317	318	"smooth"
		318	319	"smooth"
		319	300	"smooth"
		320	321	"smooth"
		321	322	"smooth"
		322	323	"smooth"
		323	324	"smooth"
		324	325	"smooth"
		325	326	"smooth"
		326	327	"smooth"
		327	328	"smooth"
		328	329	"smooth"
		329	330	"smooth"
		330	331	"smooth"
		331	332	"smooth"
		332	333	"smooth"
		333	334	"smooth"
		334	335	"smooth"
		335	336	"smooth"
		336	337	"smooth"
		337	338	"smooth"
		338	339	"smooth"
		339	320	"smooth"
		340	341	"smooth"
		341	342	"smooth"
		342	343	"smooth"
		343	344	"smooth"
		344	345	"smooth"
		345	346	"smooth"
		346	347	"smooth"
		347	348	"smooth"
		348	349	"smooth"
		349	350	"smooth"
		350	351	"smooth"
		351	352	"smooth"
		352	353	"smooth"
		353	354	"smooth"
		354	355	"smooth"
		355	356	"smooth"
		356	357	"smooth"
		357	358	"smooth"
		358	359	"smooth"
		359	340	"smooth"
		360	361	"smooth"
		361	362	"smooth"
		362	363	"smooth"
		363	364	"smooth"
		364	365	"smooth"
		365	366	"smooth"
		366	367	"smooth"
		367	368	"smooth"
		368	369	"smooth"
		369	370	"smooth"
		370	371	"smooth"
		371	372	"smooth"
		372	373	"smooth"
		373	374	"smooth"
		374	375	"smooth"
		375	376	"smooth"
		376	377	"smooth"
		377	378	"smooth"
		378	379	"smooth"
		379	360	"smooth"
		0	20	"smooth"
		1	21	"smooth"
		2	22	"smooth"
		3	23	"smooth"
		4	24	"smooth"
		5	25	"smooth"
		6	26	"smooth"
		7	27	"smooth"
		8	28	"smooth"
		9	29	"smooth"
		10	30	"smooth"
		11	31	"smooth"
		12	32	"smooth"
		13	33	"smooth"
		14	34	"smooth"
		15	35	"smooth"
		16	36	"smooth"
		17	37	"smooth"
		18	38	"smooth"
		19	39	"smooth"
		20	40	"smooth"
		21	41	"smooth"
		22	42	"smooth"
		23	43	"smooth"
		24	44	"smooth"
		25	45	"smooth"
		26	46	"smooth"
		27	47	"smooth"
		28	48	"smooth"
		29	49	"smooth"
		30	50	"smooth"
		31	51	"smooth"
		32	52	"smooth"
		33	53	"smooth"
		34	54	"smooth"
		35	55	"smooth"
		36	56	"smooth"
		37	57	"smooth"
		38	58	"smooth"
		39	59	"smooth"
		40	60	"smooth"
		41	61	"smooth"
		42	62	"smooth"
		43	63	"smooth"
		44	64	"smooth"
		45	65	"smooth"
		46	66	"smooth"
		47	67	"smooth"
		48	68	"smooth"
		49	69	"smooth"
		50	70	"smooth"
		51	71	"smooth"
		52	72	"smooth"
		53	73	"smooth"
		54	74	"smooth"
		55	75	"smooth"
		56	76	"smooth"
		57	77	"smooth"
		58	78	"smooth"
		59	79	"smooth"
		60	80	"smooth"
		61	81	"smooth"
		62	82	"smooth"
		63	83	"smooth"
		64	84	"smooth"
		65	85	"smooth"
		66	86	"smooth"
		67	87	"smooth"
		68	88	"smooth"
		69	89	"smooth"
		70	90	"smooth"
		71	91	"smooth"
		72	92	"smooth"
		73	93	"smooth"
		74	94	"smooth"
		75	95	"smooth"
		76	96	"smooth"
		77	97	"smooth"
		78	98	"smooth"
		79	99	"smooth"
		80	100	"smooth"
		81	101	"smooth"
		82	102	"smooth"
		83	103	"smooth"
		84	104	"smooth"
		85	105	"smooth"
		86	106	"smooth"
		87	107	"smooth"
		88	108	"smooth"
		89	109	"smooth"
		90	110	"smooth"
		91	111	"smooth"
		92	112	"smooth"
		93	113	"smooth"
		94	114	"smooth"
		95	115	"smooth"
		96	116	"smooth"
		97	117	"smooth"
		98	118	"smooth"
		99	119	"smooth"
		100	120	"smooth"
		101	121	"smooth"
		102	122	"smooth"
		103	123	"smooth"
		104	124	"smooth"
		105	125	"smooth"
		106	126	"smooth"
		107	127	"smooth"
		108	128	"smooth"
		109	129	"smooth"
		110	130	"smooth"
		111	131	"smooth"
		112	132	"smooth"
		113	133	"smooth"
		114	134	"smooth"
		115	135	"smooth"
		116	136	"smooth"
		117	137	"smooth"
		118	138	"smooth"
		119	139	"smooth"
		120	140	"smooth"
		121	141	"smooth"
		122	142	"smooth"
		123	143	"smooth"
		124	144	"smooth"
		125	145	"smooth"
		126	146	"smooth"
		127	147	"smooth"
		128	148	"smooth"
		129	149	"smooth"
		130	150	"smooth"
		131	151	"smooth"
		132	152	"smooth"
		133	153	"smooth"
		134	154	"smooth"
		135	155	"smooth"
		136	156	"smooth"
		137	157	"smooth"
		138	158	"smooth"
		139	159	"smooth"
		140	160	"smooth"
		141	161	"smooth"
		142	162	"smooth"
		143	163	"smooth"
		144	164	"smooth"
		145	165	"smooth"
		146	166	"smooth"
		147	167	"smooth"
		148	168	"smooth"
		149	169	"smooth"
		150	170	"smooth"
		151	171	"smooth"
		152	172	"smooth"
		153	173	"smooth"
		154	174	"smooth"
		155	175	"smooth"
		156	176	"smooth"
		157	177	"smooth"
		158	178	"smooth"
		159	179	"smooth"
		160	180	"smooth"
		161	181	"smooth"
		162	182	"smooth"
		163	183	"smooth"
		164	184	"smooth"
		165	185	"smooth"
		166	186	"smooth"
		167	187	"smooth"
		168	188	"smooth"
		169	189	"smooth"
		170	190	"smooth"
		171	191	"smooth"
		172	192	"smooth"
		173	193	"smooth"
		174	194	"smooth"
		175	195	"smooth"
		176	196	"smooth"
		177	197	"smooth"
		178	198	"smooth"
		179	199	"smooth"
		180	200	"smooth"
		181	201	"smooth"
		182	202	"smooth"
		183	203	"smooth"
		184	204	"smooth"
		185	205	"smooth"
		186	206	"smooth"
		187	207	"smooth"
		188	208	"smooth"
		189	209	"smooth"
		190	210	"smooth"
		191	211	"smooth"
		192	212	"smooth"
		193	213	"smooth"
		194	214	"smooth"
		195	215	"smooth"
		196	216	"smooth"
		197	217	"smooth"
		198	218	"smooth"
		199	219	"smooth"
		200	220	"smooth"
		201	221	"smooth"
		202	222	"smooth"
		203	223	"smooth"
		204	224	"smooth"
		205	225	"smooth"
		206	226	"smooth"
		207	227	"smooth"
		208	228	"smooth"
		209	229	"smooth"
		210	230	"smooth"
		211	231	"smooth"
		212	232	"smooth"
		213	233	"smooth"
		214	234	"smooth"
		215	235	"smooth"
		216	236	"smooth"
		217	237	"smooth"
		218	238	"smooth"
		219	239	"smooth"
		220	240	"smooth"
		221	241	"smooth"
		222	242	"smooth"
		223	243	"smooth"
		224	244	"smooth"
		225	245	"smooth"
		226	246	"smooth"
		227	247	"smooth"
		228	248	"smooth"
		229	249	"smooth"
		230	250	"smooth"
		231	251	"smooth"
		232	252	"smooth"
		233	253	"smooth"
		234	254	"smooth"
		235	255	"smooth"
		236	256	"smooth"
		237	257	"smooth"
		238	258	"smooth"
		239	259	"smooth"
		240	260	"smooth"
		241	261	"smooth"
		242	262	"smooth"
		243	263	"smooth"
		244	264	"smooth"
		245	265	"smooth"
		246	266	"smooth"
		247	267	"smooth"
		248	268	"smooth"
		249	269	"smooth"
		250	270	"smooth"
		251	271	"smooth"
		252	272	"smooth"
		253	273	"smooth"
		254	274	"smooth"
		255	275	"smooth"
		256	276	"smooth"
		257	277	"smooth"
		258	278	"smooth"
		259	279	"smooth"
		260	280	"smooth"
		261	281	"smooth"
		262	282	"smooth"
		263	283	"smooth"
		264	284	"smooth"
		265	285	"smooth"
		266	286	"smooth"
		267	287	"smooth"
		268	288	"smooth"
		269	289	"smooth"
		270	290	"smooth"
		271	291	"smooth"
		272	292	"smooth"
		273	293	"smooth"
		274	294	"smooth"
		275	295	"smooth"
		276	296	"smooth"
		277	297	"smooth"
		278	298	"smooth"
		279	299	"smooth"
		280	300	"smooth"
		281	301	"smooth"
		282	302	"smooth"
		283	303	"smooth"
		284	304	"smooth"
		285	305	"smooth"
		286	306	"smooth"
		287	307	"smooth"
		288	308	"smooth"
		289	309	"smooth"
		290	310	"smooth"
		291	311	"smooth"
		292	312	"smooth"
		293	313	"smooth"
		294	314	"smooth"
		295	315	"smooth"
		296	316	"smooth"
		297	317	"smooth"
		298	318	"smooth"
		299	319	"smooth"
		300	320	"smooth"
		301	321	"smooth"
		302	322	"smooth"
		303	323	"smooth"
		304	324	"smooth"
		305	325	"smooth"
		306	326	"smooth"
		307	327	"smooth"
		308	328	"smooth"
		309	329	"smooth"
		310	330	"smooth"
		311	331	"smooth"
		312	332	"smooth"
		313	333	"smooth"
		314	334	"smooth"
		315	335	"smooth"
		316	336	"smooth"
		317	337	"smooth"
		318	338	"smooth"
		319	339	"smooth"
		320	340	"smooth"
		321	341	"smooth"
		322	342	"smooth"
		323	343	"smooth"
		324	344	"smooth"
		325	345	"smooth"
		326	346	"smooth"
		327	347	"smooth"
		328	348	"smooth"
		329	349	"smooth"
		330	350	"smooth"
		331	351	"smooth"
		332	352	"smooth"
		333	353	"smooth"
		334	354	"smooth"
		335	355	"smooth"
		336	356	"smooth"
		337	357	"smooth"
		338	358	"smooth"
		339	359	"smooth"
		340	360	"smooth"
		341	361	"smooth"
		342	362	"smooth"
		343	363	"smooth"
		344	364	"smooth"
		345	365	"smooth"
		346	366	"smooth"
		347	367	"smooth"
		348	368	"smooth"
		349	369	"smooth"
		350	370	"smooth"
		351	371	"smooth"
		352	372	"smooth"
		353	373	"smooth"
		354	374	"smooth"
		355	375	"smooth"
		356	376	"smooth"
		357	377	"smooth"
		358	378	"smooth"
		359	379	"smooth"
		380	0	"smooth"
		380	1	"smooth"
		380	2	"smooth"
		380	3	"smooth"
		380	4	"smooth"
		380	5	"smooth"
		380	6	"smooth"
		380	7	"smooth"
		380	8	"smooth"
		380	9	"smooth"
		380	10	"smooth"
		380	11	"smooth"
		380	12	"smooth"
		380	13	"smooth"
		380	14	"smooth"
		380	15	"smooth"
		380	16	"smooth"
		380	17	"smooth"
		380	18	"smooth"
		380	19	"smooth"
		360	381	"smooth"
		361	381	"smooth"
		362	381	"smooth"
		363	381	"smooth"
		364	381	"smooth"
		365	381	"smooth"
		366	381	"smooth"
		367	381	"smooth"
		368	381	"smooth"
		369	381	"smooth"
		370	381	"smooth"
		371	381	"smooth"
		372	381	"smooth"
		373	381	"smooth"
		374	381	"smooth"
		375	381	"smooth"
		376	381	"smooth"
		377	381	"smooth"
		378	381	"smooth"
		379	381	"smooth"

		"face"	
		"l"	4	0	381	-21	-381	
		"lt"	4	0	1	22	21	

		"face"	
		"l"	4	1	382	-22	-382	
		"lt"	4	1	2	23	22	

		"face"	
		"l"	4	2	383	-23	-383	
		"lt"	4	2	3	24	23	

		"face"	
		"l"	4	3	384	-24	-384	
		"lt"	4	3	4	25	24	

		"face"	
		"l"	4	4	385	-25	-385	
		"lt"	4	4	5	26	25	

		"face"	
		"l"	4	5	386	-26	-386	
		"lt"	4	5	6	27	26	

		"face"	
		"l"	4	6	387	-27	-387	
		"lt"	4	6	7	28	27	

		"face"	
		"l"	4	7	388	-28	-388	
		"lt"	4	7	8	29	28	

		"face"	
		"l"	4	8	389	-29	-389	
		"lt"	4	8	9	30	29	

		"face"	
		"l"	4	9	390	-30	-390	
		"lt"	4	9	10	31	30	

		"face"	
		"l"	4	10	391	-31	-391	
		"lt"	4	10	11	32	31	

		"face"	
		"l"	4	11	392	-32	-392	
		"lt"	4	11	12	33	32	

		"face"	
		"l"	4	12	393	-33	-393	
		"lt"	4	12	13	34	33	

		"face"	
		"l"	4	13	394	-34	-394	
		"lt"	4	13	14	35	34	

		"face"	
		"l"	4	14	395	-35	-395	
		"lt"	4	14	15	36	35	

		"face"	
		"l"	4	15	396	-36	-396	
		"lt"	4	15	16	37	36	

		"face"	
		"l"	4	16	397	-37	-397	
		"lt"	4	16	17	38	37	

		"face"	
		"l"	4	17	398	-38	-398	
		"lt"	4	17	18	39	38	

		"face"	
		"l"	4	18	399	-39	-399	
		"lt"	4	18	19	40	39	

		"face"	
		"l"	4	19	380	-40	-400	
		"lt"	4	19	20	41	40	

		"face"	
		"l"	4	20	401	-41	-401	
		"lt"	4	21	22	43	42	

		"face"	
		"l"	4	21	402	-42	-402	
		"lt"	4	22	23	44	43	

		"face"	
		"l"	4	22	403	-43	-403	
		"lt"	4	23	24	45	44	

		"face"	
		"l"	4	23	404	-44	-404	
		"lt"	4	24	25	46	45	

		"face"	
		"l"	4	24	405	-45	-405	
		"lt"	4	25	26	47	46	

		"face"	
		"l"	4	25	406	-46	-406	
		"lt"	4	26	27	48	47	

		"face"	
		"l"	4	26	407	-47	-407	
		"lt"	4	27	28	49	48	

		"face"	
		"l"	4	27	408	-48	-408	
		"lt"	4	28	29	50	49	

		"face"	
		"l"	4	28	409	-49	-409	
		"lt"	4	29	30	51	50	

		"face"	
		"l"	4	29	410	-50	-410	
		"lt"	4	30	31	52	51	

		"face"	
		"l"	4	30	411	-51	-411	
		"lt"	4	31	32	53	52	

		"face"	
		"l"	4	31	412	-52	-412	
		"lt"	4	32	33	54	53	

		"face"	
		"l"	4	32	413	-53	-413	
		"lt"	4	33	34	55	54	

		"face"	
		"l"	4	33	414	-54	-414	
		"lt"	4	34	35	56	55	

		"face"	
		"l"	4	34	415	-55	-415	
		"lt"	4	35	36	57	56	

		"face"	
		"l"	4	35	416	-56	-416	
		"lt"	4	36	37	58	57	

		"face"	
		"l"	4	36	417	-57	-417	
		"lt"	4	37	38	59	58	

		"face"	
		"l"	4	37	418	-58	-418	
		"lt"	4	38	39	60	59	

		"face"	
		"l"	4	38	419	-59	-419	
		"lt"	4	39	40	61	60	

		"face"	
		"l"	4	39	400	-60	-420	
		"lt"	4	40	41	62	61	

		"face"	
		"l"	4	40	421	-61	-421	
		"lt"	4	42	43	64	63	

		"face"	
		"l"	4	41	422	-62	-422	
		"lt"	4	43	44	65	64	

		"face"	
		"l"	4	42	423	-63	-423	
		"lt"	4	44	45	66	65	

		"face"	
		"l"	4	43	424	-64	-424	
		"lt"	4	45	46	67	66	

		"face"	
		"l"	4	44	425	-65	-425	
		"lt"	4	46	47	68	67	

		"face"	
		"l"	4	45	426	-66	-426	
		"lt"	4	47	48	69	68	

		"face"	
		"l"	4	46	427	-67	-427	
		"lt"	4	48	49	70	69	

		"face"	
		"l"	4	47	428	-68	-428	
		"lt"	4	49	50	71	70	

		"face"	
		"l"	4	48	429	-69	-429	
		"lt"	4	50	51	72	71	

		"face"	
		"l"	4	49	430	-70	-430	
		"lt"	4	51	52	73	72	

		"face"	
		"l"	4	50	431	-71	-431	
		"lt"	4	52	53	74	73	

		"face"	
		"l"	4	51	432	-72	-432	
		"lt"	4	53	54	75	74	

		"face"	
		"l"	4	52	433	-73	-433	
		"lt"	4	54	55	76	75	

		"face"	
		"l"	4	53	434	-74	-434	
		"lt"	4	55	56	77	76	

		"face"	
		"l"	4	54	435	-75	-435	
		"lt"	4	56	57	78	77	

		"face"	
		"l"	4	55	436	-76	-436	
		"lt"	4	57	58	79	78	

		"face"	
		"l"	4	56	437	-77	-437	
		"lt"	4	58	59	80	79	

		"face"	
		"l"	4	57	438	-78	-438	
		"lt"	4	59	60	81	80	

		"face"	
		"l"	4	58	439	-79	-439	
		"lt"	4	60	61	82	81	

		"face"	
		"l"	4	59	420	-80	-440	
		"lt"	4	61	62	83	82	

		"face"	
		"l"	4	60	441	-81	-441	
		"lt"	4	63	64	85	84	

		"face"	
		"l"	4	61	442	-82	-442	
		"lt"	4	64	65	86	85	

		"face"	
		"l"	4	62	443	-83	-443	
		"lt"	4	65	66	87	86	

		"face"	
		"l"	4	63	444	-84	-444	
		"lt"	4	66	67	88	87	

		"face"	
		"l"	4	64	445	-85	-445	
		"lt"	4	67	68	89	88	

		"face"	
		"l"	4	65	446	-86	-446	
		"lt"	4	68	69	90	89	

		"face"	
		"l"	4	66	447	-87	-447	
		"lt"	4	69	70	91	90	

		"face"	
		"l"	4	67	448	-88	-448	
		"lt"	4	70	71	92	91	

		"face"	
		"l"	4	68	449	-89	-449	
		"lt"	4	71	72	93	92	

		"face"	
		"l"	4	69	450	-90	-450	
		"lt"	4	72	73	94	93	

		"face"	
		"l"	4	70	451	-91	-451	
		"lt"	4	73	74	95	94	

		"face"	
		"l"	4	71	452	-92	-452	
		"lt"	4	74	75	96	95	

		"face"	
		"l"	4	72	453	-93	-453	
		"lt"	4	75	76	97	96	

		"face"	
		"l"	4	73	454	-94	-454	
		"lt"	4	76	77	98	97	

		"face"	
		"l"	4	74	455	-95	-455	
		"lt"	4	77	78	99	98	

		"face"	
		"l"	4	75	456	-96	-456	
		"lt"	4	78	79	100	99	

		"face"	
		"l"	4	76	457	-97	-457	
		"lt"	4	79	80	101	100	

		"face"	
		"l"	4	77	458	-98	-458	
		"lt"	4	80	81	102	101	

		"face"	
		"l"	4	78	459	-99	-459	
		"lt"	4	81	82	103	102	

		"face"	
		"l"	4	79	440	-100	-460	
		"lt"	4	82	83	104	103	

		"face"	
		"l"	4	80	461	-101	-461	
		"lt"	4	84	85	106	105	

		"face"	
		"l"	4	81	462	-102	-462	
		"lt"	4	85	86	107	106	

		"face"	
		"l"	4	82	463	-103	-463	
		"lt"	4	86	87	108	107	

		"face"	
		"l"	4	83	464	-104	-464	
		"lt"	4	87	88	109	108	

		"face"	
		"l"	4	84	465	-105	-465	
		"lt"	4	88	89	110	109	

		"face"	
		"l"	4	85	466	-106	-466	
		"lt"	4	89	90	111	110	

		"face"	
		"l"	4	86	467	-107	-467	
		"lt"	4	90	91	112	111	

		"face"	
		"l"	4	87	468	-108	-468	
		"lt"	4	91	92	113	112	

		"face"	
		"l"	4	88	469	-109	-469	
		"lt"	4	92	93	114	113	

		"face"	
		"l"	4	89	470	-110	-470	
		"lt"	4	93	94	115	114	

		"face"	
		"l"	4	90	471	-111	-471	
		"lt"	4	94	95	116	115	

		"face"	
		"l"	4	91	472	-112	-472	
		"lt"	4	95	96	117	116	

		"face"	
		"l"	4	92	473	-113	-473	
		"lt"	4	96	97	118	117	

		"face"	
		"l"	4	93	474	-114	-474	
		"lt"	4	97	98	119	118	

		"face"	
		"l"	4	94	475	-115	-475	
		"lt"	4	98	99	120	119	

		"face"	
		"l"	4	95	476	-116	-476	
		"lt"	4	99	100	121	120	

		"face"	
		"l"	4	96	477	-117	-477	
		"lt"	4	100	101	122	121	

		"face"	
		"l"	4	97	478	-118	-478	
		"lt"	4	101	102	123	122	

		"face"	
		"l"	4	98	479	-119	-479	
		"lt"	4	102	103	124	123	

		"face"	
		"l"	4	99	460	-120	-480	
		"lt"	4	103	104	125	124	

		"face"	
		"l"	4	100	481	-121	-481	
		"lt"	4	105	106	127	126	

		"face"	
		"l"	4	101	482	-122	-482	
		"lt"	4	106	107	128	127	

		"face"	
		"l"	4	102	483	-123	-483	
		"lt"	4	107	108	129	128	

		"face"	
		"l"	4	103	484	-124	-484	
		"lt"	4	108	109	130	129	

		"face"	
		"l"	4	104	485	-125	-485	
		"lt"	4	109	110	131	130	

		"face"	
		"l"	4	105	486	-126	-486	
		"lt"	4	110	111	132	131	

		"face"	
		"l"	4	106	487	-127	-487	
		"lt"	4	111	112	133	132	

		"face"	
		"l"	4	107	488	-128	-488	
		"lt"	4	112	113	134	133	

		"face"	
		"l"	4	108	489	-129	-489	
		"lt"	4	113	114	135	134	

		"face"	
		"l"	4	109	490	-130	-490	
		"lt"	4	114	115	136	135	

		"face"	
		"l"	4	110	491	-131	-491	
		"lt"	4	115	116	137	136	

		"face"	
		"l"	4	111	492	-132	-492	
		"lt"	4	116	117	138	137	

		"face"	
		"l"	4	112	493	-133	-493	
		"lt"	4	117	118	139	138	

		"face"	
		"l"	4	113	494	-134	-494	
		"lt"	4	118	119	140	139	

		"face"	
		"l"	4	114	495	-135	-495	
		"lt"	4	119	120	141	140	

		"face"	
		"l"	4	115	496	-136	-496	
		"lt"	4	120	121	142	141	

		"face"	
		"l"	4	116	497	-137	-497	
		"lt"	4	121	122	143	142	

		"face"	
		"l"	4	117	498	-138	-498	
		"lt"	4	122	123	144	143	

		"face"	
		"l"	4	118	499	-139	-499	
		"lt"	4	123	124	145	144	

		"face"	
		"l"	4	119	480	-140	-500	
		"lt"	4	124	125	146	145	

		"face"	
		"l"	4	120	501	-141	-501	
		"lt"	4	126	127	148	147	

		"face"	
		"l"	4	121	502	-142	-502	
		"lt"	4	127	128	149	148	

		"face"	
		"l"	4	122	503	-143	-503	
		"lt"	4	128	129	150	149	

		"face"	
		"l"	4	123	504	-144	-504	
		"lt"	4	129	130	151	150	

		"face"	
		"l"	4	124	505	-145	-505	
		"lt"	4	130	131	152	151	

		"face"	
		"l"	4	125	506	-146	-506	
		"lt"	4	131	132	153	152	

		"face"	
		"l"	4	126	507	-147	-507	
		"lt"	4	132	133	154	153	

		"face"	
		"l"	4	127	508	-148	-508	
		"lt"	4	133	134	155	154	

		"face"	
		"l"	4	128	509	-149	-509	
		"lt"	4	134	135	156	155	

		"face"	
		"l"	4	129	510	-150	-510	
		"lt"	4	135	136	157	156	

		"face"	
		"l"	4	130	511	-151	-511	
		"lt"	4	136	137	158	157	

		"face"	
		"l"	4	131	512	-152	-512	
		"lt"	4	137	138	159	158	

		"face"	
		"l"	4	132	513	-153	-513	
		"lt"	4	138	139	160	159	

		"face"	
		"l"	4	133	514	-154	-514	
		"lt"	4	139	140	161	160	

		"face"	
		"l"	4	134	515	-155	-515	
		"lt"	4	140	141	162	161	

		"face"	
		"l"	4	135	516	-156	-516	
		"lt"	4	141	142	163	162	

		"face"	
		"l"	4	136	517	-157	-517	
		"lt"	4	142	143	164	163	

		"face"	
		"l"	4	137	518	-158	-518	
		"lt"	4	143	144	165	164	

		"face"	
		"l"	4	138	519	-159	-519	
		"lt"	4	144	145	166	165	

		"face"	
		"l"	4	139	500	-160	-520	
		"lt"	4	145	146	167	166	

		"face"	
		"l"	4	140	521	-161	-521	
		"lt"	4	147	148	169	168	

		"face"	
		"l"	4	141	522	-162	-522	
		"lt"	4	148	149	170	169	

		"face"	
		"l"	4	142	523	-163	-523	
		"lt"	4	149	150	171	170	

		"face"	
		"l"	4	143	524	-164	-524	
		"lt"	4	150	151	172	171	

		"face"	
		"l"	4	144	525	-165	-525	
		"lt"	4	151	152	173	172	

		"face"	
		"l"	4	145	526	-166	-526	
		"lt"	4	152	153	174	173	

		"face"	
		"l"	4	146	527	-167	-527	
		"lt"	4	153	154	175	174	

		"face"	
		"l"	4	147	528	-168	-528	
		"lt"	4	154	155	176	175	

		"face"	
		"l"	4	148	529	-169	-529	
		"lt"	4	155	156	177	176	

		"face"	
		"l"	4	149	530	-170	-530	
		"lt"	4	156	157	178	177	

		"face"	
		"l"	4	150	531	-171	-531	
		"lt"	4	157	158	179	178	

		"face"	
		"l"	4	151	532	-172	-532	
		"lt"	4	158	159	180	179	

		"face"	
		"l"	4	152	533	-173	-533	
		"lt"	4	159	160	181	180	

		"face"	
		"l"	4	153	534	-174	-534	
		"lt"	4	160	161	182	181	

		"face"	
		"l"	4	154	535	-175	-535	
		"lt"	4	161	162	183	182	

		"face"	
		"l"	4	155	536	-176	-536	
		"lt"	4	162	163	184	183	

		"face"	
		"l"	4	156	537	-177	-537	
		"lt"	4	163	164	185	184	

		"face"	
		"l"	4	157	538	-178	-538	
		"lt"	4	164	165	186	185	

		"face"	
		"l"	4	158	539	-179	-539	
		"lt"	4	165	166	187	186	

		"face"	
		"l"	4	159	520	-180	-540	
		"lt"	4	166	167	188	187	

		"face"	
		"l"	4	160	541	-181	-541	
		"lt"	4	168	169	190	189	

		"face"	
		"l"	4	161	542	-182	-542	
		"lt"	4	169	170	191	190	

		"face"	
		"l"	4	162	543	-183	-543	
		"lt"	4	170	171	192	191	

		"face"	
		"l"	4	163	544	-184	-544	
		"lt"	4	171	172	193	192	

		"face"	
		"l"	4	164	545	-185	-545	
		"lt"	4	172	173	194	193	

		"face"	
		"l"	4	165	546	-186	-546	
		"lt"	4	173	174	195	194	

		"face"	
		"l"	4	166	547	-187	-547	
		"lt"	4	174	175	196	195	

		"face"	
		"l"	4	167	548	-188	-548	
		"lt"	4	175	176	197	196	

		"face"	
		"l"	4	168	549	-189	-549	
		"lt"	4	176	177	198	197	

		"face"	
		"l"	4	169	550	-190	-550	
		"lt"	4	177	178	199	198	

		"face"	
		"l"	4	170	551	-191	-551	
		"lt"	4	178	179	200	199	

		"face"	
		"l"	4	171	552	-192	-552	
		"lt"	4	179	180	201	200	

		"face"	
		"l"	4	172	553	-193	-553	
		"lt"	4	180	181	202	201	

		"face"	
		"l"	4	173	554	-194	-554	
		"lt"	4	181	182	203	202	

		"face"	
		"l"	4	174	555	-195	-555	
		"lt"	4	182	183	204	203	

		"face"	
		"l"	4	175	556	-196	-556	
		"lt"	4	183	184	205	204	

		"face"	
		"l"	4	176	557	-197	-557	
		"lt"	4	184	185	206	205	

		"face"	
		"l"	4	177	558	-198	-558	
		"lt"	4	185	186	207	206	

		"face"	
		"l"	4	178	559	-199	-559	
		"lt"	4	186	187	208	207	

		"face"	
		"l"	4	179	540	-200	-560	
		"lt"	4	187	188	209	208	

		"face"	
		"l"	4	180	561	-201	-561	
		"lt"	4	189	190	211	210	

		"face"	
		"l"	4	181	562	-202	-562	
		"lt"	4	190	191	212	211	

		"face"	
		"l"	4	182	563	-203	-563	
		"lt"	4	191	192	213	212	

		"face"	
		"l"	4	183	564	-204	-564	
		"lt"	4	192	193	214	213	

		"face"	
		"l"	4	184	565	-205	-565	
		"lt"	4	193	194	215	214	

		"face"	
		"l"	4	185	566	-206	-566	
		"lt"	4	194	195	216	215	

		"face"	
		"l"	4	186	567	-207	-567	
		"lt"	4	195	196	217	216	

		"face"	
		"l"	4	187	568	-208	-568	
		"lt"	4	196	197	218	217	

		"face"	
		"l"	4	188	569	-209	-569	
		"lt"	4	197	198	219	218	

		"face"	
		"l"	4	189	570	-210	-570	
		"lt"	4	198	199	220	219	

		"face"	
		"l"	4	190	571	-211	-571	
		"lt"	4	199	200	221	220	

		"face"	
		"l"	4	191	572	-212	-572	
		"lt"	4	200	201	222	221	

		"face"	
		"l"	4	192	573	-213	-573	
		"lt"	4	201	202	223	222	

		"face"	
		"l"	4	193	574	-214	-574	
		"lt"	4	202	203	224	223	

		"face"	
		"l"	4	194	575	-215	-575	
		"lt"	4	203	204	225	224	

		"face"	
		"l"	4	195	576	-216	-576	
		"lt"	4	204	205	226	225	

		"face"	
		"l"	4	196	577	-217	-577	
		"lt"	4	205	206	227	226	

		"face"	
		"l"	4	197	578	-218	-578	
		"lt"	4	206	207	228	227	

		"face"	
		"l"	4	198	579	-219	-579	
		"lt"	4	207	208	229	228	

		"face"	
		"l"	4	199	560	-220	-580	
		"lt"	4	208	209	230	229	

		"face"	
		"l"	4	200	581	-221	-581	
		"lt"	4	210	211	232	231	

		"face"	
		"l"	4	201	582	-222	-582	
		"lt"	4	211	212	233	232	

		"face"	
		"l"	4	202	583	-223	-583	
		"lt"	4	212	213	234	233	

		"face"	
		"l"	4	203	584	-224	-584	
		"lt"	4	213	214	235	234	

		"face"	
		"l"	4	204	585	-225	-585	
		"lt"	4	214	215	236	235	

		"face"	
		"l"	4	205	586	-226	-586	
		"lt"	4	215	216	237	236	

		"face"	
		"l"	4	206	587	-227	-587	
		"lt"	4	216	217	238	237	

		"face"	
		"l"	4	207	588	-228	-588	
		"lt"	4	217	218	239	238	

		"face"	
		"l"	4	208	589	-229	-589	
		"lt"	4	218	219	240	239	

		"face"	
		"l"	4	209	590	-230	-590	
		"lt"	4	219	220	241	240	

		"face"	
		"l"	4	210	591	-231	-591	
		"lt"	4	220	221	242	241	

		"face"	
		"l"	4	211	592	-232	-592	
		"lt"	4	221	222	243	242	

		"face"	
		"l"	4	212	593	-233	-593	
		"lt"	4	222	223	244	243	

		"face"	
		"l"	4	213	594	-234	-594	
		"lt"	4	223	224	245	244	

		"face"	
		"l"	4	214	595	-235	-595	
		"lt"	4	224	225	246	245	

		"face"	
		"l"	4	215	596	-236	-596	
		"lt"	4	225	226	247	246	

		"face"	
		"l"	4	216	597	-237	-597	
		"lt"	4	226	227	248	247	

		"face"	
		"l"	4	217	598	-238	-598	
		"lt"	4	227	228	249	248	

		"face"	
		"l"	4	218	599	-239	-599	
		"lt"	4	228	229	250	249	

		"face"	
		"l"	4	219	580	-240	-600	
		"lt"	4	229	230	251	250	

		"face"	
		"l"	4	220	601	-241	-601	
		"lt"	4	231	232	253	252	

		"face"	
		"l"	4	221	602	-242	-602	
		"lt"	4	232	233	254	253	

		"face"	
		"l"	4	222	603	-243	-603	
		"lt"	4	233	234	255	254	

		"face"	
		"l"	4	223	604	-244	-604	
		"lt"	4	234	235	256	255	

		"face"	
		"l"	4	224	605	-245	-605	
		"lt"	4	235	236	257	256	

		"face"	
		"l"	4	225	606	-246	-606	
		"lt"	4	236	237	258	257	

		"face"	
		"l"	4	226	607	-247	-607	
		"lt"	4	237	238	259	258	

		"face"	
		"l"	4	227	608	-248	-608	
		"lt"	4	238	239	260	259	

		"face"	
		"l"	4	228	609	-249	-609	
		"lt"	4	239	240	261	260	

		"face"	
		"l"	4	229	610	-250	-610	
		"lt"	4	240	241	262	261	

		"face"	
		"l"	4	230	611	-251	-611	
		"lt"	4	241	242	263	262	

		"face"	
		"l"	4	231	612	-252	-612	
		"lt"	4	242	243	264	263	

		"face"	
		"l"	4	232	613	-253	-613	
		"lt"	4	243	244	265	264	

		"face"	
		"l"	4	233	614	-254	-614	
		"lt"	4	244	245	266	265	

		"face"	
		"l"	4	234	615	-255	-615	
		"lt"	4	245	246	267	266	

		"face"	
		"l"	4	235	616	-256	-616	
		"lt"	4	246	247	268	267	

		"face"	
		"l"	4	236	617	-257	-617	
		"lt"	4	247	248	269	268	

		"face"	
		"l"	4	237	618	-258	-618	
		"lt"	4	248	249	270	269	

		"face"	
		"l"	4	238	619	-259	-619	
		"lt"	4	249	250	271	270	

		"face"	
		"l"	4	239	600	-260	-620	
		"lt"	4	250	251	272	271	

		"face"	
		"l"	4	240	621	-261	-621	
		"lt"	4	252	253	274	273	

		"face"	
		"l"	4	241	622	-262	-622	
		"lt"	4	253	254	275	274	

		"face"	
		"l"	4	242	623	-263	-623	
		"lt"	4	254	255	276	275	

		"face"	
		"l"	4	243	624	-264	-624	
		"lt"	4	255	256	277	276	

		"face"	
		"l"	4	244	625	-265	-625	
		"lt"	4	256	257	278	277	

		"face"	
		"l"	4	245	626	-266	-626	
		"lt"	4	257	258	279	278	

		"face"	
		"l"	4	246	627	-267	-627	
		"lt"	4	258	259	280	279	

		"face"	
		"l"	4	247	628	-268	-628	
		"lt"	4	259	260	281	280	

		"face"	
		"l"	4	248	629	-269	-629	
		"lt"	4	260	261	282	281	

		"face"	
		"l"	4	249	630	-270	-630	
		"lt"	4	261	262	283	282	

		"face"	
		"l"	4	250	631	-271	-631	
		"lt"	4	262	263	284	283	

		"face"	
		"l"	4	251	632	-272	-632	
		"lt"	4	263	264	285	284	

		"face"	
		"l"	4	252	633	-273	-633	
		"lt"	4	264	265	286	285	

		"face"	
		"l"	4	253	634	-274	-634	
		"lt"	4	265	266	287	286	

		"face"	
		"l"	4	254	635	-275	-635	
		"lt"	4	266	267	288	287	

		"face"	
		"l"	4	255	636	-276	-636	
		"lt"	4	267	268	289	288	

		"face"	
		"l"	4	256	637	-277	-637	
		"lt"	4	268	269	290	289	

		"face"	
		"l"	4	257	638	-278	-638	
		"lt"	4	269	270	291	290	

		"face"	
		"l"	4	258	639	-279	-639	
		"lt"	4	270	271	292	291	

		"face"	
		"l"	4	259	620	-280	-640	
		"lt"	4	271	272	293	292	

		"face"	
		"l"	4	260	641	-281	-641	
		"lt"	4	273	274	295	294	

		"face"	
		"l"	4	261	642	-282	-642	
		"lt"	4	274	275	296	295	

		"face"	
		"l"	4	262	643	-283	-643	
		"lt"	4	275	276	297	296	

		"face"	
		"l"	4	263	644	-284	-644	
		"lt"	4	276	277	298	297	

		"face"	
		"l"	4	264	645	-285	-645	
		"lt"	4	277	278	299	298	

		"face"	
		"l"	4	265	646	-286	-646	
		"lt"	4	278	279	300	299	

		"face"	
		"l"	4	266	647	-287	-647	
		"lt"	4	279	280	301	300	

		"face"	
		"l"	4	267	648	-288	-648	
		"lt"	4	280	281	302	301	

		"face"	
		"l"	4	268	649	-289	-649	
		"lt"	4	281	282	303	302	

		"face"	
		"l"	4	269	650	-290	-650	
		"lt"	4	282	283	304	303	

		"face"	
		"l"	4	270	651	-291	-651	
		"lt"	4	283	284	305	304	

		"face"	
		"l"	4	271	652	-292	-652	
		"lt"	4	284	285	306	305	

		"face"	
		"l"	4	272	653	-293	-653	
		"lt"	4	285	286	307	306	

		"face"	
		"l"	4	273	654	-294	-654	
		"lt"	4	286	287	308	307	

		"face"	
		"l"	4	274	655	-295	-655	
		"lt"	4	287	288	309	308	

		"face"	
		"l"	4	275	656	-296	-656	
		"lt"	4	288	289	310	309	

		"face"	
		"l"	4	276	657	-297	-657	
		"lt"	4	289	290	311	310	

		"face"	
		"l"	4	277	658	-298	-658	
		"lt"	4	290	291	312	311	

		"face"	
		"l"	4	278	659	-299	-659	
		"lt"	4	291	292	313	312	

		"face"	
		"l"	4	279	640	-300	-660	
		"lt"	4	292	293	314	313	

		"face"	
		"l"	4	280	661	-301	-661	
		"lt"	4	294	295	316	315	

		"face"	
		"l"	4	281	662	-302	-662	
		"lt"	4	295	296	317	316	

		"face"	
		"l"	4	282	663	-303	-663	
		"lt"	4	296	297	318	317	

		"face"	
		"l"	4	283	664	-304	-664	
		"lt"	4	297	298	319	318	

		"face"	
		"l"	4	284	665	-305	-665	
		"lt"	4	298	299	320	319	

		"face"	
		"l"	4	285	666	-306	-666	
		"lt"	4	299	300	321	320	

		"face"	
		"l"	4	286	667	-307	-667	
		"lt"	4	300	301	322	321	

		"face"	
		"l"	4	287	668	-308	-668	
		"lt"	4	301	302	323	322	

		"face"	
		"l"	4	288	669	-309	-669	
		"lt"	4	302	303	324	323	

		"face"	
		"l"	4	289	670	-310	-670	
		"lt"	4	303	304	325	324	

		"face"	
		"l"	4	290	671	-311	-671	
		"lt"	4	304	305	326	325	

		"face"	
		"l"	4	291	672	-312	-672	
		"lt"	4	305	306	327	326	

		"face"	
		"l"	4	292	673	-313	-673	
		"lt"	4	306	307	328	327	

		"face"	
		"l"	4	293	674	-314	-674	
		"lt"	4	307	308	329	328	

		"face"	
		"l"	4	294	675	-315	-675	
		"lt"	4	308	309	330	329	

		"face"	
		"l"	4	295	676	-316	-676	
		"lt"	4	309	310	331	330	

		"face"	
		"l"	4	296	677	-317	-677	
		"lt"	4	310	311	332	331	

		"face"	
		"l"	4	297	678	-318	-678	
		"lt"	4	311	312	333	332	

		"face"	
		"l"	4	298	679	-319	-679	
		"lt"	4	312	313	334	333	

		"face"	
		"l"	4	299	660	-320	-680	
		"lt"	4	313	314	335	334	

		"face"	
		"l"	4	300	681	-321	-681	
		"lt"	4	315	316	337	336	

		"face"	
		"l"	4	301	682	-322	-682	
		"lt"	4	316	317	338	337	

		"face"	
		"l"	4	302	683	-323	-683	
		"lt"	4	317	318	339	338	

		"face"	
		"l"	4	303	684	-324	-684	
		"lt"	4	318	319	340	339	

		"face"	
		"l"	4	304	685	-325	-685	
		"lt"	4	319	320	341	340	

		"face"	
		"l"	4	305	686	-326	-686	
		"lt"	4	320	321	342	341	

		"face"	
		"l"	4	306	687	-327	-687	
		"lt"	4	321	322	343	342	

		"face"	
		"l"	4	307	688	-328	-688	
		"lt"	4	322	323	344	343	

		"face"	
		"l"	4	308	689	-329	-689	
		"lt"	4	323	324	345	344	

		"face"	
		"l"	4	309	690	-330	-690	
		"lt"	4	324	325	346	345	

		"face"	
		"l"	4	310	691	-331	-691	
		"lt"	4	325	326	347	346	

		"face"	
		"l"	4	311	692	-332	-692	
		"lt"	4	326	327	348	347	

		"face"	
		"l"	4	312	693	-333	-693	
		"lt"	4	327	328	349	348	

		"face"	
		"l"	4	313	694	-334	-694	
		"lt"	4	328	329	350	349	

		"face"	
		"l"	4	314	695	-335	-695	
		"lt"	4	329	330	351	350	

		"face"	
		"l"	4	315	696	-336	-696	
		"lt"	4	330	331	352	351	

		"face"	
		"l"	4	316	697	-337	-697	
		"lt"	4	331	332	353	352	

		"face"	
		"l"	4	317	698	-338	-698	
		"lt"	4	332	333	354	353	

		"face"	
		"l"	4	318	699	-339	-699	
		"lt"	4	333	334	355	354	

		"face"	
		"l"	4	319	680	-340	-700	
		"lt"	4	334	335	356	355	

		"face"	
		"l"	4	320	701	-341	-701	
		"lt"	4	336	337	358	357	

		"face"	
		"l"	4	321	702	-342	-702	
		"lt"	4	337	338	359	358	

		"face"	
		"l"	4	322	703	-343	-703	
		"lt"	4	338	339	360	359	

		"face"	
		"l"	4	323	704	-344	-704	
		"lt"	4	339	340	361	360	

		"face"	
		"l"	4	324	705	-345	-705	
		"lt"	4	340	341	362	361	

		"face"	
		"l"	4	325	706	-346	-706	
		"lt"	4	341	342	363	362	

		"face"	
		"l"	4	326	707	-347	-707	
		"lt"	4	342	343	364	363	

		"face"	
		"l"	4	327	708	-348	-708	
		"lt"	4	343	344	365	364	

		"face"	
		"l"	4	328	709	-349	-709	
		"lt"	4	344	345	366	365	

		"face"	
		"l"	4	329	710	-350	-710	
		"lt"	4	345	346	367	366	

		"face"	
		"l"	4	330	711	-351	-711	
		"lt"	4	346	347	368	367	

		"face"	
		"l"	4	331	712	-352	-712	
		"lt"	4	347	348	369	368	

		"face"	
		"l"	4	332	713	-353	-713	
		"lt"	4	348	349	370	369	

		"face"	
		"l"	4	333	714	-354	-714	
		"lt"	4	349	350	371	370	

		"face"	
		"l"	4	334	715	-355	-715	
		"lt"	4	350	351	372	371	

		"face"	
		"l"	4	335	716	-356	-716	
		"lt"	4	351	352	373	372	

		"face"	
		"l"	4	336	717	-357	-717	
		"lt"	4	352	353	374	373	

		"face"	
		"l"	4	337	718	-358	-718	
		"lt"	4	353	354	375	374	

		"face"	
		"l"	4	338	719	-359	-719	
		"lt"	4	354	355	376	375	

		"face"	
		"l"	4	339	700	-360	-720	
		"lt"	4	355	356	377	376	

		"face"	
		"l"	4	340	721	-361	-721	
		"lt"	4	357	358	379	378	

		"face"	
		"l"	4	341	722	-362	-722	
		"lt"	4	358	359	380	379	

		"face"	
		"l"	4	342	723	-363	-723	
		"lt"	4	359	360	381	380	

		"face"	
		"l"	4	343	724	-364	-724	
		"lt"	4	360	361	382	381	

		"face"	
		"l"	4	344	725	-365	-725	
		"lt"	4	361	362	383	382	

		"face"	
		"l"	4	345	726	-366	-726	
		"lt"	4	362	363	384	383	

		"face"	
		"l"	4	346	727	-367	-727	
		"lt"	4	363	364	385	384	

		"face"	
		"l"	4	347	728	-368	-728	
		"lt"	4	364	365	386	385	

		"face"	
		"l"	4	348	729	-369	-729	
		"lt"	4	365	366	387	386	

		"face"	
		"l"	4	349	730	-370	-730	
		"lt"	4	366	367	388	387	

		"face"	
		"l"	4	350	731	-371	-731	
		"lt"	4	367	368	389	388	

		"face"	
		"l"	4	351	732	-372	-732	
		"lt"	4	368	369	390	389	

		"face"	
		"l"	4	352	733	-373	-733	
		"lt"	4	369	370	391	390	

		"face"	
		"l"	4	353	734	-374	-734	
		"lt"	4	370	371	392	391	

		"face"	
		"l"	4	354	735	-375	-735	
		"lt"	4	371	372	393	392	

		"face"	
		"l"	4	355	736	-376	-736	
		"lt"	4	372	373	394	393	

		"face"	
		"l"	4	356	737	-377	-737	
		"lt"	4	373	374	395	394	

		"face"	
		"l"	4	357	738	-378	-738	
		"lt"	4	374	375	396	395	

		"face"	
		"l"	4	358	739	-379	-739	
		"lt"	4	375	376	397	396	

		"face"	
		"l"	4	359	720	-380	-740	
		"lt"	4	376	377	398	397	

		"face"	
		"l"	3	-1	-741	741	
		"lt"	3	1	0	399	

		"face"	
		"l"	3	-2	-742	742	
		"lt"	3	2	1	400	

		"face"	
		"l"	3	-3	-743	743	
		"lt"	3	3	2	401	

		"face"	
		"l"	3	-4	-744	744	
		"lt"	3	4	3	402	

		"face"	
		"l"	3	-5	-745	745	
		"lt"	3	5	4	403	

		"face"	
		"l"	3	-6	-746	746	
		"lt"	3	6	5	404	

		"face"	
		"l"	3	-7	-747	747	
		"lt"	3	7	6	405	

		"face"	
		"l"	3	-8	-748	748	
		"lt"	3	8	7	406	

		"face"	
		"l"	3	-9	-749	749	
		"lt"	3	9	8	407	

		"face"	
		"l"	3	-10	-750	750	
		"lt"	3	10	9	408	

		"face"	
		"l"	3	-11	-751	751	
		"lt"	3	11	10	409	

		"face"	
		"l"	3	-12	-752	752	
		"lt"	3	12	11	410	

		"face"	
		"l"	3	-13	-753	753	
		"lt"	3	13	12	411	

		"face"	
		"l"	3	-14	-754	754	
		"lt"	3	14	13	412	

		"face"	
		"l"	3	-15	-755	755	
		"lt"	3	15	14	413	

		"face"	
		"l"	3	-16	-756	756	
		"lt"	3	16	15	414	

		"face"	
		"l"	3	-17	-757	757	
		"lt"	3	17	16	415	

		"face"	
		"l"	3	-18	-758	758	
		"lt"	3	18	17	416	

		"face"	
		"l"	3	-19	-759	759	
		"lt"	3	19	18	417	

		"face"	
		"l"	3	-20	-760	740	
		"lt"	3	20	19	418	

		"face"	
		"l"	3	360	761	-761	
		"lt"	3	378	379	419	

		"face"	
		"l"	3	361	762	-762	
		"lt"	3	379	380	420	

		"face"	
		"l"	3	362	763	-763	
		"lt"	3	380	381	421	

		"face"	
		"l"	3	363	764	-764	
		"lt"	3	381	382	422	

		"face"	
		"l"	3	364	765	-765	
		"lt"	3	382	383	423	

		"face"	
		"l"	3	365	766	-766	
		"lt"	3	383	384	424	

		"face"	
		"l"	3	366	767	-767	
		"lt"	3	384	385	425	

		"face"	
		"l"	3	367	768	-768	
		"lt"	3	385	386	426	

		"face"	
		"l"	3	368	769	-769	
		"lt"	3	386	387	427	

		"face"	
		"l"	3	369	770	-770	
		"lt"	3	387	388	428	

		"face"	
		"l"	3	370	771	-771	
		"lt"	3	388	389	429	

		"face"	
		"l"	3	371	772	-772	
		"lt"	3	389	390	430	

		"face"	
		"l"	3	372	773	-773	
		"lt"	3	390	391	431	

		"face"	
		"l"	3	373	774	-774	
		"lt"	3	391	392	432	

		"face"	
		"l"	3	374	775	-775	
		"lt"	3	392	393	433	

		"face"	
		"l"	3	375	776	-776	
		"lt"	3	393	394	434	

		"face"	
		"l"	3	376	777	-777	
		"lt"	3	394	395	435	

		"face"	
		"l"	3	377	778	-778	
		"lt"	3	395	396	436	

		"face"	
		"l"	3	378	779	-779	
		"lt"	3	396	397	437	

		"face"	
		"l"	3	379	760	-780	
		"lt"	3	397	398	438	;
	setAttr ".lo" yes;
createNode objectSet -n "ffd1Set1";
	rename -uid "06C2F100-0002-8846-5C8B-14A4000002AD";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode cluster -n "cluster1";
	rename -uid "06C2F100-0002-8846-5C8B-14F2000002C1";
	setAttr ".gm[0]" -type "matrix" 2.0000002384185791 0 0 0 0 2 0 0
		 0 0 2.0000005960464478 0 -1.1920928955078125e-07 0 -1.7881393432617188e-07 1;
createNode tweak -n "tweak2";
	rename -uid "06C2F100-0002-8846-5C8B-14F2000002C2";
	setAttr -s 2 ".pl";
createNode objectSet -n "cluster1Set";
	rename -uid "06C2F100-0002-8846-5C8B-14F2000002C3";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "cluster1GroupId";
	rename -uid "06C2F100-0002-8846-5C8B-14F2000002C4";
	setAttr ".ihi" 0;
createNode groupParts -n "cluster1GroupParts";
	rename -uid "06C2F100-0002-8846-5C8B-14F2000002C5";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "pt[*][*][*]";
createNode objectSet -n "tweakSet2";
	rename -uid "06C2F100-0002-8846-5C8B-14F2000002C6";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "groupId4";
	rename -uid "06C2F100-0002-8846-5C8B-14F2000002C7";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts4";
	rename -uid "06C2F100-0002-8846-5C8B-14F2000002C8";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "pt[*][*][*]";
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "06C2F100-0002-8846-5C8B-14F3000002CD";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -886.38867734099199 -862.07794440849318 ;
	setAttr ".tgi[0].vh" -type "double2" 910.56563366232729 492.91931617892891 ;
	setAttr -s 18 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 288.57144165039062;
	setAttr ".tgi[0].ni[0].y" 1052.857177734375;
	setAttr ".tgi[0].ni[0].nvs" 18306;
	setAttr ".tgi[0].ni[1].x" 725.71429443359375;
	setAttr ".tgi[0].ni[1].y" 454.28570556640625;
	setAttr ".tgi[0].ni[1].nvs" 18914;
	setAttr ".tgi[0].ni[2].x" 288.57144165039062;
	setAttr ".tgi[0].ni[2].y" -442.85714721679688;
	setAttr ".tgi[0].ni[2].nvs" 18306;
	setAttr ".tgi[0].ni[3].x" 288.57144165039062;
	setAttr ".tgi[0].ni[3].y" 828.5714111328125;
	setAttr ".tgi[0].ni[3].nvs" 18306;
	setAttr ".tgi[0].ni[4].x" 288.57144165039062;
	setAttr ".tgi[0].ni[4].y" 295.71429443359375;
	setAttr ".tgi[0].ni[4].nvs" 18306;
	setAttr ".tgi[0].ni[5].x" 288.57144165039062;
	setAttr ".tgi[0].ni[5].y" 71.428573608398438;
	setAttr ".tgi[0].ni[5].nvs" 18306;
	setAttr ".tgi[0].ni[6].x" 725.71429443359375;
	setAttr ".tgi[0].ni[6].y" -37.142856597900391;
	setAttr ".tgi[0].ni[6].nvs" 18306;
	setAttr ".tgi[0].ni[7].x" 725.71429443359375;
	setAttr ".tgi[0].ni[7].y" -492.85714721679688;
	setAttr ".tgi[0].ni[7].nvs" 18546;
	setAttr ".tgi[0].ni[8].x" -18.571428298950195;
	setAttr ".tgi[0].ni[8].y" -488.57144165039062;
	setAttr ".tgi[0].ni[8].nvs" 18306;
	setAttr ".tgi[0].ni[9].x" -654.28570556640625;
	setAttr ".tgi[0].ni[9].y" -291.42855834960938;
	setAttr ".tgi[0].ni[9].nvs" 18306;
	setAttr ".tgi[0].ni[10].x" 725.71429443359375;
	setAttr ".tgi[0].ni[10].y" -1045.7142333984375;
	setAttr ".tgi[0].ni[10].nvs" 18546;
	setAttr ".tgi[0].ni[11].x" -654.28570556640625;
	setAttr ".tgi[0].ni[11].y" -124.28571319580078;
	setAttr ".tgi[0].ni[11].nvs" 18306;
	setAttr ".tgi[0].ni[12].x" -347.14285278320312;
	setAttr ".tgi[0].ni[12].y" 258.57144165039062;
	setAttr ".tgi[0].ni[12].nvs" 18306;
	setAttr ".tgi[0].ni[13].x" 725.71429443359375;
	setAttr ".tgi[0].ni[13].y" -1251.4285888671875;
	setAttr ".tgi[0].ni[13].nvs" 18546;
	setAttr ".tgi[0].ni[14].x" -1268.5714111328125;
	setAttr ".tgi[0].ni[14].y" -567.14288330078125;
	setAttr ".tgi[0].ni[14].nvs" 18306;
	setAttr ".tgi[0].ni[15].x" -961.4285888671875;
	setAttr ".tgi[0].ni[15].y" -355.71429443359375;
	setAttr ".tgi[0].ni[15].nvs" 18306;
	setAttr ".tgi[0].ni[16].x" -347.14285278320312;
	setAttr ".tgi[0].ni[16].y" 15.714285850524902;
	setAttr ".tgi[0].ni[16].nvs" 18546;
	setAttr ".tgi[0].ni[17].x" -347.14285278320312;
	setAttr ".tgi[0].ni[17].y" -517.14288330078125;
	setAttr ".tgi[0].ni[17].nvs" 18306;
select -ne :time1;
	setAttr ".o" 0;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "glimpse";
	setAttr ".an" yes;
	setAttr ".ufe" yes;
	setAttr ".pff" yes;
select -ne :defaultResolution;
	setAttr ".w" 1920;
	setAttr ".h" 1080;
	setAttr ".pa" 1;
	setAttr ".dar" 1.7779999971389771;
select -ne :defaultColorMgtGlobals;
	setAttr ".cfe" yes;
	setAttr ".cfp" -type "string" "/film/tools/packages/ALColour_banzai/0.1.0/config.ocio";
	setAttr ".vtn" -type "string" "Output Transform (P3-D60)";
	setAttr ".wsn" -type "string" "acescg";
	setAttr ".otn" -type "string" "Output Transform (P3-D60)";
	setAttr ".potn" -type "string" "Output Transform (P3-D60)";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "ffd1GroupId.id" "pSphereShape1.iog.og[0].gid";
connectAttr "ffd1Set.mwc" "pSphereShape1.iog.og[0].gco";
connectAttr "groupId2.id" "pSphereShape1.iog.og[1].gid";
connectAttr "tweakSet1.mwc" "pSphereShape1.iog.og[1].gco";
connectAttr "ffd1.og[0]" "pSphereShape1.i";
connectAttr "tweak1.vl[0].vt[0]" "pSphereShape1.twl";
connectAttr "polySphere1.out" "pSphereShape1Orig.i";
connectAttr "cluster1.og[0]" "ffd1LatticeShape.li";
connectAttr "tweak2.pl[0].cp[0]" "ffd1LatticeShape.twl";
connectAttr "cluster1GroupId.id" "ffd1LatticeShape.iog.og[2].gid";
connectAttr "cluster1Set.mwc" "ffd1LatticeShape.iog.og[2].gco";
connectAttr "groupId4.id" "ffd1LatticeShape.iog.og[3].gid";
connectAttr "tweakSet2.mwc" "ffd1LatticeShape.iog.og[3].gco";
connectAttr "transformGeometry1.og" "pPlaneShape1.i";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "ffd1GroupParts.og" "ffd1.ip[0].ig";
connectAttr "ffd1GroupId.id" "ffd1.ip[0].gi";
connectAttr "ffd1LatticeShape.wm" "ffd1.dlm";
connectAttr "ffd1LatticeShape.lo" "ffd1.dlp";
connectAttr "ffd1BaseShape.wm" "ffd1.blm";
connectAttr "groupParts2.og" "tweak1.ip[0].ig";
connectAttr "groupId2.id" "tweak1.ip[0].gi";
connectAttr "ffd1GroupId.msg" "ffd1Set.gn" -na;
connectAttr "pSphereShape1.iog.og[0]" "ffd1Set.dsm" -na;
connectAttr "ffd1.msg" "ffd1Set.ub[0]";
connectAttr "tweak1.og[0]" "ffd1GroupParts.ig";
connectAttr "ffd1GroupId.id" "ffd1GroupParts.gi";
connectAttr "groupId2.msg" "tweakSet1.gn" -na;
connectAttr "pSphereShape1.iog.og[1]" "tweakSet1.dsm" -na;
connectAttr "tweak1.msg" "tweakSet1.ub[0]";
connectAttr "pSphereShape1Orig.w" "groupParts2.ig";
connectAttr "groupId2.id" "groupParts2.gi";
connectAttr "polyPlane1.out" "transformGeometry1.ig";
connectAttr "pPlaneShape1.w" "LHCurveWeightNode1.pmesh";
connectAttr "LHCurveWeightNode1_Inputs_0__AnimCurveU.o" "LHCurveWeightNode1.inputs[0].acu"
		;
connectAttr "LHCurveWeightNode1_Inputs_0__AnimCurveV.o" "LHCurveWeightNode1.inputs[0].acv"
		;
connectAttr "ffd1LatticeWEIGHTBASEShape.wireMembership" "LHCurveWeightNode1.mweights"
		;
connectAttr "ffd1LatticeWEIGHTBASEShape.wl" "LHCurveWeightNode1.inputgeo";
connectAttr "ffd1LatticeWEIGHTBASEShape.wm" "ffd2.dlm";
connectAttr "ffd1LatticeWEIGHTBASEShape.lo" "ffd2.dlp";
connectAttr "ffd1Base1Shape.wm" "ffd2.blm";
connectAttr "ffd2.msg" "ffd1Set1.ub[0]";
connectAttr "cluster1GroupParts.og" "cluster1.ip[0].ig";
connectAttr "cluster1GroupId.id" "cluster1.ip[0].gi";
connectAttr "cluster1Handle.wm" "cluster1.ma";
connectAttr "cluster1HandleShape.x" "cluster1.x";
connectAttr "groupParts4.og" "tweak2.ip[0].ig";
connectAttr "groupId4.id" "tweak2.ip[0].gi";
connectAttr "cluster1GroupId.msg" "cluster1Set.gn" -na;
connectAttr "ffd1LatticeShape.iog.og[2]" "cluster1Set.dsm" -na;
connectAttr "cluster1.msg" "cluster1Set.ub[0]";
connectAttr "tweak2.og[0]" "cluster1GroupParts.ig";
connectAttr "cluster1GroupId.id" "cluster1GroupParts.gi";
connectAttr "groupId4.msg" "tweakSet2.gn" -na;
connectAttr "ffd1LatticeShape.iog.og[3]" "tweakSet2.dsm" -na;
connectAttr "tweak2.msg" "tweakSet2.ub[0]";
connectAttr "ffd1LatticeShapeOrig.wl" "groupParts4.ig";
connectAttr "groupId4.id" "groupParts4.gi";
connectAttr "LHCurveWeightNode1_Inputs_0__AnimCurveV.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "LHCurveWeightNode1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "ffd1LatticeShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "pPlaneShape1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn";
connectAttr "LHCurveWeightNode1_Inputs_0__AnimCurveU.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "ffd1LatticeWEIGHTBASEShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "ffd1LatticeWEIGHTBASEShapeOrig.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn"
		;
connectAttr "ffd1LatticeWEIGHTBASE.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn"
		;
connectAttr "cluster1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn";
connectAttr "tweak2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn";
connectAttr "cluster1Set.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn";
connectAttr "cluster1GroupId.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn"
		;
connectAttr "cluster1GroupParts.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn"
		;
connectAttr "tweakSet2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn";
connectAttr "groupId4.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn";
connectAttr "groupParts4.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn";
connectAttr "cluster1Handle.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn";
connectAttr "cluster1HandleShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[17].dn"
		;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "pSphereShape1.iog" ":initialShadingGroup.dsm" -na;
connectAttr "pPlaneShape1.iog" ":initialShadingGroup.dsm" -na;
// End of latticeCurveWeightsTest.ma
