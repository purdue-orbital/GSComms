cmake_minimum_required(VERSION 3.0)
project(SERIAL_TEST)

# setup c++ building
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -I../ -I../QOL -I../Modulation -I../Lime")


#build test files
add_executable(Test_BPSK.test Test_BPSK.cpp)
add_executable(Test_FSK.test Test_FSK.cpp)
add_executable(Test_IQ.test Test_IQ.cpp)
add_executable(Test_Viterbi.test Test_Viterbi.cpp)
add_executable(Test_All.test Test_All.cpp)

#if(${CMAKE_BUILD_TYPE} NOT EQUAL CMAKE_C_FLAGS_DEBUG)
    add_custom_command(
        TARGET Test_BPSK.test POST_BUILD
        COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/bin/Test_All.test
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin
        COMMENT "Running tests..."
    )
#endif()