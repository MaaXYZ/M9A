include_directories(${CMAKE_SOURCE_DIR}/deps/include)
link_directories(${CMAKE_SOURCE_DIR}/deps/lib)

add_executable(MAA1999_CLI main.cpp)
target_link_libraries(MAA1999_CLI PRIVATE MaaFramework MaaToolkit)

add_dependencies(MAA1999_CLI AssetsAgentBinary AssetsResource)

install(TARGETS MAA1999_CLI RUNTIME DESTINATION share)
install(DIRECTORY "${CMAKE_SOURCE_DIR}/deps/bin/" DESTINATION share)
