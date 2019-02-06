//Maya ASCII 2018ff09 scene
//Name: geoConstrainttest.ma
//Last modified: Wed, Feb 06, 2019 11:54:52 AM
//Codeset: UTF-8
requires maya "2018ff09";
requires -nodeType "glimpseGlobals" "glimpseMaya" "03.22.05";
requires -nodeType "assetResolverConfig" "assetResolverMaya" "AssetResolverMaya 1.0";
requires -nodeType "decomposeMatrix" "matrixNodes" "1.0";
requires "stereoCamera" "10.0";
requires -nodeType "ALF_globals" -dataType "ALF_data" "ALF" "ALF 0.0";
requires "AL_MayaExtensionAttributes" "1.0";
requires -nodeType "LHGeometryConstraint" -nodeType "nullTransform" "collision" "1.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201811281902-7c8857228f";
fileInfo "osv" "Linux 3.10.0-693.21.1.el7.x86_64 #1 SMP Wed Mar 7 19:03:37 UTC 2018 x86_64";
createNode transform -s -n "persp";
	rename -uid "6986F100-0002-0F7B-5C5A-26A20000095A";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 2.9852451520133836 0.94345681827024575 -0.2237214759116124 ;
	setAttr ".r" -type "double3" -2.1383527295949869 91.799999999991016 0 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "6986F100-0002-0F7B-5C5A-26A20000095B";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 3.1205838262467216;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0.079079701964853255 0 -0.75670286072843274 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "6986F100-0002-0F7B-5C5A-26A20000095C";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "6986F100-0002-0F7B-5C5A-26A20000095D";
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
	rename -uid "6986F100-0002-0F7B-5C5A-26A20000095E";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "6986F100-0002-0F7B-5C5A-26A20000095F";
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
	rename -uid "6986F100-0002-0F7B-5C5A-26A200000960";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "6986F100-0002-0F7B-5C5A-26A200000961";
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
	rename -uid "6986F100-0002-0F7B-5C5A-26A50000096E";
	setAttr ".t" -type "double3" -0.10810390746711079 0.17509803696704798 -1.0495176933977191 ;
	setAttr ".r" -type "double3" -93.359674986442727 16.027073366008302 -42.948400105925643 ;
