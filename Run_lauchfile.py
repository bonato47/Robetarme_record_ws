import subprocess
import sys
from testpython import bla

def main(parameter_value):
    package_name = "cobod_arm_study"
    launch_file = "rviz_iiwa.launch"  # Replace with your launch file name
    roslaunch_cmd = ["roslaunch", package_name, launch_file]
    rosparam_cmd = ["rosparam", "set", "/name", str(parameter_value)]

    try:
        subprocess.run(rosparam_cmd, check=True)
        subprocess.run(roslaunch_cmd, check=True)
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
