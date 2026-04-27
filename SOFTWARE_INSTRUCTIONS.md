# OpenPodCar_V2 Software Instructions

OpenPodcar2 uses a new software stack based on Robot Operating System version 2 (ROS2).  ROS2 is firstly a middleware system implementing publish-subscribe message passing between nodes across a TCP/IP network. Messages are published on named topics which can be subscribed to by any nodes interested in them. ROS2 is secondly a software ecosystem of state-of-the-art implementations of drivers for robots and simulators and of standard robotics algorithms. 

## Kinematic Control

OpenPodcar2 is as an Ackermann-steered vehicle.   The ROS2 community uses `Twist` as the standard for sending mobile robot motion commands (ROS REP-119), so OpenPodcar2 takes `cmd_vel:Twist` commands as inputs.    ROS2 also provides an Ackermann drive message `ackermann_msgs/msg/AckermannDrive` which contains fields for speed and steering angle.

<p align="center">
  <img src="./Images and videos/Ackermann Steering.png" width="100%" />
</p>

## Manual Teleoperation

* An Xbox controller is used as the manual controller.  `joy` is a standard ROS2 package which consists of node to interface this controller (or many others) to send messages of type `joy` on the topic `/joy`.

* `telelop_twist_joy` is a standard ROS2 node which converts `joy` messages to `Twist` type `cmd_vel` messages.  It includes an additional DMH configured on a button on the controller used via standard ROS2 YAML parameter file (RL for XBox). This DMH button must be held down on the controller in order for any other controls to have an effect.

## Localization and mapping

* The ROS2 ecosystem provides several alternative tools for SLAM.   We use RTAB-Map, a 3D voxel based SLAM which is specialised for use with RGBD cameras. The RTAB-Map package also provides the visual odometry named as RGBD odometry which is deployed in the vehicle to provide the pose information and `odom` to `base_link` transform. This has shown reliable results for indoor operations.


* RTAB-Map SLAM package is used to perform the the mapping and localization which takes the `odom` to `base_link` transform as input and corrects the pose information of OpenPodcar2 in the map frame. 


* The Intel Realsense D435 mounted on the vehicle has range of 10m but offers good accuracy for 5m range. The system checked with both ranges and default is set to 5m.


<p align="center">
  <img src="./Images and videos/Large_indoor_map.png" width="100%" />
</p>


## Navigation

The ROS2 ecosystem includes a navigation stack,  Navigation2 (nav2), designed to facilitate the smooth navigation of a vehicle from one point to another (from point A to B) while avoiding obstacles along the path.  OpenPodcar2 utilizes A* hybrid as global path planner, DWB controller server, specific behaviour servers (wait, back).


<p align="center">
  <img src="./Images and videos/Podcar_Nav2_node_graph.png" width="100%" />
</p>


## Pedestrian detection and tracking

* The RGBD camera is used for pedestrian detection and tracking as well as for SLAM.   An off-the-shelf ROS2-wrapped YOLOv8 (https://github.com/Rak-r/yolov8_ros2_OpenPodCarV2.git) is linked to the camera to perform and report pedestrian and vehicle detection and tracking in 3D space. 


* YOLOv8 2D detection reports bounding box co-ordinates as ($x$ center, $y$ center, width of the box, height of the box); class name, class ID, confidence score are also extracted. YOLOv8 includes 2D tracking on these detection with BotSORT and ByteTrack which provides acceptable real-time performance but suffers from false re-id errors.  ByteTrack is used as default here. 

* An Intel depth camera ROS2 wrapper is provided by the Intel Realsense SDK (https://www.intelrealsense.com/sdk-2/) which publishes the data over `/camera_image_raw` for RGB image, `/depth` for the depth image, and `/depth_camera_info` reporting the  intrinsic cameras parameters.


<p align="center">
  <img src="./Images and videos/Masked_pedestrian.png" width="100%" />
</p>



## Simulation

A ROS2 simulation of OpenPodcar2, is provided, using the newly released Gazebo sim. To handle time/clock synchronization issues at the software level, it is necessary that both the systems; ROS2 stack and Gazebo simulation should work on the same time. Although ROS/ROS2 provides the configurable parameter for the nodes named  \lstinline{use_sim_time} which could be set to a boolean value of either true or false, there are still some issues faced namely; lookup transforms, message filter dropping when setting the the whole NAV2 stack with Gazebo which generates lags in the system and ultimately failures. Nevertheless, Navigation2 must be implemented on the real/physical OpenPodcar2, so it makes sense to set the stack with working on wall time/system time. To achieve this condition, the gazebo plugins used in our stack Ackermann Steering plugin which deals the kinematic control for the robot, lidar sensor system plugin to receive the LaserScan data in case of using lidar, rgbd sensor system plugin for simulating the depth image and  odometry publisher plugin to get the ground-truth odometry data out from Gazebo needs to publish the data on wall time and such condition in Gazebo (making use wall time) is not a very discussed topic and in the recently introduced the new Gazebo 7 makes it more of a highly debugging task. To handle this condition, custom ROS2 nodes are created which subscribes to the gazebo output topics and publishes the topic data on wall/system time.
