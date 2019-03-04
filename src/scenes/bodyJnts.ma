//Maya ASCII 2018 scene
//Name: bodyJnts.ma
//Last modified: Mon, Mar 04, 2019 06:27:36 AM
//Codeset: UTF-8
requires maya "2018";
requires -nodeType "mentalrayFramebuffer" -nodeType "mentalrayOutputPass" -nodeType "mentalrayRenderPass"
		 -nodeType "mentalrayUserBuffer" -nodeType "mentalraySubdivApprox" -nodeType "mentalrayCurveApprox"
		 -nodeType "mentalraySurfaceApprox" -nodeType "mentalrayDisplaceApprox" -nodeType "mentalrayOptions"
		 -nodeType "mentalrayGlobals" -nodeType "mentalrayItemsList" -nodeType "mentalrayShader"
		 -nodeType "mentalrayUserData" -nodeType "mentalrayText" -nodeType "mentalrayTessellation"
		 -nodeType "mentalrayPhenomenon" -nodeType "mentalrayLightProfile" -nodeType "mentalrayVertexColors"
		 -nodeType "mentalrayIblShape" -nodeType "mapVizShape" -nodeType "mentalrayCCMeshProxy"
		 -nodeType "cylindricalLightLocator" -nodeType "discLightLocator" -nodeType "rectangularLightLocator"
		 -nodeType "sphericalLightLocator" -nodeType "abcimport" -nodeType "mia_physicalsun"
		 -nodeType "mia_physicalsky" -nodeType "mia_material" -nodeType "mia_material_x" -nodeType "mia_roundcorners"
		 -nodeType "mia_exposure_simple" -nodeType "mia_portal_light" -nodeType "mia_light_surface"
		 -nodeType "mia_exposure_photographic" -nodeType "mia_exposure_photographic_rev" -nodeType "mia_lens_bokeh"
		 -nodeType "mia_envblur" -nodeType "mia_ciesky" -nodeType "mia_photometric_light"
		 -nodeType "mib_texture_vector" -nodeType "mib_texture_remap" -nodeType "mib_texture_rotate"
		 -nodeType "mib_bump_basis" -nodeType "mib_bump_map" -nodeType "mib_passthrough_bump_map"
		 -nodeType "mib_bump_map2" -nodeType "mib_lookup_spherical" -nodeType "mib_lookup_cube1"
		 -nodeType "mib_lookup_cube6" -nodeType "mib_lookup_background" -nodeType "mib_lookup_cylindrical"
		 -nodeType "mib_texture_lookup" -nodeType "mib_texture_lookup2" -nodeType "mib_texture_filter_lookup"
		 -nodeType "mib_texture_checkerboard" -nodeType "mib_texture_polkadot" -nodeType "mib_texture_polkasphere"
		 -nodeType "mib_texture_turbulence" -nodeType "mib_texture_wave" -nodeType "mib_reflect"
		 -nodeType "mib_refract" -nodeType "mib_transparency" -nodeType "mib_continue" -nodeType "mib_opacity"
		 -nodeType "mib_twosided" -nodeType "mib_refraction_index" -nodeType "mib_dielectric"
		 -nodeType "mib_ray_marcher" -nodeType "mib_illum_lambert" -nodeType "mib_illum_phong"
		 -nodeType "mib_illum_ward" -nodeType "mib_illum_ward_deriv" -nodeType "mib_illum_blinn"
		 -nodeType "mib_illum_cooktorr" -nodeType "mib_illum_hair" -nodeType "mib_volume"
		 -nodeType "mib_color_alpha" -nodeType "mib_color_average" -nodeType "mib_color_intensity"
		 -nodeType "mib_color_interpolate" -nodeType "mib_color_mix" -nodeType "mib_color_spread"
		 -nodeType "mib_geo_cube" -nodeType "mib_geo_torus" -nodeType "mib_geo_sphere" -nodeType "mib_geo_cone"
		 -nodeType "mib_geo_cylinder" -nodeType "mib_geo_square" -nodeType "mib_geo_instance"
		 -nodeType "mib_geo_instance_mlist" -nodeType "mib_geo_add_uv_texsurf" -nodeType "mib_photon_basic"
		 -nodeType "mib_light_infinite" -nodeType "mib_light_point" -nodeType "mib_light_spot"
		 -nodeType "mib_light_photometric" -nodeType "mib_cie_d" -nodeType "mib_blackbody"
		 -nodeType "mib_shadow_transparency" -nodeType "mib_lens_stencil" -nodeType "mib_lens_clamp"
		 -nodeType "mib_lightmap_write" -nodeType "mib_lightmap_sample" -nodeType "mib_amb_occlusion"
		 -nodeType "mib_fast_occlusion" -nodeType "mib_map_get_scalar" -nodeType "mib_map_get_integer"
		 -nodeType "mib_map_get_vector" -nodeType "mib_map_get_color" -nodeType "mib_map_get_transform"
		 -nodeType "mib_map_get_scalar_array" -nodeType "mib_map_get_integer_array" -nodeType "mib_fg_occlusion"
		 -nodeType "mib_bent_normal_env" -nodeType "mib_glossy_reflection" -nodeType "mib_glossy_refraction"
		 -nodeType "builtin_bsdf_architectural" -nodeType "builtin_bsdf_architectural_comp"
		 -nodeType "builtin_bsdf_carpaint" -nodeType "builtin_bsdf_ashikhmin" -nodeType "builtin_bsdf_lambert"
		 -nodeType "builtin_bsdf_mirror" -nodeType "builtin_bsdf_phong" -nodeType "contour_store_function"
		 -nodeType "contour_store_function_simple" -nodeType "contour_contrast_function_levels"
		 -nodeType "contour_contrast_function_simple" -nodeType "contour_shader_simple" -nodeType "contour_shader_silhouette"
		 -nodeType "contour_shader_maxcolor" -nodeType "contour_shader_curvature" -nodeType "contour_shader_factorcolor"
		 -nodeType "contour_shader_depthfade" -nodeType "contour_shader_framefade" -nodeType "contour_shader_layerthinner"
		 -nodeType "contour_shader_widthfromcolor" -nodeType "contour_shader_widthfromlightdir"
		 -nodeType "contour_shader_widthfromlight" -nodeType "contour_shader_combi" -nodeType "contour_only"
		 -nodeType "contour_composite" -nodeType "contour_ps" -nodeType "mi_metallic_paint"
		 -nodeType "mi_metallic_paint_x" -nodeType "mi_bump_flakes" -nodeType "mi_car_paint_phen"
		 -nodeType "mi_metallic_paint_output_mixer" -nodeType "mi_car_paint_phen_x" -nodeType "physical_lens_dof"
		 -nodeType "physical_light" -nodeType "dgs_material" -nodeType "dgs_material_photon"
		 -nodeType "dielectric_material" -nodeType "dielectric_material_photon" -nodeType "oversampling_lens"
		 -nodeType "path_material" -nodeType "parti_volume" -nodeType "parti_volume_photon"
		 -nodeType "transmat" -nodeType "transmat_photon" -nodeType "mip_rayswitch" -nodeType "mip_rayswitch_advanced"
		 -nodeType "mip_rayswitch_environment" -nodeType "mip_card_opacity" -nodeType "mip_motionblur"
		 -nodeType "mip_motion_vector" -nodeType "mip_matteshadow" -nodeType "mip_cameramap"
		 -nodeType "mip_mirrorball" -nodeType "mip_grayball" -nodeType "mip_gamma_gain" -nodeType "mip_render_subset"
		 -nodeType "mip_matteshadow_mtl" -nodeType "mip_binaryproxy" -nodeType "mip_rayswitch_stage"
		 -nodeType "mip_fgshooter" -nodeType "mib_ptex_lookup" -nodeType "misss_physical"
		 -nodeType "misss_physical_phen" -nodeType "misss_fast_shader" -nodeType "misss_fast_shader_x"
		 -nodeType "misss_fast_shader2" -nodeType "misss_fast_shader2_x" -nodeType "misss_skin_specular"
		 -nodeType "misss_lightmap_write" -nodeType "misss_lambert_gamma" -nodeType "misss_call_shader"
		 -nodeType "misss_set_normal" -nodeType "misss_fast_lmap_maya" -nodeType "misss_fast_simple_maya"
		 -nodeType "misss_fast_skin_maya" -nodeType "misss_fast_skin_phen" -nodeType "misss_fast_skin_phen_d"
		 -nodeType "misss_mia_skin2_phen" -nodeType "misss_mia_skin2_phen_d" -nodeType "misss_lightmap_phen"
		 -nodeType "misss_mia_skin2_surface_phen" -nodeType "surfaceSampler" -nodeType "mib_data_bool"
		 -nodeType "mib_data_int" -nodeType "mib_data_scalar" -nodeType "mib_data_vector"
		 -nodeType "mib_data_color" -nodeType "mib_data_string" -nodeType "mib_data_texture"
		 -nodeType "mib_data_shader" -nodeType "mib_data_bool_array" -nodeType "mib_data_int_array"
		 -nodeType "mib_data_scalar_array" -nodeType "mib_data_vector_array" -nodeType "mib_data_color_array"
		 -nodeType "mib_data_string_array" -nodeType "mib_data_texture_array" -nodeType "mib_data_shader_array"
		 -nodeType "mib_data_get_bool" -nodeType "mib_data_get_int" -nodeType "mib_data_get_scalar"
		 -nodeType "mib_data_get_vector" -nodeType "mib_data_get_color" -nodeType "mib_data_get_string"
		 -nodeType "mib_data_get_texture" -nodeType "mib_data_get_shader" -nodeType "mib_data_get_shader_bool"
		 -nodeType "mib_data_get_shader_int" -nodeType "mib_data_get_shader_scalar" -nodeType "mib_data_get_shader_vector"
		 -nodeType "mib_data_get_shader_color" -nodeType "user_ibl_env" -nodeType "user_ibl_rect"
		 -nodeType "mia_material_x_passes" -nodeType "mi_metallic_paint_x_passes" -nodeType "mi_car_paint_phen_x_passes"
		 -nodeType "misss_fast_shader_x_passes" -dataType "byteArray" "Mayatomr" "2014.0 - 3.11.1.13 ";
currentUnit -l centimeter -a degree -t ntsc;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "201706261615-f9658c4cfc";
fileInfo "osv" "Mac OS X 10.11.6";
fileInfo "license" "student";
createNode transform -s -n "persp";
	rename -uid "ACA2FD33-2442-E86A-6675-A59A00A6A13F";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -6.3878698111481551 99.760157040918884 145.13749594259323 ;
	setAttr ".r" -type "double3" -5.7383527299432178 -4.1999999999987114 0 ;
	setAttr ".rp" -type "double3" 5.5511151231257827e-17 1.1102230246251565e-16 2.2204460492503131e-16 ;
	setAttr ".rpt" -type "double3" 7.9172661478972685e-17 6.2372232607435172e-17 -9.3569502538918145e-17 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "36FE8474-464C-8275-ED76-999D18DFCF34";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999986;
	setAttr ".coi" 148.57070755077129;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 9.2962627410888672 105.10679626464844 8.2726278305053711 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr -s 4 ".b";
createNode transform -s -n "top";
	rename -uid "817A5ACF-F948-2407-A76A-BAA31E8F1A65";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 61.486820664592322 171.85689679070845 1.7195400860200887 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "BAB37583-EA40-7EC8-645B-FA83338CAA63";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 67.640180300042616;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "32BE4203-6A43-417C-7AE4-169F5B06AF97";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 4.6230694893964905 138.07144470068565 150.7001040200102 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "799F8E69-FC40-25C7-6692-A494E0885085";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 61.360215301670628;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "56B501E7-F840-41CD-ECB7-998322601555";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 155.97981794045441 85.61366439647459 -10.36109264087442 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "FBCFA3EE-1D43-A601-F381-D1B16A53C4EE";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 86.801236107370883;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "character_grp";
	rename -uid "2EF86C44-0846-F5E3-F6B4-E595CBF9D964";
createNode transform -n "bind_grp" -p "character_grp";
	rename -uid "EB8AB166-F148-7397-1E11-1A94F222BE41";
	setAttr ".ove" yes;
createNode joint -n "root_bind" -p "bind_grp";
	rename -uid "340D31E0-AF49-26EF-305B-AB9825C4DF0F";
	addAttr -ci true -sn "isRoot" -ln "isRoot" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "ignoreRotate" -ln "ignoreRotate" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "notes" -ln "notes" -dt "string";
	setAttr -k off ".v";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 3.552713678800512e-15 98.91236480447489 -1.309399394935409 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -89.999999999999972 -8.7166113527418361 89.999999999999972 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0
		 0 1.0670999999999999 0 1;
	setAttr ".isRoot" yes;
	setAttr ".ignoreRotate" yes;
	setAttr -k on ".notes" -type "string" "version 5\nNew rig with fixed partial sets\nversion 6\ncleaned up all sets\nversion 7\nadded muscle joints to partial anim-sets as well as \nadded new prop attachment joints\nversion 8\nfixing anims, and wrinkle maps, (bump)\nversion 9 \nadded new joints for muscle stuff and shirt up animation. \nversion 10\nbump because buildbig is dumb ;)\nversion 11\nbump because buildbig is dumb ;)\nversion 12\nadded holster_gun_bind joint\nversion 13\nadded anim flippable attributes to joints\nversion 14\ngot rid of align offset\n\n.\n";
