# - Find CAENHVWrapper
# Find the CAENHVWrapper include directory and library
#
#  CAENHVWRAPPER_INCLUDE_DIR    - where to find <CAENHVWrapper.h>, etc.
#  CAENHVWRAPPER_LIBRARIES      - List of libraries when using libcaenhvwrapper.
#  CAENHVWRAPPER_FOUND          - True if libcaenhvwrapper found.

IF (CAENHVWRAPPER_INCLUDE_DIR)
  # Already in cache, be silent
  SET(CAENHVWRAPPER_FIND_QUIETLY TRUE)
ENDIF (CAENHVWRAPPER_INCLUDE_DIR)

set(_caenhvwrapperdirs
  ${CAENHVWRAPPER_ROOT} 
  $ENV{CAENHVWRAPPER_ROOT}
)

FIND_PATH(CAENHVWRAPPER_INCLUDE_DIR 
  NAMES CAENHVWrapper.h
  HINTS ${_caenhvwrapperdirs}
  PATH_SUFFIXES include
)

FIND_LIBRARY(CAENHVWRAPPER_LIBRARY
  NAMES caenhvwrapper
  HINTS ${_caenhvwrapperdirs}
  PATH_SUFFIXES lib
)

# handle the QUIETLY and REQUIRED arguments and set NETTLE_FOUND to TRUE if 
# all listed variables are TRUE
INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(CAENHVWrapper DEFAULT_MSG CAENHVWRAPPER_LIBRARY CAENHVWRAPPER_INCLUDE_DIR)

IF(CAENHVWRAPPER_FOUND)
  SET(CAENHVWRAPPER_LIBRARIES ${CAENHVWRAPPER_LIBRARY})
ENDIF(CAENHVWRAPPER_FOUND)
