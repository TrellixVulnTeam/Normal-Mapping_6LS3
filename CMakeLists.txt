# CMake entry point
cmake_minimum_required (VERSION 3.0)
project (NormalMap)
set (CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS ${CMAKE_CSS_FLAGS} "-fPIC")
# set(CMAKE_BUILD_TYPE Release)

#Bring the headers into the project
include_directories(include)

file(GLOB SOURCES "src/*.cpp")

# search for pkg-config
include (FindPkgConfig)
if (NOT PKG_CONFIG_FOUND)
    message (FATAL_ERROR "pkg-config not found")
endif ()

add_executable(main ${SOURCES})
