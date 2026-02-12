cmake_minimum_required(VERSION 3.8)
project(lidar_wrapper)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Copied from sllidar_ros2/CMakeLists
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 14)
endif()
if(MSVC)
  add_compile_definitions(
    _USE_MATH_DEFINES
  )
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(diagnostic_msgs REQUIRED)
# find_package(iros_mobile_platform_msgs REQUIRED)

# TODO: check if there is better way to include files from other package
set(SLLIDAR_RELATIVE_PATH "../lidar")
set(SLLIDAR_SDK_RELATIVE_PATH "${SLLIDAR_RELATIVE_PATH}/sdk")
FILE(GLOB SLLIDAR_SDK_SRC_RELATIVE
  "${SLLIDAR_SDK_RELATIVE_PATH}/src/arch/linux/*.cpp"
  "${SLLIDAR_SDK_RELATIVE_PATH}/src/hal/*.cpp"
  "${SLLIDAR_SDK_RELATIVE_PATH}/src/*.cpp"
  "${SLLIDAR_SDK_RELATIVE_PATH}/src/dataunpacker/*.cpp"
  "${SLLIDAR_SDK_RELATIVE_PATH}/src/dataunpacker/unpacker/*.cpp"
)


# Build
include_directories(
  ${SLLIDAR_SDK_RELATIVE_PATH}/include
  ${SLLIDAR_SDK_RELATIVE_PATH}/src
  ${SLLIDAR_RELATIVE_PATH}/src
  ${Boost_INCLUDE_DIRS}
)

add_executable(sllidar_node src/sllidar_node.cpp ${SLLIDAR_SDK_SRC_RELATIVE})
ament_target_dependencies(sllidar_node
  rclcpp
  std_srvs
  sensor_msgs
  diagnostic_msgs
)

install(
  TARGETS sllidar_node
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
