project(cmake_wrapper)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
message("Conan CMake wrapper")

add_subdirectory("source_subfolder")
