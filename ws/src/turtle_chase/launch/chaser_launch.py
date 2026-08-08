"""
Container B: chase logic and mode switching.
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtle_chase',
            executable='mode_node',
            name='mode_node',
            output='screen',
        ),
        Node(
            package='turtle_chase',
            executable='chase_node',
            name='chase_node',
            output='screen',
        ),
    ])