createNode joint -n "lower_base" -p "root_bind";
	rename -uid "9BE958B2-2441-9043-F599-F493737006E5";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 0 3.5527136788005009e-15 2.1545152423428635e-17 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -89.999999999999872 2.2976055318002393 -86.603374686267387 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0
		 0 1.0670999999999999 1.2856667564442436e-21 1;
createNode joint -n "upper_base" -p "root_bind";
	rename -uid "8E262370-5C4B-6A24-830B-448B23C58059";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 0 3.5527136788005009e-15 6.3108872417680944e-30 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.3492989215379538e-14 -3.7355255252664601e-15 93.396625313732642 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 2.2204460492503131e-16 -1 0 0 1 2.2204460492503131e-16 0
		 0 1.0670999999999999 1.2856667564442436e-21 1;
createNode joint -n "pelvis_bind" -p "root_bind";
	rename -uid "C6259699-FC40-64E0-3A0C-9E89E40BE002";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 4.0003043759844985 0.51913368883656119 5.9292746059340872e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.5444437451708134e-14 179.99999999999994 1.099019781932419 ;
	setAttr ".bps" -type "matrix" -1 -1.2246467991473532e-16 -2.7192621468937821e-32 0
		 0 2.2204460492503131e-16 -1 0 1.2246467991473532e-16 -1 -2.2204460492503131e-16 0
		 1.2621907363761846e-18 1.0566331386725929 -0.00041995600714367766 1;
createNode joint -n "pelvis_bind_end" -p "pelvis_bind";
	rename -uid "D2FEA9FF-7144-64EA-CF99-8A8CABC55EB3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 10.897711051996687 -0.7278079366548843 1.5691531420841449e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -87.702394468199728 89.999999999999815 0 ;
	setAttr ".bps" -type "matrix" -1 -1.2246063538223773e-16 -2.7191723402317286e-32 0
		 -1.2246063538223773e-16 1 -7.7715611723760958e-16 0 1.2236275531042779e-31 -7.7715611723760958e-16 -1 0
		 1.6859059829559953e-17 0.92927083122986975 -0.00041995600714357867 1;
createNode joint -n "l_leg_bind" -p "pelvis_bind_end";
	rename -uid "7B15C288-8949-70B9-E155-B6B9D6D8E2B6";
	setAttr ".t" -type "double3" -5.7940581746413624 6.0846796023677285 1.226483628127335 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 179.06339581223912 3.2083364404814185 -102.6598433391233 ;
	setAttr ".radi" 2;
createNode joint -n "l_knee_bind" -p "l_leg_bind";
	rename -uid "5A73493E-5E4D-85E5-F013-1A87D91AB593";
	setAttr ".t" -type "double3" 42.97559436283553 -1.7763568394002505e-14 6.2172489379008766e-15 ;
	setAttr ".r" -type "double3" -1.3107364019312539e-15 7.9809908655803713e-16 2.7990977753919945e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.049618189879076458 3.0687766629297699 0.17215762098600934 ;
	setAttr ".radi" 2;
createNode joint -n "l_ankle_bind" -p "l_knee_bind";
	rename -uid "D86F2C50-BF43-F87B-BD0B-558B9B5039D1";
	setAttr ".t" -type "double3" 47.297918865768416 0 -2.6645352591003757e-14 ;
	setAttr ".r" -type "double3" -1.0933156717530834e-15 -6.3052011751669314e-15 -3.9756933518293944e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -5.4535507452341854 -55.236980224196394 4.954417194228701 ;
	setAttr ".radi" 1.0139640363189053;
createNode joint -n "l_toe_bind" -p "l_ankle_bind";
	rename -uid "FD08E157-6C47-BA4C-39CF-A4AEB2DBE9A7";
	setAttr ".t" -type "double3" 14.222955448802448 0.89237732629159083 1.9516518153431051 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -16.674235275019946 -22.068904936164373 5.4241868564992117 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "l_toe_bind_end" -p "l_toe_bind";
	rename -uid "FC57E214-844A-3A4A-F20B-C4B197E5E692";
	setAttr ".t" -type "double3" 13.848393411416048 -0.2233676286844144 2.8074266694776497 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 3.9511661468601882 81.548741204740935 32.376809602341673 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "l_toeTipFront_bind" -p "l_ankle_bind";
	rename -uid "09398772-B946-B78B-04B7-B7BDB5E53A78";
	setAttr ".t" -type "double3" 27.388247358569739 1.6066291414095097 7.9677419322301883 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -157.42938796309693 -49.048676140572624 159.08261563564068 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "l_toeTipLeft_bind" -p "l_ankle_bind";
	rename -uid "485AFB61-2047-226E-0753-E0B5747CD49E";
	setAttr ".t" -type "double3" 14.550152146852543 5.9455515170575168 -3.7831781629751986 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -36.991599147695069 18.987098538778472 92.441780290160594 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "l_toeTipRight_bind" -p "l_ankle_bind";
	rename -uid "453645E2-1943-AF48-87D4-779732B41C4F";
	setAttr ".t" -type "double3" 15.072078108033331 -5.6811136900090808 0.24209302053059956 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 38.995804415151277 -13.641850129915273 -94.67672427132004 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "l_toeTipBack_bind" -p "l_ankle_bind";
	rename -uid "6E50341F-284D-9E86-EAB9-0DA109901F72";
	setAttr ".t" -type "double3" 2.2545356349007015 -2.7892752751225665 -11.043828644007808 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 25.036256619284984 -49.048676140572645 159.08261563564076 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "l_ikOrientationFoot_bind" -p "l_ankle_bind";
	rename -uid "4FADF3C0-8847-E325-9143-EB8852DCD0F4";
	setAttr ".t" -type "double3" 0.012973513433488293 0.00247075706305111 0.0096961979274556853 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -20.850376099562968 -36.285679232249372 10.782642797832269 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "r_leg_bind" -p "pelvis_bind_end";
	rename -uid "0348E634-8A4F-DC3D-B4E8-A9949B4E9A79";
	setAttr ".t" -type "double3" 5.7940599999999982 6.0846702420043357 1.2264863119124954 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.93660418776084287 -3.208336440481411 102.65984333912365 ;
	setAttr ".radi" 2;
createNode joint -n "r_knee_bind" -p "r_leg_bind";
	rename -uid "AF1FC836-5F43-54C0-83C8-F7A870FEEB23";
	setAttr ".t" -type "double3" -42.975552009707357 2.4632665237334095e-05 -5.4612627407024661e-06 ;
	setAttr ".r" -type "double3" -1.3107364019312539e-15 7.9809908655803713e-16 2.7990977753919945e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.049618189881457497 3.0687766629296553 0.17215762098601553 ;
	setAttr ".radi" 2;
createNode joint -n "r_ankle_bind" -p "r_knee_bind";
	rename -uid "0EAE7823-9340-75DB-91EF-748D77F1B63E";
	setAttr ".t" -type "double3" -47.297959286191777 -5.7818320062352768e-05 1.0549975417717405e-06 ;
	setAttr ".r" -type "double3" -1.0933156717530834e-15 -6.3052011751669314e-15 -3.9756933518293944e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -5.4535507452388208 -55.236980224196124 4.9544171942322359 ;
	setAttr ".radi" 1.0139640363189053;
createNode joint -n "r_toe_bind" -p "r_ankle_bind";
	rename -uid "5EF1D748-3144-6213-FFE7-9AA3ED656F84";
	setAttr ".t" -type "double3" -14.22295633755509 -0.89238402387514881 -1.9516501248005038 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -16.67423527501958 -22.068904936164383 5.4241868564990723 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "r_toe_bind_end" -p "r_toe_bind";
	rename -uid "336AEAAA-4748-531E-C098-EE9D85857581";
	setAttr ".t" -type "double3" -13.848379904793429 0.22337844931449524 -2.8074273005182491 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 3.9511661468600381 81.548741204740935 32.376809602341609 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "r_toeTipFront_bind" -p "r_ankle_bind";
	rename -uid "CD53C40D-324B-584D-E47E-2490BB400919";
	setAttr ".t" -type "double3" -27.388283766595798 -1.6066166444964338 -7.96777491841046 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -157.42938796309741 -49.048676140572752 159.08261563564105 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "r_toeTipLeft_bind" -p "r_ankle_bind";
	rename -uid "86384509-5E48-DDC6-66E6-6C85370E5352";
	setAttr ".t" -type "double3" -14.550150822785751 -5.9455412097909495 3.7831764410267343 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -36.991599147695041 18.987098538778131 92.441780290160594 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "r_toeTipRight_bind" -p "r_ankle_bind";
	rename -uid "C97F4616-8944-5F66-016B-DAA946715601";
	setAttr ".t" -type "double3" -15.072078621382762 5.6811334943529417 -0.24209917430051431 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 38.995804415151206 -13.641850129914946 -94.67672427132004 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "r_toeTipBack_bind" -p "r_ankle_bind";
	rename -uid "3336924B-CF4B-8625-0546-AD9D22B68A81";
	setAttr ".t" -type "double3" -2.2545067413402906 2.7892704639323256 11.043853954063557 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 25.036256619284533 -49.048676140572788 159.0826156356411 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "r_ikOrientationFoot_bind" -p "r_ankle_bind";
	rename -uid "DDE61F7E-5946-0657-3BE2-648169740CCE";
	setAttr ".t" -type "double3" -0.012940616315144204 -0.0024294640245230426 -0.0097370300368038176 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 159.14962390043749 -36.285679232249407 10.782642797832018 ;
	setAttr ".radi" 1.0884578140401078;
createNode joint -n "spinea_bind" -p "root_bind";
	rename -uid "3B039A39-1442-6FD3-3136-FC9DE5128328";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 5.7907141856965341 0.5727453376278776 3.6908239912176056e-15 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.1019703183559703e-14 1.7081224066273485e-14 2.6060970724468988 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.013383715203514191 -0.9999104340726479 0
		 0 0.9999104340726479 0.013383715203514191 0 0 1.0828252999999999 9.3677603692584042e-17 1;
createNode joint -n "spineb_bind" -p "spinea_bind";
	rename -uid "1E6DE4E5-2D41-0E56-F031-BD84D11CC7CA";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 8.7802547634213788 0.21863493093209002 2.8236679436803051e-15 ;
	setAttr ".r" -type "double3" -2.1373327459434834e-12 2.9261103069464353e-13 -5.4577068594130612e-27 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 8.3867229504112508 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -0.28728848046479127 -0.95784410474368487 0
		 0 0.95784410474368487 -0.28728848046479127 0 -1.4044399999999999e-17 1.1594070402710164 0.0010250400102359435 1;
createNode joint -n "spinec_bind" -p "spineb_bind";
	rename -uid "3B20D915-E348-EBF4-C6A3-61A634E9671D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 8.5229734589961872 -0.29313968593882583 -4.3896448633106406e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 10.81035301941057 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -0.10835094671969514 -0.99411270605749014 0
		 0 0.99411270605749014 -0.10835094671969514 0 1.7038860000000002e-16 1.2531688671338082 -0.027097169680893572 1;
createNode joint -n "spined_bind" -p "spinec_bind";
	rename -uid "D852892C-FD4B-F7CE-B17D-D88BD3FF1883";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 7.4467578061469055 0.16512896419178347 1.2790882156728984e-09 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.2863949620650191e-06 -2.3696978997167331e-23 18.93675129849381 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 -0.10835094671969514 -0.99411270605749014 0
		 0 0.99411270605749014 -0.10835094671969514 0 1.7038860000000002e-16 1.2531688671338082 -0.027097169680893572 1;
createNode joint -n "spinef_bind" -p "spined_bind";
	rename -uid "47574271-CC4D-B1F4-4915-788C112FF0A0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "jtr" -ln "jtrans" -at "compound" -nc 3;
	addAttr -ci true -sn "jtrx" -ln "jtransx" -at "float" -p "jtrans";
	addAttr -ci true -sn "jtry" -ln "jtransy" -at "float" -p "jtrans";
	addAttr -ci true -sn "jtrz" -ln "jtransz" -at "float" -p "jtrans";
	setAttr ".ihi" 0;
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 1.5983665059862489 0 -8.7527779681747895e-08 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.4131375292478416e-06 7.1167025876775607e-07 -7.5811227524393709 ;
	setAttr ".pa" -type "double3" 0 0 14.999999999999998 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.30510039240436221 -0.95232019329357087 0
		 0 0.95232019329357087 0.30510039240436221 0 2.6802947779167195e-10 1.4439098441174543 -0.047886528179669624 1;
	setAttr ".jtrx" 2.6802932096003929e-10;
	setAttr ".jtry" -1.1114800744584411e-16;
	setAttr ".jtrz" 0.19187057018280029;
createNode joint -n "l_scapula_bind" -p "spinef_bind";
	rename -uid "EA1FE5AB-B548-37DB-7E61-2CBD5421C8E3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -1.5332104731039493 7.7277353821410131 -9.2439323476757256 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 175.53301340429226 82.420412096612438 82.728962441817515 ;
	setAttr ".pa" -type "double3" -39.801311003972025 3.7285552875104893 -1.6118947839533955 ;
	setAttr ".bps" -type "matrix" -0.48489633279294364 -5.8601179464545794e-11 -0.87457163597040755 0
		 0.18438504917195703 0.97752296117517079 -0.10223020110114545 0 0.85491385535959719 -0.21082898371743303 -0.47399729908393395 0
		 0.03128376249734309 1.5329638506577044 0.063995442003242503 1;
