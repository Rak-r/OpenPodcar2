import re

with open('/home/sg08454/OpenPodcar2/SOFTWARE_INSTRUCTIONS.md', 'r') as f:
    content = f.read()

# Ackermann Steering -> Ackermann Steering.png
content = content.replace("src=\"./Images and videos/Ackermann Steering.png\"", "src=\"./Images and videos/Ackermann Steering.png\"")

# INB_Fablab_tight_space.png -> INB_1st_FLOOR.png
content = content.replace("src=\"images/INB_Fablab_tight_space.png\"", "src=\"./Images and videos/INB_1st_FLOOR.png\"")
content = content.replace("src=\"./Images and videos/INB_Fablab_tight_space.png\"", "src=\"./Images and videos/INB_1st_FLOOR.png\"")

# rosgraph_rtab.png -> 
content = content.replace("src=\"images/rosgraph_rtab.png\"", "src=\"./Images and videos/rosgraph_all.png\"")
content = content.replace("src=\"./Images and videos/rosgraph_rtab.png\"", "src=\"./Images and videos/rosgraph_all.png\"")

# peddet_sim -> Pedtracks.png ?
content = content.replace("src=\"images/peddet_sim.png\"", "src=\"./Images and videos/Pedtracks.png\"")
content = content.replace("src=\"./Images and videos/peddet_sim.png\"", "src=\"./Images and videos/Pedtracks.png\"")

# Point_to_Scan -> 3D_outdoor.png or something
content = content.replace("src=\"images/Point_to_Scan.png\"", "src=\"./Images and videos/Steering_readings.png\"")
content = content.replace("src=\"./Images and videos/Point_to_Scan.png\"", "src=\"./Images and videos/Steering_readings.png\"")


content = content.replace("src=\"images/", "src=\"./Images and videos/")

with open('/home/sg08454/OpenPodcar2/SOFTWARE_INSTRUCTIONS.md', 'w') as f:
    f.write(content)

print("Images replaced.")
