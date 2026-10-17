# Smart Shopping Trolley with Autonomous Navigation

## Project Overview

The Smart Shopping Trolley integrates RFID-based product identification
and smart billing with a ROS 2-based autonomous navigation system.

The project combines embedded systems, instrumentation, sensor integration,
robot modelling, and mobile robotics.

## Key Components

### 1. Smart Billing and Product Identification
- RFID-based product identification.
- Trolley weight measurement.
- Automated billing functionality.
- Inventory monitoring.

### 2. Autonomous Navigation
- ROS 2-based robotics framework.
- YDLIDAR integration.
- SLAM configuration for environment mapping.
- Trolley robot model using URDF/Xacro.
- Gazebo simulation and navigation development.

## Technology Stack

- ROS 2
- Ubuntu Linux
- Python
- RFID
- YDLIDAR
- SLAM
- URDF/Xacro
- Gazebo

## Repository Structure

```text
smart-shopping-trolley/
├── README.md
├── ros2_ws/
│   └── src/
│       ├── trolley_slam/
│       └── ydlidar_ros2_driver/
├── maps/
├── firmware/
├── hardware/
└── images/
## Mapping Results

The following maps were generated during the Smart Shopping Trolley's
LiDAR-based mapping and SLAM development.

### Map 1

![Smart Shopping Trolley SLAM Map 1](maps/my_house_map.jpg)

### Map 2

![Smart Shopping Trolley SLAM Map 2](maps/my_house_map1.jpg)
