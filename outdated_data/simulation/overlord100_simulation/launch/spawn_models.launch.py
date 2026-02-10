import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import (
    ExecuteProcess,
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
    AppendEnvironmentVariable,
)


def generate_launch_description():

    world_arg = DeclareLaunchArgument(
        "world",
        default_value="mvp_world.sdf",
        description="Defines the world that will be used in the simulation. Three worlds are supplied together with the package: \n\n            - 'simple_office.sdf' -> a small office simulation with hardware and actors \n            - 'large_office.sdf' -> a large version of the office with actors, but without furniture \n            - 'clear_world.sdf' -> a scene consisting only of a plane\n\n        To add a new scene, you need to add the world file (.sdf extension) to the 'world' folder. And, if necessary, the models in the 'models' folder.",
    )

    is_custom_controller = DeclareLaunchArgument(
        "enable_custom_controller",
        default_value="True",
        description="Defines the type of robot control:\n\n            - 'True' -> a third-party controller will be used for control \n            - 'False' -> the built-in 'rqt_robot_steernig' controlle  will be used\n",
    )

    pack_dir = get_package_share_directory("overlord100_simulation")
    # Spawn robot
    ignition_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-name",
            "overlord100",
            "-file",
            PathJoinSubstitution(
                [
                    get_package_share_directory("overlord100_simulation"),
                    "description",
                    "overlord100.urdf",
                ]
            ),
            "-allow_renaming",
            "true",
            "-x",
            "-2.0",
            "-y",
            "-0.5",
            "-z",
            "1",
        ],
        condition=IfCondition(LaunchConfiguration("enable_custom_controller")),
    )

    ignition_spawn_entity_with_diffdrive = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-name",
            "overlord100",
            "-file",
            PathJoinSubstitution(
                [
                    get_package_share_directory("overlord100_simulation"),
                    "description",
                    "overlord100_with_diffdrive.urdf",
                ]
            ),
            "-allow_renaming",
            "true",
            "-x",
            "-2.0",
            "-y",
            "-0.5",
            "-z",
            "1",
        ],
        condition=UnlessCondition(LaunchConfiguration("enable_custom_controller")),
    )

    # Spawn world using sdf with world tag
    start_world = ExecuteProcess(
        cmd=[
            "ign",
            "gazebo",
            "-v 4",
            "-r",
            PathJoinSubstitution(
                [
                    get_package_share_directory("overlord100_simulation"),
                    "worlds",
                    LaunchConfiguration("world"),
                ]
            ),
        ]
    )

    def find(name, path):
        for root, dirs, files in os.walk(path):
            if name in dirs:
                return os.path.join(root, name)

    model_path = find("models", os.getenv("PWD"))
    print(model_path)
    set_env_vars_resources = AppendEnvironmentVariable(
        "IGN_GAZEBO_RESOURCE_PATH", model_path
    )

    return LaunchDescription(
        [
            world_arg,
            is_custom_controller,
            set_env_vars_resources,
            start_world,
            ignition_spawn_entity,
            ignition_spawn_entity_with_diffdrive,
        ]
    )
