from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command, FindExecutable


def generate_launch_description():

    # use_sim_time = DeclareLaunchArgument(
    #     "use_sim_time",
    #     default_value="True",
    #     description="Use simulation (Gazebo) clock if launch argument is 'True'"
    # )

    # use_mock_hardware = DeclareLaunchArgument(
    #     "use_mock_hardware",
    #     default_value="false",
    #     description="Use mock hardware"
    # )

    # robot_description_content = Command(
    #     [
    #         PathJoinSubstitution([FindExecutable(name="xacro")]),
    #         " ",
    #         PathJoinSubstitution(
    #             [FindPackageShare("overlord100_simulation"), "description", "overlord100.urdf.xacro"]
    #         ),
    #         " ",
    #         "use_mock_hardware:=",
    #         LaunchConfiguration("use_mock_hardware"),
    #     ]
    # )
    # robot_description = {"robot_description": robot_description_content}

    # return LaunchDescription(
    #     [
    #         use_sim_time,
    #         use_mock_hardware,
    #         Node(
    #             package="robot_state_publisher",
    #             executable="robot_state_publisher",
    #             name="robot_state_publisher_control",
    #             output="both",
    #             parameters=[
    #                 {"use_sim_time": LaunchConfiguration("use_sim_time")},
    #                 robot_description,
    #             ],
    #         ),
    #     ]
    # )

    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_mock_hardware",
            default_value="false",
            description="Start robot with mock hardware mirroring command to its states.",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="False",
            description="Use simulation (Gazebo) clock if launch argument is 'True'",
        )
    )

    # Get URDF via xacro
    use_mock_hardware = LaunchConfiguration("use_mock_hardware")
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [
                    FindPackageShare("overlord100_simulation"),
                    "urdf",
                    "overlord100.urdf.xacro",
                ]
            ),
            " ",
            "use_mock_hardware:=",
            use_mock_hardware,
        ]
    )
    robot_description = {"robot_description": robot_description_content}
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher_control",
        output="both",
        parameters=[
            robot_description,
            {"use_sim_time": LaunchConfiguration("use_sim_time")},
        ],
    )

    nodes = [
        robot_state_publisher_node,
    ]

    return LaunchDescription(declared_arguments + nodes)
