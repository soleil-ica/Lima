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
# Camera options
# --------------------------------------------------------------------------

set(AVAILABLE_CAMERAS "")

if (WIN32)
    if(NOT CMAKE_SIZEOF_VOID_P EQUAL 8)
        if (MSVC AND MSVC_VERSION LESS_EQUAL 1900)
            message(STATUS "Cameras for Windows 32 bits for MSVC 14 (Visual Studio 2015)")
            list(APPEND AVAILABLE_CAMERAS
                andor
                perkinelmer
                roperscientific
                uview
            )
        else()
            message(STATUS "Cameras for other compilers for Windows 32 bits")
        endif()
    else()
        if (MSVC AND MSVC_VERSION LESS_EQUAL 1900)
            message(STATUS "Cameras for Windows 64 bits for MSVC 14 (Visual Studio 2015)")
            list(APPEND AVAILABLE_CAMERAS
                dhyana
                hamamatsu
                perkinelmer
                pco
                spectrumone
            )
        else()
            message(STATUS "Cameras for other compilers for Windows 64 bits")
        endif()
    endif()
else()
    if(NOT CMAKE_SIZEOF_VOID_P EQUAL 8)
        message(STATUS "Cameras for Linux 32 bits")
        if(CMAKE_CXX_COMPILER_VERSION STREQUAL "4.4.7")
            message(STATUS "Cameras for CentOS 6 32 bits with GCC 4.4.7")
            list(APPEND AVAILABLE_CAMERAS
                imxpad
                marccd
                merlin
                pilatus
                xpad
            )
        else()
            message(STATUS "Cameras for other compilers for Linux versions 32 bits")
        endif()
    else()
        message(STATUS "Cameras for Linux 64 bits")
        if(CMAKE_CXX_COMPILER_VERSION STREQUAL "4.4.7")
            message(STATUS "Cameras for CentOS 6 64 bits with GCC 4.4.7")
            list(APPEND AVAILABLE_CAMERAS
                eiger
                imxpad
                marccd
                merlin
                slseiger
                slsjungfrau
                spectralinstrument
                ufxc
            )
        elseif(CMAKE_CXX_COMPILER_VERSION STREQUAL "4.8.5")
            message(STATUS "Cameras for CentOS 7 64 bits with GCC 4.8.5")
            list(APPEND AVAILABLE_CAMERAS
                basler
                lambda
            )
        else()
            message(STATUS "Cameras for other compilers for Linux versions 64 bits")
        endif()    
    endif()
endif()

foreach(cam ${AVAILABLE_CAMERAS})
    string(TOUPPER ${cam} CAM_U)
    option(WITH_${CAM_U} "Enable camera ${cam}" ON)
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

add_subdirectory(camera/simulator)

foreach(cam ${AVAILABLE_CAMERAS})
    string(TOUPPER ${cam} CAM_U)
    if (WITH_${CAM_U})
        add_subdirectory(camera/${cam})
    endif()
endforeach()

add_subdirectory(applications/tango/cpp)