createNode joint -n "l_scapula1_bind" -p "l_scapula_bind";
	rename -uid "D3CB9EEA-2344-F8E8-8883-809E808E674F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 5.0620951726844057 4.8118884593331899 2.4813223671417077 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 17.084271193462705 8.6188672141555589 -41.757159183358866 ;
	setAttr ".bps" -type "matrix" -0.066211429724184589 -8.0009193714758453e-12 -0.99786996343449652 0
		 0.71357839870845874 0.6990654209232251 -0.047347898760033008 0 0.69753159987303492 -0.71514750549821438 -0.046283149300045234 0
		 0.19727811122323929 1.4920282410342087 -0.028038243573389521 1;
createNode joint -n "l_pec_bind" -p "spinef_bind";
	rename -uid "F4EF2CB6-1E46-D425-ED38-22979DB37C16";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -0.89181104497711772 -15.127371274210255 -10.505857150129344 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 175.53301340429243 82.420412096612466 82.728962441817558 ;
	setAttr ".pa" -type "double3" -39.801311003972025 3.7285552875104893 -1.6118947839533955 ;
	setAttr ".bps" -type "matrix" -0.48489633279294364 -5.8601179464545794e-11 -0.87457163597040755 0
		 0.18438504917195703 0.97752296117517079 -0.10223020110114545 0 0.85491385535959719 -0.21082898371743303 -0.47399729908393395 0
		 0.03128376249734309 1.5329638506577044 0.063995442003242503 1;
createNode joint -n "l_pec1_bind" -p "l_pec_bind";
	rename -uid "41786CB2-B147-F3C3-317D-ED96056167C7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 6.3932501088619178 3.7141238973919002 -1.6108540585925368 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 17.596808543780782 -28.593730948096596 -64.851615352666002 ;
	setAttr ".bps" -type "matrix" -0.066211429724184589 -8.0009193714758453e-12 -0.99786996343449652 0
		 0.71357839870845874 0.6990654209232251 -0.047347898760033008 0 0.69753159987303492 -0.71514750549821438 -0.046283149300045234 0
		 0.19727811122323929 1.4920282410342087 -0.028038243573389521 1;
createNode joint -n "r_scapula_bind" -p "spinef_bind";
	rename -uid "F28BDAC5-F843-9872-5B5F-0BA7729213DF";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -1.5331375042786561 7.7277513844964432 9.2439300558210551 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 175.53301340429161 82.420412096613504 -97.27103755818321 ;
	setAttr ".pa" -type "double3" -39.801311003972025 3.7285552875104893 -1.6118947839533955 ;
	setAttr ".bps" -type "matrix" -0.48489633279294364 -5.8601179464545794e-11 -0.87457163597040755 0
		 0.18438504917195703 0.97752296117517079 -0.10223020110114545 0 0.85491385535959719 -0.21082898371743303 -0.47399729908393395 0
		 0.03128376249734309 1.5329638506577044 0.063995442003242503 1;
createNode joint -n "r_scapula1_bind" -p "r_scapula_bind";
	rename -uid "F7574DD8-7144-3BB4-846C-62831F5C8442";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -5.0621239927947475 -4.8114297385777576 -2.4813565816509708 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 17.084271193462687 8.6188672141555536 -41.757159183358873 ;
	setAttr ".bps" -type "matrix" -0.066211429724184589 -8.0009193714758453e-12 -0.99786996343449652 0
		 0.71357839870845874 0.6990654209232251 -0.047347898760033008 0 0.69753159987303492 -0.71514750549821438 -0.046283149300045234 0
		 0.19727811122323929 1.4920282410342087 -0.028038243573389521 1;
createNode joint -n "r_pec_bind" -p "spinef_bind";
	rename -uid "D23E3F84-D940-B48F-B10D-0BB740EF3695";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -0.8918379991835792 -15.127355784555355 10.505900085901612 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 175.53301340429178 82.42041209661356 -97.271037558183011 ;
	setAttr ".pa" -type "double3" -39.801311003972025 3.7285552875104893 -1.6118947839533955 ;
	setAttr ".bps" -type "matrix" -0.48489633279294364 -5.8601179464545794e-11 -0.87457163597040755 0
		 0.18438504917195703 0.97752296117517079 -0.10223020110114545 0 0.85491385535959719 -0.21082898371743303 -0.47399729908393395 0
		 0.03128376249734309 1.5329638506577044 0.063995442003242503 1;
createNode joint -n "r_pec1_bind" -p "r_pec_bind";
	rename -uid "428E0BD4-D840-1596-603C-A8824009ED99";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -6.3932531360822491 -3.7145967425102384 1.6108563459871377 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 17.59680854378411 -28.593730948096571 -64.85161535266603 ;
	setAttr ".bps" -type "matrix" -0.066211429724184589 -8.0009193714758453e-12 -0.99786996343449652 0
		 0.71357839870845874 0.6990654209232251 -0.047347898760033008 0 0.69753159987303492 -0.71514750549821438 -0.046283149300045234 0
		 0.19727811122323929 1.4920282410342087 -0.028038243573389521 1;
createNode joint -n "l_clav_bind" -p "spinef_bind";
	rename -uid "3F8F0DB1-754E-76C5-51CF-E2BAAE715553";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 11.847455193989376 -11.856012915378891 -1.2322815529352538 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 175.53301340429226 82.420412096612466 82.728962441817458 ;
	setAttr ".pa" -type "double3" -39.801311003972025 3.7285552875104893 -1.6118947839533955 ;
	setAttr ".bps" -type "matrix" -0.48489633279294364 -5.8601179464545794e-11 -0.87457163597040755 0
		 0.18438504917195703 0.97752296117517079 -0.10223020110114545 0 0.85491385535959719 -0.21082898371743303 -0.47399729908393395 0
		 0.03128376249734309 1.5329638506577044 0.063995442003242503 1;
createNode joint -n "l_clav1_bind" -p "l_clav_bind";
	rename -uid "F56A64CA-744C-DF96-E74C-1099C182C800";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 7.4311908109991327 -0.27960696984371225 -1.048607679703629 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 7.2357619003295003e-14 1.5902773407317592e-15 -2.8177726631090856e-14 ;
	setAttr ".bps" -type "matrix" -0.066211429724184589 -8.0009193714758453e-12 -0.99786996343449652 0
		 0.71357839870845874 0.6990654209232251 -0.047347898760033008 0 0.69753159987303492 -0.71514750549821438 -0.046283149300045234 0
		 0.19727811122323929 1.4920282410342087 -0.028038243573389521 1;
createNode joint -n "r_clav_bind" -p "spinef_bind";
	rename -uid "93E46E41-964B-3BC1-22F4-8D888EE21660";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 11.847879149728485 -11.856015331476563 1.2322800239966309 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 175.53301340429167 82.42041209661356 -97.27103755818311 ;
	setAttr ".pa" -type "double3" -39.801311003972025 3.7285552875104893 -1.6118947839533955 ;
	setAttr ".bps" -type "matrix" -0.48489633279294364 -5.8601179464545794e-11 -0.87457163597040755 0
		 0.18438504917195703 0.97752296117517079 -0.10223020110114545 0 0.85491385535959719 -0.21082898371743303 -0.47399729908393395 0
		 0.03128376249734309 1.5329638506577044 0.063995442003242503 1;
createNode joint -n "r_clav1_bind" -p "r_clav_bind";
	rename -uid "E0EF9FF5-2B47-13A7-E8AE-42AE68382589";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -7.4311773792335512 0.28050468153577413 1.0485715581227311 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.5377364625159387e-07 -2.3696979879948583e-23 1.1848489480928038e-22 ;
	setAttr ".bps" -type "matrix" -0.066211429724184589 -8.0009193714758453e-12 -0.99786996343449652 0
		 0.71357839870845874 0.6990654209232251 -0.047347898760033008 0 0.69753159987303492 -0.71514750549821438 -0.046283149300045234 0
		 0.19727811122323929 1.4920282410342087 -0.028038243573389521 1;
createNode joint -n "l_clavicle_bind" -p "spinef_bind";
	rename -uid "A5333C4A-0F49-38A3-C5B6-D88BA3CE441D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 14.050518687032358 -4.9441227195400428 -2.066326430050943 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -92.365018988278649 76.30682732346807 153.25993780974846 ;
	setAttr ".pa" -type "double3" -39.801311003972025 3.7285552875104893 -1.6118947839533955 ;
	setAttr ".bps" -type "matrix" -0.48489633279294364 -5.8601179464545794e-11 -0.87457163597040755 0
		 0.18438504917195703 0.97752296117517079 -0.10223020110114545 0 0.85491385535959719 -0.21082898371743303 -0.47399729908393395 0
		 0.03128376249734309 1.5329638506577044 0.063995442003242503 1;
createNode joint -n "l_shoulder_bind" -p "l_clavicle_bind";
	rename -uid "C33F6D27-3644-C88A-65AC-B583AA9F78C2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 22.633343278109542 0.84843321993531617 -4.8139413565236975 ;
	setAttr ".r" -type "double3" -3.508549382989441e-14 -3.0414054141494871e-14 -8.4980445395353407e-15 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -5.0394728474775015 2.5870321795305005 -22.458009235873593 ;
	setAttr ".bps" -type "matrix" -0.066211429724184589 -8.0009193714758453e-12 -0.99786996343449652 0
		 0.71357839870845874 0.6990654209232251 -0.047347898760033008 0 0.69753159987303492 -0.71514750549821438 -0.046283149300045234 0
		 0.19727811122323929 1.4920282410342087 -0.028038243573389521 1;
createNode joint -n "l_elbow_bind" -p "l_shoulder_bind";
	rename -uid "7BF28FEB-9547-C56C-2075-4EA7929A40F0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 19.661277490315037 -1.3951708410786523e-07 2.5308341089491648e-08 ;
	setAttr ".r" -type "double3" -4.1620539776963991e-16 -7.6712635398546309e-34 -2.1120870931593667e-16 ;
	setAttr ".mnrl" -type "double3" 0 -360 0 ;
	setAttr ".mxrl" -type "double3" 0 360 0 ;
	setAttr ".jo" -type "double3" 0.46695678350419528 -9.0378839211416828 0.27020420605315792 ;
	setAttr ".bps" -type "matrix" 0.175282942372263 -0.1506173281637625 -0.97292872841238043 0
		 0.71262847795635598 0.70126141598168834 0.019826216506562903 0 0.6792912059779147 -0.69681191645390739 0.23025336168860505 0
		 0.41527766213155909 1.2685231911408519 -0.042503116224132616 1;
createNode joint -n "l_wrist_bind" -p "l_elbow_bind";
	rename -uid "CA14E2B2-0646-589E-28FB-B2A6A7A532C0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 26.951654938979981 -0.15563571795212283 -0.46678032754151921 ;
	setAttr ".ro" 1;
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -80.998891167231207 0.040741830307370178 0.25801203708023701 ;
	setAttr ".pa" -type "double3" 0 1.4312496066585827e-14 0 ;
	setAttr ".bps" -type "matrix" 0.24009939508979117 -0.21341532807689279 -0.94699851014631942 0
		 0.71354847243399577 0.70022465434691006 0.023108676549333809 0 0.65817995864704659 -0.68127771957299676 0.32040569727891827 0
		 0.57960185652744001 1.09996064269464 0.013196409742722834 1;
createNode joint -n "l_palm_bind" -p "l_wrist_bind";
	rename -uid "5EE0B37E-AB4D-9D04-C179-4B84CE00713D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 5.3756974215672066 1.7763568394002505e-15 -4.2632564145606011e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -133.34096998824489 -12.336431013898938 -135.23511189917883 ;
	setAttr ".bps" -type "matrix" 0.5347350989130617 -0.12635543252472892 -0.83551940651425127 0
		 0.59778543083948077 0.75540983235973813 0.26834411461831809 0 0.5972528381401756 -0.64295434507103322 0.47947758809748808 0
		 0.62283930118148434 1.0552058498646941 0.034244640429380267 1;
createNode joint -n "l_thumba_bind" -p "l_palm_bind";
	rename -uid "5514D03E-7D4D-D479-CF25-E193289AF4FD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 2.1068361753406748 -3.8256550360630683 -3.0758963851955912 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -89.626744505133104 23.04099893573683 -92.68353273485485 ;
	setAttr ".bps" -type "matrix" 0.88524390354050531 0.46125314320563177 0.059906336286686651 0
		 -0.46291036920937945 0.86112758274632539 0.21017439499593332 0 0.045356601755473569 -0.21378686609891553 0.97582680561706236 0
		 0.58462461106580021 1.056112673438097 0.035249484757339945 1;
createNode joint -n "l_thumbb_bind" -p "l_thumba_bind";
	rename -uid "E7DB0351-BB43-CA93-06A1-4FA1C04A1B43";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 3.5456781728867384 0 4.2632564145606011e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.920780632268055 -1.0806415903226139 -23.486691139576273 ;
	setAttr ".bps" -type "matrix" 0.46589271926010201 0.75038784456701824 0.46889450505043484 0
		 -0.88320558052345877 0.36216323890051755 0.29796927848573024 0 0.053776171978376482 -0.55295196094701682 0.83147594806596858 0
		 0.58661159691975429 1.046747080288287 0.077998588165121757 1;
createNode joint -n "l_thumbc_bind" -p "l_thumbb_bind";
	rename -uid "AD96E70A-0049-DCCE-275A-F2AC0F92E78D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 2.4618581697488082 0.051966322261606024 -0.13219860546494999 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.8328953702983992 0.20512077311893115 -12.295811375016546 ;
	setAttr ".bps" -type "matrix" 0.70126201469425209 0.48792542992097176 0.51976952737092386 0
		 -0.71182809594887841 0.43919967543601102 0.54809160449207439 0 0.039145224035032254 -0.75434237580381058 0.65531307899500224 0
		 0.58853766990225242 1.0269422895525737 0.10777912664991646 1;
