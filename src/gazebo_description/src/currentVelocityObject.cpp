#include <ros/ros.h>
#include <gazebo_msgs/SetModelState.h>
#include <gazebo_msgs/SetPhysicsProperties.h>
#include <cstdlib>
#include "std_msgs/String.h"
#include <std_msgs/Float32.h>
#include <geometry_msgs/Twist.h>
//I'm going to implement user-specified twist values later.
  std_msgs::Float32 lin_data;
void counterCallback(const geometry_msgs::Twist::ConstPtr& msg)
{
//  ROS_INFO("%d", msg->linear.x);// we are using ROS_INFO to print message data to screen 

  lin_data.data=msg->linear.x;
}

int main (int argc, char **argv)
{
  ros::init(argc,argv,"robot_mover_mark_two");
  ros::NodeHandle n;
  ros::ServiceClient client = n.serviceClient<gazebo_msgs::SetModelState>("/gazebo/set_model_state");


  gazebo_msgs::SetModelState setmodelstate;
  gazebo_msgs::ModelState modelstate;
  modelstate.model_name = "simple_box";
  modelstate.reference_frame = "world";
  geometry_msgs::Twist model_twist;
  model_twist.linear.x = lin_data.data;
  model_twist.linear.y = 0;
  model_twist.linear.z = 0;
  model_twist.angular.x = 0;
  model_twist.angular.y = 0.0;
  model_twist.angular.z = 0.0;
  geometry_msgs::Pose model_pose;
  model_pose.position.x=-5;
  model_pose.position.y=0;
  model_pose.position.z=-8;
  model_pose.orientation.x=0;
  model_pose.orientation.y=0;
  model_pose.orientation.z=0;
  model_pose.orientation.w=0;
  modelstate.twist=model_twist;
  modelstate.pose=model_pose;
  setmodelstate.request.model_state = modelstate;

  ros::Subscriber sub = n.subscribe("cmd_vel", 1000, counterCallback);




  if (client.call(setmodelstate))
  {
    ROS_INFO("BRILLIANT!!!");
    ROS_INFO("%f, %f",modelstate.pose.position.x,modelstate.pose.position.y);
  }  
  else
  {
    ROS_ERROR("Failed to call service ");
    return 1;
  }
  ros::spin();
  return 0;  
}
