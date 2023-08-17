#!/usr/bin/env python

import subprocess
import signal
import sys
import rospy
from geometry_msgs.msg import WrenchStamped




class TimeSubscriber:
    def __init__(self,nameTarget):
        # Initialize the ROS node
        rospy.init_node('save_time', anonymous=True)

        # Subscribe to the topic /vrpn/target1 with message type PoseStamped
        self.subscriber = rospy.Subscriber("/ft_sensor/netft_data", WrenchStamped, self.ft_stamped_callback)

        self.received_ft = WrenchStamped
        self.nameTarget = nameTarget
        self.time = []
    def ft_stamped_callback(self, msg):
        # This function will be called whenever a new message is received on the topic 
        self.received_ft= msg
        
    def space_callback(self):
        print("Saving Time")
        self.time.append(self.received_ft.header.stamp)
        print(self.time)

def launch_my_launch_file(parameter_value):
    try:
        subprocess.run(["roslaunch", "runningfolder", "save_bag.launch", f"name:={parameter_value}"])
    except KeyboardInterrupt:
        pass



def run_my_python_code():
    try:
        # Replace with the command to run your other Pythonroslaunc code
        print("run code")
        subprocess.run(["python", "test.py"])
        pass
    except KeyboardInterrupt:
        print("stop code")

        pass

def main():
    
    
    if len(sys.argv) != 2:
        print("Usage: python script_name.py name_to_save")
        return

    parameter_value = sys.argv[1]
    # # Set up Ctrl+C handler to exit the launch process
    # signal.signal(signal.SIGINT, lambda sig, frame: run_my_python_code())
    timeSubscriber = TimeSubscriber(parameter_value)

    print("Press 'Enter' to launch the ROS launch file.")
    input()

    # Launch the ROS launch file
    launch_process = subprocess.Popen(["roslaunch", "runningfolder", "save_bag.launch", f"name:={parameter_value}"])

    print("Press 'Space' to save rostime or Ctrl+C to exit.")
    try:
        while True:
            key = input()
            if key == ' ':
                timeSubscriber.space_callback()
    except KeyboardInterrupt:
        launch_process.terminate()
        run_my_python_code()
    finally:
        # Terminate the launch process when exiting
        launch_process.terminate()

if __name__ == '__main__':
    main()
