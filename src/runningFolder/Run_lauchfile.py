
import subprocess
import os
import signal
import time
import keyboard
def start_roslaunch(launch_file):
    roslaunch_cmd = f"roslaunch {launch_file}"
    return subprocess.Popen(roslaunch_cmd, shell=True, preexec_fn=os.setsid)
def pause_roslaunch(process):
    os.killpg(os.getpgid(process.pid), signal.SIGSTOP)
def resume_roslaunch(process):
    os.killpg(os.getpgid(process.pid), signal.SIGCONT)
if __name__ == "__main__":
    
    launch_file_path = "/path/to/your/roslaunch_file.launch"
    # Start the roslaunch process
    roslaunch_process = start_roslaunch(launch_file_path)
    
    print("Press the space bar to pause the roslaunch process.")
    print("Press 'Ctrl+C' to terminate the program gracefully.")
    try:
        while True:
            if keyboard.is_pressed(" "):
                # Pause the roslaunch process
                print("Pausing the roslaunch process...")
                pause_roslaunch(roslaunch_process)
                print("Press the space bar to resume the roslaunch process.")
                # Wait for the space bar to be released before resuming
                while keyboard.is_pressed(" "):
                    time.sleep(0.1)
                # Resume the roslaunch process
                print("Resuming the roslaunch process...")
                resume_roslaunch(roslaunch_process)
            # Add any other operations or logic here while the roslaunch is running
            # ...
            time.sleep(0.1)  # Sleep to reduce CPU usage
    except KeyboardInterrupt:
        # Terminate the roslaunch process and exit the program when Ctrl+C is pressed
        print("\nTerminating the program...")
        roslaunch_process.terminate()
        roslaunch_process.wait()


"""import subprocess
import sys
import os
import signal
import time
import keyboard
from testpython import bla

def pause_roslaunch(process):
    os.killpg(os.getpgid(process.pid), signal.SIGSTOP)
def resume_roslaunch(process):
    os.killpg(os.getpgid(process.pid), signal.SIGCONT)
    
def main(parameter_value):
    package_name = "cobod_arm_study"
    launch_file = "rviz_iiwa.launch"  # Replace with your launch file name
    roslaunch_cmd = ["roslaunch", package_name, launch_file]
    rosparam_cmd = ["rosparam", "set", "/name", str(parameter_value)]

    try:
        while True:
            if keyboard.is_pressed(" "):
                # Pause the roslaunch process
                print("Pausing the roslaunch process...")
                pause_roslaunch(roslaunch_process)
                print("Press the space bar to resume the roslaunch process.")
                # Wait for the space bar to be released before resuming
                while keyboard.is_pressed(" "):
                    time.sleep(0.1)
                # Resume the roslaunch process
                print("Resuming the roslaunch process...")
                resume_roslaunch(roslaunch_process)
            # Add any other operations or logic here while the roslaunch is running
            # ...
            time.sleep(0.1)  # Sleep to reduce CPU usage

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Process interrupted by user.")
        bla()

if __name__ == "__main__":
  if len(sys.argv) != 2:
        print("Usage: python script_name.py <name_to_record>")
  else:
        parameter_value = sys.argv[1]
        main(parameter_value)


"""

 