# OpenPodCar_V2 Hardware Instructions

## I. Physical R4 interface

* The physical hardware interface is based around the R4 open-source hardware board  R4. 


* To establish the communication between the physical hardware board with high level ROS2 stack in order to perform manual teleoperation, Autonomous driving operation via NAV2, UDP protocol is utilized. There are three sets of ROS2 hardware nodes namely; `/R4_Websockets-Clients` which is responsible to establish the connection to transfer the data packets from R4 hardware board to ROS2 over the topic named `/R4` which gets unpacked by the second node `/R4_Publisher` to publish the individual component sub-messages mainly, steer voltage reading, main OSMC motor driver readings over the topics `/R4_AINSTEER` and `/R4_OSMC1`. 


* Following this, these topics are subscribed by ROS2 nodes to control the steering and speed of the vehicle via gamepad for manual teleoperation and via \lstinline{nav2} for autonomous driving tasks.

* The output of either manual teleoperation or `nav2` is same and published over the standard ROS2 message type `Twist` over `/cmd_vel` topic and this information is then subscribed by the third node named as `/R4_Receiver` .


<p align="center">
  <img src="./Images and videos/R4onperspex.png" width="100%" />
  <br><br><i>Figure 2: Physical R4 electrical interface.</i>
</p>

## II. Sensors

OpenPodcar2 uses a single depthcam mounted on the front of the vehicle. This  outputs RGB and depth image data as standard ROS2 `Image` messages, along with pointcloud data over `PointCloud2` messages. `PointCloud2` messages are produced directly by the RGBD camera, as for lidar sensors.

<p align="center">
  <img src="./Images and videos/d435.png" width="100%" />
  <br><br><i>Figure 3: Intel RealSense D435 Depth Camera.</i>
</p>

## III. Bill of Materials

