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
        
        # Launch the second ROS launch file
        l2 = subprocess.Popen(["roslaunch", "netft_rdt_driver", "ft_sensor.launch"])
    except KeyboardInterrupt:
        l1.terminate()
        l2.terminate()


def space_callback(parameter_value):
        print("saving target postition...")
        subprocess.run(["python3", "targetToCsv.py", parameter_value])    
        print("target position saved")
        print("saving bias FT sensor...")
        subprocess.run(["python3", "biasToCsv.py", parameter_value])    
        print("bias FT saved")

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
    print("Press 'Space' to save target and bias or Ctrl+C to exit.")
    try:
        while True:
            key = input()
            if key == ' ':
                space_callback(parameter_value)
                # launch_process.terminate()

    except KeyboardInterrupt:
        pass
    finally:
        print("stop")
        # Terminate the launch process when exiting
        # launch_process.terminate()

if __name__ == '__main__':
    main()
