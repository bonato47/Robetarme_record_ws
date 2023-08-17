import rospy
from geometry_msgs.msg import WrenchStamped
import csv
import sys

class FtStampedSubscriber:
    def __init__(self,nameTarget):
        # Initialize the ROS node
        rospy.init_node('bias_to_csv', anonymous=True)

        # Subscribe to the topic /vrpn/target1 with message type ftStamped
        self.subscriber = rospy.Subscriber("/ft_sensor/netft_data", WrenchStamped, self.ft_stamped_callback)

        self.received_fts = []
        self.nameTarget = nameTarget

    def ft_stamped_callback(self, msg):
        # This function will be called whenever a new message is received on the topic
 
        self.received_fts.append(msg.wrench)

        if len(self.received_fts) == 100:
            self.calculate_and_save_mean_ft()

    def calculate_and_save_mean_ft(self):
        if not self.received_fts:
            return

        mean_ft = self.calculate_mean_ft(self.received_fts)
        self.save_mean_ft_to_csv(mean_ft)
        rospy.signal_shutdown("Mean ft calculated and saved, exiting program.")

    @staticmethod
    def calculate_mean_ft(fts):
        num_fts = len(fts)
        mean_force = [sum(p.force.x for p in fts) / num_fts,
                      sum(p.force.y for p in fts) / num_fts,
                      sum(p.force.z for p in fts) / num_fts]

        mean_torque = [sum(p.torque.x for p in fts) / num_fts,
                       sum(p.torque.y for p in fts) / num_fts,
                       sum(p.torque.z for p in fts) / num_fts]

        mean_ft = WrenchStamped()
        mean_ft.wrench.force.x = mean_force[0]
        mean_ft.wrench.force.y = mean_force[1]
        mean_ft.wrench.force.z = mean_force[2]
        mean_ft.wrench.torque.x = mean_torque[0]
        mean_ft.wrench.torque.y = mean_torque[1]
        mean_ft.wrench.torque.z = mean_torque[2]
        return mean_ft

    def save_mean_ft_to_csv(self, mean_ft):
        nameCSV = "../bias/bias_" + self.nameTarget + ".csv"
        with open(nameCSV, 'w') as csvfile:
            fieldnames = ['Force_X', 'Force_Y', 'Force_Z', 'Torque_X', 'Torque_Y', 'Torque_Z']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({
                'Force_X': mean_ft.wrench.force.x,
                'Force_Y': mean_ft.wrench.force.y,
                'Force_Z': mean_ft.wrench.force.z,
                'Torque_X': mean_ft.wrench.torque.x,
                'Torque_Y': mean_ft.wrench.torque.y,
                'Torque_Z': mean_ft.wrench.torque.z,
            })

    def run(self):
        # Keep the program running until ROS shutdown
        rospy.spin()
def main():
    
    if len(sys.argv) != 2:
        print("Usage: python script_name.py name_to_save")
        return

    parameter_name = sys.argv[1]
    
    ft_stamped_subscriber = FtStampedSubscriber(parameter_name)
    ft_stamped_subscriber.run()
    return

if __name__ == '__main__':
    
    main()

