if (NOT DEFINED MAYA_VERSION)
    set(MAYA_VERSION 2018 CACHE STRING "Maya version")
endif()

set(MAYA_INSTALL_BASE_SUFFIX "")
set(MAYA_LIB_SUFFIX "lib")
set(MAYA_INC_SUFFIX "include")
if (WIN32)
    # Windows
    set(MAYA_INSTALL_BASE_DEFAULT "C:Program Files/Autodesk")
    set(OPENMAYA OpenMaya.lib)
elseif(APPLE)
    # Mac
    set(MAYA_INSTALL_BASE_DEFAULT "/Applications/Autodesk")
    set(OPENMAYA libOpenMaya.dylib)
    set(MAYA_LIB_SUFFIX "Maya.app/Contents/MacOS")
    set(MAYA_INC_SUFFIX "devkit/include")
    
else()
    #Linux
    set(MAYA_INSTALL_BASE_DEFAULT "/usr/Autodesk")
    set(MAYA_INSTALL_BASE_SUFFIX -x64)
    set(OPENMAYA libOpenMaya.so)
    
endif

set(MAYA_INSTALL_BASE_PATH ${MAYA_INSTALL_BASE_DEFAULT} CACHE STRING "Root Maya installation path")
set(MAYA_LOCATION ${MAYA_INSTALL_BASE_PATH}/maya${MAYA_VERSION}$MAYA_INSTALL_BASE_SUFFIX)

find_path(MAYA_LIBRARY_DIR ${OPENMAYA}
    PATHS
        ${MAYA_LOCATION}
        $ENV{MAYA_LOCATION}
    PATH_SUFFIXES
        "${MAYA_LIB_SUFFIX}/"
    DOC "Maya library path"
)
find_path(MAYA_INCLUDE_DIR maya/MFn.h
    PATHS
        ${MAYA_LOCATION}
        $ENV{MAYA_LOCATION}
    PATH_SUFFIXES
        "${MAYA_INC_SUFFIX}/"
    DOC "Maya include path"
)
# Absolute Path
set(_MAYA_LIBRARIES OpenMaya OpenMayaAnim OpenMayaFX OpenMayaRender OpenMayaUI Foundation)
foreach(MAYA_LIB ${_MAYA_LIBRARIES})
    find_library(MAYA_${MAYA_LIB}_LIBRARY NAMES ${MAYA_LIB} PATHS ${MAYA_LIBRARY_DIR} NO_DEFAULT_PATH)
    set(MAYA_LIBRARIES ${MAYA_LIBRARIES} ${MAYA_${MAYA_LIB}_LIBRARY})
endforeach()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(Maya DEFAULT_MSG MAYA_INCLUDE_DIR MAYA_LIBRARIES)