"""
Container A: the GUI, the second turtle, and mouse control.
"""

from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node


def generate_launch_description():
    turtlesim = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim',
        output='screen',
    )

    # /spawn does not exist until turtlesim is running, so delay this.
    spawn_turtle2 = TimerAction(
        period=3.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'service', 'call', '/spawn',
                    'turtlesim/srv/Spawn',
                    '{x: 2.0, y: 2.0, theta: 0.0, name: "turtle2"}',
                ],
                output='screen',
            )
        ],
    )

    mouse = TimerAction(
        period=2.0,
        actions=[
            Node(
                package='turtle_chase',
                executable='mouse_node',
                name='mouse_node',
                output='screen',
            )
        ],
    )

    return LaunchDescription([turtlesim, spawn_turtle2, mouse])
