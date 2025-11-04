# --------------------------------------------------------------------------
# Collect sources and includes
# --------------------------------------------------------------------------

file(GLOB_RECURSE sources src/*.cpp)
set(includedirs
    include/
)

# --------------------------------------------------------------------------
# Target
# --------------------------------------------------------------------------

add_library(limasimulator ${sources})
target_include_directories(limasimulator
    PUBLIC
        ${includedirs}
)
target_link_libraries(limasimulator
    PUBLIC
        limacore
        yat::yat
)

limatools_set_library_soversion(limasimulator "VERSION")

# --------------------------------------------------------------------------
# Compile definitions
# --------------------------------------------------------------------------

file(READ "${CMAKE_CURRENT_SOURCE_DIR}/VERSION" SIMULATOR_VERSION_RAW)
string(STRIP "${SIMULATOR_VERSION_RAW}" SIMULATOR_VERSION)

target_compile_definitions(limasimulator
    PUBLIC
        SIMULATOR_NAME=Simulator
        SIMULATOR_VERSION=${SIMULATOR_VERSION}
        SIMULATOR_ENABLED
)

message(STATUS "Camera enabled: Simulator ${SIMULATOR_VERSION}")

# Windows DLL export
if (WIN32 AND BUILD_SHARED_LIBS)
    target_compile_definitions(limasimulator
        PRIVATE
            LIBSIMULATOR_EXPORTS
    )
endif()

# --------------------------------------------------------------------------
# Install
# --------------------------------------------------------------------------

install(
    TARGETS limasimulator 
    LIBRARY DESTINATION lib
)
