from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, PythonExpression
from launch.conditions import IfCondition, UnlessCondition
from ament_index_python.packages import get_package_share_directory
import os
from launch_ros import substitutions


def generate_launch_description():

    run_hardware = DeclareLaunchArgument(
        "run_hardware",
        default_value="False",
        description="If True, this launch file runs only nodes specific for the hardware,"
        "and skips everything gazebo-related",
    )

    # Find the package share directory for your package
    pkg_share = substitutions.FindPackageShare(package="overlord100_simulation").find("overlord100_simulation")

    # Set GAZEBO_MODEL_PATH using os.environ
    os.environ["GAZEBO_MODEL_PATH"] = os.path.join(pkg_share, "models")
    os.environ["IGN_GAZEBO_RESOURCE_PATH"] = os.path.join(pkg_share, "models")

    world_arg = DeclareLaunchArgument(
        "world",
        default_value="simple_office.sdf",
        description="Defines the world that will be used in the simulation.",
    )

    is_custom_controller = DeclareLaunchArgument(
        "enable_custom_controller",
        default_value="True",
        description="Defines the type of robot control.",
    )

    # Package directory
    pack_dir = get_package_share_directory("overlord100_simulation")
    # pack_dir = get_package_share_directory("overlord100_simulation")

    # Xacro file path
    xacro_file = PathJoinSubstitution(
        [pack_dir, "urdf", "overlord100.urdf.xacro"]
        # [pack_dir, "description", "overlord100.urdf"]
    )

    # Convert Xacro to URDF
    robot_description = Command(["xacro", " ", xacro_file])

    # Spawn robot with the processed URDF
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_description}],
    )

    # Spawn robot entity in Gazebo
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-name",
            "overlord100",
            "-topic",
            "robot_description",  # Topic where robot description is published
            "-x",
            "-2.0",
            "-y",
            "-0.5",
            "-z",
            "1",
        ],
        condition=IfCondition(
            PythonExpression(
                [LaunchConfiguration("enable_custom_controller"), " and not ", LaunchConfiguration("run_hardware")]
            )
        ),
    )

    # Launch the world
    start_world = ExecuteProcess(
        cmd=[
            "ign",
            "gazebo",
            "-v 0",
            "-r",
            PathJoinSubstitution([pack_dir, "worlds", LaunchConfiguration("world")]),
        ],
        output="screen",
        condition=UnlessCondition(LaunchConfiguration("run_hardware")),
    )

    return LaunchDescription(
        [
            world_arg,
            run_hardware,
            is_custom_controller,
            robot_state_publisher,  # Publishes the processed URDF from Xacro
            spawn_robot,  # Spawns the robot entity
            start_world,  # Launches the world in Gazebo
        ]
    )
