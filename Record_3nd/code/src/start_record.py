#!/usr/bin/env python

import subprocess
import signal
import sys
import time

from transformCsv import mainTransform


def main():
    
    if len(sys.argv) != 2:
        print("Usage: python script_name.py name_to_save")
        return

    parameter_value = sys.argv[1]
    task =1 
    if not (parameter_value.find("shot") == -1):
        task = 0
    # # Set up Ctrl+C handler to exit the launch process
    # signal.signal(signal.SIGINT, lambda sig, frame: run_my_python_code())
    if task == 1:
        l1 = subprocess.Popen(["roslaunch", "runningfolder", "main_surf_and_shot.launch"])
    else:
        l1 = subprocess.Popen(["roslaunch", "runningfolder", "vrpn_optitrack.launch"])
    # Add a delay of 3 seconds

    time.sleep(6)
    print("Press 'Enter' to start record the ROS launch file.")
    input()

    # Launch the ROS launch file
    if task == 1:
    	l3 =subprocess.Popen(["roslaunch", "runningfolder", "save_bag_surface.launch", f"name:={parameter_value}"])
    else:
	    l3 = subprocess.Popen(["roslaunch", "runningfolder", "save_bag_shotcrete.launch", f"name:={parameter_value}"])
    print("Press 'Enter' to stop record and plot")
    input()
    l1.terminate()

    l3.terminate()
    time.sleep(8)
    print("exit well done running plot, please wait boss")
    mainTransform(parameter_value)

    
if __name__ == '__main__':
    main()
