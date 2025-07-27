#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster
import serial
import math

class SerialLaserScanNode(Node):
    def __init__(self):
        super().__init__('serial_laserscan')
        self.port = '/dev/ttyUSB0'
        self.baud = 115200

        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=0.1)
            self.get_logger().info(f'Connected to {self.port} at {self.baud} baud')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to open serial port: {e}')
            rclpy.shutdown()
            return

        self.pub = self.create_publisher(LaserScan, 'scan', 10)

        self.num_samples = 181
        self.ranges = [float('inf')] * self.num_samples

        self.laser_msg = LaserScan()
        self.laser_msg.header.frame_id = 'laser_frame'
        self.laser_msg.angle_min = 0.0
        self.laser_msg.angle_max = math.pi
        self.laser_msg.angle_increment = math.pi / (self.num_samples - 1)
        self.laser_msg.time_increment = 0.0
        self.laser_msg.scan_time = 0.1
        self.laser_msg.range_min = 0.02
        self.laser_msg.range_max = 10.0

        # ساخت broadcaster برای TF
        self.tf_broadcaster = TransformBroadcaster(self)

        self.timer = self.create_timer(0.1, self.timer_callback)

    def publish_static_transform(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'map'           
        t.child_frame_id = 'laser_frame'    
        # تبدیل صفر (ثابت)
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(t)

    def timer_callback(self):
      
        self.publish_static_transform()

        lines_read = 0
        max_lines_per_callback = 10

        while self.ser.in_waiting > 0 and lines_read < max_lines_per_callback:
            line = self.ser.readline().decode('utf-8', errors='replace').strip()
            if line:
                try:
                    index_str, dist_str = line.split(',')
                    index = int(index_str)
                    distance_cm = float(dist_str)
                    distance_m = distance_cm / 100.0

                    if 0 <= index < self.num_samples:
                        self.ranges[index] = distance_m

                    self.get_logger().info(f'Received: index={index}, distance={distance_m:.2f}m')

                except Exception as e:
                    self.get_logger().warn(f'Failed to parse line: "{line}" error: {e}')
            lines_read += 1

        self.laser_msg.header.stamp = self.get_clock().now().to_msg()
        self.laser_msg.ranges = self.ranges.copy()
        self.pub.publish(self.laser_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SerialLaserScanNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
