#!/bin/bash

gnome-terminal --tab -e "sh -c 'roslaunch opti_track_ros_interface vrpn_optitrack.launch'" 
gnome-terminal --tab -e "sh -c ' roslaunch xsens_mti_driver xsens_mti_node.launch '" 
