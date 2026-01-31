cmake_minimum_required(VERSION 3.8)
project(overlord100_mode_switcher)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(overlord100_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)

add_executable(mode_switcher src/mode_switcher.cpp)

ament_target_dependencies(
  mode_switcher 
  rclcpp 
  geometry_msgs 
  overlord100_msgs
)

add_executable(change_mode_client src/change_mode_client.cpp)

ament_target_dependencies(
  change_mode_client 
  rclcpp 
  geometry_msgs 
  overlord100_msgs
)


add_executable(manual_vel_publisher src/manual_vel_publisher.cpp)

ament_target_dependencies(
  manual_vel_publisher 
  rclcpp 
  geometry_msgs 
  overlord100_msgs
)

add_executable(auto_vel_publisher src/auto_vel_publisher.cpp)

ament_target_dependencies(
  auto_vel_publisher 
  rclcpp 
  geometry_msgs 
  overlord100_msgs
)

install(TARGETS
  mode_switcher
  change_mode_client
  manual_vel_publisher
  auto_vel_publisher
  DESTINATION lib/${PROJECT_NAME})

ament_package()
