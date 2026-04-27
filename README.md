# OpenPodcar2

OpenPodcar2 is a donor scooter vehicle which is transformed into autonomous vehicle with the integration of Robot Operating
System (ROS) with the added support of newly released ROS2. The vehicle used for the implementation of our research and experiments named as Pihsiang TE-889XLSN hard-canopy scooter (branded in UK as ShopriderTraverso) (found here: https://www.smartscooters.co.uk/Traveso-Mobility-Scooter).
![IMG_6667](https://github.com/Rak-r/OpenPodCar_V2/assets/85680564/d19d6d02-5144-453d-9e30-7fc675c42a9b)

This is an Open Source Hardware and Software platform for Autonomous driivng research applications.


#### Development and testing credit of hardware platform named R4 board (R4: rapid reproducible robotics research open hardware control system https://ojs.lib.uwo.ca/index.php/openhardware/article/view/22878) is given to Mr. Chris Waltham (University of Lincoln,UK) and Dr. Charles Fox (https://staff.lincoln.ac.uk/4311dbb7-1b10-4844-bba9-20f527168e7b)  (University of Lincoln,UK).


## Table of Contents
I. [General Info](#general-info)

II. [Hardware Description](HARDWARE_INSTRUCTIONS.md)
   - [Physical R4 interface](HARDWARE_INSTRUCTIONS.md#i-physical-r4-interface)
   - [Sensors](HARDWARE_INSTRUCTIONS.md#ii-sensors)
   - [Bill of Materials](HARDWARE_INSTRUCTIONS.md#iii-bill-of-materials)
   - [Calibration](HARDWARE_INSTRUCTIONS.md#iv-calibration)

III. [Software Description](SOFTWARE_INSTRUCTIONS.md)
   - [Kinematic Control](SOFTWARE_INSTRUCTIONS.md#kinematic-control)
   - [Manual Teleoperation](SOFTWARE_INSTRUCTIONS.md#manual-teleoperation)
   - [Localization and mapping](SOFTWARE_INSTRUCTIONS.md#localization-and-mapping)
   - [Navigation](SOFTWARE_INSTRUCTIONS.md#navigation)
   - [Pedestrian detection and tracking](SOFTWARE_INSTRUCTIONS.md#pedestrian-detection-and-tracking)
   - [Simulation](SOFTWARE_INSTRUCTIONS.md#simulation)

IV. [Software setup](#software-setup)

V. [Testing installation](#testing-installation)

VI. [Installation for Openpodcar2](#installation-for-openpodcar_v2)

VII. [Docker support for OpenPodcar2](#docker-support-for-OpenPodcar2)

VIII. [Operator instructions](#operator-instructions)



## For hardware setup, bill of materials, and calibration details jump to the [Hardware Description](#hardware-description). For running or testing the stack in simulation or real physical vehicles, refer to [Software setup](#software-setup) followed by [Operator instructions](#operator-instructions).


## I. <a name="general-info"></a> General Info

This project is an open source hardware and software platform based upon its predecessor OpenPodcar [cite OpenPodcar here]. 

* OpenPodcar2 extends OpenPodcar’s design for robust long-term operation. It replaces OpenPodcar’s entire electronics system with new electronics based on the open source hardware R4 [27]. R4 (Rapid Reproducible Robotics Research) is a general purpose medium-sized robotics (i.e. robots capable of transporting a human or similar load) control board, developed to high robustness.
* OpenPodcar2 also replaces OpenPodcar’s entire ROS self-driving software stack with a new ROS2 stack, which are interfaced to R4 electronics and which are robust at the software level for long-term driving – ROS2 being targeted at robust industrial robotics.
* OpenPodcar2 replaces all physical connectors used in OpenPodcar with new robust connectors able to withstand tilts and vibrations of the vehicle.



## II. <a name="hardware-description"></a> Hardware Description

Complete hardware instructions, including the Physical R4 Interface, Sensors, Bill of Materials and Calibration, can be found in the [HARDWARE_INSTRUCTIONS.md](HARDWARE_INSTRUCTIONS.md) file.

## III. <a name="software-description"></a> Software description

Complete software instructions can be found in the [SOFTWARE_INSTRUCTIONS.md](SOFTWARE_INSTRUCTIONS.md) file.

## IV. <a name="software-setup"></a> Software setup


1. Ubuntu 22.04


2. ROS2 Humble full desktop install: https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html

3. Install colcon for package building: `sudo apt install python3-colcon-common-extensions`

4. Install rosdep for resolving package dependencies: `sudo apt-get install python3-rosdep`

### NOTE:
OpenPodcar2 stack uses RMW cycloneDDS, this might be missed by rosdep  command. It is recommended to verify or to install seperately using command.
`sudo apt install ros-humble-rmw-cyclonedds-cpp`

3. Gazebo Fortress binary install: https://gazebosim.org/docs/fortress/install


4. The only difference between the Gazebo Fortress and Gazebo Garden is the ros-gz integration package is to build from source for Gazebo Garden while if you are using Gazebo Fortress, the ros_gz package will be installed by binary installation.


5. Gazebo Fortress uses the ignition namepsace when dealing with plugins and setting frame ids for the robot in URDFs or SDFs.

6. Docker installation: https://docs.docker.com/engine/install/ubuntu/ 


## V. <a name="testing-installation"></a> Testing Installation

1. To test that ROS2 is installed properly.
* Open bashrc and add the folowing and save it. `source /opt/ros/humble/setup.bash`.


* Open two terminals, in first run: `ros2 run demo_nodes_cpp talker`, you should see  `hello` in the console.


* In other terminal, run: `ros2 run demo_nodes_py listener`, you should see `I Heard`.


* In order to keep the nodes communication robust, set the `ROS_DOMAIN_ID` in your bashrc. For example: `export ROS_DOMAIN_ID=0`


2. To test the Gazebo Fortress is installed on the system, in the terminal run: `ign gazebo`.If it launches, you'll see the simulation software window.


3. To test the ros_gz package, source the workspace of the package and try the following command:



* `ros2 run ros_gz_bridge parameter_bridge /chatter@std_msgs/msg/String@gz.msgs.StringMsg` and view the topic in other terminal using: `ros2 topic list -t`



## VI. <a name="installation-for-openpodcar_v2"></a> Installation for OpenPodcar2

To use this package for testing and running simulations using gazebo and ROS2 follow the below instructions:


1. If using Gazebo Fortress, clone this repo following below commands. 



* Select the directory where you want to clone the project (by default is /home).


* Clone the repository using: `git clone --recurse-submodules -b Fortress https://github.com/Rak-r/OpenPodcar2.git`



2. After cloning the repository, you should have `pod2_description`, `pod2_bringup`, `pod2_navigation`, `pod2_sensor_tools`, `pod2_rtabamap`, `pod2_msgs`in your `src` directory.



3. To avoid package dependencies error, try running: `rosdep update && rosdep install --from-paths src --ignore-src -y`. 



4.  Now, build the packages:  `colcon build --symlink-install`. 


* This will build the packages and the `--symlink-install` is used to make changes in the packages in src directory and also changes in the install dircetory without re-building the package.

5. If everything works well, you will have three directories alomg with `src` named `install`, `build` ad `log`.


6. Once the package is build successfully, open bashrc and add : `source /home/<usr_name>/OpenPodcar2/install/setup.bash`


* **For example** : `source /home/<usr_name>/ros2_ws/install/setup.bash`. Replace `<usr_name>` with your user name, get using `pwd` command.

## VII. <a name="docker-support-for-OpenPodcar2"></a> Docker support for OpenPodcar2

The docker version is supported for ROS2 humble and gazebo Fortress due to LTS version of gazebo at the time project development. In future more version suppport will be added. Follow the below instructions for using docker version of OpenPodcar2 with simulation.


1.  After cloning the repository from same above instructions, make sure docker is installed correctly.

2. Install rocker in the local machine to run GUI applications without any hastle inside the container.



` pip3 install rocker`

3. Build the image:     `docker build -t openpodcar2_docker .`

4. Run the container with rocker: `rocker --x11 openpodcar2_docker`.


#### The above will build the container with custom ros2 packages for all tele-operation, mapping and navigation. If want to build the perception stack as well, then build the image with argument in below command.


5. `docker build --build-arg INCLUDE_YOLO=true -t openpodcar2_docker .`

6. Source ros2 and the workspace before running any ros2 nodes or launch files as done in normal local machine setup.

7.  Test the setup by running the below:



`ros2 launch pod2_description pod2_description.launch.py scan_node:=false rgbd_node:=true`

## VIII. <a name="operator-instructions"></a> Operator instructions

Openpodcar_v2 has been tested in both gazebo simulation and real physical envrionment (indoor/outdoor). Follow the below sections for running the vehicle in simulation and real physical world.

## Simulation guide

Gazebo Fortress is used for the simulation of OpenPodcar2. The new gazebo features more functionalities with enhanced inetrface. As our robot behaves as car-like robot and features Ackermann-Steering kinematics. To maintain this behaviour in simulation the new gazebo now has an Ackermann system plugin which could be used according the robot configuartions. The plugin outputs standard `Twist` messages of field `linear.x` and `angular.z`. This also outputs the odometry information which might not be the correct odometry for the whole robot instead it is the odometry information for steering.





#### If you want to launch the PodCar with Lidar enabled, run the below launch file:

* Launch along with Rviz: `ros2 launch pod2_description pod2_description.launch.py rviz:=true scan_node:=true rgbd_node:=false`



#### If you want to launch the PodCar with depth camera enabled, run the below launch file:


* Launch along with Rviz: `ros2 launch pod2_description pod2_description.launch.py rviz:=true scan_node:=false rgbd_node:=true`


This above will launch the simulation in gazebo and don't forget to turn on the play pause button to run the simulation. 
To view the active topics in ros2, use `ros2 topic list -t` in the terminal window.
To view active topics in gazebo, use `gz topic -l` in the terminal window.
[Podcar_V2_GZ_garden.webm](https://github.com/Rak-r/OpenPodCar_/assets/85680564/26ea85f9-a46d-4f53-b81a-1f23425ab1f7)



#### Simulation Teleoperation and Autonomous operation

1. Start gamepad to publish twist to gazebo: `ros2 launch pod2_bringup generic_gamepad.launch.py`

2. Start the rtabmap rgbd odometry and slam: ` ros2 launch pod2_rtabmap rtabmap_sim.launch.py`

3. Launch NAV2 stack: `ros2 launch pod2_navigation OpenPodCar_NAV2_sim.launch.py slam:=false amcl:=false`

After mapping, if want to start the NAV2 stack in pre-build map, rtabmap can be started in localization mode. In order to autonomous drive while mapping the above  could be just followed.



## Physical vehicle Tele-operation & Autonomous operation

To launch the physical OpenPodcar2 with teleoperation mode, the higher-level incoming game-pad commands as Twist message `linear.x, angualr.z` are converted to R4 protocol message which controls the main driver motor for forward and backward movement and linear actuator for controlling the steering for the OpenPodcar2. 

To start the physical vehicle for tele-operation, after building the OpenPodCar2 packaghe from following above instruction.

1. Start the R4-ROS2 communication nodes using the launch file:

`ros2 launch pod2_bringup R4_ros.launch.py teleop_node:=true`

2. Launch the robot model: `ros2 launch pod2_description pod2_description.launch.py rviz:=true`

3. Start the camera sensor along with point to laserscan node: `ros2 launch pod2_sensor_tools point_to_scan.launch.py`

4. Start the rtabmap rgbd odometry and slam: ` ros2 launch pod2_rtabmap rtabmap.launch.py`

5. Launch NAV2 stack: `ros2 launch pod2_navigation OpenPodCar_NAV2.launch.py slam:=false amcl:=false`

After mapping, if want to start the NAV2 stack in pre-build map, rtabmap can be started in localization mode. In order to autonomous drive while mapping the above  could be just followed.


## Images and Videos

### Simulation OpenPodcar2 with Pedestrian detection and NAV2 operation


https://github.com/user-attachments/assets/e513bdaa-67ae-4721-bcec-ed717356f360


### OpenPodcar2 on outdoor operation

<p align="center">
  <img src="./Images and videos/Podcar2_outdoor.jpg" width="100%" />
</p>




### Outdoor 3D map built using RTABMAP and single rgbd sensor (intel realsense D435)

<p align="center">
  <img src="./Images and videos/3D_outdoor.png" width="100%" />
</p>



### Autonomous drive tight indoor
   

https://github.com/user-attachments/assets/48aa4406-728c-42f7-9629-9f4f719aca1d


