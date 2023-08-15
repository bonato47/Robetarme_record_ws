#!/usr/bin/env python

import subprocess
import signal
import sys

def launch_my_launch_file(parameter_value):
    try:
        subprocess.run(["roslaunch", "runningfolder", "vrpn_optitrack.launch"])
    except KeyboardInterrupt:
        pass

def space_callback(parameter_value):
        print("run code")
        subprocess.run(["python3", "targetToCsv.py", parameter_value])    
        print("code done")
        
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
    launch_process = subprocess.Popen(["roslaunch", "runningfolder", "vrpn_optitrack.launch"])

    print("Press 'Space' to print 'Hello' or Ctrl+C to exit.")
    try:
        while True:
            key = input()
            if key == ' ':
                space_callback(parameter_value)
                launch_process.terminate()

    except KeyboardInterrupt:
        pass
    finally:
        # Terminate the launch process when exiting
        launch_process.terminate()

if __name__ == '__main__':
    main()
