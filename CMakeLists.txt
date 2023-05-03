cmake_minimum_required(VERSION 3.18 FATAL_ERROR)
project(RootUtil CXX)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

### CAENHVWeapper
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/modules)

find_package(CAENHVWrapper REQUIRED)
add_definitions(-DUNIX)

include_directories(SYSTEM ${PROJECT_SOURCE_DIR} ${CAENHVWRAPPER_INCLUDE_DIR} )

set( caen_hv_reader_SOURCES
  Connection.cpp
  main.cpp
)

add_executable( caen_hv_reader ${caen_hv_reader_SOURCES} )
target_link_libraries(caen_hv_reader ${CAENHVWRAPPER_LIBRARIES})
install( TARGETS caen_hv_reader DESTINATION ${CMAKE_INSTALL_PREFIX}/bin )
