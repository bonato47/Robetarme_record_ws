#!/usr/bin/env python

import subprocess
import signal
import sys

def launch_my_launch_file(parameter_value):
    try:
        subprocess.run(["roslaunch", "runningfolder", "save_bag.launch", f"name:={parameter_value}"])
    except KeyboardInterrupt:
        pass

def space_callback():
    print("Space bar pressed. Hello!")
    
def run_my_python_code():
    try:
        # Replace with the command to run your other Python code
        print("run code")
        subprocess.run(["python3", "test.py"])
        pass
    except KeyboardInterrupt:
        print("run code")

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
    launch_process = subprocess.Popen(["roslaunch", "runningfolder", "save_bag.launch", f"name:={parameter_value}"])

    print("Press 'Space' to print 'Hello' or Ctrl+C to exit.")
    try:
        while True:
            key = input()
            if key == ' ':
                space_callback()
    except KeyboardInterrupt:
        pass
    finally:
        # Terminate the launch process when exiting
        launch_process.terminate()
        run_my_python_code()

if __name__ == '__main__':
    main()
