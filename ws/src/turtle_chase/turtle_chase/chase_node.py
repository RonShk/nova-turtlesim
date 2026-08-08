"""
Drives turtle2 to chase or flee from turtle1, based on /chase_mode.
"""

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from turtle_interfaces.msg import ChaseMode


# Tuning constants
STOP_CHASING_BELOW = 1.0   # close enough, stop chasing
STOP_FLEEING_ABOVE = 4.0   # far enough, stop fleeing
ANGULAR_GAIN = 4.0
LINEAR_GAIN = 1.5
MAX_LINEAR = 3.0


class ChaseNode(Node):
    def __init__(self):
        super().__init__('chase_node')

        # Latest known state. None until the first message arrives.
        self.turtle1_pose = None
        self.turtle2_pose = None
        self.chase = True

        self.create_subscription(Pose, '/turtle1/pose', self.on_pose1, 10)
        self.create_subscription(Pose, '/turtle2/pose', self.on_pose2, 10)
        self.create_subscription(ChaseMode, '/chase_mode', self.on_mode, 10)

        self.cmd_pub = self.create_publisher(Twist, '/turtle2/cmd_vel', 10)

        # Drive from a fixed-rate timer, NOT from a subscriber callback.
        self.create_timer(0.05, self.control_loop)   # 20 Hz

        self.get_logger().info('Chase node started.')

    def on_pose1(self, msg):
        self.turtle1_pose = msg

    def on_pose2(self, msg):
        self.turtle2_pose = msg

    def on_mode(self, msg):
        if msg.chase != self.chase:
            self.get_logger().info(
                f'Switching to {"CHASE" if msg.chase else "FLEE"}')
        self.chase = msg.chase

    def control_loop(self):
        # Don't command anything until we know where both turtles are.
        if self.turtle1_pose is None or self.turtle2_pose is None:
            return

        me = self.turtle2_pose
        target = self.turtle1_pose

        # Vector from me to the other turtle.
        dx = target.x - me.x
        dy = target.y - me.y
        distance = math.hypot(dx, dy)

        # Which way do I want to face?
        if self.chase:
            desired_heading = math.atan2(dy, dx)      # toward
            should_move = distance > STOP_CHASING_BELOW
        else:
            desired_heading = math.atan2(-dy, -dx)    # directly away
            should_move = distance < STOP_FLEEING_ABOVE

        # Angle error, wrapped to [-pi, pi].
        # Doing it via atan2(sin, cos) handles wraparound correctly:
        # naive subtraction gives 350 degrees where the answer is -10.
        raw_error = desired_heading - me.theta
        heading_error = math.atan2(math.sin(raw_error), math.cos(raw_error))

        cmd = Twist()
        cmd.angular.z = ANGULAR_GAIN * heading_error

        if should_move:
            cmd.linear.x = min(LINEAR_GAIN * distance, MAX_LINEAR)
        else:
            cmd.linear.x = 0.0

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = ChaseNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