createNode mesh -n "pSphereShape1" -p "pSphere1";
	rename -uid "6986F100-0002-0F7B-5C5A-26A50000096D";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".pv" -type "double2" 0.50000005960464478 0.45000007748603821 ;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 180 ".pt";
	setAttr ".pt[0]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[1]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[2]" -type "float3" -7.4505806e-09 0 7.4505806e-09 ;
	setAttr ".pt[3]" -type "float3" 0 -7.4505806e-09 -1.8626451e-09 ;
	setAttr ".pt[4]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[5]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[6]" -type "float3" -1.4901161e-08 2.2351742e-08 8.5681677e-08 ;
	setAttr ".pt[7]" -type "float3" 1.4901161e-08 7.4505806e-09 5.7742e-08 ;
	setAttr ".pt[8]" -type "float3" -1.4901161e-08 0 -1.1175871e-08 ;
	setAttr ".pt[9]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[10]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[11]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[12]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[13]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[14]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[15]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[16]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[17]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[18]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[19]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[22]" -type "float3" -1.0244548e-08 1.4901161e-08 -3.7252903e-09 ;
	setAttr ".pt[23]" -type "float3" -7.4505806e-09 7.4505806e-09 -1.8626451e-09 ;
	setAttr ".pt[24]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[25]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[26]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[27]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[28]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[29]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[30]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[31]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[32]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[33]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[34]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[35]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[36]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[37]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[38]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[44]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[45]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[46]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[47]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[48]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[49]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[50]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[51]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[52]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[53]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[54]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[55]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[56]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[57]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[65]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[66]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[67]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[68]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[69]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[70]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[71]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[72]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[73]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[74]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[75]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[76]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[77]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[85]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[86]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[87]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[88]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[89]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[90]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[91]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[92]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[93]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[94]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[95]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[105]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[106]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[107]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[108]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[109]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[110]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[111]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[112]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[113]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[114]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[125]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[126]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[127]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[128]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[129]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[130]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[131]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[145]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[146]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[147]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[148]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[149]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[150]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[151]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[153]" -type "float3" 1.4901161e-08 -7.4505806e-09 2.9802322e-08 ;
	setAttr ".pt[154]" -type "float3" 7.4505806e-09 -1.8626451e-08 0 ;
	setAttr ".pt[165]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[166]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[167]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[168]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[169]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[170]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[171]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[173]" -type "float3" -5.9604645e-08 -3.7252903e-08 2.9802322e-08 ;
	setAttr ".pt[174]" -type "float3" -7.4505806e-09 -6.7055225e-08 5.2154064e-08 ;
	setAttr ".pt[175]" -type "float3" 1.7881393e-07 -1.2433156e-07 1.8626451e-08 ;
	setAttr ".pt[176]" -type "float3" -4.1723251e-07 5.9604645e-08 -1.937151e-07 ;
	setAttr ".pt[185]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[186]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[187]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[188]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[189]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[190]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[192]" -type "float3" 0 1.7881393e-07 1.0430813e-07 ;
	setAttr ".pt[193]" -type "float3" -1.0430813e-07 2.2351742e-08 4.4703484e-08 ;
	setAttr ".pt[194]" -type "float3" 2.2351742e-08 0 -2.2351742e-08 ;
	setAttr ".pt[195]" -type "float3" 1.4901161e-07 -9.4994903e-08 6.7055225e-08 ;
	setAttr ".pt[196]" -type "float3" 0 -1.1920929e-07 2.9802322e-08 ;
	setAttr ".pt[205]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[206]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[207]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[208]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[209]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[210]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[211]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[216]" -type "float3" 0 0 -1.937151e-07 ;
	setAttr ".pt[224]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[225]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[226]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[227]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[228]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[229]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[230]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[231]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[244]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[245]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[246]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[247]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[248]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[249]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[250]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[251]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[263]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[264]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[265]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[266]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[267]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[268]" -type "float3" -2.2351742e-08 4.4703484e-08 -4.8428774e-08 ;
	setAttr ".pt[269]" -type "float3" 7.4505806e-09 -8.1956387e-08 -3.7252903e-09 ;
	setAttr ".pt[270]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[271]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[283]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[284]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[285]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[286]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[287]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[288]" -type "float3" 5.2154064e-08 -7.4505806e-09 -1.1920929e-07 ;
	setAttr ".pt[289]" -type "float3" -2.2351742e-08 8.1956387e-08 -1.8626451e-08 ;
	setAttr ".pt[290]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[291]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[304]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[305]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[306]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[307]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[308]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[309]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[310]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[325]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[326]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[327]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[328]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[329]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[347]" -type "float3" 0 7.4505806e-09 0 ;
	setAttr ".pt[380]" -type "float3" -2.9802322e-08 3.7252903e-08 5.5879354e-08 ;
createNode transform -n "locator1";
	rename -uid "6986F100-0002-0F7B-5C5A-26AC00000971";
	setAttr ".t" -type "double3" -0.033525249336030905 0.3341371788374155 -0.051056660621546346 ;
createNode locator -n "locatorShape1" -p "locator1";
	rename -uid "6986F100-0002-0F7B-5C5A-26AC00000972";
	setAttr -k off ".v";
createNode transform -n "R_New_CPT";
	rename -uid "6986F100-0002-0F7B-5C5B-343C000020A5";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_New_CPT1";
	rename -uid "6986F100-0002-0F7B-5C5B-34850000228D";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	addAttr -s false -ci true -sn "control" -ln "control" -at "message";
	addAttr -s false -ci true -sn "transform" -ln "transform" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_New_LOC" -p "R_New_CPT1";
	rename -uid "6986F100-0002-0F7B-5C5B-348500002290";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode locator -n "R_New_LOCShape" -p "R_New_LOC";
	rename -uid "6986F100-0002-0F7B-5C5B-348500002293";
	setAttr -k off ".v" no;
