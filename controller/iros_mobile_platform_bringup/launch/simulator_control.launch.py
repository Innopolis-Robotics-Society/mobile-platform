from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    controller = Node(
        package="iros_mobile_platform_controller",
        executable="diff_drive_controller",
        name="diff_drive_controller",
        output="screen",
    )

    rqt_controller = Node(
        package="rqt_robot_steering",
        executable="rqt_robot_steering",
    )
    return LaunchDescription(
        [
            # Start log_collector node
            controller,
            rqt_controller,
        ]
    )
