# 2D-SonarMapper

**2D-SonarMapper** is a low-cost ROS2-based solution that simulates 2D LiDAR scans using an **ultrasonic sensor mounted on a servo motor**. It publishes range data as `LaserScan` messages, which can be visualized in RViz2 for mapping and navigation tasks.

This project is ideal for educational and hobbyist robotics where real LiDARs are too expensive.

---

## 🔧 Components

- **Arduino/ESP32** running `2D_Map_Sonar.ino`
- **ROS2 node** that reads serial data and publishes `/scan` topic
- **RViz2** for visualization

---

## 🚀 Getting Started

### 1. Flash the Arduino/ESP32

Upload the [`2D_Map_Sonar.ino`](./2D_Map_Sonar.ino) sketch to your **Arduino or ESP32** board using the Arduino IDE.

This program continuously rotates a servo motor and sends angle-distance pairs over the serial port in the following format:



### 2. Connect the Board

Connect your microcontroller via USB. Identify the serial port (e.g., `/dev/ttyUSB0` or `COM3` on Windows).

### 3. Run the ROS2 Node

In a terminal with your ROS2 workspace sourced:


ros2 run sonar_lidar sonar

This node reads the serial data and publishes it as sensor_msgs/msg/LaserScan on the /scan topic.

4. Start Static Transform Publisher
You need a static transform between map and laser_frame:


ros2 run tf2_ros static_transform_publisher 0 0 0 0 0 0 map laser_frame

🖥️ Visualize in RViz2
To see the scan:

Launch RViz2:

rviz2

In RViz:

Set Fixed Frame to map

Add a LaserScan display

Set the topic to /scan

You should now see a 2D scan generated from the ultrasonic sensor, emulating a LiDAR sweep.



Make sure the serial port in sonar.cpp matches your board's port.

You can modify the scanning resolution and angle range in the Arduino code.