createNode joint -n "l_thumbd_bind_end" -p "l_thumbc_bind";
	rename -uid "953F646B-C645-94F8-AB6C-1DB67E2D65DD";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 2.6940285139025875 -0.049808099492565816 -0.019896876105661931 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 16.108925804359941 65.192242486607739 82.106540523002195 ;
	setAttr ".bps" -type "matrix" 0.92881034772787729 0.22110258146565348 0.29736339119475363 0
		 -0.13500380342612328 0.94923741016148722 -0.28411672286296952 0 -0.34508739619710904 0.22374536334667758 0.91151121845359762 0
		 0.58962474555988287 1.0059939553823189 0.12597738490141411 1;
createNode joint -n "l_indexa_bind" -p "l_palm_bind";
	rename -uid "2AADA65E-A044-A786-9690-55BAD2FFEBDB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -3.8014875940855326 -6.825674695967777 -0.9177401696908305 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 43.279671050394441 204.7636799549278 45.422151241198286 ;
	setAttr ".bps" -type "matrix" 0.52215554280650389 -0.22073389341899374 -0.82379010519217666 0
		 0.75423234613957879 0.57040399044796575 0.32522739078654483 0 0.39810445507835257 -0.79114842853735712 0.46432424755728496 0
		 0.64144250660015312 1.0243046082985687 0.079643438690811946 1;
createNode joint -n "l_indexb_bind" -p "l_indexa_bind";
	rename -uid "A8ABF1CD-D94A-00EA-0684-4B9F925AD03A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 4.1856057872435795 0.21928152403657464 -0.072054670363087325 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.72467303031538299 -0.86850766360856702 1.7877377323651913 ;
	setAttr ".bps" -type "matrix" 0.49256646035740631 -0.14962556304680452 -0.8573158537049822 0
		 0.86106152724259299 0.22675387393819496 0.45514363332543184 0 0.12629856861274974 -0.96239018674181631 0.24052816888968073 0
		 0.656994128321986 0.99339904838963999 0.097781881911359017 1;
createNode joint -n "l_indexc_bind" -p "l_indexb_bind";
	rename -uid "B4E46834-EF4D-A5B3-6795-F3BF3A9ED9A0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 3.1264956891797206 -0.019133291250502442 -0.059994232974966241 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.0414053598392154 1.4167658875116391 -1.7680567365568631 ;
	setAttr ".bps" -type "matrix" 0.4960843811498743 -0.17221495460309391 -0.85102426298560996 0
		 0.86736033339865726 0.053330647781204998 0.49481500993180055 0 -0.039828869249789067 -0.98361468645923111 0.17582892184163523 0
		 0.66092751052532717 0.96342682879301678 0.10527277614163155 1;
createNode joint -n "l_indexd_bind_end" -p "l_indexc_bind";
	rename -uid "D1C2CC3A-F74E-E2AB-26C5-B8BCDB8961BB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 2.8076413847755122 -0.017452796183128783 -0.048012297714507213 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.93603363407709683 0.12732333020942935 0.32806981796685375 0
		 -0.037796623659636187 0.96323449848835407 -0.26599006778791728 0 -0.34987490781185743 0.23657571833615881 0.90643228008350119 0
		 0.65987770672517909 0.93750084959309654 0.10990725042629286 1;
createNode joint -n "l_middlea_bind" -p "l_palm_bind";
	rename -uid "6204AB59-9D45-0FA2-F98D-6682FA0D5286";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -5.1719847500476739 -4.9408515551435102 1.6628237314913434 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 42.855984006601183 204.92323006206632 36.504422896175427 ;
	setAttr ".bps" -type "matrix" 0.45828506718536549 -0.11278181493926621 -0.88162070042275553 0
		 0.7782578946606743 0.53001145380911041 0.33675288896977312 0 0.42928946713521887 -0.84045709054666107 0.33066967256856472 0
		 0.6539885671046799 1.0256881825546664 0.056252701590324486 1;
createNode joint -n "l_middleb_bind" -p "l_middlea_bind";
	rename -uid "5E4D2BA3-1741-1F6B-601E-3B902C892CE0";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 3.9484219999492236 0.12652921386692384 0.0032532447677056098 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.3510332762580228 -0.22530114753625463 -2.1619414685746139 ;
	setAttr ".bps" -type "matrix" 0.38702607229240549 -0.13756361699827316 -0.91174945607017821 0
		 0.91898965460583737 0.13828898186943556 0.36923457614497474 0 0.075291660184629794 -0.98079172548093385 0.17994098236581618 0
		 0.67449672870853206 0.98553758219389609 0.072049565016262973 1;
createNode joint -n "l_middlec_bind" -p "l_middleb_bind";
	rename -uid "A322615D-D84F-0C9B-7CE8-1A8F43D8C202";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 3.613160482077316 0.072363578593613198 -0.011806575371764438 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.3005939208800326 1.0579153405037429 -0.089101465031665369 ;
	setAttr ".bps" -type "matrix" 0.39274839033955616 -0.1604851381957163 -0.90553477144943983 0
		 0.90424446768037114 -0.11206075203475949 0.41204894190235103 0 -0.16760263886684557 -0.98065636604863082 0.10110611837650442 0
		 0.6773311741846072 0.94861449320310831 0.07882366060900968 1;
createNode joint -n "l_middled_bind_end" -p "l_middlec_bind";
	rename -uid "BB58332B-044B-15A0-ADB4-66A7D00D688B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 2.6509983480971568 -3.3750779948604759e-14 8.5265128291212022e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.93603363407709916 0.12732333020942807 0.32806981796684909 0
		 -0.037796623659636534 0.9632344984883543 -0.26599006778791723 0 -0.34987490781185238 0.2365757183361594 0.90643228008350285 0
		 0.6731098004973658 0.92391490011882282 0.081370199915427016 1;
createNode joint -n "l_ringa_bind" -p "l_palm_bind";
	rename -uid "C2E17ED3-3643-7C7B-492D-71ABBD66DA6D";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -5.1845010182715399 -1.993089440246024 3.7761212287073818 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 43.056958145061763 210.95953032020796 33.680071382232946 ;
	setAttr ".bps" -type "matrix" 0.33492163914162032 -0.065071528645235438 -0.93999637860709995 0
		 0.84029644400573755 0.47197368755430574 0.26672593508637954 0 0.42629729277348594 -0.87920790170252849 0.212753575194012 0
		 0.65575237509483886 1.0208472517202545 0.033475985903515415 1;
createNode joint -n "l_ringb_bind" -p "l_ringa_bind";
	rename -uid "0A64E6C7-6346-ADD1-1052-C795DCE3C965";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 3.6289300393608919 0.089049904819862746 0.077761138723957401 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.5537272899059773 -0.87208094816532244 0.11864945425525021 ;
	setAttr ".bps" -type "matrix" 0.23504713099850685 -0.089613810749258907 -0.96784410476706761 0
		 0.95063597886214035 0.22873972930992098 0.20968875012275962 0 0.20259339056887229 -0.96935416704021049 0.13895472982086038 0
		 0.67505583608778164 0.98103523385642066 0.043109826909512476 1;
createNode joint -n "l_ringc_bind" -p "l_ringb_bind";
	rename -uid "597CFC3B-0349-2DBA-0315-66A4F92BF490";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 3.4976736481361215 -0.043328318635554197 0.0080458849967897095 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.82748677994505182 -1.2809673577701561 -2.5788214025702398 ;
	setAttr ".bps" -type "matrix" 0.22718555234343543 -0.07572970860488773 -0.97090253683931982 0
		 0.97029761034519724 -0.067493264857803964 0.23230842980235286 0 -0.083122031765401228 -0.99484153031196543 0.058146860635278672 0
		 0.68220113229188439 0.94684693861769231 0.048010641791691927 1;
createNode joint -n "l_ringd_bind_end" -p "l_ringc_bind";
	rename -uid "D43BE070-7D47-6BA6-E683-09AF30D16C4E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 2.7005903192547507 5.8619775700208265e-14 7.1054273576010019e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.93603363407709717 0.12732333020943271 0.3280698179668517 0
		 -0.037796623659640691 0.9632344984883543 -0.2659900677879159 0 -0.34987490781185615 0.23657571833615618 0.90643228008350207 0
		 0.68038696923777042 0.92513422646835719 0.049279714311176961 1;
createNode joint -n "l_pinkya_bind" -p "l_palm_bind";
	rename -uid "0482D2E1-0D44-F5AD-B655-D1B3DE2D5C38";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 2.1717251527657737 2.2594377273752997 1.8479219998213097 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 50.799553297543021 196.24853273345636 32.616112690150828 ;
	setAttr ".bps" -type "matrix" 0.23954380354128638 4.163336342344337e-16 -0.97088555771778462 0
		 0.67461897226244028 0.71915554988301766 0.16644680031777015 0 0.69821773713401369 -0.69484911676741357 0.1722692557568033 0
		 0.60584402130958726 1.0704814278182453 -0.00071503730178219121 1;
createNode joint -n "l_pinkyb_bind" -p "l_pinkya_bind";
	rename -uid "A90E994E-E546-3364-F934-33BF5B71A911";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 7.6890739275182751 -0.025274725024949873 -2.8955048478251797 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -10.429797663887797 10.464702382644221 -10.452714237192247 ;
	setAttr ".bps" -type "matrix" 0.083143044287796272 -0.0012175000872797354 -0.99653687933768687 0
		 0.95382338064915329 0.28973141827026222 0.079225398668124239 0 0.28863158647933584 -0.95710721602161164 0.025250432190000338 0
		 0.65852209097084002 1.0180575087018675 0.012282071440397018 1;
createNode joint -n "l_pinkyc_bind" -p "l_pinkyb_bind";
	rename -uid "434EF15B-DB4A-736D-0C2B-4AB6D935537C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 2.3446511660792062 -0.10585490287860466 -0.0025044979454662553 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.32737881379993772 -0.12026856010996576 -5.7674160218355848 ;
	setAttr ".bps" -type "matrix" 0.15321260910740112 -0.035693990178980881 -0.98754839652323156 0
		 0.97694723984473975 0.15580977417762182 0.14593630401810007 0 0.14866064364937834 -0.98714196209857341 0.058743167210589101 0
		 0.66946651615947839 0.9817656099148151 0.013239525437220859 1;
createNode joint -n "l_pinkyd_bind" -p "l_pinkyc_bind";
	rename -uid "72AD20E1-7C4A-63E6-A5D8-BD909B27CF2E";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 2.8982053228166613 -0.021301341424851294 0.006515986253575079 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.65860514602433917 -1.4505229894274945 1.2072949640301418 ;
	setAttr ".bps" -type "matrix" 0.12600627886724242 0.024929795599760017 -0.99171615040664995 0
		 0.99155755436884785 0.027665706141153795 0.12668158934028564 0 0.030594673721092647 -0.99930631639906375 -0.021233274472731871 0
		 0.67299661479279138 0.95832491703372613 0.014634441866990037 1;
createNode joint -n "l_pinkye_bind_end" -p "l_pinkyd_bind";
	rename -uid "F5A80083-9E42-AFD9-A65E-49A93D2B5F3A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 2.0394126117188414 2.3092638912203256e-14 -4.2632564145606011e-14 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.94740634517070332 -0.02092298289026728 0.31934847098000019 0
		 0.011303433397696931 0.99942566627116614 0.031946361167740835 0 -0.31983347154998343 -0.02665645110305399 0.94709871929534162 0
		 0.67354220667513531 0.94050438332996544 0.014255790919654858 1;
createNode joint -n "neck_bind" -p "spinef_bind";
	rename -uid "0D7838B4-D64A-9BEF-7A13-F9B7A6F3A7E8";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr -k off ".v";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 21.389009967953555 -6.6128010689053056 4.275982820666948e-09 ;
	setAttr -l on ".ro" 1;
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0 0 -32.779910038357251 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 3.5579240251770727e-06 -0.99999999999367062 0
		 0 0.99999999999367062 3.5579240251770727e-06 0 2.9481969701141876e-10 1.5662519807111872 -0.0086910620484275322 1;
	setAttr ".radi" 0.5;
createNode joint -n "head_bind" -p "neck_bind";
	rename -uid "0A8FC1E3-954B-B953-7ECC-05BBC36E5676";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 9.5069632430065667 0.0040347416002184389 3.2726464524493058e-08 ;
	setAttr -l on ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -2.2071323838088906e-12 -3.7638054054776661e-08 0.0067197613399407052 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 0.095567781730337281 -0.99542292473859706 0
		 0 0.99542292473859706 0.095567781730337281 0 3.3644913694349526e-10 1.2434674676729853 0.60390246816076032 1;
	setAttr ".radi" 0.5;
createNode joint -n "l_neckClav_bind" -p "neck_bind";
	rename -uid "C119F3D0-F34D-00CF-F260-C592FC4CF155";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 2.1458397820665214 6.139014825155491 -6.6051332998121213 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 175.53301163872914 82.420410908404932 99.519712714173068 ;
	setAttr ".pa" -type "double3" -39.801311003972025 3.7285552875104893 -1.6118947839533955 ;
	setAttr ".bps" -type "matrix" -0.48489633279294364 -5.8601179464545794e-11 -0.87457163597040755 0
		 0.18438504917195703 0.97752296117517079 -0.10223020110114545 0 0.85491385535959719 -0.21082898371743303 -0.47399729908393395 0
		 0.03128376249734309 1.5329638506577044 0.063995442003242503 1;
