
# include guard
if(__cdashinit_is_loaded)
    return()
endif()
set(__cdashinit_is_loaded ON)

include(ProcessorCount)
ProcessorCount(CTEST_PROCESSOR_COUNT)

cmake_policy(SET CMP0009 NEW)
cmake_policy(SET CMP0011 NEW)

# ---------------------------------------------------------------------------- #
# -- Defaults
# ---------------------------------------------------------------------------- #
set(CTEST_GENERATOR_PLATFORM "")
set(CTEST_TRIGGER "Any" CACHE STRING "Delay submit until CTEST_TRIGGER == '(Any|Build|Test|Coverage|MemCheck)'")


# ---------------------------------------------------------------------------- #
# -- Programs
# ---------------------------------------------------------------------------- #
find_program(CTEST_CMAKE_COMMAND    NAMES cmake)
find_program(CTEST_UNAME_COMMAND    NAMES uname)
find_program(CTEST_GIT_COMMAND      NAMES git)
find_program(CTEST_VALGRIND_COMMAND NAMES valgrind)
find_program(CTEST_GNU_COV_COMMAND  NAMES gcov)
find_program(CTEST_LLVM_COV_COMMAND NAMES llvm-cov)


# ---------------------------------------------------------------------------- #
# Use uname
# ---------------------------------------------------------------------------- #
function(GET_UNAME NAME FLAG)
    # checking if worked
    set(_RET 1)
    # iteration limiting
    set(_NITER 0)
    set(_NAME "")
    while(_RET GREATER 0 AND _NITER LESS 100 AND "${_NAME}" STREQUAL "")
        execute_process(COMMAND ${CTEST_UNAME_COMMAND} ${FLAG}
            OUTPUT_VARIABLE _NAME
            WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
            RESULT_VARIABLE _RET
            OUTPUT_STRIP_TRAILING_WHITESPACE)
        math(EXPR _NITER "${_NITER}+1")
    endwhile(_RET GREATER 0 AND _NITER LESS 100 AND "${_NAME}" STREQUAL "")
    # fail if not successful
    if(_RET GREATER 0)
        message(FATAL_ERROR
            "Unable to successfully execute: '${CTEST_UNAME_COMMAND} ${FLAG}'")
    endif(_RET GREATER 0)
    # set the variable in parent scope
    set(${NAME} ${_NAME} PARENT_SCOPE)
endfunction(GET_UNAME NAME FLAG)


# ---------------------------------------------------------------------------- #
# Get the OS machine hardware name (e.g. x86_64)
# ---------------------------------------------------------------------------- #
function(GET_OS_MACHINE_HARDWARE_NAME VAR)
    get_uname(_VAR -m)
    set(${VAR} ${_VAR} PARENT_SCOPE)
endfunction(GET_OS_MACHINE_HARDWARE_NAME VAR)


# ---------------------------------------------------------------------------- #
# Get the OS system name (e.g. Darwin, Linux)
# ---------------------------------------------------------------------------- #
function(GET_OS_SYSTEM_NAME VAR)
    get_uname(_VAR -s)
    set(${VAR} ${_VAR} PARENT_SCOPE)
endfunction(GET_OS_SYSTEM_NAME VAR)


# ---------------------------------------------------------------------------- #
# -- Include file if exists
# ---------------------------------------------------------------------------- #
macro(include_if _TESTFILE)
    if(EXISTS "${_TESTFILE}")
        include("${_TESTFILE}")
    else(EXISTS "${_TESTFILE}")
        if(NOT "${ARGN}" STREQUAL "")
            include("${ARGN}")
        endif(NOT "${ARGN}" STREQUAL "")
    endif(EXISTS "${_TESTFILE}")
endmacro(include_if _TESTFILE)


# ---------------------------------------------------------------------------- #
# -- Settings
# ---------------------------------------------------------------------------- #
## -- Process timeout in seconds
set(CTEST_TIMEOUT           "7200")
## -- Set output to English
set(ENV{LC_MESSAGES}        "en_EN" )


# ---------------------------------------------------------------------------- #
# -- Clean/Reset
# ---------------------------------------------------------------------------- #
macro(CLEAN_DIRECTORIES)
    message(STATUS "Cleaning ${CTEST_BINARY_DIRECTORY}...")
    execute_process(
        COMMAND ${CTEST_CMAKE_COMMAND} -E remove_directory ${CTEST_BINARY_DIRECTORY}
        WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR})
