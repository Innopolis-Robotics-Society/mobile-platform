from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='overlord100_database',
            executable='database_node',
            name='overlord100_database_node',
            output='screen',
            parameters=[
                {'mongodb_uri': 'mongodb://localhost:27017/'},
                {'db_name': 'overlord_db'}
            ]
        ),
    ])