| **Name** | **Component** | **USD** | **Source** | **Interface** | **Implementation** |
|---|---|---:|---|---|---|
| Donor vehicle | Phiseng TE-889XLSN mobility scooter (branded as Shoprider Traverso) | 6000 new or 1000+ used | [Shoprider Traverso](https://romamedical.co.uk/shoprider-traveso/) | Generic (motor and brake control voltages; mechanical steering linkage) | Patented |
| R4 | R4 OSH PCB robot control board | 300 | [JOH article](https://doi.org/10.5206/joh.v9i1.22878) | CERN-OHL-W | CERN-OHL-W |
| DepthCam | Intel RealSense D435 | 300 | [Intel RealSense D435](https://store.intelrealsense.com/buy-intel-realsense-depth-camera-d435.html) | ROS2 standard | Closed |
| OSMC | OSMC motor driver with 24V fan kit | 230 | [Robot Power catalog](https://www.robotpower.com/catalog/) | Generic | Public domain |
| Linear actuator | Gimson Robotics GLA750-P 12V DC (100 mm stroke, 240 mm install) | 100 | [Gimson Robotics actuator](https://gimsonrobotics.co.uk/products/gla-q40-12v-250n-compact-fast-travel-linear-actuator-with-encoder?variant=47116053905684) | Generic | Generic |
| Laptop stand | Pyle | 60 | [Laptop stand](https://uk.redbrain.shop/p/00132017804903) | Generic | Generic |
| Motor relay | Ripca 12V, 200A REL-1/H-DUTY/200A/12V | 40 | [Ripca relay](https://parts.easycabin.co.uk/products/relay-200a-12volt-heavy-duty) | Generic | Generic |
| 24/12DCDC | 20A | 40 | [Sure Marine Service](https://www.suremarineservice.com/Heat/Converters/DC2412-20C_2.html) | Generic | Generic |
| Fuses (5A, 12A, 2A, 10A, 20A, 100A ×2) | Blade fuses and holders | 40 | [RS Components fuse kit](https://uk.rs-online.com/web/p/fuse-kits/2199556) | DIN 72581 standard | Generic |
| Battery charger | Nexpeak, 10A 12V/24V car battery charger | 25 | [Amazon listing](https://www.amazon.co.uk/Automatic-Temperature-Compensation-Motorcycle-Batteries-Red/dp/B094VQ88X2) | Generic | Closed |
| DBH12 | Dual H-bridge 12V motor driver | 25 | [Amazon listing](https://www.amazon.co.uk/Akozon-DC5-12V-0A-30A-Dual-channel-Arduino/dp/B07H2MDXMN) | Generic | Closed |
| 24/19DCDC | 5A | 20 | [Amazon listing](https://www.amazon.co.uk/Converter-Waterproof-Regulator-Printers-Surveillance/dp/B087WWTSC4) | Generic | Generic |
| Wifi router | Any, 12V powered | 20 | ... | IEEE WiFi standard | Closed |
| DMH relay | SRD-05VDC-SL-C | 13 | [Amazon listing](https://www.amazon.co.uk/HUAREW-1-channle-optocoupler-isolation-triggering/dp/B0B52RPY43/) | Generic | Generic |
| 8-way relay Bank | 8-Channel 5V Relay Module | 13 | [SainSmart 8-channel relay module](https://www.sainsmart.com/products/8-channel-5v-relay-module) | Generic | Generic |
| Perspex board, ×3 | 400 × 200 × 5 mm | 10 | [Amazon listing](https://www.amazon.co.uk/Perspex-Black-Acrylic-Plastic-Choose/dp/B09PRDRGXS/) | Generic | Generic |
| Circuit breaker | DZ47-63 C10 | 10 | [Amazon listing](https://www.amazon.co.uk/RKURCK-DZ47-63-Low-voltage-Miniature-Circuit/dp/B0C3CQVWTS) | ISO standard | Generic |
| DMH | Philmore 30-825 SPST hand-held push button switch | 10 | [Amazon listing](https://www.amazon.com/Hand-Held-Button-Switch-30-825/dp/B00T6RCGNC) | Generic | Generic |
| USB 3.0 | USB cable | 7 | [Amazon listing](https://www.amazon.co.uk/AAA-Products-USB-3-0-Cable/dp/B07778DHSM) | Generic | Generic |
| Alu brackets | 3 mm thickness aluminium plate; 2 pieces cut to 137 × 17 mm and 152 × 25 mm | 5 | [Amazon listing](https://www.amazon.co.uk/Aluminium-Sheet-plate-0-5mm-aluminium/dp/B0FHMDML7S/) | Generic | Generic |
| 12/5DCDC | 10A | 5 | [Amazon short link](https://amzn.eu/d/4D8Er8h) | Generic | Generic |
| Fan | Cooling fan for OSMC motor driver | 4 | [eBay listing](https://www.ebay.co.uk/p/26035083262) | Generic | Public domain |
| Connectors | XT60, IDC headers, ribbon cables, Wago connectors, velcro, heatshrink, ring terminal, zip ties, JST (three pin) | ... | ... | Generic | Generic |
| Nuts, bolts, standoffs | M2-M6 metal and plastic | ... | ... | ISO standard | Generic |
| Tools | Hand toolkit, soldering tools, power drill, axle stands | ... | ... | Generic | Generic |


## IV. Calibration

### Depthcam calibration


<p align="center">
  <img src="./Images and videos/Depthcam_calib.jpg" width="100%" />
  <br><br><i>Figure 4: Depthcam calibration setup.</i>
</p>



* The depthcam needs physical calibration in order to achieve reliable SLAM and mapping operation. For this,  place an object 10m away at the same height as the camera from the ground. 


* Adjust camera to ensure that the object appears in the center of the camera image (same height measurement at different distances from the camera). This calibration is essential to verify that the camera is mounted parallel to the ground to avoid irregularities in the mapping which may consider floor as an obstacle.


### Steering calibration


* To calibrate the Ackermann steering angles on both left and right turnings various voltages are sent to the linear actuator and both inner and outer wheel angles are measured. The output result shown that the steering mechanism can be approximated as linear with some fluctuations while small turning angles.


* The mapping between steering angle and desired linear actuator voltage then could be computed using linear regression fit.

<p align="center">
  <img src="./Images and videos/Steering_readings.png" width="100%" />
  <br><br><i>Figure 5: Steering mechanism calibration readings.</i>
</p>