endmacro(CLEAN_DIRECTORIES)


# ---------------------------------------------------------------------------- #
# -- Copy ctest configuration file
# ---------------------------------------------------------------------------- #
macro(COPY_CTEST_CONFIG_FILES)
    if(NOT "${CMAKE_CURRENT_LIST_DIR}" STREQUAL "${CTEST_BINARY_DIRECTORY}" AND
       NOT "${CTEST_SOURCE_DIRECTORY}" STREQUAL "${CTEST_BINARY_DIRECTORY}")
        ## -- CTest Config
        configure_file(${CMAKE_CURRENT_LIST_DIR}/CTestConfig.cmake
                       ${CTEST_BINARY_DIRECTORY}/CTestConfig.cmake COPYONLY)
        ## -- CTest Custom
        configure_file(${CMAKE_CURRENT_LIST_DIR}/CTestCustom.cmake
                       ${CTEST_BINARY_DIRECTORY}/CTestCustom.cmake COPYONLY)
    endif(NOT "${CMAKE_CURRENT_LIST_DIR}" STREQUAL "${CTEST_BINARY_DIRECTORY}" AND
          NOT "${CTEST_SOURCE_DIRECTORY}" STREQUAL "${CTEST_BINARY_DIRECTORY}")
endmacro(COPY_CTEST_CONFIG_FILES)


# ---------------------------------------------------------------------------- #
# -- Run submit scripts
# ---------------------------------------------------------------------------- #
macro(READ_PRESUBMIT_SCRIPTS)
    ## check
    file(GLOB_RECURSE PRESUBMIT_SCRIPTS "${CTEST_BINARY_DIRECTORY}/*CTestPreSubmitScript.cmake")
    if("${PRESUBMIT_SCRIPTS}" STREQUAL "")
        message(STATUS "No scripts matching '${CTEST_BINARY_DIRECTORY}/*CTestPreSubmitScript.cmake' were found")
    endif()
    foreach(_FILE ${PRESUBMIT_SCRIPTS})
        message(STATUS "Including pre-submit script: \"${_FILE}\"...")
        include("${_FILE}")
    endforeach(_FILE ${PRESUBMIT_SCRIPTS})
endmacro(READ_PRESUBMIT_SCRIPTS)


# ---------------------------------------------------------------------------- #
# -- Read CTestNotes.cmake file
# ---------------------------------------------------------------------------- #
macro(READ_NOTES)
    ## check
    file(GLOB_RECURSE NOTE_FILES "${CTEST_BINARY_DIRECTORY}/*CTestNotes.cmake")
    foreach(_FILE ${NOTE_FILES})
        message(STATUS "Including CTest notes files: \"${_FILE}\"...")
        include("${_FILE}")
    endforeach(_FILE ${NOTE_FILES})
endmacro(READ_NOTES)


# ---------------------------------------------------------------------------- #
# -- Check to see if there is a ctest token (for CDash submission)
# ---------------------------------------------------------------------------- #
macro(CHECK_FOR_CTEST_TOKEN)

    # set using token to off
    set(CTEST_USE_TOKEN OFF)
    # set token to empty
    set(CTEST_TOKEN     "")

    if(NOT "${CTEST_TOKEN_FILE}" STREQUAL "")
        string(REGEX REPLACE "^~" "$ENV{HOME}" CTEST_TOKEN_FILE "${CTEST_TOKEN_FILE}")
    endif(NOT "${CTEST_TOKEN_FILE}" STREQUAL "")

    # check for a file containing token
    if(NOT "${CTEST_TOKEN_FILE}" STREQUAL "" AND EXISTS "${CTEST_TOKEN_FILE}")
        message(STATUS "Reading CTest token file: ${CTEST_TOKEN_FILE}")
        file(READ "${CTEST_TOKEN_FILE}" CTEST_TOKEN)
        string(REPLACE "\n" "" CTEST_TOKEN "${CTEST_TOKEN}")
    endif(NOT "${CTEST_TOKEN_FILE}" STREQUAL "" AND EXISTS "${CTEST_TOKEN_FILE}")

    # if no file, check the environment
    if("${CTEST_TOKEN}" STREQUAL "" AND NOT "$ENV{CTEST_TOKEN}" STREQUAL "")
        set(CTEST_TOKEN "$ENV{CTEST_TOKEN}")
    endif("${CTEST_TOKEN}" STREQUAL "" AND NOT "$ENV{CTEST_TOKEN}" STREQUAL "")

    # if non-empty token, set CTEST_USE_TOKEN to ON
    if(NOT "${CTEST_TOKEN}" STREQUAL "")
        set(CTEST_USE_TOKEN ON)
    endif(NOT "${CTEST_TOKEN}" STREQUAL "")

