#!/usr/bin/env python

import subprocess
import signal
import sys
import time

def launch_my_launch_file(parameter_value):
    try:
        # Launch the first ROS launch file
        l1= subprocess.Popen(["roslaunch", "runningfolder", "vrpn_optitrack.launch"])

        # Add a delay of 3 seconds
        time.sleep(2)

    except KeyboardInterrupt:
        l1.terminate()


def space_callback(parameter_value):
        print("saving one postition...")
        subprocess.run(["python3", "KULToCsv.py", parameter_value])    
        print("one position saved")

def space_callback_housing(parameter_value):
        print("saving housing postition...")
        subprocess.run(["python3", "KULToCsv_housing.py", parameter_value])    
        print("one position saved")


def run_my_python_code():
    try:
        # Replace with the command to run your other Python code

        pass
    except KeyboardInterrupt:
        print("exit")

        pass

def main():
    
    if len(sys.argv) != 2:
        print("Usage: python script_name.py name_to_save")
        return

    parameter_value = sys.argv[1]
    # # Set up Ctrl+C handler to exit the launch process
    # signal.signal(signal.SIGINT, lambda sig, frame: run_my_python_code())
    
    print("Press 'Enter' to launch the ROS launch file.")
    input()

    # Launch the ROS launch file
    launch_my_launch_file(parameter_value)
    print("Press 'Enter' to save KUL stuff and calib  or Ctrl+C to exit.")
    input()
    space_callback_housing(parameter_value+"_housing")

    i = 0
    while i <= 7:
        input()
        parameter = parameter_value +"calib"+str(i)
        space_callback(parameter)
        i = i+1

                
if __name__ == '__main__':
    main()
