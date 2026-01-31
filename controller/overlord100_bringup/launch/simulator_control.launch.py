from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    logger = Node(
        package="overlord100_logger",
        executable="log_collector",
        name="log_collector",
        output="screen",
    )

    controller = Node(
        package="overlord100_controller",
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
            logger,
            controller,
            rqt_controller,
        ]
    )
