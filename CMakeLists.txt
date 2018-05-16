project(cmake_wrapper)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
message(STATUS "Conan CMake Wrapper")

add_subdirectory("source_subfolder")