createNode joint -n "l_neckClav1_bind" -p "l_neckClav_bind";
	rename -uid "6F512E18-CD4D-4FA5-A874-509A62F45A1A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 9.1609220159261984 -5.4915686045536631 0.73768843273417595 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 22.594047785884761 -12.723711310984337 -92.308903682560612 ;
	setAttr ".bps" -type "matrix" -0.066211429724184589 -8.0009193714758453e-12 -0.99786996343449652 0
		 0.71357839870845874 0.6990654209232251 -0.047347898760033008 0 0.69753159987303492 -0.71514750549821438 -0.046283149300045234 0
		 0.19727811122323929 1.4920282410342087 -0.028038243573389521 1;
createNode joint -n "r_neckClav_bind" -p "neck_bind";
	rename -uid "B15723ED-A749-1709-E5DC-A49878A6145C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 2.1455117952957607 6.1389846561531485 6.6051300097218988 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 175.53301010082041 82.420410520819516 -80.480288810298362 ;
	setAttr ".pa" -type "double3" -39.801311003972025 3.7285552875104893 -1.6118947839533955 ;
	setAttr ".bps" -type "matrix" -0.48489633279294364 -5.8601179464545794e-11 -0.87457163597040755 0
		 0.18438504917195703 0.97752296117517079 -0.10223020110114545 0 0.85491385535959719 -0.21082898371743303 -0.47399729908393395 0
		 0.03128376249734309 1.5329638506577044 0.063995442003242503 1;
createNode joint -n "r_neckClav1_bind" -p "r_neckClav_bind";
	rename -uid "120E4E7D-5346-BA08-DD06-85960D0130A7";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -9.160887906356276 5.4911482374276659 -0.73772365738830814 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 22.594047785884801 -12.723711310984299 -92.308903682560626 ;
	setAttr ".bps" -type "matrix" -0.066211429724184589 -8.0009193714758453e-12 -0.99786996343449652 0
		 0.71357839870845874 0.6990654209232251 -0.047347898760033008 0 0.69753159987303492 -0.71514750549821438 -0.046283149300045234 0
		 0.19727811122323929 1.4920282410342087 -0.028038243573389521 1;
createNode joint -n "r_clavicle_bind" -p "spinef_bind";
	rename -uid "18EFCB44-E446-C11E-D3D8-FCAD467C7699";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 14.050791915559657 -4.9442504114851999 2.0663300565367568 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -92.365020674573145 76.306827502423673 -26.740063828617078 ;
	setAttr ".pa" -type "double3" -39.801311003972025 3.7285552875104893 -1.6118947839533955 ;
	setAttr ".bps" -type "matrix" -0.48489633279294364 -5.8601179464545794e-11 -0.87457163597040755 0
		 0.18438504917195703 0.97752296117517079 -0.10223020110114545 0 0.85491385535959719 -0.21082898371743303 -0.47399729908393395 0
		 0.03128376249734309 1.5329638506577044 0.063995442003242503 1;
createNode joint -n "r_shoulder_bind" -p "r_clavicle_bind";
	rename -uid "71AACDEC-9C4B-F2BB-FAED-DDBFF7C44772";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -22.63328745239788 -0.8485767095496044 4.8139494164395318 ;
	setAttr ".r" -type "double3" -3.508549382989441e-14 -3.0414054141494871e-14 -8.4980445395353407e-15 ;
	setAttr ".ro" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -5.0394728474774215 2.5870321795305244 -22.458009235873611 ;
	setAttr ".bps" -type "matrix" -0.066211429724184589 -8.0009193714758453e-12 -0.99786996343449652 0
		 0.71357839870845874 0.6990654209232251 -0.047347898760033008 0 0.69753159987303492 -0.71514750549821438 -0.046283149300045234 0
		 0.19727811122323929 1.4920282410342087 -0.028038243573389521 1;
createNode joint -n "r_elbow_bind" -p "r_shoulder_bind";
	rename -uid "B60B37BD-7B40-489B-5E7A-0CBC75DE92C1";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -19.661488100545711 0.00032811191317705379 6.4314524274022844e-06 ;
	setAttr ".r" -type "double3" -4.1620539776963991e-16 -7.6712635398546309e-34 -2.1120870931593667e-16 ;
	setAttr ".mnrl" -type "double3" 0 -360 0 ;
	setAttr ".mxrl" -type "double3" 0 360 0 ;
	setAttr ".jo" -type "double3" 0.46695678350458641 -9.0378839211416704 0.27020420605314704 ;
	setAttr ".bps" -type "matrix" 0.175282942372263 -0.1506173281637625 -0.97292872841238043 0
		 0.71262847795635598 0.70126141598168834 0.019826216506562903 0 0.6792912059779147 -0.69681191645390739 0.23025336168860505 0
		 0.41527766213155909 1.2685231911408519 -0.042503116224132616 1;
createNode joint -n "r_wrist_bind" -p "r_elbow_bind";
	rename -uid "3E2C27B0-8C41-410D-6BE4-9A9665B21814";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 2;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -26.951912860662226 0.15591184134916602 0.46684146891272249 ;
	setAttr ".ro" 1;
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -80.998891167231633 0.040741830306562338 0.25801203708023523 ;
	setAttr ".pa" -type "double3" 0 1.4312496066585827e-14 0 ;
	setAttr ".bps" -type "matrix" 0.24009939508979117 -0.21341532807689279 -0.94699851014631942 0
		 0.71354847243399577 0.70022465434691006 0.023108676549333809 0 0.65817995864704659 -0.68127771957299676 0.32040569727891827 0
		 0.57960185652744001 1.09996064269464 0.013196409742722834 1;
createNode joint -n "r_palm_bind" -p "r_wrist_bind";
	rename -uid "BDDB4E42-CB49-F076-1329-99A152427F1B";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 3;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -5.3757715951147915 -1.0350490686761304e-06 5.9631964390405301e-05 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -133.34096998824501 -12.336431013899047 -135.23511189917801 ;
	setAttr ".bps" -type "matrix" 0.5347350989130617 -0.12635543252472892 -0.83551940651425127 0
		 0.59778543083948077 0.75540983235973813 0.26834411461831809 0 0.5972528381401756 -0.64295434507103322 0.47947758809748808 0
		 0.62283930118148434 1.0552058498646941 0.034244640429380267 1;
createNode joint -n "r_thumba_bind" -p "r_palm_bind";
	rename -uid "C080D3AA-2F4F-164A-24BE-A4A9763C22A3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -2.1072381796443125 3.8257923066364299 3.0764222591885044 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -89.626744505133104 23.040998935736898 -92.683532734854822 ;
	setAttr ".bps" -type "matrix" 0.88524390354050531 0.46125314320563177 0.059906336286686651 0
		 -0.46291036920937945 0.86112758274632539 0.21017439499593332 0 0.045356601755473569 -0.21378686609891553 0.97582680561706236 0
		 0.58462461106580021 1.056112673438097 0.035249484757339945 1;
createNode joint -n "r_thumbb_bind" -p "r_thumba_bind";
	rename -uid "63C3180A-C94B-CC0C-C213-C9B9DDDEDA51";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -3.5457277955230779 -1.2285750159435338e-05 -1.9974647322840156e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.9207806322676446 -1.0806415903226028 -23.486691139576273 ;
	setAttr ".bps" -type "matrix" 0.46589271926010201 0.75038784456701824 0.46889450505043484 0
		 -0.88320558052345877 0.36216323890051755 0.29796927848573024 0 0.053776171978376482 -0.55295196094701682 0.83147594806596858 0
		 0.58661159691975429 1.046747080288287 0.077998588165121757 1;
createNode joint -n "r_thumbc_bind" -p "r_thumbb_bind";
	rename -uid "507E87EF-384E-E4BA-0C6F-5F8B40923E21";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -2.4617895012871145 -0.051819148717896724 0.1322799957620866 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.8328953702986421 0.20512077311901553 -12.295811375016566 ;
	setAttr ".bps" -type "matrix" 0.70126201469425209 0.48792542992097176 0.51976952737092386 0
		 -0.71182809594887841 0.43919967543601102 0.54809160449207439 0 0.039145224035032254 -0.75434237580381058 0.65531307899500224 0
		 0.58853766990225242 1.0269422895525737 0.10777912664991646 1;
createNode joint -n "r_thumbd_bind_end" -p "r_thumbc_bind";
	rename -uid "FC4984C1-BB4E-7F9A-C37F-78B8C5AAF044";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -2.6940377786841765 0.049817511034007111 0.019913237224745473 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 16.108925804360062 65.192242486607569 82.106540523002309 ;
	setAttr ".bps" -type "matrix" 0.92881034772787729 0.22110258146565348 0.29736339119475363 0
		 -0.13500380342612328 0.94923741016148722 -0.28411672286296952 0 -0.34508739619710904 0.22374536334667758 0.91151121845359762 0
		 0.58962474555988287 1.0059939553823189 0.12597738490141411 1;
createNode joint -n "r_indexa_bind" -p "r_palm_bind";
	rename -uid "02700680-6345-5835-74F6-1BA3E8D5DA00";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 3.8010301879845514 6.8258653744513964 0.91835891501914091 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 43.279671050394441 204.7636799549278 45.422151241198208 ;
	setAttr ".bps" -type "matrix" 0.52215554280650389 -0.22073389341899374 -0.82379010519217666 0
		 0.75423234613957879 0.57040399044796575 0.32522739078654483 0 0.39810445507835257 -0.79114842853735712 0.46432424755728496 0
		 0.64144250660015312 1.0243046082985687 0.079643438690811946 1;
createNode joint -n "r_indexb_bind" -p "r_indexa_bind";
	rename -uid "AD2F0B94-F84D-BEBE-8384-9F95F8E0B69C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -4.185858474161706 -0.21926273967571319 0.072608964175685742 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.72467303031656916 -0.86850766360851384 1.7877377323650436 ;
	setAttr ".bps" -type "matrix" 0.49256646035740631 -0.14962556304680452 -0.8573158537049822 0
		 0.86106152724259299 0.22675387393819496 0.45514363332543184 0 0.12629856861274974 -0.96239018674181631 0.24052816888968073 0
		 0.656994128321986 0.99339904838963999 0.097781881911359017 1;
createNode joint -n "r_indexc_bind" -p "r_indexb_bind";
	rename -uid "EB72C6A8-2443-A306-9991-149BF115C031";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -3.1265239140219592 0.019110835330458542 0.059907884470419503 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.0414053598400015 1.4167658875115823 -1.7680567365568103 ;
	setAttr ".bps" -type "matrix" 0.4960843811498743 -0.17221495460309391 -0.85102426298560996 0
		 0.86736033339865726 0.053330647781204998 0.49481500993180055 0 -0.039828869249789067 -0.98361468645923111 0.17582892184163523 0
		 0.66092751052532717 0.96342682879301678 0.10527277614163155 1;
createNode joint -n "r_indexd_bind_end" -p "r_indexc_bind";
	rename -uid "6E341E81-AC45-BEDA-DBDB-84B6024287B2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -2.8074823699969267 0.017453022434537502 0.047751939901274909 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.93603363407709683 0.12732333020942935 0.32806981796685375 0
		 -0.037796623659636187 0.96323449848835407 -0.26599006778791728 0 -0.34987490781185743 0.23657571833615881 0.90643228008350119 0
		 0.65987770672517909 0.93750084959309654 0.10990725042629286 1;
createNode joint -n "r_middlea_bind" -p "r_palm_bind";
	rename -uid "0682A58F-C34C-BADC-91A5-D487C92D45DC";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 5.1719066569293197 4.9408736654749106 -1.6627314541821221 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 42.855984006601183 204.92323006206632 36.504422896175427 ;
	setAttr ".bps" -type "matrix" 0.45828506718536549 -0.11278181493926621 -0.88162070042275553 0
		 0.7782578946606743 0.53001145380911041 0.33675288896977312 0 0.42928946713521887 -0.84045709054666107 0.33066967256856472 0
		 0.6539885671046799 1.0256881825546664 0.056252701590324486 1;
createNode joint -n "r_middleb_bind" -p "r_middlea_bind";
	rename -uid "DDBE4EB8-B14F-C0B0-C98A-5BA8556D09A2";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -3.9482838386711672 -0.12653217764978031 -0.0034044393276531082 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 2.3510332762576289 -0.22530114753625569 -2.1619414685745784 ;
	setAttr ".bps" -type "matrix" 0.38702607229240549 -0.13756361699827316 -0.91174945607017821 0
		 0.91898965460583737 0.13828898186943556 0.36923457614497474 0 0.075291660184629794 -0.98079172548093385 0.17994098236581618 0
		 0.67449672870853206 0.98553758219389609 0.072049565016262973 1;
createNode joint -n "r_middlec_bind" -p "r_middleb_bind";
	rename -uid "D77A0AEE-E847-BAB0-CC8A-A7A6F99A468F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -3.6127792475923508 -0.072365544755218281 0.011379037678324266 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -1.3005939208792332 1.0579153405035999 -0.089101465031697219 ;
	setAttr ".bps" -type "matrix" 0.39274839033955616 -0.1604851381957163 -0.90553477144943983 0
		 0.90424446768037114 -0.11206075203475949 0.41204894190235103 0 -0.16760263886684557 -0.98065636604863082 0.10110611837650442 0
		 0.6773311741846072 0.94861449320310831 0.07882366060900968 1;
