#!/usr/bin/env python
import rospy
import math
import numpy as np
from std_msgs.msg import Float32
from geometry_msgs.msg import TwistStamped, Twist, Pose
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from ros_turtlebot_control.srv import *
from nav_msgs.msg import Odometry
import sys
sys.path.insert(1, '/home/xiaoran/catkin_ws/src/robot-play/trunk/src/ros_tutorials-noetic-devel/turtleBot3/ros_turtlebot_control/utils')
#from geo_maths import *
import geo_maths as geo_maths

#x_wg=Float32();
#y_wg=Float32();
theta_wg=Float32();

def callback(data):
    global x_wg, y_wg
    pose=Pose();
    x_wg=Float32();
    y_wg=Float32();
    theta_wg=Float32();
    pose=geo_maths.pose_to_xytheta(data.pose.pose);
    T_wb = geo_maths.xytheta_to_T(pose[0], pose[1], pose[2])  # T_world_to_robot. Using relative pose as in turtle_lib.py
   # T_bg = xytheta_to_T(-1, 0, 0)  # T_robot_to_goal, robot facing the white small box
    T_bg = geo_maths.xytheta_to_T(2, 1, -1.57)  # T_robot_to_goal, robot facing to the side of the simple box
    T_wg = np.dot(T_wb, T_bg)
    x_wg.data, y_wg.data, theta_wg.data = geo_maths.T_to_xytheta(T_wg)

def main():
    global x_wg, y_wg
    x_wg=Float32();
    y_wg=Float32();
    rospy.init_node('set_vel_py')
    rate=rospy.Rate(5)
    rospy.Subscriber('/ground_truth/state', Odometry, callback)
    while not rospy.is_shutdown():  
       x=x_wg.data;
       y=y_wg.data;
       the_ta=theta_wg.data;
       moveToPose=MoveToPoseRequest()
       moveToPose.x=x;
       moveToPose.y=y;
       moveToPose.theta=the_ta;
       rate.sleep()
       rospy.wait_for_service('/turtle/move_to_pose')
      # try:
      #     set_state = rospy.ServiceProxy('/turtle/move_to_pose', MoveToPose)
      #     resp = set_state(moveToPose)
      # except rospy.ServiceException, e:
      #    print "Service call failed: %s" % e
       set_state = rospy.ServiceProxy('/turtle/move_to_pose', MoveToPose)
       resp = set_state(moveToPose) 

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
