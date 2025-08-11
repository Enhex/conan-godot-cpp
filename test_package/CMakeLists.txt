cmake_minimum_required(VERSION 3.15)
project(PackageTest CXX)

find_package(godot-cpp CONFIG REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example godot-cpp::godot-cpp)