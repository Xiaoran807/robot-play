#include <ros/ros.h>
#include <gazebo_msgs/SetModelState.h>
#include <gazebo_msgs/SetPhysicsProperties.h>
#include <cstdlib>
//I'm going to implement user-specified twist values later.
int main (int argc, char **argv)
{
  ros::init(argc,argv,"robot_mover_mark_two");
  ros::NodeHandle n;
  ros::ServiceClient client = n.serviceClient<gazebo_msgs::SetModelState>("/gazebo/set_model_state");
  ros::ServiceClient client1 = n.serviceClient<gazebo_msgs::SetPhysicsProperties>("/gazebo/set_physics_properties");

  gazebo_msgs::SetModelState setmodelstate;
  gazebo_msgs::ModelState modelstate;
  modelstate.model_name = "myObject";
  modelstate.reference_frame = "world";

  geometry_msgs::Twist model_twist;
  model_twist.linear.x = 1.0;
  model_twist.linear.y = 1;
  model_twist.linear.z = 0;
  model_twist.angular.x = 0;
  model_twist.angular.y = 0.0;
  model_twist.angular.z = 0.0;
  
  geometry_msgs::Pose model_pose;
  model_pose.position.x=1;
  model_pose.position.y=1;
  model_pose.position.z=1;
  model_pose.orientation.x=0;
  model_pose.orientation.y=0;
  model_pose.orientation.z=0;
  model_pose.orientation.w=0;


  modelstate.twist=model_twist;
  modelstate.pose=model_pose;
  setmodelstate.request.model_state = modelstate;


  gazebo_msgs::SetPhysicsProperties setPhysicsProperties;
  setPhysicsProperties.request.gravity.z=0;


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


if (client1.call(setPhysicsProperties))
  {
    ROS_INFO("BRILLIANT!!! Gravity is turned to zero");
  }  
  else
  {
    ROS_ERROR("Failed to call service ");
    return 1;
  }
  return 0;  
}
