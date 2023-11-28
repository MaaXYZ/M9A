install(DIRECTORY "${CMAKE_SOURCE_DIR}/deps/bin/" DESTINATION .
    PATTERN "*MaaDbgControlUnit*" EXCLUDE
    PATTERN "*MaaThriftControlUnit*" EXCLUDE
    PATTERN "*MaaWin32ControlUnit*" EXCLUDE
    PATTERN "*MaaRpc*" EXCLUDE
)
install(DIRECTORY "${CMAKE_SOURCE_DIR}/deps/share/MaaAgentBinary" DESTINATION .)
