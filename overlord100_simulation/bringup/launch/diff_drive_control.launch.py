# Copyright 2020 ros2_control Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.substitutions import (
    Command,
    FindExecutable,
    PathJoinSubstitution,
    LaunchConfiguration,
)

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    # Modify run_hardware to use boolean
    run_hardware = DeclareLaunchArgument(
        "run_hardware",
        default_value="False",
        description="If True, this launch file runs only nodes specific for the hardware,"
        "and skips everything gazebo-related",
    )

    world_arg = DeclareLaunchArgument(
        "world",
        default_value="simple_office.sdf",
        description="Defines the world that will be used in the simulation. Three worlds are supplied together with the package: \n\n            - 'simple_office.sdf' -> a small office simulation with hardware and actors \n            - 'large_office.sdf' -> a large version of the office with actors, but without furniture \n            - 'clear_world.sdf' -> a scene consisting only of a plane\n\n        To add a new scene, you need to add the world file (.sdf extension) to the 'world' folder. And, if necessary, the models in the 'models' folder.",
    )

    is_custom_controller = DeclareLaunchArgument(
        "enable_custom_controller",
        default_value="True",
        description="Defines the type of robot control:\n\n            - 'True' -> a third-party controller will be used for control \n            - 'False' -> the built-in 'rqt_robot_steernig' controlle  will be used\n",
    )

    custom_controller_pkg = DeclareLaunchArgument(
        "custom_controller_pkg",
        default_value="overlord100_controller",
        description="Defines which ros 2 package will control the robot \n            (works only if the launch argument 'enable_custom_controller' is 'True')",
    )

    use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="False",
        description="Use simulation (Gazebo) clock if launch argument is 'True'",
    )

    spawn_models_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("overlord100_simulation"), "launch"),
                "/spawn_models.launch.py",
            ]
        ),
        launch_arguments=[
            ("world", LaunchConfiguration("world")),
            ("enable_custom_controller", LaunchConfiguration("enable_custom_controller")),
            ("run_hardware", LaunchConfiguration("run_hardware")),  # Pass hardware flag
        ],
    )

    bridge_setup_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("overlord100_simulation"), "launch"),
                "/setup_bridges.launch.py",
            ]
        ),
        condition=UnlessCondition(LaunchConfiguration("run_hardware")),
    )

    transforms = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("overlord100_simulation"), "launch"),
                "/static_transforms.launch.py",
            ]
        )
    )

    converter = Node(package="overlord100_simulation", executable="converter.py")

    return LaunchDescription(
        [
            run_hardware,
            world_arg,
            is_custom_controller,
            custom_controller_pkg,
            use_sim_time,
            spawn_models_node,
            bridge_setup_node,
            transforms,
            converter,
        ]
    )
