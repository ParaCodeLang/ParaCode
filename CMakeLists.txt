cmake_minimum_required(VERSION 3.16)

project(ParaCode)

set(GCC_COVERAGE_COMPILE_FLAGS "-fcompare-debug-second -Werror")
set(GCC_COVERAGE_LINK_FLAGS    "-lboost_system -lreadline")
set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}")
set(CMAKE_EXE_LINKER_FLAGS  "${CMAKE_EXE_LINKER_FLAGS} ${GCC_COVERAGE_LINK_FLAGS}")

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(ExternalProject)
include("${CMAKE_SOURCE_DIR}/vendor/libcpr.cmake")
include("${CMAKE_SOURCE_DIR}/vendor/rapidjson.cmake")
include("${CMAKE_SOURCE_DIR}/vendor/boost.cmake")

set(HEADER_FILES
	src/pch.h
)

set(SOURCE_FILES
    src/util.cpp
    src/interpreter/basic_value.cpp
    src/interpreter/typing/basic_type.cpp
    src/interpreter/variable.cpp
    src/lexer.cpp
    src/parse/parser.cpp
    src/parse/node.cpp
    src/ParaCode.cpp
	src/main.cpp
	${HEADER_FILES}
)

include_directories(
    ${Boost_INCLUDE_DIRS}
    ${RAPIDJSON_INCLUDE_DIR}
    src
)

set(LIBRARIES
    cpr::cpr
    ${Boost_SYSTEM_LIBRARY}
    ${Boost_FILESYSTEM_LIBRARY}
    ${Boost_REGEX_LIBRARY}
    ${Boost_LIBRARIES}
)

add_executable(ParaCode ${SOURCE_FILES})
target_precompile_headers(ParaCode PRIVATE ${HEADER_FILES})
if(MSVC OR MSYS OR MINGW)
    target_link_libraries(ParaCode PRIVATE ${LIBRARIES})
else()
    target_link_libraries(ParaCode PRIVATE readline ${LIBRARIES})
endif()
add_dependencies(ParaCode rapidjson)
