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
  modelstate.model_name = "simple_box";
  modelstate.reference_frame = "world";
  geometry_msgs::Twist model_twist;
  model_twist.linear.x = .3;
  model_twist.linear.y = 0;
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
  setPhysicsProperties.request.time_step=0.001;
  setPhysicsProperties.request.max_update_rate=1000.0;
  setPhysicsProperties.request.gravity.x=0;
  setPhysicsProperties.request.gravity.y=0;
  setPhysicsProperties.request.gravity.z=0;
  setPhysicsProperties.request.ode_config.auto_disable_bodies=false;
  setPhysicsProperties.request.ode_config.auto_disable_bodies= false;
  setPhysicsProperties.request.ode_config.sor_pgs_precon_iters= 0;
  setPhysicsProperties.request.ode_config.sor_pgs_iters= 50;
  setPhysicsProperties.request.ode_config.sor_pgs_w=1.3;
  setPhysicsProperties.request.ode_config.sor_pgs_rms_error_tol= 0.0;
  setPhysicsProperties.request.ode_config.contact_surface_layer= 0.001;
  setPhysicsProperties.request.ode_config.contact_max_correcting_vel= 100.0;
  setPhysicsProperties.request.ode_config.cfm=0.0;
  setPhysicsProperties.request.ode_config.erp= 0.2;
  setPhysicsProperties.request.ode_config.max_contacts= 20;




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
