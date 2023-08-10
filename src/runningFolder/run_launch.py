#!/usr/bin/env python

import sys
import signal
import subprocess
import keyboard

def run_my_launch_file(parameter_value):
    try:
        # Replace with the appropriate roslaunch command
        subprocess.run(["roslaunch", "runningFolder", "save_bag.launch", f"name:={parameter_value}"])
    except KeyboardInterrupt:
        pass
def run_my_python_code():
    try:
        # Replace with the command to run your other Python code
        subprocess.run(["python", "path_to_your_script.py"])
    except KeyboardInterrupt:
        pass
    
def space_callback(event):
    print("Hello")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script_name.py name_to_save")
        return

    parameter_value = sys.argv[1]

    run_my_launch_file(parameter_value)
    
    # Set up Ctrl+C handler to run roslaunch
    signal.signal(signal.SIGINT, run_my_python_code)

    # Set up space bar callback
    keyboard.add_hotkey('space', space_callback)

    signal.pause()

if __name__ == '__main__':
    main()

