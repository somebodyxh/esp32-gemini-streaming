# The following five lines of boilerplate have to be in your project's
# CMakeLists in this exact order for cmake to work correctly
cmake_minimum_required(VERSION 3.16)

# 包含 IDF 的核心构建脚本
include($ENV{IDF_PATH}/tools/cmake/project.cmake)

# 定义项目名称
project(project-name)