createNode transform -n "R_NewBuffer2_GRP" -p "R_New_LOC";
	rename -uid "6986F100-0002-0F7B-5C5B-348500002296";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr ".t" -type "double3" -2.7104761227136898e-08 -7.2050641231058421e-08 -0.0048730944806709142 ;
	setAttr ".r" -type "double3" 43.382676432364391 -21.522173197688623 -0.41285871523321366 ;
	setAttr ".s" -type "double3" 0.99999999999999944 0.999999999999999 1 ;
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode transform -n "R_NewBuffer1_GRP" -p "R_NewBuffer2_GRP";
	rename -uid "6986F100-0002-0F7B-5C5B-348500002299";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nullTransform -n "R_New_CTL" -p "R_NewBuffer1_GRP";
	rename -uid "6986F100-0002-0F7B-5C5B-3485000022A2";
	addAttr -ci true -sn "gimbal_vis" -ln "gimbal_vis" -min 0 -max 1 -at "short";
	addAttr -ci true -k true -sn "xSpeed" -ln "xSpeed" -dv 0.1 -at "float";
	addAttr -ci true -k true -sn "ySpeed" -ln "ySpeed" -dv 0.1 -at "float";
	addAttr -ci true -k true -sn "zSpeed" -ln "zSpeed" -dv 0.1 -at "float";
	addAttr -ci true -sn "componentType" -ln "componentType" -dt "string";
	addAttr -s false -ci true -sn "root" -ln "root" -at "message";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr -cb on ".gimbal_vis";
	setAttr -l on ".componentType" -type "string" "meshRivetCtrl";
createNode nurbsCurve -n "curveShape1" -p "R_New_CTL";
	rename -uid "6986F100-0002-0F7B-5C5B-34850000229C";
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
		-0.5 -6.123233995736766e-17 0.99999999999999989
		-0.43301249999999997 -0.25000000000000006 0.99999999999999989
		-0.24999999999999994 -0.43301250000000008 1
		6.123233995736766e-17 -0.5 1
		0.25000000000000006 -0.43301249999999997 1
		0.43301250000000008 -0.24999999999999994 1
		0.5 6.123233995736766e-17 1
		0.43301249999999997 0.25000000000000006 1
		0.24999999999999994 0.43301250000000008 1
		-6.123233995736766e-17 0.5 1
		-0.25000000000000006 0.43301249999999997 0.99999999999999989
		-0.43301250000000008 0.24999999999999994 0.99999999999999989
		-0.5 -6.123233995736766e-17 0.99999999999999989
		-0.35355349999999997 -4.3297816210234379e-17 0.64644649999999992
		1.1102230246251565e-16 0 0.5
		0.35355350000000008 4.3297816210234379e-17 0.64644650000000003
		0.5 6.123233995736766e-17 1
		0.35355349999999997 4.3297816210234379e-17 1.3535535000000001
		-1.1102230246251565e-16 0 1.5
		-6.5531919511416288e-17 -0.25 1.4330125
		-2.4824140196784936e-18 -0.43301250000000002 1.25
		6.123233995736766e-17 -0.5 1
		1.0853988844283717e-16 -0.43301250000000002 0.75
		1.2676425946878396e-16 -0.25 0.56698749999999998
		1.1102230246251565e-16 0 0.5
		6.5531919511416288e-17 0.25 0.56698749999999998
		2.4824140196784936e-18 0.43301250000000002 0.75
		-6.123233995736766e-17 0.5 1
		-1.0853988844283717e-16 0.43301250000000002 1.25
		-1.2676425946878396e-16 0.25 1.4330125
		-1.1102230246251565e-16 0 1.5
		-0.35355350000000008 -4.3297816210234379e-17 1.3535534999999999
		-0.5 -6.123233995736766e-17 0.99999999999999989
		;
