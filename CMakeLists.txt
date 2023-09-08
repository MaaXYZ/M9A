cmake_minimum_required(VERSION 3.21)
project(MAA1999)

if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release" CACHE STRING "Choose the type of build." FORCE)
endif ()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake/modules")

set_property(GLOBAL PROPERTY USE_FOLDERS ON)
set(CMAKE_MAP_IMPORTED_CONFIG_DebWithRelDeps "DebWithRelDeps;Release;")
set(Boost_NO_WARN_NEW_VERSIONS 1)

include(${PROJECT_SOURCE_DIR}/cmake/config.cmake) # Basic compile & link configuration
include(${PROJECT_SOURCE_DIR}/cmake/assets.cmake)
include(${PROJECT_SOURCE_DIR}/cmake/utils.cmake)
include(${PROJECT_SOURCE_DIR}/cmake/version.cmake)

# if(USE_MAADEPS)
#     include(${PROJECT_SOURCE_DIR}/MaaDeps/maadeps.cmake)
# endif()
# find_package(OpenCV REQUIRED COMPONENTS core imgproc imgcodecs videoio)
# find_package(Boost REQUIRED COMPONENTS system url)

add_subdirectory(source/cli)
