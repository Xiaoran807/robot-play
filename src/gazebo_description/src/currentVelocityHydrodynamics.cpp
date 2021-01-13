#include <ros/ros.h>
#include <gazebo_msgs/SetModelState.h>
#include <cstdlib>
#include <std_msgs/Float32.h>
#include <geometry_msgs/TwistStamped.h>
#include <geometry_msgs/Pose.h>
#include <geometry_msgs/Twist.h>
#include <tf/tf.h>
//I'm going to implement user-specified twist values later.
  std_msgs::Float32 lin_x;
  std_msgs::Float32 lin_y;
  std_msgs::Float32 lin_z;
  std_msgs::Float32 ang_z;
void callback(const geometry_msgs::TwistStamped::ConstPtr& msg)
{
 // lin_x.data=msg->twist.linear.x;
 // lin_y.data=msg->twist.linear.y;
}

void callbackBox(const geometry_msgs::TwistStamped::ConstPtr& msg)
{
  ang_z.data=msg->twist.angular.z;
  lin_z.data=msg->twist.linear.z;
  lin_x.data=msg->twist.linear.x;
  lin_y.data=msg->twist.linear.y;

}

int main (int argc, char **argv)
{
  ros::init(argc,argv,"robot_mover_mark_two");
  ros::NodeHandle n;
  ros::Rate loop_rate(500);
  ros::Subscriber sub = n.subscribe("/hydrodynamics/current_velocity", 1, callback);
  ros::Subscriber velBox_sub = n.subscribe("/cmd_velBox", 1, callbackBox);
  double x=-10; // -10 if 2x, -20 if x
  double y=0;
  double z=-15;
  double theta=0;
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
     double delta_theta = ang_z.data * dt;
     x += delta_x;
     y += delta_y;
     z += delta_z;
     //theta += delta_theta = delta_theta;
     theta += delta_theta;
     geometry_msgs::Quaternion odom_quat = tf::createQuaternionMsgFromYaw(theta);

     ros::ServiceClient client = n.serviceClient<gazebo_msgs::SetModelState>("/gazebo/set_model_state");
     geometry_msgs::Pose model_pose;
     model_pose.position.x=2*x;
     model_pose.position.y=2*y;
     model_pose.position.z=z;
     model_pose.orientation.x=odom_quat.x;
     model_pose.orientation.y=odom_quat.y;
     model_pose.orientation.z=odom_quat.z;
     model_pose.orientation.w=odom_quat.w;

     geometry_msgs::Twist model_twist;
     model_twist.linear.x = 0;
     model_twist.linear.y = 0;
     model_twist.linear.z = 0;
     model_twist.angular.x = 0;
     model_twist.angular.y = 0.0;
     model_twist.angular.z = 0.0;

     gazebo_msgs::SetModelState setmodelstate;
     gazebo_msgs::ModelState modelstate;
     modelstate.model_name = "objectUnderwater";
     modelstate.reference_frame = "world";
     modelstate.twist=model_twist;
     modelstate.pose=model_pose;
     setmodelstate.request.model_state = modelstate;
     last_time=current_time;
     loop_rate.sleep();
  if (client.call(setmodelstate))
  {
    //ROS_INFO("BRILLIANT!!!");
   // ROS_INFO("%f, %f, %f, %f",lin_x.data, lin_y.data, lin_z.data, dt);
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
