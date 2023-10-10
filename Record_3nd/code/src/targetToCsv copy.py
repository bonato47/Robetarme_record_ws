import rospy
from geometry_msgs.msg import PoseStamped
import csv
import sys

class PoseStampedSubscriber:
    def __init__(self,nameTarget):
        # Initialize the ROS node
        rospy.init_node('calib_to_csv', anonymous=True)

        # Subscribe to the topic /vrpn/target1 with message type PoseStamped
        self.subscriber = rospy.Subscriber("/vrpn_client_node/calib/pose", PoseStamped, self.pose_stamped_callback)

        self.received_poses = []
        self.nameTarget = nameTarget

    def pose_stamped_callback(self, msg):
        # This function will be called whenever a new message is received on the topic
 
        self.received_poses.append(msg.pose)

        if len(self.received_poses) == 100:
            self.calculate_and_save_mean_pose()

    def calculate_and_save_mean_pose(self):
        if not self.received_poses:
            return

        mean_pose = self.calculate_mean_pose(self.received_poses)
        self.save_mean_pose_to_csv(mean_pose)
        rospy.signal_shutdown("Mean pose calculated and saved, exiting program.")

    @staticmethod
    def calculate_mean_pose(poses):
        num_poses = len(poses)
        mean_position = [sum(p.position.x for p in poses) / num_poses,
                         sum(p.position.y for p in poses) / num_poses,
                         sum(p.position.z for p in poses) / num_poses]
        
        mean_orientation = [sum(p.orientation.x for p in poses) / num_poses,
                            sum(p.orientation.y for p in poses) / num_poses,
                            sum(p.orientation.z for p in poses) / num_poses,
                            sum(p.orientation.w for p in poses) / num_poses]

        mean_pose = PoseStamped()
        mean_pose.pose.position.x = mean_position[0]
        mean_pose.pose.position.y = mean_position[1]
        mean_pose.pose.position.z = mean_position[2]

        mean_pose.pose.orientation.x = mean_orientation[0]
        mean_pose.pose.orientation.y = mean_orientation[1]
        mean_pose.pose.orientation.z = mean_orientation[2]
        mean_pose.pose.orientation.w = mean_orientation[3]


        return mean_pose

    def save_mean_pose_to_csv(self, mean_pose):
        nameCSV = "../data/targets/" + self.nameTarget + ".csv"
        with open(nameCSV, 'w') as csvfile:
            fieldnames = ['Position_X', 'Position_Y', 'Position_Z', 'Orientation_X', 'Orientation_Y', 'Orientation_Z', 'Orientation_W']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({
                'Position_X': mean_pose.pose.position.x,
                'Position_Y': mean_pose.pose.position.y,
                'Position_Z': mean_pose.pose.position.z,
                'Orientation_X': mean_pose.pose.orientation.x,
                'Orientation_Y': mean_pose.pose.orientation.y,
                'Orientation_Z': mean_pose.pose.orientation.z,
                'Orientation_W': mean_pose.pose.orientation.w,
            })

    def run(self):
        # Keep the program running until ROS shutdown
        rospy.spin()
def main(param):
    

    parameter_name = param
    
    pose_stamped_subscriber = PoseStampedSubscriber(parameter_name)
    pose_stamped_subscriber.run()
    return

if __name__ == '__main__':
    
    main()

