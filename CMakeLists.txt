cmake_minimum_required(VERSION 3.21)
project(MAA1999)

set_property(GLOBAL PROPERTY USE_FOLDERS ON)
set(Boost_NO_WARN_NEW_VERSIONS 1)

include(${PROJECT_SOURCE_DIR}/cmake/config.cmake) # Basic compile & link configuration
include(${PROJECT_SOURCE_DIR}/cmake/assets.cmake)
include(${PROJECT_SOURCE_DIR}/cmake/utils.cmake)
include(${PROJECT_SOURCE_DIR}/cmake/version.cmake)
include(${PROJECT_SOURCE_DIR}/cmake/framework.cmake)

# if(USE_MAADEPS)
#     include(${PROJECT_SOURCE_DIR}/MaaDeps/maadeps.cmake)
# endif()
# find_package(OpenCV REQUIRED COMPONENTS core imgproc imgcodecs videoio)
# find_package(Boost REQUIRED COMPONENTS system url)

add_subdirectory(source/cli)
