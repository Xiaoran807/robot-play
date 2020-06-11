#include <ros/ros.h>
#include <gazebo_msgs/SetModelState.h>
#include <cstdlib>
#include <std_msgs/Float32.h>
#include <geometry_msgs/TwistStamped.h>
#include <geometry_msgs/Pose.h>
#include <geometry_msgs/Twist.h>
#include <ros_turtlebot_control/MoveToPose.h>
#include <nav_msgs/Odometry.h>
//I'm going to implement user-specified twist values later.
  std_msgs::Float32 pose_x;
  std_msgs::Float32 pose_y;
  std_msgs::Float32 theta;
  std_msgs::Float32 ori_x;
  std_msgs::Float32 ori_y;
  std_msgs::Float32 ori_z;
  std_msgs::Float32 ori_w;


void callback(const nav_msgs::Odometry::ConstPtr& msg)
{
  pose_x.data=msg->pose.pose.position.x;
  pose_y.data=msg->pose.pose.position.y;
  theta.data=0;
  ori_x.data=msg->pose.pose.orientation.x;
  ori_y.data=msg->pose.pose.orientation.y;
  ori_z.data=msg->pose.pose.orientation.z;
  ori_w.data=msg->pose.pose.orientation.w;

}


int main (int argc, char **argv)
{
  ros::init(argc,argv,"turtlebot3_waffle_pi");
  ros::NodeHandle n;
  ros::Rate loop_rate(1);
  ros::Subscriber sub = n.subscribe("/ground_truth/state", 1, callback);


  while (ros::ok()){
     ros::spinOnce();
     double x=pose_x.data;
     double y=pose_y.data;
     double the_ta=theta.data;
     ros::ServiceClient client = n.serviceClient<ros_turtlebot_control::MoveToPose>("/turtle/move_to_pose");
     ros_turtlebot_control::MoveToPose moveToPose;
     moveToPose.request.x = x;
     moveToPose.request.y = y;
     moveToPose.request.theta = the_ta;
     loop_rate.sleep();
  if (client.call(moveToPose))
  {
    ROS_INFO("BRILLIANT!!!");
    ROS_INFO("%f, %f",pose_x.data, pose_y.data);
  }  
  else
  {
    ROS_ERROR("Failed to call service ");
    return 1;
  }

  }




//  ros::spin();
  return 0;  
}
