cmake_minimum_required(VERSION 3.18 FATAL_ERROR)
project(RootUtil CXX)

### CAENHVWeapper
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/modules)

find_package(CAENHVWrapper REQUIRED)
add_definitions(-DUNIX)

include_directories(SYSTEM ${PROJECT_SOURCE_DIR} ${CAENHVWRAPPER_INCLUDE_DIR} )

set( caen_reader_SOURCES
  Connection.cpp
  main.cpp
)

add_executable( caen_reader ${caen_reader_SOURCES} )
target_link_libraries(caen_reader ${CAENHVWRAPPER_LIBRARIES})
