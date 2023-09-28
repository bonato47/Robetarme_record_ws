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
    # # Set up Ctrl+C handler to exit the launch process
    # signal.signal(signal.SIGINT, lambda sig, frame: run_my_python_code())
    l1 = subprocess.Popen(["roslaunch", "runningfolder", "vrpn_optitrack.launch"])
    # Add a delay of 3 seconds
    time.sleep(2)
    # Launch the second ROS launch file
    l2 = subprocess.Popen(["roslaunch", "netft_rdt_driver", "ft_sensor.launch"])
    

    time.sleep(4)
    print("Press 'Enter' to start record the ROS launch file.")
    input()

    # Launch the ROS launch file
    l3 =subprocess.Popen(["roslaunch", "runningfolder", "save_bag.launch", f"name:={parameter_value}"])
    print("Press 'Enter' to stop record and plot")
    input()
    l1.terminate()
    l2.terminate()    
    l3.terminate()
    time.sleep(4)
    print("exit well done running plot, please wait boss")
    mainTransform(parameter_value)

    
if __name__ == '__main__':
    main()
