import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions.declare_launch_argument import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    world_arg = DeclareLaunchArgument(
        "world_name",
        default_value="simple_office",
        description="Defines the world that will be used in the simulation. Three worlds are supplied together with the package: \n\n            - 'simple_office.sdf' -> a small office simulation with hardware and actors \n            - 'large_office.sdf' -> a large version of the office with actors, but without furniture \n            - 'clear_world.sdf' -> a scene consisting only of a plane\n\n        To add a new scene, you need to add the world file (.sdf extension) to the 'world' folder. And, if necessary, the models in the 'models' folder.",
    )

    use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation (Gazebo) clock if launch argument is 'True'",
    )
    
    spawn_models_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("iros_mobile_platform_simulation"), "launch"),
                "/gazebo.launch.py",
            ]
        ),
        launch_arguments=[
            ("world_name", LaunchConfiguration("world_name")),
            ("use_sim_time", LaunchConfiguration("use_sim_time"))
        ],
    )

    bridge_setup_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("iros_mobile_platform_simulation"), "launch"),
                "/setup_bridges.launch.py",
            ]
        ),
    )

    converter = Node(package="iros_mobile_platform_simulation", executable="converter")

    return LaunchDescription(
        [
            world_arg,
            use_sim_time,
            spawn_models_node,
            bridge_setup_node,
            # converter
        ]
    )
