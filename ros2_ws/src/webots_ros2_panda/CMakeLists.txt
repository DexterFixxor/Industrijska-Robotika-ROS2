cmake_minimum_required(VERSION 3.8)
project(webots_ros2_panda)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(webots_ros2_control REQUIRED)

# Install launch files.
install(DIRECTORY
  config
  launch
  
  protos
  resource
  worlds

  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
