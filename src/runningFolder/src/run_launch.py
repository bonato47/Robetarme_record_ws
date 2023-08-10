#!/usr/bin/env python

import sys
import rospy
import signal
import subprocess

def run_my_launch_file(parameter_value):
    try:
        # Replace with the appropriate roslaunch command
        subprocess.run(["roslaunch", "runningfolder", "save_bag.launch", f"name:={parameter_value}"])
    except KeyboardInterrupt:
        pass
def run_my_python_code():
    try:
        # Replace with the command to run your other Python code
        print("run code")
        subprocess.run(["python3", "test.py"])
    except KeyboardInterrupt:
        print("run code")

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

    rospy.init_node('my_ros_node', anonymous=True)
    rate = rospy.Rate(1)  # 1 Hz

    while not rospy.is_shutdown():
        space_key = input("Press Enter to print 'Hello', or Ctrl+C to quit: ")
        if space_key == '':
            space_callback()
        rate.sleep()

if __name__ == '__main__':
    main()

