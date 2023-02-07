cmake_minimum_required(VERSION 3.20)
set(CMAKE_CXX_STANDARD 20)

#------------------
# Break up projects
#------------------

#------------------
# main projects
#------------------
project(ground_station)
project(launch_station)

#------------------
# Test projects
#------------------
project(radio_modulation)
project(radio_self_test)
project(rx_test)
project(tx_test)



# include library
find_library(LIME LimeSuite lib REQUIRED)


# add executables
add_executable(ground_station src/ground_station/ground_station.cpp)
add_executable(launch_station src/launch_station/launch_station.cpp)
add_executable(radio_modulation test/radio_modulation.cpp)
add_executable(radio_self_test test/radio_self_test.cpp)
add_executable(rx_test test/rx_test.cpp)
add_executable(tx_test test/tx_test.cpp)

# pass lime dependence
target_link_libraries(radio_self_test ${LIME})
target_link_libraries(rx_test ${LIME})
target_link_libraries(tx_test ${LIME})
