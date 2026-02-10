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
        default_value="True",
        description="Use simulation (Gazebo) clock if launch argument is 'True'",
    )
    
    spawn_models_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("overlord100_simulation"), "launch"),
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
                os.path.join(get_package_share_directory("overlord100_simulation"), "launch"),
                "/setup_bridges.launch.py",
            ]
        ),
    )

    transforms = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("overlord100_simulation"), "launch"),
                "/static_transforms.launch.py",
            ]
        )
    )
    converter = Node(package="overlord100_simulation", executable="converter")

    rviz_node = Node(
        package="rviz2",
        namespace="",
        executable="rviz2",
        name="rviz2",
        arguments=[
            "-d",
            [
                os.path.join(
                    get_package_share_directory("overlord100_simulation"),
                    "rviz",
                    "simulator.rviz",
                )
            ],
        ],
    )

    ros2_controller = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(get_package_share_directory("overlord100_controller"), "launch"),
                "/controller.launch.py",
            ]
        )
    )

    rqt_node_with_ros2_controller = Node(
        package="rqt_robot_steering",
        executable="rqt_robot_steering",
        remappings=[
            ("/cmd_vel", "/overlord100_controller/cmd_vel_unstamped"),
        ],
    )
    
    return LaunchDescription(
        [
            world_arg,
            use_sim_time,
            spawn_models_node,
            bridge_setup_node,
            transforms,
            converter,
            rviz_node,
            ros2_controller,
            rqt_node_with_ros2_controller,
        ]
    )