endmacro(CHECK_FOR_CTEST_TOKEN)


# ---------------------------------------------------------------------------- #
# -- Submit command
# ---------------------------------------------------------------------------- #
macro(SUBMIT_COMMAND)

    # check for token
    check_for_ctest_token()
    read_notes()
    read_presubmit_scripts()

    if(NOT CTEST_USE_TOKEN)
        # standard submit
        ctest_submit(RETURN_VALUE ret ${ARGN})
    else(NOT CTEST_USE_TOKEN)
        # submit with token
        ctest_submit(RETURN_VALUE ret
                     HTTPHEADER "Authorization: Bearer ${CTEST_TOKEN}"
                     ${ARGN})
    endif(NOT CTEST_USE_TOKEN)

endmacro(SUBMIT_COMMAND)


# ---------------------------------------------------------------------------- #
# -- Determine if submit time
# ---------------------------------------------------------------------------- #
macro(SUBMIT KEY)

    if("${CTEST_TRIGGER}" STREQUAL "Any" OR "${CTEST_TRIGGER}" STREQUAL "Submit")
        submit_command(${ARGN})
    else("${CTEST_TRIGGER}" STREQUAL "Any" OR "${CTEST_TRIGGER}" STREQUAL "Submit")
        if("${CTEST_TRIGGER}" STREQUAL "${KEY}")
            submit_command(${ARGN})
        endif("${CTEST_TRIGGER}" STREQUAL "${KEY}")
    endif("${CTEST_TRIGGER}" STREQUAL "Any" OR "${CTEST_TRIGGER}" STREQUAL "Submit")

endmacro(SUBMIT KEY)


# ---------------------------------------------------------------------------- #
# -- Setup the test
# ---------------------------------------------------------------------------- #
macro(SETUP KEY)

    if("${CTEST_TRIGGER}" STREQUAL "Any" OR "${KEY}" STREQUAL "Build")

        message(STATUS "Key (${KEY}) triggered a fresh build...")
        copy_ctest_config_files()
        ctest_read_custom_files("${CMAKE_CURRENT_LIST_DIR}")

        ctest_start(${CTEST_MODEL}   TRACK ${CTEST_MODEL})

        copy_ctest_config_files()
        ctest_read_custom_files("${CTEST_BINARY_DIRECTORY}")

        if(NOT "${CTEST_CONFIGURE_COMMAND}" STREQUAL "")
            ctest_configure (BUILD "${CTEST_BINARY_DIRECTORY}" RETURN_VALUE ret)
        endif(NOT "${CTEST_CONFIGURE_COMMAND}" STREQUAL "")
        if(NOT "${CTEST_UPDATE_COMMAND}" STREQUAL "")
            ctest_update    (BUILD "${CTEST_BINARY_DIRECTORY}" RETURN_VALUE ret)
        endif(NOT "${CTEST_UPDATE_COMMAND}" STREQUAL "")
        if(NOT "${CTEST_BUILD_COMMAND}" STREQUAL "")
            ctest_build     (BUILD "${CTEST_BINARY_DIRECTORY}" RETURN_VALUE ret)
        endif(NOT "${CTEST_BUILD_COMMAND}" STREQUAL "")

    else("${CTEST_TRIGGER}" STREQUAL "Any" OR "${KEY}" STREQUAL "Build")

        unset(CTEST_CHECKOUT_COMMAND)
        copy_ctest_config_files()
        ctest_read_custom_files("${CMAKE_CURRENT_LIST_DIR}")

        ctest_start(${CTEST_MODEL}   TRACK ${CTEST_MODEL} APPEND)

        copy_ctest_config_files()
        ctest_read_custom_files("${CTEST_BINARY_DIRECTORY}")

    endif("${CTEST_TRIGGER}" STREQUAL "Any" OR "${KEY}" STREQUAL "Build")

endmacro(SETUP KEY)
