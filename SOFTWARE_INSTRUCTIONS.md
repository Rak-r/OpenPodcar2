# OpenPodcar2 Software architecture reference

The build instructions are user guide suffice to build and use the system, including the ROS2 software.   The following is provided as a description of the software architecture for users wishing to modify or debug the software or otherwise learn about how it works internally.

## Vehicle state

ROS2's `robot_state_publisher` and `joint_state_publisher` packages play distinct roles in broadcasting information about a robot's spatial configuration.
The `robot_state_publisher` is responsible for computing the positions and orientations of all the robot's links based on the joint states, typically provided by a URDF (Unified Robot Description Format) file. The derived information is then published as transform over topics `/tf` and `/tf_static`.  The `joint_state_publisher` package specializes in broadcasting information related to the positions, velocities, and efforts of all the joints within a robot.


## Kinematic control

OpenPodcar2 is as an Ackermann-steered vehicle.   The ROS2 community uses `Twist` as the standard for sending mobile robot motion commands (ROS REP-119), so OpenPodcar2 takes `cmd_vel:Twist` commands as inputs.    ROS2 also provides an Ackermann drive message (`ackermann_msgs/msg/AckermannDrive`) which contains fields for speed and steering angle.

ROS2 `Twist` messages can map exactly onto differential drive vehicle control, but cannot map exactly onto Ackermann control.  This is because a twist is defined as a linear velocity and a rotational velocity.   When the linear velocity is zero, a differential drive vehicle can still perform the rotational velocity by turning on the spot, but this is impossible for an Ackermann vehicle. An Ackermann vehicle can however dry turn its front steering wheels while it is stationary, which is not describable as a Twist.   To map between this, OpenPodcar2 re-interprets turn-on-spot Twist commands as dry steering commands as follows:

<p align="center">
  <img src="./Images and videos/Ackermann Steering.png" width="100%" />
  <br><br><i>Figure 6: Ackermann steering kinematic control.</i>
</p>

Ackermann steering angle represents the angle of a single (tricycle-like) front virtual wheel which can be computed using the physical vehicle's wheelbase, the turning radius. The turning radius is defined by the distance between the centre of curvature and each wheel. The curve radii for the wheels can take positive and negative values, depending on the chosen coordinate system. Typically, a Cartesian coordinate system is established with the $x$-axis aligned with the facing direction of the robot and the $y$-axis to its left. In this setup, a left turn corresponds to a positive radius, while a right turn has a negative radius. When driving straight forward, the curve radius, and consequently the Instantaneous Center of Curvature (ICC), approaches plus or minus infinity. When the ICC is at plus or minus infinity, the perpendicular lines on all wheels become parallel. For simplicity, only one wheel is considered. Following the approach, the two angles namely; inner wheel and outer wheel angle can be computed using mathematical relation.

In the conversion, the `Linear.x` field of Twist messages represents the velocity which is assumed to be same for the Ackermann vehicles. To calculate the steering angle, the physical steering limit of real-robot should be known using this the steering angle could be determined. %Considering only one wheel case for simplicity.

## Manual teleoperation

An Xbox controller is used as the manual controller.  `joy` is a standard ROS2 package which consists of node to interface this controller (or many others) to send messages of type `joy` on the topic `/joy`.

`telelop_twist_joy` is a standard ROS2 node which converts `joy` messages to `Twist` type `cmd_vel` messages.  It includes an additional DMH configured on a button on the controller used via standard ROS2 YAML parameter file (RL for XBox). This DMH button must be held down on the controller in order for any other controls to have an effect.  

The package provides scales for managing the linear and angular velocities of the twist message. To make sure that the speed scales are under safety threshold for OpenPodcar2's motor driver, which is currently set to the limit of 400, the maximum speed according to the odometry measurement is set to 0.2 m/s. To ensure this limit is followed by the `teleop_twist_joy` package, the scale in $x$ is set to 0.2 which on the low level motor driver reads 400. To test the if values are set at the high level ROS2 package, test the framework without pressing the DMH, and echo `/R4_OSMC1` topic to visualize the max range (this should read 400). Otherwise it may damage the motor driver.