createNode transform -n "R_NewGimbal_CTL" -p "R_New_CTL";
	rename -uid "6986F100-0002-0F7B-5C5B-3485000022A8";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -cb on ".ro";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "curveShape2" -p "R_NewGimbal_CTL";
	rename -uid "6986F100-0002-0F7B-5C5B-3485000022A7";
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
		0 0 0.45000000000000001
		0 0.22500000000000001 0.38971125000000001
		0 0.38971125000000001 0.22500000000000001
		0 0.45000000000000001 0
		0 0.38971125000000001 -0.22500000000000001
		0 0.22500000000000001 -0.38971125000000001
		0 0 -0.45000000000000001
		0 -0.22500000000000001 -0.38971125000000001
		0 -0.38971125000000001 -0.22500000000000001
		0 -0.45000000000000001 0
		0 -0.38971125000000001 0.22500000000000001
		0 -0.22500000000000001 0.38971125000000001
		0 0 0.45000000000000001
		0.31819815000000001 0 0.31819815000000001
		0.45000000000000001 0 0
		0.31819815000000001 0 -0.31819815000000001
		0 0 -0.45000000000000001
		-0.31819815000000001 0 -0.31819815000000001
		-0.45000000000000001 0 0
		-0.38971125000000001 0.22500000000000001 0
		-0.22500000000000001 0.38971125000000001 0
		0 0.45000000000000001 0
		0.22500000000000001 0.38971125000000001 0
		0.38971125000000001 0.22500000000000001 0
		0.45000000000000001 0 0
		0.38971125000000001 -0.22500000000000001 0
		0.22500000000000001 -0.38971125000000001 0
		0 -0.45000000000000001 0
		-0.22500000000000001 -0.38971125000000001 0
		-0.38971125000000001 -0.22500000000000001 0
		-0.45000000000000001 0 0
		-0.31819815000000001 0 0.31819815000000001
		0 0 0.45000000000000001
		;
createNode lightLinker -s -n "lightLinker1";
	rename -uid "6986F100-0002-0F7B-5C5A-26D0000009C7";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode assetResolverConfig -n "assetResolverConfig";
	rename -uid "6986F100-0002-0F7B-5C5A-26A300000963";
createNode glimpseGlobals -s -n "glimpseGlobals";
	rename -uid "6986F100-0002-0F7B-5C5A-26A300000964";
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
	rename -uid "6986F100-0002-0F7B-5C5A-26A300000965";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "6986F100-0002-0F7B-5C5A-26D0000009CB";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "6986F100-0002-0F7B-5C5A-26D0000009CC";
createNode displayLayerManager -n "layerManager";
	rename -uid "6986F100-0002-0F7B-5C5A-26D0000009CD";
createNode displayLayer -n "defaultLayer";
	rename -uid "6986F100-0002-0F7B-5C5A-26A300000969";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "6986F100-0002-0F7B-5C5A-26D0000009CF";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "6986F100-0002-0F7B-5C5A-26A30000096B";
	setAttr ".g" yes;
createNode polySphere -n "polySphere1";
	rename -uid "6986F100-0002-0F7B-5C5A-26A50000096C";
