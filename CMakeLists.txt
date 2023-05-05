cmake_minimum_required(VERSION 3.15 FATAL_ERROR)
project(tpot_hv_interface CXX)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

### CAENHVWrapper
list(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake/modules)
find_package(CAENHVWrapper REQUIRED)
add_definitions(-DUNIX)

list( APPEND CMAKE_INSTALL_RPATH ${CAENHVWRAPPER_LIBDIR} )

include_directories(SYSTEM ${PROJECT_SOURCE_DIR} ${CAENHVWRAPPER_INCLUDE_DIR} )

### caen_hv_reader library, for python binding
set( tpot_hv_interface_SOURCES
  Connection.cpp
  CaenInterface.cpp
)

add_library( tpot_hv_interface SHARED ${tpot_hv_interface_SOURCES} )
target_link_libraries(tpot_hv_interface ${CAENHVWRAPPER_LIBRARIES})
install( TARGETS tpot_hv_interface DESTINATION ${CMAKE_INSTALL_PREFIX}/lib )
