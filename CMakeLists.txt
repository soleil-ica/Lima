cmake_minimum_required(VERSION 3.15)
project(Lima LANGUAGES C CXX)

option(BUILD_SHARED_LIBS "Build using shared libraries" ON)

# --------------------------------------------------------------------------
# CMake infrastructure
# --------------------------------------------------------------------------
list(PREPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
include(LimaTools)

# --------------------------------------------------------------------------
# Dependencies
# --------------------------------------------------------------------------
add_subdirectory(third-party/Processlib)
find_package(nexuscpp CONFIG REQUIRED)
find_package(HDF5 CONFIG REQUIRED)

# --------------------------------------------------------------------------
# Options
# --------------------------------------------------------------------------

option(WITH_RIXS "Enable RIXS support" OFF)
option(WITH_FITGAUSSIAN "Enable FitGaussian support" OFF)

set(ALL_CAMERAS
    andor
    basler
    dhyana
    eiger
    hamamatsu
    imxpad
    lambda
    marccd
    merlin
    pco
    perkinelmer
    pilatus
    roperscientific
    simulator
    slseiger
    slsjungfrau
    spectralinstrument
    spectrumone
    ufxc
    uview
    xpad
)

foreach(cam ${ALL_CAMERAS})
    string(TOUPPER ${cam} CAM_U)
    option(WITH_${CAM_U} "Enable camera ${cam}" OFF)
endforeach()

set(AVAILABLE_CAMERAS "")
foreach(cam ${ALL_CAMERAS})
    string(TOUPPER ${cam} CAM_U)
    if(WITH_${CAM_U})
        list(APPEND AVAILABLE_CAMERAS ${cam})
    endif()
endforeach()

# --------------------------------------------------------------------------
# Collect sources and includes
# --------------------------------------------------------------------------

file(GLOB_RECURSE sources 
    common/src/*.cpp 
    control/src/*.cpp
    control/software_operation/src/*.cpp
    hardware/src/*.cpp
)

set(includedirs 
    common/include
    control/include
    control/src
    control/software_operation/include
    hardware/include
)

# --------------------------------------------------------------------------
# Filters (deactivate files)
# --------------------------------------------------------------------------
list(FILTER sources EXCLUDE REGEX ".*/control/src/CtSaving_Cbf.cpp$")
list(FILTER sources EXCLUDE REGEX ".*/control/src/CtSaving_Fits.cpp$")
list(FILTER sources EXCLUDE REGEX ".*/control/src/CtSaving_Tiff.cpp$")
list(FILTER sources EXCLUDE REGEX ".*/control/src/CtSaving_Hdf5.cpp$")
list(FILTER sources EXCLUDE REGEX ".*/control/src/CtSpsImage.cpp$")

if (WIN32)
    list(FILTER sources EXCLUDE REGEX ".*/control/src/CtSaving_Hdf5.cpp$")
    list(FILTER sources EXCLUDE REGEX ".*/camera/pilatus/doc/camera_sirius.def$")
    list(FILTER sources EXCLUDE REGEX ".*/camera/pilatus/doc/camera_px1.def$")
    list(FILTER sources EXCLUDE REGEX ".*/common/src/SimplePipe.cpp$")
    list(FILTER sources EXCLUDE REGEX ".*/common/src/RegExUtils.cpp$")
    list(FILTER sources EXCLUDE REGEX ".*/hardware/src/HwFileEventMgr.cpp$")
endif()

# --------------------------------------------------------------------------
# Target
# --------------------------------------------------------------------------

add_library(limacore SHARED ${sources})
target_include_directories(limacore
    PUBLIC ${includedirs}
)
target_link_libraries(limacore
    PUBLIC 
        processlib
    PRIVATE 
        ${nexuscpp_LIBRARIES}
        ${HDF5_LIBRARIES}
        
)

limatools_set_library_soversion(limacore "VERSION")

# --------------------------------------------------------------------------
# Compile definitions
# --------------------------------------------------------------------------

file(READ "${CMAKE_CURRENT_SOURCE_DIR}/VERSION" LIMACORE_VERSION_RAW)
string(STRIP "${LIMACORE_VERSION_RAW}" LIMACORE_VERSION)

target_compile_definitions(limacore
    PUBLIC
        LIMACORE_NAME=LimaCore
        LIMACORE_VERSION=${LIMACORE_VERSION}
        WITH_NXS_SAVING
        WITH_YAT_STREAM
        PUSH_EVENT_PROJ_ENABLED
        PUSH_EVENT_MYPUSHTIME_ENABLED
)

# Windows DLL export
if (WIN32 AND BUILD_SHARED_LIBS)
    target_compile_definitions(limacore
        PRIVATE
            LIMACORE_EXPORTS
        PUBLIC
            LIMA_PROCESSCORE_DLL
    )
endif()

# --------------------------------------------------------------------------
# Install
# --------------------------------------------------------------------------

install(
    TARGETS limacore
    LIBRARY DESTINATION lib
)

# --------------------------------------------------------------------------
# Submodules
# --------------------------------------------------------------------------

set(HAS_ENABLED_CAMERA FALSE)
foreach(cam ${AVAILABLE_CAMERAS})
    string(TOUPPER ${cam} CAM_U)
    if (WITH_${CAM_U})
        set(HAS_ENABLED_CAMERA TRUE)    
        add_subdirectory(camera/${cam})
    endif()
endforeach()

if (HAS_ENABLED_CAMERA)
    message(STATUS "At least one camera enabled → building Tango device")
    add_subdirectory(applications/tango/cpp)
else()
    message(WARNING "No cameras enabled → Tango device will NOT be built")
endif()
