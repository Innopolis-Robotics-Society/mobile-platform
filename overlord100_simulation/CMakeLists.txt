cmake_minimum_required(VERSION 3.16)
project(overlord100_simulation LANGUAGES CXX)

if(CMAKE_CXX_COMPILER_ID MATCHES "(GNU|Clang)")
  add_compile_options(-Wall -Wextra)
endif()

# set the same behavior for windows as it is on linux
set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)

# find dependencies
set(THIS_PACKAGE_INCLUDE_DEPENDS
  hardware_interface
  pluginlib
  rclcpp
  rclcpp_lifecycle
)

# find dependencies
find_package(backward_ros REQUIRED)
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

# Skip if Gazebo not present
find_package(gazebo QUIET)
if(NOT gazebo_FOUND)
  message(WARNING "===================================Gazebo not found, proceeding without that simulator.==============")
  return()
endif()


foreach(Dependency IN ITEMS ${THIS_PACKAGE_INCLUDE_DEPENDS})
  find_package(${Dependency} REQUIRED)
endforeach()

## COMPILE
add_library(
  odom_pub_diff_control
  SHARED
  hardware/diffbot_system.cpp
)
target_compile_features(odom_pub_diff_control PUBLIC cxx_std_17)
target_include_directories(odom_pub_diff_control PUBLIC
$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/hardware/include>
$<INSTALL_INTERFACE:include/odom_pub_diff_control>
)
ament_target_dependencies(
  odom_pub_diff_control PUBLIC
  ${THIS_PACKAGE_INCLUDE_DEPENDS}
)

# Export hardware plugins
pluginlib_export_plugin_description_file(hardware_interface odom_pub_diff_control.xml)

# INSTALL
install(
  DIRECTORY hardware/include/
  DESTINATION include/overlord100_simulation
)
install(
  DIRECTORY description/launch description/ros2_control description/urdf
  DESTINATION share/overlord100_simulation
)
install(
  DIRECTORY bringup/launch bringup/config
  DESTINATION share/overlord100_simulation
)

install(
  DIRECTORY description/
  DESTINATION share/${PROJECT_NAME}/description
)

install(
  DIRECTORY models/
  DESTINATION share/${PROJECT_NAME}/models
)

install(
  DIRECTORY worlds/
  DESTINATION share/${PROJECT_NAME}/worlds
)

install(TARGETS odom_pub_diff_control
  EXPORT export_odom_pub_diff_control
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(PROGRAMS
urdf_dummy/converter.py
  DESTINATION lib/${PROJECT_NAME}
)

install(PROGRAMS
urdf_dummy/controller.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)

  ament_add_pytest_test(example_2_urdf_xacro test/test_urdf_xacro.py)
  ament_add_pytest_test(view_example_2_launch test/test_view_robot_launch.py)
  ament_add_pytest_test(run_example_2_launch test/test_diffbot_launch.py)
endif()

## EXPORTS
ament_export_targets(export_odom_pub_diff_control HAS_LIBRARY_TARGET)
ament_export_dependencies(${THIS_PACKAGE_INCLUDE_DEPENDS})
ament_package()
