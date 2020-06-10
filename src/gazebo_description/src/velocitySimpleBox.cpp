#include <ros/ros.h>
#include <gazebo_msgs/SetModelState.h>
#include <cstdlib>
#include <std_msgs/Float32.h>
#include <geometry_msgs/TwistStamped.h>
#include <geometry_msgs/Pose.h>
#include <geometry_msgs/Twist.h>
//I'm going to implement user-specified twist values later.
  std_msgs::Float32 lin_x;
  std_msgs::Float32 lin_y;
  std_msgs::Float32 lin_z;
void callback(const geometry_msgs::TwistStamped::ConstPtr& msg)
{
  lin_x.data=msg->twist.linear.x;
  lin_y.data=msg->twist.linear.y;
  lin_z.data=msg->twist.linear.z;
}


int main (int argc, char **argv)
{
  ros::init(argc,argv,"simpleBox");
  ros::NodeHandle n;
  ros::Rate loop_rate(1);
  ros::Subscriber sub = n.subscribe("cmd_velBox", 1, callback);
  double x=-5;
  double y=0;
  double z=-8;
  ros::Time current_time, last_time;
  current_time=ros::Time::now();
  last_time=ros::Time::now();


  while (ros::ok()){
     ros::spinOnce();
     current_time=ros::Time::now();
     double dt = (current_time - last_time).toSec();
     double delta_x = lin_x.data * dt;
     double delta_y = lin_y.data * dt;
     double delta_z = lin_z.data * dt;

     x += delta_x;
     y += delta_y;
     z += delta_z;

     ros::ServiceClient client = n.serviceClient<gazebo_msgs::SetModelState>("/gazebo/set_model_state");
     geometry_msgs::Pose model_pose;
     model_pose.position.x=x;
     model_pose.position.y=y;
     model_pose.position.z=z;
     model_pose.orientation.x=0;
     model_pose.orientation.y=0;
     model_pose.orientation.z=0;
     model_pose.orientation.w=0;

     geometry_msgs::Twist model_twist;
     //model_twist.linear.x = lin_x.data;
     //model_twist.linear.y = lin_y.data;
     //model_twist.linear.z = lin_z.data;
     model_twist.angular.x = 0;
     model_twist.angular.y = 0.0;
     model_twist.angular.z = 0.0;

     gazebo_msgs::SetModelState setmodelstate;
     gazebo_msgs::ModelState modelstate;
     modelstate.model_name = "simple_box";
     modelstate.reference_frame = "world";
     modelstate.twist=model_twist;
     modelstate.pose=model_pose;
     setmodelstate.request.model_state = modelstate;
     last_time=current_time;
     loop_rate.sleep();
  if (client.call(setmodelstate))
  {
    ROS_INFO("BRILLIANT!!!");
    ROS_INFO("%f, %f, %f, %f",lin_x.data, lin_y.data, lin_z.data, dt);
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