createNode joint -n "r_middled_bind_end" -p "r_middlec_bind";
	rename -uid "B5BBA402-7D44-E138-EAF3-0984E668972C";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -2.6513561663488128 -3.5398283166898636e-06 0.000378881944953946 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 8.5377364625159345e-07 -1.6587883802806369e-22 -2.0068379100585021e-21 ;
	setAttr ".bps" -type "matrix" 0.93603363407709916 0.12732333020942807 0.32806981796684909 0
		 -0.037796623659636534 0.9632344984883543 -0.26599006778791723 0 -0.34987490781185238 0.2365757183361594 0.90643228008350285 0
		 0.6731098004973658 0.92391490011882282 0.081370199915427016 1;
createNode joint -n "r_ringa_bind" -p "r_palm_bind";
	rename -uid "A256C344-1D4C-13CB-86B2-C2AB79B9D124";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" 5.1841709034120882 1.9931607057171306 -3.7757207421895913 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 43.056958145061763 210.95953032020796 33.680071382232974 ;
	setAttr ".bps" -type "matrix" 0.33492163914162032 -0.065071528645235438 -0.93999637860709995 0
		 0.84029644400573755 0.47197368755430574 0.26672593508637954 0 0.42629729277348594 -0.87920790170252849 0.212753575194012 0
		 0.65575237509483886 1.0208472517202545 0.033475985903515415 1;
createNode joint -n "r_ringb_bind" -p "r_ringa_bind";
	rename -uid "0151E6A5-5141-45EE-8575-CEACF0EED944";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -3.6287286554515639 -0.089037925816883856 -0.077975571628911666 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.5537272899061534 -0.87208094816543014 0.1186494542552526 ;
	setAttr ".bps" -type "matrix" 0.23504713099850685 -0.089613810749258907 -0.96784410476706761 0
		 0.95063597886214035 0.22873972930992098 0.20968875012275962 0 0.20259339056887229 -0.96935416704021049 0.13895472982086038 0
		 0.67505583608778164 0.98103523385642066 0.043109826909512476 1;
createNode joint -n "r_ringc_bind" -p "r_ringb_bind";
	rename -uid "579A3574-7441-B90F-F148-E58E4EA7E049";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -3.4978242700755864 0.043323093943079982 -0.0079423423127025217 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.82748677994627695 -1.28096735777003 -2.5788214025702287 ;
	setAttr ".bps" -type "matrix" 0.22718555234343543 -0.07572970860488773 -0.97090253683931982 0
		 0.97029761034519724 -0.067493264857803964 0.23230842980235286 0 -0.083122031765401228 -0.99484153031196543 0.058146860635278672 0
		 0.68220113229188439 0.94684693861769231 0.048010641791691927 1;
createNode joint -n "r_ringd_bind_end" -p "r_ringc_bind";
	rename -uid "F5CF58F3-9643-917A-897B-7FB4844EC9DE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -2.7007642790075153 -1.1582442125401826e-05 0.00020298497621240585 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 1.2074182697257325e-06 -5.0268884155058425e-22 5.0059429416146228e-22 ;
	setAttr ".bps" -type "matrix" 0.93603363407709717 0.12732333020943271 0.3280698179668517 0
		 -0.037796623659640691 0.9632344984883543 -0.2659900677879159 0 -0.34987490781185615 0.23657571833615618 0.90643228008350207 0
		 0.68038696923777042 0.92513422646835719 0.049279714311176961 1;
createNode joint -n "r_pinkya_bind" -p "r_palm_bind";
	rename -uid "F364F871-8D4B-101F-0181-39948075F56F";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 4;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -2.1721072363955187 -2.2592994773029318 -1.8474259020477888 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 50.799553297543873 196.24853273345636 32.61611269015085 ;
	setAttr ".bps" -type "matrix" 0.23954380354128638 4.163336342344337e-16 -0.97088555771778462 0
		 0.67461897226244028 0.71915554988301766 0.16644680031777015 0 0.69821773713401369 -0.69484911676741357 0.1722692557568033 0
		 0.60584402130958726 1.0704814278182453 -0.00071503730178219121 1;
createNode joint -n "r_pinkyb_bind" -p "r_pinkya_bind";
	rename -uid "12BBD1E9-C240-E7A7-D4CE-87B59FD9C9B3";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 5;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -7.6889782819559054 0.025236114266832033 2.8953371945677162 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -10.429797663888587 10.464702382644059 -10.452714237192435 ;
	setAttr ".bps" -type "matrix" 0.083143044287796272 -0.0012175000872797354 -0.99653687933768687 0
		 0.95382338064915329 0.28973141827026222 0.079225398668124239 0 0.28863158647933584 -0.95710721602161164 0.025250432190000338 0
		 0.65852209097084002 1.0180575087018675 0.012282071440397018 1;
createNode joint -n "r_pinkyc_bind" -p "r_pinkyb_bind";
	rename -uid "4DFA8285-9642-8970-C8A9-5183E6E805D9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 6;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -2.3448068564155342 0.10583850234710646 0.0026334630486388733 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" 0.32737881379806161 -0.12026856010997711 -5.7674160218355475 ;
	setAttr ".bps" -type "matrix" 0.15321260910740112 -0.035693990178980881 -0.98754839652323156 0
		 0.97694723984473975 0.15580977417762182 0.14593630401810007 0 0.14866064364937834 -0.98714196209857341 0.058743167210589101 0
		 0.66946651615947839 0.9817656099148151 0.013239525437220859 1;
createNode joint -n "r_pinkyd_bind" -p "r_pinkyc_bind";
	rename -uid "70C7528D-B340-F1F9-7DC0-1BA8F24EA8A9";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".oc" 7;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -2.8983214846383341 0.021285978708024622 -0.0063758367455477583 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".jo" -type "double3" -0.65860514601984554 -1.4505229894275025 1.2072949640300275 ;
	setAttr ".bps" -type "matrix" 0.12600627886724242 0.024929795599760017 -0.99171615040664995 0
		 0.99155755436884785 0.027665706141153795 0.12668158934028564 0 0.030594673721092647 -0.99930631639906375 -0.021233274472731871 0
		 0.67299661479279138 0.95832491703372613 0.014634441866990037 1;
createNode joint -n "r_pinkye_bind_end" -p "r_pinkyd_bind";
	rename -uid "5B669166-5548-239D-70AE-64937BF5046A";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".ove" yes;
	setAttr ".ovc" 23;
	setAttr ".t" -type "double3" -2.0394477782060143 -4.0526946518681939e-06 7.3543967289424472e-06 ;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 0.94740634517070332 -0.02092298289026728 0.31934847098000019 0
		 0.011303433397696931 0.99942566627116614 0.031946361167740835 0 -0.31983347154998343 -0.02665645110305399 0.94709871929534162 0
		 0.67354220667513531 0.94050438332996544 0.014255790919654858 1;
createNode transform -n "persp1";
	rename -uid "CA2AAD83-4A4B-6E87-ADDF-8BBF2E86C195";
	setAttr ".t" -type "double3" 161.37510652376284 24.244618630322535 -18.749341598783516 ;
	setAttr ".r" -type "double3" 1.4616472707441415 94.199999999997232 0 ;
	setAttr ".rp" -type "double3" 5.5511151231257827e-17 1.1102230246251565e-16 2.2204460492503131e-16 ;
	setAttr ".rpt" -type "double3" 7.9172661478972685e-17 6.2372232607435172e-17 -9.3569502538918145e-17 ;
createNode camera -n "persp1Shape" -p "persp1";
	rename -uid "A73B6D5F-584D-A125-EDFC-588719333678";
	setAttr -k off ".v";
	setAttr ".fl" 34.999999999999986;
	setAttr ".coi" 171.49089124487332;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" -0.00011183220534860538 117.88998774595345 -5.3508886559819047 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "6DAB3094-804D-887D-5A10-AEA40CBD5622";
	setAttr -s 4 ".lnk";
	setAttr -s 4 ".slnk";
createNode displayLayerManager -n "layerManager";
	rename -uid "399464D6-4B4C-EF9B-FDEA-1EBFEC0239A6";
createNode displayLayer -n "defaultLayer";
	rename -uid "D8BF43AA-C640-38A3-C754-3D9A449714AD";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "83D51AAD-D54D-D98C-EAFF-E1BFF6E1CD39";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "8575366D-4E40-8B33-2914-4AB1643D7FAB";
	setAttr ".g" yes;
createNode displayLayer -n "nd_body_test_nd_body_test_defaultLayer";
	rename -uid "A8CE5079-B043-1243-D473-77BB09C751DA";
createNode renderLayer -n "nd_body_test_nd_body_test_defaultRenderLayer";
	rename -uid "89EBE2E3-B542-A921-2EB6-C4A617882DBB";
	setAttr ".g" yes;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "5B18AF9C-D94A-2FB1-A748-AEAEB968DCD9";
	setAttr ".b" -type "string" "playbackOptions -min 1.25 -max 30 -ast 1.25 -aet 60 ";
	setAttr ".st" 6;
createNode mentalrayItemsList -s -n "mentalrayItemsList";
	rename -uid "06466A27-D541-E3A6-D4C6-6D95FC1336BC";
createNode mentalrayGlobals -s -n "mentalrayGlobals";
	rename -uid "5983F049-394B-6365-BAF3-E9B622407A2B";
	setAttr ".xsv" 0;
	setAttr ".outp" -type "string" "y:/big";
createNode mentalrayOptions -s -n "miDefaultOptions";
	rename -uid "99EC9706-394D-0DE9-A629-D280D46423DD";
	setAttr ".splck" 1;
	setAttr ".fil" 0;
	setAttr ".filw" 1;
	setAttr ".filh" 1;
	setAttr ".rflr" 1;
	setAttr ".rfrr" 1;
	setAttr ".maxr" 2;
	setAttr ".shrd" 2;
createNode mentalrayFramebuffer -s -n "miDefaultFramebuffer";
	rename -uid "909025B5-7A48-3168-3293-0BB8965E8486";
	setAttr ".dat" 2;
createNode cameraView -n "cameraView1";
	rename -uid "077A35BF-C747-BDB7-4671-61B59B5584BE";
	setAttr ".e" -type "double3" -0.0070842251398074221 1.7802432970089819 0.7229489438017751 ;
	setAttr ".coi" -type "double3" -1.8000602722165367e-05 1.7337871193885803 0.048198871314525604 ;
	setAttr ".u" -type "double3" 0.00071923466868826038 0.99763852713099122 -0.068679341037884603 ;
	setAttr ".tp" -type "double3" -1.8000602722167969e-05 1.7337871193885803 0.048198871314525604 ;
	setAttr ".fl" 49.999999999999993;
createNode cameraView -n "hair_only_cameraView1";
	rename -uid "BD9E2B12-D741-8A27-3337-8482A2B3CE43";
	setAttr ".e" -type "double3" -0.0070842251398074221 1.7802432970089819 0.7229489438017751 ;
	setAttr ".coi" -type "double3" -1.8000602722165367e-05 1.7337871193885803 0.048198871314525604 ;
	setAttr ".u" -type "double3" 0.00071923466868826038 0.99763852713099122 -0.068679341037884603 ;
	setAttr ".tp" -type "double3" -1.8000602722167969e-05 1.7337871193885803 0.048198871314525604 ;
	setAttr ".fl" 49.999999999999993;
createNode cameraView -n "temp_cameraView1";
	rename -uid "CB9D32DE-524B-35F6-277D-E69EB6602565";
	setAttr ".e" -type "double3" -0.0070842251398074221 1.7802432970089819 0.7229489438017751 ;
	setAttr ".coi" -type "double3" -1.8000602722165367e-05 1.7337871193885803 0.048198871314525604 ;
	setAttr ".u" -type "double3" 0.00071923466868826038 0.99763852713099122 -0.068679341037884603 ;
	setAttr ".tp" -type "double3" -1.8000602722167969e-05 1.7337871193885803 0.048198871314525604 ;
	setAttr ".fl" 49.999999999999993;
