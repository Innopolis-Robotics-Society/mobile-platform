cmake_minimum_required(VERSION 3.8)
project(iros_mobile_platform_controller)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(iros_mobile_platform_msgs REQUIRED)

install(
  DIRECTORY config launch
  DESTINATION share/${PROJECT_NAME}/
)

add_executable(diff_drive_controller src/controller.cpp)

ament_target_dependencies(
  diff_drive_controller 
  rclcpp 
  geometry_msgs 
  iros_mobile_platform_msgs
)

add_executable(controller_subscriber src/controller_subscriber.cpp)

ament_target_dependencies(
  controller_subscriber 
  rclcpp 
  geometry_msgs 
  iros_mobile_platform_msgs
)

add_executable(cmd_vel_publisher src/cmd_vel_publisher.cpp)

ament_target_dependencies(
 cmd_vel_publisher 
 rclcpp 
 geometry_msgs 
 iros_mobile_platform_msgs
)

install(TARGETS 
  diff_drive_controller
  controller_subscriber
  cmd_vel_publisher
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS 
  scripts/encoders_to_odom.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME encoders_to_odom
)

ament_package()
