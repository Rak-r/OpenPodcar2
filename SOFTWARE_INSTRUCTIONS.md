# OpenPodCar_V2 Software Instructions

OpenPodcar2 uses a new software stack based on Robot Operating System version 2 (ROS2).  ROS2 is firstly a middleware system implementing publish-subscribe message passing between nodes across a TCP/IP network. Messages are published on named topics which can be subscribed to by any nodes interested in them. ROS2 is secondly a software ecosystem of state-of-the-art implementations of drivers for robots and simulators and of standard robotics algorithms. 

## Kinematic Control

OpenPodcar2 is as an Ackermann-steered vehicle.   The ROS2 community uses `Twist` as the standard for sending mobile robot motion commands (ROS REP-119), so OpenPodcar2 takes `cmd_vel:Twist` commands as inputs.    ROS2 also provides an Ackermann drive message `ackermann_msgs/msg/AckermannDrive` which contains fields for speed and steering angle.

<p align="center">
  <img src="./Images and videos/Ackermann Steering.png" width="100%" />
  <br><br><i>Figure 6: Ackermann steering kinematic control.</i>
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
  <br><br><i>Figure 7: SLAM map of a large indoor environment.</i>
</p>


## Navigation

The ROS2 ecosystem includes a navigation stack,  Navigation2 (nav2), designed to facilitate the smooth navigation of a vehicle from one point to another (from point A to B) while avoiding obstacles along the path.  OpenPodcar2 utilizes A* hybrid as global path planner, DWB controller server, specific behaviour servers (wait, back).


<p align="center">
  <img src="./Images and videos/Podcar_Nav2_node_graph.png" width="100%" />
  <br><br><i>Figure 8: OpenPodcar2 Nav2 node graph.</i>
</p>


## Pedestrian detection and tracking