## Localization and Mapping

The ROS2 ecosystem provides several alternative tools for SLAM.  OpenPodcar2 is equipped with Intel RealSense D435 RGBD camera which outputs RGB and depth image. The sensor also outputs the `PointCloud2` ROS2 message which is the standard message used by stereo and RGB-D sensors. The `PointCloud` message has been deprecated after ROS2 Foxy version.
Therefore to comply with the sensor setup and input data, we use Real-Time Appearance based Mapping (RTAB-Map) [labbe2019rtab], a graph based SLAM framework that supports RGB-D cameras by leveraging both visual appearance and depth information for 3D mapping and loop-closure detection. RTAB-Map was selected over LiDAR oriented alternatives such as 2D SlamToolbox [macenski2021slam], Hector Slam [kohlbrecher2011flexible], Cartographer [hess2016real]. Also nav2 (which is primarily a planning framework) includes an AMCL localizer-only (no mapping) similar to ROS1's AMCL.


<p align="center">
  <img src="images/INB_Fablab_tight_space.png" width="100%" />
  <br><br><i>Figure: RTAB 3D Indoor Map in a tight lab space</i>
</p>

The RTAB-Map package also provides the visual odometry named as RGBD odometry which is deployed in the vehicle to provide the pose information and `odom` to `base_link` transform. This has shown reliable results for indoor operations. Moreover, the RTAB-Map SLAM package is used to perform the the mapping and localization which takes the `odom` to `base_link` transform as input and corrects the pose information of OpenPodcar2 in the map frame. 
To ensure that the 2D occupancy grid map space is marked as free space from the RGBD camera mounted in-front of the vehicle, there is need to tweak the Grid/RangeMax, Grid/RangeMin and Grid/RayTracing according to the range of the RGBD camera. The Intel Realsense D435 mounted on the vehicle has range of 10m but offers good accuracy for 5m range. The system checked with both ranges and default is set to 5m.
The outputs are the `map` to `base_link` transform, and the corrected pose information of the robot over the topic `/localization_pose` which can be used for further applications. 

<p align="center">
  <img src="images/rosgraph_rtab.png" width="100%" />
  <br><br><i>Figure: ROS2 RTAB nodes and messages</i>
</p>

The pose only gets updated when the robot explores the environment, however to achieve continuous pose updates we can enable the RTAB-Map SLAM `map_always_update` parameter. Figure shows the 3D map of indoor lab space using RTAB-Map while Figure highlights the topics subcribed by RTAB-Map node via ros2 node graph

For more accurate odometry estimation, more RGBD sensors can be used for wider field-of-view (FOV), IMU sensors for orientation estimation can be fused together using the ros2 `robot_localization`  package. 


## Navigation



The ROS2 ecosystem includes a navigation stack,  Navigation2 (`nav2`) [macenski2020marathon2], designed to facilitate the smooth navigation of a vehicle from one pose to another while avoiding obstacles along the path. Navigation2 comprises nodes which host plugins providing  navigation capabilities, including cost map generators, planners, controllers, and recovery behaviors. OpenPodcar2 integrates these packages within its system architecture to provide onboard autonomous navigation:

* *nav_costmap_2d:* This `nav2` subpackage reads the map and publishes the global costmap.  It also reads the sensor and publishes a local costmap (which does not use any map data).  It inflates the obstacles to create costs close to them in both costmaps.
   
* *SMAC Planner:* Planners calculate a path (a.k.a. route) from a source point to a destination point.  We use `nav2`'s SMAC planner, which is designed for Ackermann steering kinematics. It implements a hybrid algorithm, smac-planner-hybrid, which combines local Reeds-Shepp/Dubin paths in open spaces with global A* around obstacles.  (It also has options to use two other algorithms). The Reeds-Sheep model is used as default for OpenPodcar2 it allows for the reversing behavior.
 
