#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import TwistStamped, Twist, Pose, Quaternion
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
import sys
sys.path.insert(1, '/home/xiaoran/catkin_ws/src/robot-play/trunk/src/gazebo_description/utils')
from geo_maths import *


lin_x = Float32();
lin_y = Float32();
lin_z = Float32();
ang_z = Float32();
q = Quaternion();
def callback(data):
    lin_x.data=data.twist.linear.x;
    lin_y.data=data.twist.linear.y;
    lin_z.data=data.twist.linear.z;
    ang_z.data=data.twist.angular.z;

def main():
    rospy.init_node('set_vel')
    current_time = rospy.Time.now().to_sec()
    last_time = rospy.Time.now().to_sec()
    x=-20;
    y=0;
    z=-15;
    theta=0;

    rate=rospy.Rate(5)
    rospy.Subscriber('cmd_velBox', TwistStamped, callback)
    while not rospy.is_shutdown():  
       current_time = rospy.Time.now().to_sec()
       dt=(current_time-last_time);
       delta_x = lin_x.data * dt;
       delta_y = lin_y.data * dt;
       delta_z = lin_z.data * dt;
       delta_theta = ang_z.data * dt;

       x += delta_x;
       y += delta_y;
       z += delta_z;
       theta += delta_theta;
       q=theta_to_quaternion(theta);


       modelstate=ModelState()
       modelstate.model_name='objectUnderwater'
       modelstate.reference_frame = "world";
       model_twist=Twist();
       model_twist.linear.x = 0;
       model_twist.linear.y = 0;
       model_twist.linear.z = 0;
       model_twist.angular.x = 0;
       model_twist.angular.y = 0.0;
       model_twist.angular.z = 0.0;
       model_pose=Pose();
       model_pose.position.x=x;
       model_pose.position.y=y;
       model_pose.position.z=z;
       model_pose.orientation.x=q.x;
       model_pose.orientation.y=q.y;
       model_pose.orientation.z=q.z;
       model_pose.orientation.w=q.w;
       modelstate.twist=model_twist;
       modelstate.pose=model_pose;
       last_time = rospy.Time.now().to_sec()
       rate.sleep()
       rospy.wait_for_service('/gazebo/set_model_state')
       try:
           set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
           resp = set_state( modelstate )
       except rospy.ServiceException, e:
          print "Service call failed: %s" % e


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