createNode cameraView -n "temp_hair_only_cameraView1";
	rename -uid "331FEB85-7040-A9A9-41C3-21B106207895";
	setAttr ".e" -type "double3" -0.0070842251398074221 1.7802432970089819 0.7229489438017751 ;
	setAttr ".coi" -type "double3" -1.8000602722165367e-05 1.7337871193885803 0.048198871314525604 ;
	setAttr ".u" -type "double3" 0.00071923466868826038 0.99763852713099122 -0.068679341037884603 ;
	setAttr ".tp" -type "double3" -1.8000602722167969e-05 1.7337871193885803 0.048198871314525604 ;
	setAttr ".fl" 49.999999999999993;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "CA17CD42-B044-C31B-65A7-5AA95BF5D16D";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n"
		+ "            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n"
		+ "            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n"
		+ "            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"wireframe\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n"
		+ "            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n"
		+ "            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n"
		+ "            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 1\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 1\n            -backfaceCulling 0\n"
		+ "            -xray 0\n            -jointXray 1\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"base_OpenGL_Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n"
		+ "            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n"
		+ "            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 489\n            -height 698\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -docTag \"isolOutln_fromSeln\" \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n"
		+ "            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n"
		+ "            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n"
		+ "                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n"
		+ "                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1.25\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n"
		+ "                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n"
		+ "                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n"
		+ "                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n"
		+ "                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n"
		+ "                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n"
		+ "                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 1 1 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n"
		+ "                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -highlightConnections 0\n                -copyConnectionsOnPaste 0\n                -connectionStyle \"bezier\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -keyReleaseCommand \"nodeEdKeyReleaseCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n"
		+ "                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"blendShapePanel\" (localizedPanelLabel(\"Blend Shape\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tblendShapePanel -edit -l (localizedPanelLabel(\"Blend Shape\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n"
		+ "            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"vacantCell.xP:/\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"vertical2\\\" -ps 1 39 100 -ps 2 61 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Outliner\")) \n\t\t\t\t\t\"outlinerPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showAssignedMaterials 0\\n    -showTimeEditor 1\\n    -showReferenceNodes 1\\n    -showReferenceMembers 1\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -organizeByClip 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showParentContainers 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -isSet 0\\n    -isSetMember 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    -ignoreOutlinerColor 0\\n    -renderFilterVisible 0\\n    -renderFilterIndex 0\\n    -selectionOrder \\\"chronological\\\" \\n    -expandAttribute 0\\n    $editorName\"\n"
		+ "\t\t\t\t\t\"outlinerPanel -edit -l (localizedPanelLabel(\\\"Outliner\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\noutlinerEditor -e \\n    -docTag \\\"isolOutln_fromSeln\\\" \\n    -showShapes 0\\n    -showAssignedMaterials 0\\n    -showTimeEditor 1\\n    -showReferenceNodes 1\\n    -showReferenceMembers 1\\n    -showAttributes 0\\n    -showConnected 0\\n    -showAnimCurvesOnly 0\\n    -showMuteInfo 0\\n    -organizeByLayer 1\\n    -organizeByClip 1\\n    -showAnimLayerWeight 1\\n    -autoExpandLayers 1\\n    -autoExpand 0\\n    -showDagOnly 1\\n    -showAssets 1\\n    -showContainedOnly 1\\n    -showPublishedAsConnected 0\\n    -showParentContainers 0\\n    -showContainerContents 1\\n    -ignoreDagHierarchy 0\\n    -expandConnections 0\\n    -showUpstreamCurves 1\\n    -showUnitlessCurves 1\\n    -showCompounds 1\\n    -showLeafs 1\\n    -showNumericAttrsOnly 0\\n    -highlightActive 1\\n    -autoSelectNewObjects 0\\n    -doNotSelectNewObjects 0\\n    -dropIsParent 1\\n    -transmitFilters 0\\n    -setFilter \\\"defaultSetFilter\\\" \\n    -showSetMembers 1\\n    -allowMultiSelection 1\\n    -alwaysToggleSelect 0\\n    -directSelect 0\\n    -isSet 0\\n    -isSetMember 0\\n    -displayMode \\\"DAG\\\" \\n    -expandObjects 0\\n    -setsIgnoreFilters 1\\n    -containersIgnoreFilters 0\\n    -editAttrName 0\\n    -showAttrValues 0\\n    -highlightSecondary 0\\n    -showUVAttrsOnly 0\\n    -showTextureNodesOnly 0\\n    -attrAlphaOrder \\\"default\\\" \\n    -animLayerFilterOptions \\\"allAffecting\\\" \\n    -sortOrder \\\"none\\\" \\n    -longNames 0\\n    -niceNames 1\\n    -showNamespace 1\\n    -showPinIcons 0\\n    -mapMotionTrails 0\\n    -ignoreHiddenAttribute 0\\n    -ignoreOutlinerColor 0\\n    -renderFilterVisible 0\\n    -renderFilterIndex 0\\n    -selectionOrder \\\"chronological\\\" \\n    -expandAttribute 0\\n    $editorName\"\n"
		+ "\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 489\\n    -height 698\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 1\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 1\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 1\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"base_OpenGL_Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 489\\n    -height 698\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode dagPose -n "bindPose1";
	rename -uid "129DB146-4846-4A9D-BA02-AD8E45147B5C";
	setAttr -s 3 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[22]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 52 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 1.0670999999999999 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -0.70710678118654746 0 0 0.70710678118654757 1
		 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 -1.2856667564442229e-21
		 9.3248965691950404e-20 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[4]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 -9.0184600000000003e-17
		 0.015725300000000001 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.0066920074473978538 0 0 0.99997760826746718 1
		 1 1 yes;
	setAttr ".xm[5]" -type "matrix" "xform" 1 1 1 0 0 0 0 -1.4044399999999999e-17
		 1.73472e-17 0.076588600000000007 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -0.15180031728492249 0 0 0.98841118147873908 1
		 1 1 yes;
	setAttr ".xm[6]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.8443300000000002e-16
		 -1.6653300000000002e-16 0.0978884 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.091288077567715786 0 0 0.99582452615608474 1
		 1 1 yes;
	setAttr ".xm[7]" -type "matrix" "xform" 1 1 1 0 0 0 0 2.6802930740307193e-10
		 -1.1114800209596917e-16 0.19187057546029954 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0.20777910382579295 0 0 0.97817577357719832 1 1 1 yes;
	setAttr ".xm[8]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.031283762229313609 -0.079377047130045453
		 0.11894316172775761 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.34091736673640705 0.74597056194926936 0.43124944881305421 0.37593507772093099 1
		 1 1 yes;
	setAttr ".xm[9]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.031283800341482995
		 -0.079376054972936594 0.11894629442396505 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		-0.37593507737322351 0.43124944887048416 -0.74597056217115676 0.34091736656166471 1
		 1 1 yes;
	setAttr ".xm[10]" -type "matrix" "xform" 1 1 1 -3.1166791369166833e-11 4.699118871849534e-11
		 3.2946867455741402e-11 0 0.046918152704524888 0.027942588338116438 0.17839073928470517 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -0.36537822278235277 -0.62544219553799651 0.37923293797452418 -0.57576313976515592 1
		 1 1 yes;
	setAttr ".xm[11]" -type "matrix" "xform" 1 1 1 -1.7176617441666211e-06 3.805430998564967e-07
		 -3.8478640221369934e-07 0 -0.046918291782027388 -0.027938059129924937 -0.17839147923572307 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -0.36537822278235388 -0.62544219553799563 0.37923293797452545 -0.57576313976515536 1
		 1 1 yes;
	setAttr ".xm[12]" -type "matrix" "xform" 1 1 1 -2.8320778849856653e-06 9.3543511525781733e-07
		 4.9413966150746698e-16 0 -0.050393900268029479 -0.146185386659792 0.022609385863977535 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.274454871398218 -0.64386156980185938 -0.57022059311025897 0.43007589759373616 1
		 1 1 yes;
	setAttr ".xm[13]" -type "matrix" "xform" 1 1 1 8.4859601023060068e-06 -6.3170975984272655e-06
		 -1.7899027676431618e-05 0 0.050396270949685906 -0.14618553704805434 0.022608969102747511 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.26523117185888778 0.64771389078140018 0.56402193008718693 0.43817622430239855 1
		 1 1 yes;
	setAttr ".xm[14]" -type "matrix" "xform" 1 1 1 -3.4432567907605089e-11 -2.6489338501016825e-11
		 -3.1860403204119457e-11 0 0.033374562619999999 -0.070094302760000005 0.18784397359999999 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.047951644899970877 -0.69556619291680843 0.71320273221822084 0.072319940397298277 1
		 1 1 yes;
	setAttr ".xm[15]" -type "matrix" "xform" 1 1 1 -3.7300640743654134e-06 -1.1985027018596739e-06
		 -3.4514222914693911e-06 0 -0.033374425479999997 0.070099510530000006 -0.1878454037 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.047951644604104789 -0.69556619287143095 0.7132027323152208 0.072319940073318906 1
		 1 1 yes;
	setAttr ".xm[16]" -type "matrix" "xform" 1 1 1 0 0 0 1 9.0268400000000006e-08
		 4.3380699999999996e-06 -0.19416600000000006 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0.28109204338781735 -0.19102691148413745 0.10550138305014828 0.93454022942161186 1
		 1 1 yes;
	setAttr ".xm[17]" -type "matrix" "xform" 1.0000642066141974 1.0000642066141974 1.0000642066141974 0
		 0 0 1 -1.0408300000000003e-17 -2.3592199999999998e-16 0.19416500000000003 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.28109204338781735 -0.1910269114841367 0.10550138305014824 0.93454022942161197 1
		 1 1 yes;
	setAttr ".xm[18]" -type "matrix" "xform" 1 1 1 0.014082125794104502 0.014195839750861016
		 -0.0026970244876391696 0 -0.044633827435058553 -0.011526771602088082 0.16695481939909226 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.12337591247135599 -0.071046094715327524 0.024849614165741961 0.98950155801968032 1
		 1 1 yes;
	setAttr ".xm[19]" -type "matrix" "xform" 1 1 1 0.014078168900509691 0.014208422003437075
		 -0.0026982144406563504 0 0.044631589410936687 0.011527807946468491 -0.16695256543080411 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.12337591235834111 -0.071046095141585081 0.024849614261354326 0.98950155800076511 1
		 1 1 yes;
	setAttr ".xm[20]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 -1.2856667564442229e-21
		 9.3248965691950404e-20 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[21]" -type "matrix" "xform" 1 1 1 0 0 0 0 1.2621907363761846e-18
		 0.00041995600714367533 -0.01046686132740704 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 1 0 6.123233995736766e-17 1 1 1 yes;
	setAttr ".xm[22]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[23]" -type "matrix" "xform" 1 1 1 -0.067626998666421231 1.6654352461547828
		 -0.79452742100997842 1 0.19727811122323907 1.4920282410342087 -0.028038243573389503 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[24]" -type "matrix" "xform" 1.0000000000000002 1 1 0 0 0 0 0.029103641506315385
		 -0.014179519352711334 0.24035485022757261 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		-0.26507190530411162 -0.67296134652869188 0.28324303251975946 0.6297882942908265 1
		 1 1 yes;
	setAttr ".xm[25]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.047953522926840089
		 -0.0086086821038912353 0.16931202735182604 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		-0.26507190530411162 -0.67296134652869188 0.28324303251975946 0.6297882942908265 1
		 1 1 yes;
	setAttr ".xm[26]" -type "matrix" "xform" 1 1 1 -0.067627034330979371 1.6654351845196522
		 -0.79452767766191312 1 -0.19727824751877723 1.492027075639452 -0.028038184351612792 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 6.123233995736766e-17 1 1 1 yes;
	setAttr ".xm[27]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.047953528312913801
		 0.0086066679675474711 -0.1693099662995578 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		-0.2650719052215218 -0.67296134678673059 0.28324303267316431 0.629788293980867 1 1
		 1 yes;
	setAttr ".xm[28]" -type "matrix" "xform" 1 1 1 0 0 0 1 3.4694469519536142e-18
		 1.1102230246251565e-16 2.2204460492503131e-16 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		-0.00097940291257260091 -0.00073778695254882393 7.2259403562923223e-07 0.99999924821963015 1
		 1 1 yes;
	setAttr ".xm[29]" -type "matrix" "xform" 1 1 1 6.5960612056776075e-07 -4.2298343497736697e-07
		 0 1 -6.9388939039072284e-18 1.1102230246251565e-15 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[30]" -type "matrix" "xform" 1 1 1 -5.5511151231257827e-17 -2.7755575615628914e-17
		 -3.4694469519536142e-18 0 -0.0291037242535949 0.014177388934263846 -0.24035278982047625 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -0.26507006922228493 -0.67296205531289854 0.28324482180296806 0.62978750498349623 1
		 1 1 yes;
	setAttr ".xm[31]" -type "matrix" "xform" 1 1 1 0.069497307580832099 0.078775153259785277
		 0 1 -1.0243680903521124e-12 1.7176825319875633e-06 -0.17900000000000002 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -0.0005085056858279524 -0.023164840379795257 0.023673642535517587 0.99945119452689968 1
		 1 1 yes;
	setAttr ".xm[32]" -type "matrix" "xform" 1 1 1 0 0 0 1 0.00026412734549504518
		 -0.00035062611843031388 0.17899946172564435 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0.021723070002260727 0.99976402627303851 1 1 1 yes;
	setAttr ".xm[33]" -type "matrix" "xform" 1 1 1 0 0 0 0 -5.5511199999999995e-17
		 2.2204499999999999e-16 0.31253000000000003 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0.0020078445436703622 -0.13885267836541637 0.033547229960529362 0.98974263605899793 0.9999357975080273
		 0.9999357975080273 0.9999357975080273 yes;
	setAttr ".xm[34]" -type "matrix" "xform" 1 1 1 0 0 -5.35311471636391e-06 1 -2.6350102655392504e-13
		 -1.2927214854130398e-11 0.10995577280353735 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0.10558603195018007 0.99441017183907343 1 1 1 yes;
	setAttr ".xm[35]" -type "matrix" "xform" 1 1 1 0 0 0 1 7.2389099999999998e-09
		 -9.1625000000000002e-08 -0.31252900000000006 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0.0020078430219524026 -0.1388526783874213 0.033547219113896326 0.9897426364266434 1
		 1 1 yes;
	setAttr ".xm[36]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.053815422639999999
		 -0.038630019039999998 0.22423696979999999 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		-0.053803742217052239 -0.85679944368304228 0.091344551318363526 0.50463456438527576 1
		 1 1 yes;
	setAttr ".xm[37]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.053815654560000002
		 0.038629845859999998 -0.22423660400000001 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		-0.053806016424220005 -0.8567999455834846 0.091345031143184596 0.50463338289311088 1
		 1 1 yes;
	setAttr ".xm[38]" -type "matrix" "xform" 1 1 1 0 0 0 1 -0.0881919325782963 -0.0028278348570228854
		 0.040579232713250382 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0.06357755452970916 0 0 0.99797690081485446 1
		 1 1 yes;
	setAttr ".xm[39]" -type "matrix" "xform" 1 1 1 0 0 0 1 0.088191900000000004
		 -0.0028278300000000693 0.040576020419267556 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		-0.99797690081485446 0 0 0.063577554529708508 1 1 1 yes;
	setAttr ".xm[40]" -type "matrix" "xform" 1 1 1 0 0 0 1 2.6790219219746807e-11
		 -5.5511151231257827e-17 0.12846743926600612 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		-0.1544000019242884 0 0 0.98800842071602801 1 1 1 yes;
	setAttr ".xm[41]" -type "matrix" "xform" 1 1 1 5.5511151207780001e-17 3.8857805861545085e-16
		 -1.2083972711351976e-10 1 0.41527766213155903 1.2685231911408521 -0.042503116224132657 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[42]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.0084852082550131869
		 -0.031308820962200973 -0.029257552536136763 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 yes;
	setAttr ".xm[43]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.01019450082980794
		 -0.0092521482316045844 -0.024558672656184055 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 yes;
	setAttr ".xm[44]" -type "matrix" "xform" 1 1 1 1.2246467991473515e-16 1.9428902930940239e-16
		 -1.6653345369377348e-15 1 -0.41526317062079332 1.268540036220787 -0.042502073950183204 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0 0 6.123233995736766e-17 1 1 1 yes;
	setAttr ".xm[45]" -type "matrix" "xform" 1.0000000000000002 1 1 0 0 0 0 0.011597164377722173
		 0.010210127290199995 -0.040420094100667894 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 yes;
	setAttr ".xm[46]" -type "matrix" "xform" 1 1 1 0 0 0 0 -0.0084852082550131869
		 0.031308820962200973 0.029257552536136763 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 yes;
	setAttr ".xm[47]" -type "matrix" "xform" 1 1 1 0 0 0 0 0.01019450082980794 0.0092521482316045844
		 0.024558672656184055 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[48]" -type "matrix" "xform" 1 1 1 1.1102230246251565e-16 5.5511151231257827e-17
		 1.1102230246251565e-16 0 0.13220016857787317 0.032003540545702203 0.13966301083564825 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -0.23755636933017285 0.54372258290485442 -0.79548727096746885 -0.12301514524101992 1
		 1 1 yes;
	setAttr ".xm[49]" -type "matrix" "xform" 1 1 1 -1.3877787807814469e-17 1.6653345369377348e-16
		 -1.6653345369377348e-16 0 -0.13121700026802938 0.032004131449981377 0.13966487716552578 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 -0.79548867125949285 -0.12300622006847164 -0.23754976775465969 0.54372543766314674 1
		 1 1 yes;
	setAttr ".xm[50]" -type "matrix" "xform" 1 1 1 0 0 -4.2349437369046898e-06 1 -4.9640348033508364e-08
		 -1.5342766444548239e-06 -0.10995538611181355 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0.10558604192261636 0.99441017078020455 1 1 1 yes;
	setAttr ".xm[51]" -type "matrix" "xform" 1.0000000000000002 1 1 0 0 0 0 -0.011597164377722173
		 -0.010210127290199995 0.040420094100667894 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 
		0 0 0 1 1 1 1 yes;
	setAttr -s 52 ".g[0:51]" yes yes yes yes no no no no no no no no no 
		no no no no no no no yes no yes yes no no yes no no no no no no no no no no no no 
		no no yes no no yes no no no no no no no;
	setAttr ".bp" yes;
