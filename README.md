# 2D-SonarMapper
SonarLidar is a ROS2 package that uses an ultrasonic sensor on a servo motor to simulate 2D scans. It publishes distance data as LaserScan messages for visualization in RViz. This low-cost solution offers an alternative to LiDAR for robotic mapping and navigation.

Run the node:
ros2 run sonar_lidar sonar

Run a static transform publisher (to define frame relationship):
ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map laser_frame

Open RViz2:
rviz2

In RViz, set Fixed Frame to map.

Add a LaserScan display, and set the topic to /scan.

You should now see the 2D scan data from the ultrasonic sensor visualized like a LiDAR scan.
