"""
Publishes whether turtle2 should chase or flee, flipping every 10 seconds.
"""

import rclpy
from rclpy.node import Node
from turtle_interfaces.msg import ChaseMode


class ModePublisher(Node):
    def __init__(self):
        super().__init__('mode_publisher')

        # Queue depth 10 = buffer up to 10 messages if a subscriber is slow.
        self.publisher = self.create_publisher(ChaseMode, '/chase_mode', 10)

        self.chase = True

        self.create_timer(10.0, self.flip_mode)
        self.create_timer(0.5, self.publish_mode)

        self.get_logger().info('Mode publisher started. Mode: CHASE')

    def flip_mode(self):
        self.chase = not self.chase
        self.get_logger().info(f'Mode -> {"CHASE" if self.chase else "FLEE"}')

    def publish_mode(self):
        msg = ChaseMode()
        msg.chase = self.chase
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)              # start ROS
    node = ModePublisher()
    try:
        rclpy.spin(node)               # block, processing callbacks forever
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
