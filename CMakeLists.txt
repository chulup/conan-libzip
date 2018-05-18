cmake_minimum_required(VERSION 3.0.2)
project(cmake_wrapper)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
message(STATUS "Conan CMake wrapper")

add_subdirectory("source_subfolder")
