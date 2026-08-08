"""
Drives turtle1 toward the mouse pointer.

Reads the pointer from the X server, converts screen pixels into
turtlesim world coordinates, then reuses the same proportional
controller as the chase node.
"""

import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from Xlib import display, X

CANVAS_UNITS = 11.088     # turtlesim's default world size
DEADBAND = 0.3            # stop when this close to the cursor
ANGULAR_GAIN = 6.0
LINEAR_GAIN = 2.0
MAX_LINEAR = 4.0


def find_turtlesim_window(root):
    """Depth-first search of the X window tree for turtlesim's window."""
    stack = [root]
    while stack:
        win = stack.pop()
        try:
            name = win.get_wm_name()
            if name and 'turtlesim' in name.lower():
                return win
            stack.extend(win.query_tree().children)
        except Exception:
            # Windows can vanish mid-traversal. Skip and continue.
            continue
    return None


def absolute_geometry(win, root):
    """
    Return (x, y, width, height) of a window in root coordinates.

    get_geometry() gives position relative to the PARENT window, not
    the screen, so we walk up the tree accumulating offsets.
    """
    geom = win.get_geometry()
    x, y = geom.x, geom.y
    parent = win.query_tree().parent
    while parent is not None and parent.id != root.id:
        pgeom = parent.get_geometry()
        x += pgeom.x
        y += pgeom.y
        parent = parent.query_tree().parent
    return x, y, geom.width, geom.height


class MouseNode(Node):
    def __init__(self):
        super().__init__('mouse_node')

        self.display = display.Display()
        self.root = self.display.screen().root
        self.window = None

        self.pose = None
        self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.create_timer(0.05, self.control_loop)   # 20 Hz
        self.get_logger().info('Mouse node started.')

    def on_pose(self, msg):
        self.pose = msg

    def mouse_target(self):
        """Mouse position in turtlesim world coords, or None."""
        if self.window is None:
            self.window = find_turtlesim_window(self.root)
            if self.window is None:
                return None
            self.get_logger().info('Found turtlesim window.')

        try:
            win_x, win_y, win_w, win_h = absolute_geometry(
                self.window, self.root)
            pointer = self.root.query_pointer()
        except Exception:
            self.window = None      # window closed; re-find next tick
            return None

        # Pointer relative to the window's top-left corner.
        px = pointer.root_x - win_x
        py = pointer.root_y - win_y

        # Ignore the pointer if it's outside the canvas.
        if not (0 <= px <= win_w and 0 <= py <= win_h):
            return None

        tx = px * CANVAS_UNITS / win_w
        ty = CANVAS_UNITS - (py * CANVAS_UNITS / win_h)   # flip Y
        return tx, ty

    def control_loop(self):
        if self.pose is None:
            return

        target = self.mouse_target()
        if target is None:
            self.cmd_pub.publish(Twist())    # all zeros: stop
            return

        tx, ty = target
        dx = tx - self.pose.x
        dy = ty - self.pose.y
        distance = math.hypot(dx, dy)

        cmd = Twist()
        if distance > DEADBAND:
            desired = math.atan2(dy, dx)
            raw = desired - self.pose.theta
            error = math.atan2(math.sin(raw), math.cos(raw))
            cmd.angular.z = ANGULAR_GAIN * error
            cmd.linear.x = min(LINEAR_GAIN * distance, MAX_LINEAR)

        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = MouseNode()
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
