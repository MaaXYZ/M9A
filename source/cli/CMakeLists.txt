include_directories(${CMAKE_SOURCE_DIR}/deps/include)
if (WIN32)
    link_directories(${CMAKE_SOURCE_DIR}/deps/lib)
else ()
    link_directories(${CMAKE_SOURCE_DIR}/deps/bin)
endif ()

add_executable(M9A_CLI main.cpp)
target_link_libraries(M9A_CLI PRIVATE MaaFramework MaaToolKit)

add_dependencies(M9A_CLI AssetsResource)

install(TARGETS M9A_CLI RUNTIME DESTINATION .)