createNode script -n "uiConfigurationScriptNode";
	rename -uid "6986F100-0002-0F7B-5C5A-26B600000975";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $nodeEditorPanelVisible = stringArrayContains(\"nodeEditorPanel1\", `getPanel -vis`);\n\tint    $nodeEditorWorkspaceControlOpen = (`workspaceControl -exists nodeEditorPanel1Window` && `workspaceControl -q -visible nodeEditorPanel1Window`);\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\n\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            -pluginObjects \"ALFShapeDisplayFilter\" 1 \n            $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n"
		+ "            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n"
		+ "            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n"
		+ "            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            -pluginObjects \"ALFShapeDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n"
		+ "            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n"
		+ "            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n"
		+ "            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            -pluginObjects \"ALFShapeDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n"
		+ "            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n"
		+ "            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n"
		+ "            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1247\n            -height 1031\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            -pluginObjects \"ALFShapeDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 1\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 0\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n"
		+ "            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n"
		+ "            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n"
		+ "            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 0\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n"
		+ "            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n"
		+ "                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n"
		+ "                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n"
		+ "                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                -outliner \"graphEditor1OutlineEd\" \n"
		+ "                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n"
		+ "                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n"
		+ "                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n"
		+ "                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n"
		+ "                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -autoFitTime 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n"
		+ "                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n"
		+ "                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif ($nodeEditorPanelVisible || $nodeEditorWorkspaceControlOpen) {\n\t\tif (\"\" == $panelName) {\n\t\t\tif ($useSceneConfig) {\n\t\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n"
		+ "                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -connectionMinSegment 0.03\n                -connectionOffset 0.03\n                -connectionRoundness 0.8\n                -connectionTension -100\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 0\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                $editorName;\n\t\t\t}\n\t\t} else {\n\t\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -connectionMinSegment 0.03\n                -connectionOffset 0.03\n                -connectionRoundness 0.8\n                -connectionTension -100\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n"
		+ "                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 0\n                -syncedSelection 1\n                -extendToShapes 1\n                -editorMode \"default\" \n                $editorName;\n\t\t\tif (!$useSceneConfig) {\n\t\t\t\tpanel -e -l $label $panelName;\n\t\t\t}\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n"
		+ "\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "string $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n"
		+ "                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n"
		+ "                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n"
		+ "                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                -pluginObjects \"ALFShapeDisplayFilter\" 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n"
		+ "\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1247\\n    -height 1031\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    -pluginObjects \\\"ALFShapeDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1247\\n    -height 1031\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    -pluginObjects \\\"ALFShapeDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "6986F100-0002-0F7B-5C5A-26B600000976";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode LHGeometryConstraint -n "R_New_GCS";
	rename -uid "6986F100-0002-0F7B-5C5B-3485000022AD";
	setAttr ".outmatrix" -type "matrix" 0.93025147793850338 -0.2467417933380581 -0.27157075544606923 0 -0.0067032118934152417 0.72857922164842603 -0.68492874427380079 0
		 0.36686135629627403 0.63897637296107634 0.67610793521002666 0 0.17563241678921659 0.77926551853856663 -0.31054637657789574 1;
	setAttr ".bweights" -type "float3" 0.81643975 0.040691402 0.14286885 ;
	setAttr ".apointidx" 92;
	setAttr ".bpointidx" 93;
	setAttr ".cpointidx" 113;
	setAttr ".dpointidx" 112;
createNode decomposeMatrix -n "R_New_GCS_DCP";
	rename -uid "6986F100-0002-0F7B-5C5B-3485000022AE";
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "6986F100-0002-0F7B-5C5B-3B8C0000234D";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -1553.4750316992531 -887.3169862409012 ;
	setAttr ".tgi[0].vh" -type "double2" 4648.2054666171998 2023.6073018577697 ;
	setAttr -s 17 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 784.28570556640625;
	setAttr ".tgi[0].ni[0].y" 1107.142822265625;
	setAttr ".tgi[0].ni[0].nvs" 18546;
	setAttr ".tgi[0].ni[1].x" 51.428569793701172;
	setAttr ".tgi[0].ni[1].y" -601.4285888671875;
	setAttr ".tgi[0].ni[1].nvs" 18546;
	setAttr ".tgi[0].ni[2].x" 784.28570556640625;
	setAttr ".tgi[0].ni[2].y" 554.28570556640625;
	setAttr ".tgi[0].ni[2].nvs" 18546;
	setAttr ".tgi[0].ni[3].x" 1112.857177734375;
	setAttr ".tgi[0].ni[3].y" -530;
	setAttr ".tgi[0].ni[3].nvs" 18546;
	setAttr ".tgi[0].ni[4].x" 485.71429443359375;
	setAttr ".tgi[0].ni[4].y" 1877.142822265625;
	setAttr ".tgi[0].ni[4].nvs" 18546;
	setAttr ".tgi[0].ni[5].x" 72.857139587402344;
	setAttr ".tgi[0].ni[5].y" -1705.7142333984375;
	setAttr ".tgi[0].ni[5].nvs" 18306;
	setAttr ".tgi[0].ni[6].x" 1087.142822265625;
	setAttr ".tgi[0].ni[6].y" 288.57144165039062;
	setAttr ".tgi[0].ni[6].nvs" 18546;
	setAttr ".tgi[0].ni[7].x" -343.1251220703125;
	setAttr ".tgi[0].ni[7].y" 450.12368774414062;
	setAttr ".tgi[0].ni[7].nvs" 18546;
	setAttr ".tgi[0].ni[8].x" 72.857139587402344;
	setAttr ".tgi[0].ni[8].y" -1162.857177734375;
	setAttr ".tgi[0].ni[8].nvs" 18306;
	setAttr ".tgi[0].ni[9].x" -255.71427917480469;
	setAttr ".tgi[0].ni[9].y" 2030;
	setAttr ".tgi[0].ni[9].nvs" 18546;
	setAttr ".tgi[0].ni[10].x" 72.857139587402344;
	setAttr ".tgi[0].ni[10].y" 1625.7142333984375;
	setAttr ".tgi[0].ni[10].nvs" 18306;
	setAttr ".tgi[0].ni[11].x" 51.428569793701172;
	setAttr ".tgi[0].ni[11].y" 1082.857177734375;
	setAttr ".tgi[0].ni[11].nvs" 18546;
	setAttr ".tgi[0].ni[12].x" 477.14285278320312;
	setAttr ".tgi[0].ni[12].y" -587.14288330078125;
	setAttr ".tgi[0].ni[12].nvs" 18306;
	setAttr ".tgi[0].ni[13].x" 784.28570556640625;
	setAttr ".tgi[0].ni[13].y" -491.42855834960938;
	setAttr ".tgi[0].ni[13].nvs" 18306;
	setAttr ".tgi[0].ni[14].x" -137.14285278320312;
	setAttr ".tgi[0].ni[14].y" -327.14285278320312;
	setAttr ".tgi[0].ni[14].nvs" 18306;
	setAttr ".tgi[0].ni[15].x" 784.28570556640625;
	setAttr ".tgi[0].ni[15].y" -55.714286804199219;
	setAttr ".tgi[0].ni[15].nvs" 18306;
	setAttr ".tgi[0].ni[16].x" 170;
	setAttr ".tgi[0].ni[16].y" -172.85714721679688;
	setAttr ".tgi[0].ni[16].nvs" 18306;
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 1;
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
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "glimpse";
	setAttr ".an" yes;
	setAttr ".ufe" yes;
	setAttr ".pff" yes;
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av ".w" 1920;
	setAttr -av ".h" 1080;
	setAttr -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av ".dar" 1.7779999971389771;
	setAttr -av -k on ".ldar";
	setAttr -cb on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -cb on ".isu";
	setAttr -cb on ".pdu";
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
	setAttr -k off ".ctrs" 256;
	setAttr -av -k off ".btrs" 512;
	setAttr -k off ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -cb on ".hwcc";
	setAttr -cb on ".hwdp";
	setAttr -cb on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
connectAttr "polySphere1.out" "pSphereShape1.i";
connectAttr "R_New_CPT.msg" "R_New_CPT.root";
connectAttr "R_New_CPT1.msg" "R_New_CPT1.root";
connectAttr "R_New_CTL.msg" "R_New_CPT1.control";
connectAttr "R_NewBuffer2_GRP.msg" "R_New_CPT1.transform";
connectAttr "R_New_CPT1.msg" "R_New_LOC.root";
connectAttr "R_New_GCS_DCP.ot" "R_New_LOC.t";
connectAttr "R_New_GCS_DCP.or" "R_New_LOC.r";
connectAttr "R_New_CPT1.msg" "R_NewBuffer2_GRP.root";
connectAttr "R_New_CPT1.msg" "R_NewBuffer1_GRP.root";
connectAttr "R_New_CPT1.msg" "R_New_CTL.root";
connectAttr "R_New_CTL.gimbal_vis" "curveShape2.v" -l on;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "pSphereShape1.w" "R_New_GCS.inmesh";
connectAttr "R_New_GCS.outmatrix" "R_New_GCS_DCP.imat";
connectAttr "locator1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn";
connectAttr "R_New_CPT.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn";
connectAttr "pSphere1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn";
connectAttr "R_New_LOC.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn";
connectAttr "R_New_CPT1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn";
connectAttr "R_New_LOCShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn";
connectAttr "R_NewBuffer2_GRP.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn"
		;
connectAttr "R_NewBuffer1_GRP.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn"
		;
connectAttr "curveShape1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn";
connectAttr "R_New_CTL.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn";
connectAttr "curveShape2.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn";
connectAttr "R_NewGimbal_CTL.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn"
		;
connectAttr "R_New_GCS.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn";
connectAttr "R_New_GCS_DCP.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn";
connectAttr "polySphere1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn";
connectAttr "locatorShape1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn";
connectAttr "pSphereShape1.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "pSphereShape1.iog" ":initialShadingGroup.dsm" -na;
// End of geoConstrainttest.ma