* *Dynamic Window Band controller (DWB):* Controllers (known as local planners in ROS1), transform a spatial path into a temporal trajectory, using the local costmap.    We are using DWB, which is a modified version of DWA. The DWB controller due to its collision avoidance ability is preferred as default controller for the podcar at the time of the development of the automation stack. 

* *Behaviour Tree Navigator:* A Behavior Tree action server (not messages or services) is used for communication between the planner and controller, and user goals.     User goals can include moving to a pose, but also others such as area coverage or waypoint list visiting.  It implements the NavigateToPose and NavigateThroughPoses task interfaces. 
   
* *Behaviour/recovery Servers:* For special cases of recovery from failed controls, behaviour servers add abilities to reverse and recover to a previous state.    `nav2_behaviour_server` features various kind of actions: spin, backup, wait, Assisted teleop, and Drive on-heading.

For safety, navigation requires the robot's `base_link` (the center of the robot, not the the front bumper) should be within the bounds of the map. The planner will do nothing if either the origin or destination are unknown in the map. Moreover, due to less FOV of the RGBD sensor, the global costmap warning `Robot is out of bounds` is triggered. A  short manual drive around the operating area should thus be performed to build an initial map before engaging navigation. Figure illustrates the ROS2 node graph and topics associated with the `nav2` stack. This figure provides a visual representation of the various ROS 2 nodes and their interconnections within the Nav2 framework.

<p align="center">
  <img src="./Images and videos/Podcar_Nav2_node_graph.png" width="100%" />
  <br><br><i>Figure 7: OpenPodcar2 Nav2 node graph.</i>
</p>


## Pedestrian/object detection and tracking

