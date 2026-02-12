import os
from os import pathsep
from pathlib import Path
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from launch.actions import (
    ExecuteProcess,
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    AppendEnvironmentVariable,
)
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution

def generate_launch_description():
    
    iros_mobile_platform_description = get_package_share_directory("iros_mobile_platform_simulation")
    
    use_sim_time = DeclareLaunchArgument(
        name="use_sim_time",
        default_value="true",
        description="Use simulation clock if true"
    )

    model_arg = DeclareLaunchArgument(name="model", default_value=os.path.join(
                                        iros_mobile_platform_description, "description", "iros_mobile_platform.urdf.xacro"
                                        ),
                                      description="Absolute path to robot urdf file"
    )

    world_name_arg = DeclareLaunchArgument(name="world_name", default_value="simple_office",)
    
    world_path = PathJoinSubstitution([
            iros_mobile_platform_description,
            "worlds",
            PythonExpression(expression=["'", LaunchConfiguration("world_name"), "'", " + '.sdf'"])
        ]
    )
    
    model_path = str(Path(iros_mobile_platform_description).parent.resolve())
    model_path += pathsep + os.path.join(get_package_share_directory("iros_mobile_platform_simulation"), 'models')

    gazebo_resource_path = SetEnvironmentVariable(
        "GZ_SIM_RESOURCE_PATH",
        model_path
        )
    
    robot_description = ParameterValue(Command([
            "xacro ",
            LaunchConfiguration("model")
        ]),
        value_type=str
    )

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description,
                     "use_sim_time": LaunchConfiguration("use_sim_time")}]
    )

    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory("ros_gz_sim"), "launch"), "/gz_sim.launch.py"]),
                launch_arguments={
                    "gz_args": PythonExpression(["'", world_path, " -v 4 -r'"])
                }.items()
             )

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=["-topic", "robot_description",
                    "-name", "iros_mobile_platform",
                    "-x", "-2.0",
                    "-y", "-0.5",
                    "-z", "1.0"],
    )

    return LaunchDescription([
        model_arg,
        world_name_arg,
        gazebo_resource_path,
        robot_state_publisher_node,
        gz_spawn_entity,
        gazebo,
    ])
