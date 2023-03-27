#include "ros/ros.h"
#include "std_msgs/Float64MultiArray.h"

#include "geometry_msgs/Vector3Stamped.h"
#include "geometry_msgs/QuaternionStamped.h"
#include "geometry_msgs/PoseStamped.h"

#include <fstream>
#include <cmath>
#include <iostream>
#include <sstream>
#include <eigen3/Eigen/Dense>
#include <stdio.h>
#include <filesystem>
#include <unistd.h>


using namespace Eigen;
using namespace std;
   
void CC_filter_acc(const geometry_msgs::Vector3Stamped::ConstPtr msg);
void CC_filter_vel(const geometry_msgs::Vector3Stamped::ConstPtr msg);
void CC_filter_pos(const geometry_msgs::Vector3Stamped::ConstPtr msg);
void CC_filter_quat(const geometry_msgs::QuaternionStamped::ConstPtr msg);

   

geometry_msgs::Vector3 filter_acc;
geometry_msgs::Vector3 filter_pos;
geometry_msgs::Vector3 filter_vel;
geometry_msgs::Quaternion filter_quat;


vector<double> row;
int main(int argc, char **argv)
{
    //Initialisation of the Ros Node (Service, Subscrber and Publisher)
    ros::init(argc, argv, "Save_topic");
    ros::NodeHandle Nh_;
    ros::Subscriber sub_acc = Nh_.subscribe("/filter/free_acceleration", 1000, CC_filter_acc);
    //ros::Subscriber sub = Nh_.subscribe("/vrpn_client_node/Shotcrete/pose", 1000, CC_vrpn);
    ros::Subscriber sub_vel = Nh_.subscribe("/filter/velocity", 1000, CC_filter_vel);
    //ros::Subscriber sub = Nh_.subscribe("/imu/acceleration", 1000, CC_imu_acc);
    //ros::Subscriber sub = Nh_.subscribe("/imu/angular_velocity", 1000, CC_imu_angvel);
    ros::Subscriber sub_pos = Nh_.subscribe("/filter/positionlla", 1000, CC_filter_pos);
    ros::Subscriber sub_quat = Nh_.subscribe("/filter/quaternion", 1000, CC_filter_quat);

    //ros::Publisher chatter_pub = Nh_.advertise<std_msgs::Float64MultiArray>("iiwa/PositionController/command", 1000);
    ros::Rate loop_rate(400);

    ROS_INFO("HELLO");
    std::ofstream myfile;
    myfile.open ("Data/data.csv");
    myfile <<"sec,nsec,accx,accy,accz,velx,vely,velz,pos,poy,posz,quatx,quaty,quatz,quatw\n";
    string UserInput = "go";

    //begin the ros loop
    double count = 0;
    while (ros::ok())
    {

         //if( UserInput == "stop"){
             row.push_back(count);
          row.push_back(filter_acc.x);
            row.push_back(filter_acc.y);
         row.push_back(filter_acc.z);

             row.push_back(filter_pos.x);
    row.push_back(filter_pos.y);
    row.push_back(filter_pos.z);
        row.push_back(filter_quat.x);
    row.push_back(filter_quat.y);
    row.push_back(filter_quat.z);
    row.push_back(filter_quat.w);
        row.push_back(filter_vel.x);
    row.push_back(filter_vel.y);
    row.push_back(filter_vel.z);
        std::stringstream ss;
        if(!row.empty())
        {
            for (auto it = row.begin(); it != row.end(); it++)    {
                if (it != row.begin()) {
                    ss << ",";
                }
                ss << *it;
            }    
            myfile << ss.str();
            myfile <<"\n";
            row.clear();
        }

        if (count==1000){
        myfile.close(); 
        return 0; }
        ++count;
        //--------------------------------------------------------------------
        ros::spinOnce();        
        loop_rate.sleep();  
    }
}


void CC_filter_acc(const geometry_msgs::Vector3Stamped::ConstPtr msg)
{
    filter_acc.x = msg->vector.x;
    filter_acc.y = msg->vector.y;
    filter_acc.z = msg->vector.z;
   

}
void CC_filter_pos(const geometry_msgs::Vector3Stamped::ConstPtr msg)
{
    filter_pos.x = msg->vector.x;
    filter_pos.y = msg->vector.y;
    filter_pos.z = msg->vector.z;

}
void CC_filter_quat(const geometry_msgs::QuaternionStamped::ConstPtr msg)
{
    filter_quat.x = msg->quaternion.x;
    filter_quat.y = msg->quaternion.y;
    filter_quat.z = msg->quaternion.z;
    filter_quat.w = msg->quaternion.w;


}
void CC_filter_vel(const geometry_msgs::Vector3Stamped::ConstPtr msg)
{
    filter_vel.x = msg->vector.x;
    filter_vel.y = msg->vector.y;
    filter_vel.z = msg->vector.z;

}