* The RGBD camera is used for pedestrian detection and tracking as well as for SLAM.   An off-the-shelf ROS2-wrapped YOLOv8 (https://github.com/Rak-r/yolov8_ros2_OpenPodCarV2.git) is linked to the camera to perform and report pedestrian and vehicle detection and tracking in 3D space. 


* YOLOv8 2D detection reports bounding box co-ordinates as ($x$ center, $y$ center, width of the box, height of the box); class name, class ID, confidence score are also extracted. YOLOv8 includes 2D tracking on these detection with BotSORT and ByteTrack which provides acceptable real-time performance but suffers from false re-id errors.  ByteTrack is used as default here. 

* An Intel depth camera ROS2 wrapper is provided by the Intel Realsense SDK (https://www.intelrealsense.com/sdk-2/) which publishes the data over `/camera_image_raw` for RGB image, `/depth` for the depth image, and `/depth_camera_info` reporting the  intrinsic cameras parameters.


<p align="center">
  <img src="./Images and videos/Masked_pedestrian.png" width="100%" />
  <br><br><i>Figure 9: Masked pedestrian tracking via YOLOv8.</i>
</p>



## Simulation

A ROS2 simulation of OpenPodcar2, is provided, using the newly released Gazebo sim. To handle time/clock synchronization issues at the software level, it is necessary that both the systems; ROS2 stack and Gazebo simulation should work on the same time. Although ROS/ROS2 provides the configurable parameter for the nodes named  \lstinline{use_sim_time} which could be set to a boolean value of either true or false, there are still some issues faced namely; lookup transforms, message filter dropping when setting the the whole NAV2 stack with Gazebo which generates lags in the system and ultimately failures. Nevertheless, Navigation2 must be implemented on the real/physical OpenPodcar2, so it makes sense to set the stack with working on wall time/system time. To achieve this condition, the gazebo plugins used in our stack Ackermann Steering plugin which deals the kinematic control for the robot, lidar sensor system plugin to receive the LaserScan data in case of using lidar, rgbd sensor system plugin for simulating the depth image and  odometry publisher plugin to get the ground-truth odometry data out from Gazebo needs to publish the data on wall time and such condition in Gazebo (making use wall time) is not a very discussed topic and in the recently introduced the new Gazebo 7 makes it more of a highly debugging task. To handle this condition, custom ROS2 nodes are created which subscribes to the gazebo output topics and publishes the topic data on wall/system time.
### Packages

#### 1. Pod2_description

This ROS2 package consists the robot's urdf files in the `xacro` directory, meshes of the robot model, sensors in the `meshes` and the `launch` directory contains the `pod2_description.launch.py` and  `pod2_description` file which launches the robot model's URDF and the world file in the Gazebo with a condition to start along the rviz2 node.


The launch file also consists the `ros_gz_bridge` package which is used to establish communication between Gazebo and ROS2. The parameter bridge is created for `/model/podcar/cmd_vel` topic from ROS -> GZ, on this topic the Ackermann system plugin publishes the twist messages.
GZ -> ROS is created for  `LaserScan` and `RGBD` based simulated sensor data which is coming from gazebo sensor system plugin, `/model/podcar/odometry` topic consists of ground-truth odometry data from Gazebo.


##### Scripts

This directory in `pod2_description` package consists of intermediate nodes which are used to convert the incoming messages over te topics `/model/podcar/odometry` , LiDAR and RGBD sensor based topics to publish on Wall time. This approach is employed to avoid the time realetd issues, tf errors and with an assumption that the simulation and the physical vehicle should work on same time.


* `odometry_wall_time.py` handles the ground truth odometry `/model/podcar/odometry` topic from GZ and publishes to ROS2 topic `/odom` with changing the time stamp to wall time.


* `laser_wall_time.py` handles the `/lidar_scan` topic from GZ laser plugin and publishes to ROS2 topic `/scan` with changing the time stamp to wall time.


* `RGBD_wall_timer.py` handles the `/rgbd_camera/depth`, `/rgbd_camera/camera_info`, `/rgbd_camera/image`, `rgbd_camera/points` topic from GZ laser plugin and publishes to ROS2 topic `/depth`, `/depth_camera_info`, `/camera/color/image_raw` and `/cloud_in` with changing the time stamp to wall time.


#### 2. Pod2_bringup

* This ROS2 package utilizes the ROS2 teleop-twist-joy pakcage, in order to control the OpenPodcar using the joystick controller in the simulation as well as in real world physical robot teleoperation. 


* Different joystick are tested namely; Logotech Extreme3dPro, generic linux usb joystick, PS2 and XBOX.
To test the joystick is connected to the system run `ls /dev/input`.


* In order to use specific joystick you might have to create the `.yaml` config file which can be referenced from (https://github.com/ros2/teleop_twist_joy/tree/humble/config) and the `launch` directory contains the `joy.launch.py` file which launches the `Joy node` and  `teleop_twist_joy_node`.
**For using any custom joystick, you might need to check which buttons and axis does what** 



I recommend using `https://flathub.org/apps/io.gitlab.jstest_gtk.jstest_gtk`. The tool also provide calibrataion for the joystick which mighht be helpful if deploying on the physical vehicle for teleoperation.



#### 3.  Pod2_navigation

Pod2_navigation package consists of the `launch`, `rviz`, `maps`, `config` directories. 

* Config directory:
   This includes the `nav2_dwb_smac.yaml` file which includes the parametrers for AMCL, BT_Navigator, Controller server, PLanner server, Global and Local Costmaps, Behaviour servers, Map server.


*  `mapper_params_slam_sync.yaml` and `mapper_params_slam_async.yaml` are the params file which are used to launch the slam-toolbox either in synchronous/asynchronous mode.


* To run the slam_toolbox for localization, we have to turn off the AMCL and map server. For this, another launch file `navigation.launch.py` is there which launches the required nodes. Now run the slam_toolbox using the launch file.

     `ros2 launch pod2_navigation async_slam.launch.py`.


* If want to build the localize using slam_toolbox, then change the mode to localization in `mapper_params_online_async.yaml`.


* The map can be saved either by command-line: ` ros2 run nav2_map_server map_saver_cli -f <name of the map>` or in rviz2 slam_toolbox plugin. More info could be found at: (https://github.com/SteveMacenski/slam_toolbox/tree/humble).


* In order to save the map with old format (.yaml and .pgm) hit the save map button in rviz2 slam_toolbox plugin and to save in the other format (serilaised), write the name of the map without any extension and  click the serial map button in the rviz2 slamtoolbox_plugin.


* The package has been tested with the `Sim_1.yaml`, `Sim_2.yaml`, `Sim_3.yaml`with corresponding pgm files.


* To use the localization with `slam_toolbox`, you have to provide the right path to the map which you are going to use.  When using slam_toolbox for localization, you do not have to provide the map file extension in the `mapper_params_onlie_async.yaml` and just the name.


* The launch directory consists of `OpenPodCar_NAV2.launch.py` which uses the default `nav2_bringup` package for launching all the nodes and takes the `parameters from the config directory. It uses AMCL for localization which will also be started.


#### Note that slam_toolbox is best suited for LiDAR based robots and struggles with RGBD sensor. The OpenPodCar2 features a single RGBD sensor is tested with slam_toolbox with rigorous parameter tuning both in simulation and real physical vehicle. However, due to less angular FOV, the laser scan matching results in sudden jumps of robot. This has been discussed in https://github.com/SteveMacenski/slam_toolbox/issues/662.  To handle this RGBD based slam method RTABMAP is adopted. 

