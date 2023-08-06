
# if CTEST_SITE was not provided
if(NOT DEFINED CTEST_SITE)
    # [A] if CTEST_SITE set at configure
    set(_HOSTNAME "")
    # [B] if CTEST_SITE not set at configure, grab the HOSTNAME
    if("${_HOSTNAME}" STREQUAL "")
        find_program(HOSTNAME_CMD hostname)
        execute_process(COMMAND ${HOSTNAME_CMD}
            OUTPUT_VARIABLE _HOSTNAME
            WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
            OUTPUT_STRIP_TRAILING_WHITESPACE)
    endif("${_HOSTNAME}" STREQUAL "")
    # either [A] or [B]
    set(CTEST_SITE  "${_HOSTNAME}" CACHE STRING "CTest site" FORCE)
    unset(_HOSTNAME)
endif(NOT DEFINED CTEST_SITE)

set(CTEST_PROJECT_NAME          "pyctest")
set(CTEST_NIGHTLY_START_TIME    "01:00:00 PDT")
set(CTEST_DROP_METHOD           "https")
set(CTEST_DROP_SITE             "cdash.nersc.gov")
set(CTEST_DROP_LOCATION         "/submit.php?project=PyCTest")
set(CTEST_DROP_SITE_CDASH       TRUE)
set(CTEST_CDASH_VERSION         "1.6")
set(CTEST_CDASH_QUERY_VERSION   TRUE)
