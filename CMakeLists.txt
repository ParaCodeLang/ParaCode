cmake_minimum_required(VERSION 3.16)

project(ParaCode)

SET(GCC_COVERAGE_COMPILE_FLAGS "-fcompare-debug-second")
# SET(GCC_COVERAGE_LINK_FLAGS    "-lgcov")

SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}")
# SET(CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} ${GCC_COVERAGE_LINK_FLAGS}")

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(HEADER_FILES
	src/pch.h
)

set(SOURCE_FILES
	src/main.cpp
	${HEADER_FILES}
)

include_directories(src)

add_executable(ParaCode ${SOURCE_FILES})
target_precompile_headers(ParaCode PRIVATE ${HEADER_FILES})
