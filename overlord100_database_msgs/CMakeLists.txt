cmake_minimum_required(VERSION 3.8)
project(overlord100_database_msgs)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)

# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Point.msg"
  "msg/Route.msg"

  # Maps
  "srv/StoreMap.srv"
  "srv/LoadMap.srv"
  "srv/DeleteMap.srv"
  "srv/GetMap.srv"
  "srv/GetMapList.srv"

  # Points
  "srv/AddPoint.srv"
  "srv/ListPoints.srv"
  "srv/DeletePoint.srv"

  # Routes
  "srv/AddRoute.srv"
  "srv/ListPointsInRoute.srv"
  "srv/DeletePointInRoute.srv"
  "srv/DeleteRoute.srv"
  DEPENDENCIES geometry_msgs nav_msgs
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)

  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)

  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