createNode lambert -n "lambert2";
	rename -uid "7902EEF6-0646-0C28-1EE4-A1A1629F37D8";
createNode shadingEngine -n "PROXYSG";
	rename -uid "2506FC14-3144-3057-95CC-B187A1636D81";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo1";
	rename -uid "2624B843-BE40-7C90-F079-D3942C756542";
createNode shadingEngine -n "PROXYSG1";
	rename -uid "EB1761DE-9D40-6297-BB12-B8B483CC4404";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo2";
	rename -uid "69A8E5EC-4340-C232-B6E2-FB9C5297BF44";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "B511BE51-6B42-2555-7E1A-DC976EE1E33C";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "C36A1BE9-264E-846C-C0F6-78894679CE3A";
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".o" 8;
	setAttr ".unw" 8;
select -ne :hardwareRenderingGlobals;
	setAttr ".vac" 2;
	setAttr ".etmr" no;
	setAttr ".tmr" 4096;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 4 ".st";
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
	setAttr -s 5 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -s 2 ".r";
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
	setAttr ".ep" 1;
select -ne :defaultResolution;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr -av ".w" 640;
	setAttr -av ".h" 480;
	setAttr -k on ".al";
	setAttr -av ".dar" 1.3333332538604736;
	setAttr -k on ".ldar";
	setAttr -k on ".off";
	setAttr -k on ".fld";
	setAttr -k on ".zsl";
select -ne :defaultLightSet;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr ".ro" yes;
select -ne :defaultObjectSet;
	setAttr ".ro" yes;
select -ne :defaultColorMgtGlobals;
	setAttr ".cme" no;
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
connectAttr "cameraView1.msg" ":perspShape.b" -na;
connectAttr "hair_only_cameraView1.msg" ":perspShape.b" -na;
connectAttr "temp_cameraView1.msg" ":perspShape.b" -na;
connectAttr "temp_hair_only_cameraView1.msg" ":perspShape.b" -na;
connectAttr "root_bind.s" "lower_base.is";
connectAttr "root_bind.s" "upper_base.is";
connectAttr "root_bind.s" "pelvis_bind.is";
connectAttr "pelvis_bind.s" "pelvis_bind_end.is";
connectAttr "pelvis_bind_end.s" "l_leg_bind.is";
connectAttr "l_leg_bind.s" "l_knee_bind.is";
connectAttr "l_knee_bind.s" "l_ankle_bind.is";
connectAttr "l_ankle_bind.s" "l_toe_bind.is";
connectAttr "l_toe_bind.s" "l_toe_bind_end.is";
connectAttr "l_ankle_bind.s" "l_toeTipFront_bind.is";
connectAttr "l_ankle_bind.s" "l_toeTipLeft_bind.is";
connectAttr "l_ankle_bind.s" "l_toeTipRight_bind.is";
connectAttr "l_ankle_bind.s" "l_toeTipBack_bind.is";
connectAttr "l_ankle_bind.s" "l_ikOrientationFoot_bind.is";
connectAttr "pelvis_bind_end.s" "r_leg_bind.is";
connectAttr "r_leg_bind.s" "r_knee_bind.is";
connectAttr "r_knee_bind.s" "r_ankle_bind.is";
connectAttr "r_ankle_bind.s" "r_toe_bind.is";
connectAttr "r_toe_bind.s" "r_toe_bind_end.is";
connectAttr "r_ankle_bind.s" "r_toeTipFront_bind.is";
connectAttr "r_ankle_bind.s" "r_toeTipLeft_bind.is";
connectAttr "r_ankle_bind.s" "r_toeTipRight_bind.is";
connectAttr "r_ankle_bind.s" "r_toeTipBack_bind.is";
connectAttr "r_ankle_bind.s" "r_ikOrientationFoot_bind.is";
connectAttr "root_bind.s" "spinea_bind.is";
connectAttr "spinea_bind.s" "spineb_bind.is";
connectAttr "spineb_bind.s" "spinec_bind.is";
connectAttr "spinec_bind.s" "spined_bind.is";
connectAttr "spined_bind.s" "spinef_bind.is";
connectAttr "spinef_bind.s" "l_scapula_bind.is";
connectAttr "l_scapula_bind.s" "l_scapula1_bind.is";
connectAttr "spinef_bind.s" "l_pec_bind.is";
connectAttr "l_pec_bind.s" "l_pec1_bind.is";
connectAttr "spinef_bind.s" "r_scapula_bind.is";
connectAttr "r_scapula_bind.s" "r_scapula1_bind.is";
connectAttr "spinef_bind.s" "r_pec_bind.is";
connectAttr "r_pec_bind.s" "r_pec1_bind.is";
connectAttr "spinef_bind.s" "l_clav_bind.is";
connectAttr "l_clav_bind.s" "l_clav1_bind.is";
connectAttr "spinef_bind.s" "r_clav_bind.is";
connectAttr "r_clav_bind.s" "r_clav1_bind.is";
connectAttr "spinef_bind.s" "l_clavicle_bind.is";
connectAttr "l_clavicle_bind.s" "l_shoulder_bind.is";
connectAttr "l_shoulder_bind.s" "l_elbow_bind.is";
connectAttr "l_elbow_bind.s" "l_wrist_bind.is";
connectAttr "l_wrist_bind.s" "l_palm_bind.is";
connectAttr "l_palm_bind.s" "l_thumba_bind.is";
connectAttr "l_thumba_bind.s" "l_thumbb_bind.is";
connectAttr "l_thumbb_bind.s" "l_thumbc_bind.is";
connectAttr "l_thumbc_bind.s" "l_thumbd_bind_end.is";
connectAttr "l_palm_bind.s" "l_indexa_bind.is";
connectAttr "l_indexa_bind.s" "l_indexb_bind.is";
connectAttr "l_indexb_bind.s" "l_indexc_bind.is";
connectAttr "l_indexc_bind.s" "l_indexd_bind_end.is";
connectAttr "l_palm_bind.s" "l_middlea_bind.is";
connectAttr "l_middlea_bind.s" "l_middleb_bind.is";
connectAttr "l_middleb_bind.s" "l_middlec_bind.is";
connectAttr "l_middlec_bind.s" "l_middled_bind_end.is";
connectAttr "l_palm_bind.s" "l_ringa_bind.is";
connectAttr "l_ringa_bind.s" "l_ringb_bind.is";
connectAttr "l_ringb_bind.s" "l_ringc_bind.is";
connectAttr "l_ringc_bind.s" "l_ringd_bind_end.is";
connectAttr "l_palm_bind.s" "l_pinkya_bind.is";
connectAttr "l_pinkya_bind.s" "l_pinkyb_bind.is";
connectAttr "l_pinkyb_bind.s" "l_pinkyc_bind.is";
connectAttr "l_pinkyc_bind.s" "l_pinkyd_bind.is";
connectAttr "l_pinkyd_bind.s" "l_pinkye_bind_end.is";
connectAttr "spinef_bind.s" "neck_bind.is";
connectAttr "neck_bind.s" "head_bind.is";
connectAttr "neck_bind.s" "l_neckClav_bind.is";
connectAttr "l_neckClav_bind.s" "l_neckClav1_bind.is";
connectAttr "neck_bind.s" "r_neckClav_bind.is";
connectAttr "r_neckClav_bind.s" "r_neckClav1_bind.is";
connectAttr "spinef_bind.s" "r_clavicle_bind.is";
connectAttr "r_clavicle_bind.s" "r_shoulder_bind.is";
connectAttr "r_shoulder_bind.s" "r_elbow_bind.is";
connectAttr "r_elbow_bind.s" "r_wrist_bind.is";
connectAttr "r_wrist_bind.s" "r_palm_bind.is";
connectAttr "r_palm_bind.s" "r_thumba_bind.is";
connectAttr "r_thumba_bind.s" "r_thumbb_bind.is";
connectAttr "r_thumbb_bind.s" "r_thumbc_bind.is";
connectAttr "r_thumbc_bind.s" "r_thumbd_bind_end.is";
connectAttr "r_palm_bind.s" "r_indexa_bind.is";
connectAttr "r_indexa_bind.s" "r_indexb_bind.is";
connectAttr "r_indexb_bind.s" "r_indexc_bind.is";
connectAttr "r_indexc_bind.s" "r_indexd_bind_end.is";
connectAttr "r_palm_bind.s" "r_middlea_bind.is";
connectAttr "r_middlea_bind.s" "r_middleb_bind.is";
connectAttr "r_middleb_bind.s" "r_middlec_bind.is";
connectAttr "r_middlec_bind.s" "r_middled_bind_end.is";
connectAttr "r_palm_bind.s" "r_ringa_bind.is";
connectAttr "r_ringa_bind.s" "r_ringb_bind.is";
connectAttr "r_ringb_bind.s" "r_ringc_bind.is";
connectAttr "r_ringc_bind.s" "r_ringd_bind_end.is";
connectAttr "r_palm_bind.s" "r_pinkya_bind.is";
connectAttr "r_pinkya_bind.s" "r_pinkyb_bind.is";
connectAttr "r_pinkyb_bind.s" "r_pinkyc_bind.is";
connectAttr "r_pinkyc_bind.s" "r_pinkyd_bind.is";
connectAttr "r_pinkyd_bind.s" "r_pinkye_bind_end.is";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "PROXYSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "PROXYSG1.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "PROXYSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "PROXYSG1.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "lambert2.oc" "PROXYSG.ss";
connectAttr "PROXYSG.msg" "materialInfo1.sg";
connectAttr "lambert2.msg" "materialInfo1.m";
connectAttr "lambert2.oc" "PROXYSG1.ss";
connectAttr "PROXYSG1.msg" "materialInfo2.sg";
connectAttr "lambert2.msg" "materialInfo2.m";
connectAttr "PROXYSG.pa" ":renderPartition.st" -na;
connectAttr "PROXYSG1.pa" ":renderPartition.st" -na;
connectAttr "lambert2.msg" ":defaultShaderList1.s" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "nd_body_test_nd_body_test_defaultRenderLayer.msg" ":defaultRenderingList1.r"
		 -na;
// End of bodyJnts.ma
