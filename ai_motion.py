import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class AIMotion(Node):
    def __init__(self):
        super().__init__('ai_motion')
        self.publisher = self.create_publisher(
            JointTrajectory,
            '/crane_plus_arm_controller/joint_trajectory',
            10
        )
        self.joint_names = [
            'crane_plus_joint1',
            'crane_plus_joint2',
            'crane_plus_joint4',
            'crane_plus_joint3',
        ]
        self.timer = self.create_timer(1.0, self.send_trajectory)
        self.sent = False

    def send_trajectory(self):
        if self.sent:
            return

        trajectory = JointTrajectory()
        trajectory.joint_names = self.joint_names

        start = JointTrajectoryPoint()
        start.positions = [0.0, 0.0, 0.0, 0.0]
        start.time_from_start = Duration(sec=2, nanosec=0)

        middle = JointTrajectoryPoint()
        middle.positions = [0.4, 0.0, 0.0, 0.0]
        middle.time_from_start = Duration(sec=4, nanosec=0)

        end = JointTrajectoryPoint()
        end.positions = [0.0, 0.0, 0.0, 0.0]
        end.time_from_start = Duration(sec=7, nanosec=0)

        trajectory.points = [start, middle, end]
        self.publisher.publish(trajectory)
        self.get_logger().info('AI motion trajectory published')
        self.sent = True


def main(args=None):
    rclpy.init(args=args)
    node = AIMotion()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