The RGBD camera is used for pedestrian detection and tracking as well as for SLAM.   An off-the-shelf ROS2-wrapped YOLOv8 (https://github.com/Rak-r/yolov8_ros2_OpenPodCarV2.git) is linked to the camera to perform and report pedestrian and vehicle detection and tracking in 3D space. 

YOLOv8 2D detection reports bounding box co-ordinates as ($x$ center, $y$ center, width of the box, height of the box); class name, class ID, confidence score are also extracted. YOLOv8 includes 2D tracking on these detection with BotSORT [aharon2022bot] and ByteTrack [zhang2022bytetrack] which provides acceptable real-time performance but suffers from false re-id errors.  ByteTrack is used as default here.  

An Intel depth camera ROS2 wrapper is provided by the Intel Realsense SDK (https://www.intelrealsense.com/sdk-2/) which publishes the data over `camera_image_raw` for RGB image, `depth` for the depth image, and `depth_camera_info` reporting the  intrinsic cameras parameters.

<p align="center">
  <img src="images/yolostack.png" width="100%" /> 
  <br><br><i>Figure: ROS2 nodes for pedestrian detection and tracking</i>
</p>

<p align="center">
  <img src="images/peddet_sim.png" width="45%" />
  <img src="images/Pedetsrian_crossing.png" width="45%" />
  <br><br><i>Figure: Pedestrian detection results in simulation (left) and real-world deployment on the physical OpenPodcar2 platform (right).</i>
</p>

All messages are published under the namespace of the `/yolo`. It is used  with similar structure to ROS2's standard `vison_msgs` message types. The 2D detection node subscribes to camera RGB messages and publishes `/Detection` messages. The ROS2 YOLOv8's tracker node subscribes to these Detection2D messages, and keeps track of the objects over each frame, publishing `DetectionArray` messages showing the tracks. Figure shows the detection and tracking nodes in ROS2 followed by  Figure illustrating pedestrian detection outputs from the unified perception stack in simulation (left) and during execution on the physical OpenPodcar2 platform (right), confirming functional equivalence between simulated and real-world operation.


The ROS2 YOLOv8 wrapper's 3D projection then takes as input these 2D tracks and the $z$-coordinate from the original RGBD image and outputs 3D locations.   It publishes the 3D bounding boxes in real-world coordinates ($x$, $y$ and $z$) along with the dimensions (length, width and height) in meters as `BoundingBox3D` messages. 

<p align="center">
  <img src="./Images and videos/Masked_pedestrian.png" width="100%" />
  <br><br><i>Figure 8: Masked pedestrian tracking via YOLOv8.</i>
</p>

The 3D bounding box messages reporting the center position of pedestrians are fed to a Kalman filter as noisy observations.  This creates a new message containing both smoothed location estimates and speed estimates.  
Figure illustrates the full pedestrian detection and tracking stack deployed on the physical OpenPodcar2 platform. The left panel shows the modified depth image (masked_depth), in which regions corresponding to YOLOv8 2D pedestrian detections are removed and marked as “no data”. This masked depth image is generated by feeding the detected bounding boxes back to the perception wrapper.
The same masked depth stream is provided to the localisation, mapping, and navigation components.
As shown in the right panel of Figure, the vehicle operates in mapping mode while the pedestrian remains detected via 3D markers, but is excluded from the depth data used for feature extraction and costmap updates. This prevents dynamic pedestrian motion from perturbing localisation or triggering unnecessary path replanning.

## Simulation

A ROS2 simulation of OpenPodcar2, is provided, using the open source igntion Gazebo simulator. To handle time synchronization issues at the software level, it is necessary that both the ROS2 stack and Gazebo simulation should work on the same time. Although ROS2 provides the configurable parameter for the nodes named  `use_sim_time` which could be set to a boolean value of either true or false, there are still some issues faced: lookup transforms, message filter dropping when setting the the whole NAV2 stack with Gazebo which generates lags in the system and ultimately failures. Nevertheless, Navigation2 must be implemented on the real/physical OpenPodcar2, so it makes sense to set the stack with working on wall time/system time. To achieve this condition, the Gazebo `ackermann`  steering plugin is used in our stack which deals the kinematic control for the robot, lidar sensor system plugin to receive the `LaserScan` data in case of using lidar, `rgbd` sensor system plugin for simulating the depth image and  odometry publisher plugin to get the ground-truth odometry data out from Gazebo needs to publish the data on wall time and such condition in Gazebo (making use wall time) is not a very discussed topic and in the ignition Gazebo fortress makes it more of a highly debugging task. To handle this condition, custom ROS2 nodes are created which subscribes to the gazebo output topics and publishes the topic data on wall/system time. 



<p align="center">
    <img src="images/ROS2_GZ_node_graph.png" width="100%" />
    <br><br><i>Figure: ROS2 GZ Bridge node graph with custom nodes setup.</i>
</p>

<p align="center">
    <img src="images/rosgraph_all.png" width="100%" />
    <br><br><i>Figure: ROS2 NAV2 full stack setup with Gazebo sim.</i>
</p>

To integrate ROS2 and newly released version of Gazebo, the community has introduced a new package called `ros_gz_bridge` which features an interface exchange between ROS2 messages and Gazebo protobuf messages. 

The package could be used to bridge incoming topics from ROS2 towards Gazebo or vice-versa. The other approach to generate the communication between ROS and Gazebo, is the direct embedding of ROS nodes into Gazebo plugin style codes which is still provided for application specific tasks. Using the above mentioned package, we created nodes which subscribes to bridged topics from Gazebo to ROS2, `/lidar_scan`, `/model/podcar/odometry`, `/rgbd_camera/image`, `/rgbd_camera/depth_image`, `/rgbd_camera/points` and `/rgbd_camera/camera_info` and the message field header which represents the timestamp is set to wall/system time. The nodes `scan_publisher_node`, (`/scan` topic), `odometry_publisher` (`/odom` topic), `RGBD_node` outputs the following topics with same data and with system timestamps. The custom `ros_gz_bridge` node with messages established for OpenPodcar2 is shown in Figure. In order to provide the transforms on the system time, a transform broadcaster node is created which subscribes to the `/odom` topic, to broadcast the `odom` to `base_link` transform for mapping, localization and navigation. 
The full set of working nodes and active topics in simulations is shown in Figure. 


The `pod2_description` package contains the mesh files for loading the robot in `rviz` and for simulation purposes. To make the full custom stack operate on single time source, following custom nodes were created:

* `laser_sim2real.py:`  In case of using a simulated lidar sensor this node subscribes the lidar scan topic from GZ laser/lidar plugin and publishes `sensor_msgs/msg/LaserScan` to ROS2 over topic `/scan` with changing the time stamp to wall time.

* `odometry_wall_time.py:` The node subscribes the ground truth odometry topic from GZ and publishes `nav_msgs/msg/Odometry` to ROS2 over topic `/odom` with changing the time stamp to wall time. The node also broadcasts a transform between `odom` and `base_link`.

* `RGBD_wall_timer.py:` The node subscribes the `rgb`, `depth_image`, `pointcloud2` and `camera info` topic from GZ RGBD camera plugin and publishes `sensor_msgs/msg/Image` to ROS2 over the topics `/depth`, `/depth_camera_info`, `/camera/color/image_raw`  and `/cloud_in` with changing the time stamps to wall time. The naming conventions here are focused to be the same as what the real RGBD sensor publishes.
 
The `pod2_bringup` package consist of all the control nodes for simulation which utilizes the ROS2 `teleop_twist_joy` package to control the the robot using a game pad. The system is tested with a branded XBox game pad and a compatible generic USB gamepad. The gamepads must be calibrated properly.


<p align="center">
    <img src="images/Point_to_Scan.png" width="100%" />
    <br><br><i>Figure: Simulated world with map in `rviz` along with `PointCloud2` for camera sensor</i>
</p>



The `pod2_navigation` package consists all the scripts referenced and modified from the official release [macenski2020marathon2]. For simulation tests, we have tested the different level of the stack in simple custom world created to monitor how the podcar performs in tight environments. For this, the package also involves custom built maps. `nav2` is then launched on the prebuilt map along with SLAM in localization mode. Furthermore, the `nav2` stack is also tested without providing the any pre-built map and performing actual SLAM with autonomous exploration. Figure illustrates the world in Gazebo with RGBD camera mounted in front of OpenPodcar2 and correspondingly the PointCloud2 and LaserScan topics in a map built using RTAB-Map visualized in rviz2.






## ROS2 stack callibration

ROS2 stack parameters have been tuned to match the hardware platform design.   Where new builds deviate from the original design it is likely that local retuning will be needed. The following provides some suggestions.

Initially with default parameters setup, the DWB controller failed to make any progress with entering into recoveries and for straight line forward goals huge oscillations and jerks were observed. After fine-tuning the acceleration and deceleration parameters the jerks were reduced to minimal level. The usage of rotate to goal critic was removed due to Ackermann kinematics. Following this, weights for PathAlign and GoalAlign critics have increased to make the vehicle stay on the global plan. Moreover, the oscillation related parameters are slightly tuned.

The robot_footprint parameter was carefully tested and set slightly larger than the actual vehicle dimensions to minimize close obstacle contacts. The obstacle avoidance behavior was evaluated indoors by setting close obstacle goals and adjusting the inflation_radius for the local costmap. The system effectively maintained close driving behavior without collisions.

Due to the frequent plan update, it was sometimes observed that the generated plan was not able to be followed by the controller server. The parameter which plays a crucial role for Ackermann model is `min_turning_radius` which needs to match the measurement from the real-physical vehicle. The term has been manually measured for OpenPodcar2 and was approximately resulted to 2.05m. For longer goals, it is observed due to less range of RGBD sensor, the planner server struggles to generate large plans. To improve planning for large goals, the dimension of the global costmap was increased to make the planner less constraint and it was observed that longer goals of more than 20m are generated. Tuning was required for the penalty weights to minimise heavily curve paths which might be difficult for the controller server to follow.
