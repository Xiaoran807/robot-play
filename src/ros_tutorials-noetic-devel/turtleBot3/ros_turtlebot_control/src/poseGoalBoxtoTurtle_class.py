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
import geo_maths as geo_maths

class poseGoalBox:

  def __init__(self):

    rospy.wait_for_service('/turtle/move_to_pose')
    self.set_state = rospy.ServiceProxy('/turtle/move_to_pose', MoveToPose)
    self.rate=rospy.Rate(5)
    self.moveToPose=MoveToPoseRequest()
    self.odom_sub=rospy.Subscriber('/ground_truth/state', Odometry, self.callback)
    self.x_wg=Float32()
    self.y_wg=Float32()
    self.theta_wg=Float32()
    self.pose=Pose()
    

  def main(self):
    self.moveToPose.x=self.x_wg.data;
    self.moveToPose.y=self.y_wg.data;
    self.moveToPose.theta=self.theta_wg.data;
    resp = self.set_state(self.moveToPose) 

  def callback(self,data):
    self.pose=geo_maths.pose_to_xytheta(data.pose.pose);
    T_wb = geo_maths.xytheta_to_T(self.pose[0], self.pose[1], self.pose[2]);
    T_bg = geo_maths.xytheta_to_T(-1, 0, 0);
    T_wg = np.dot(T_wb, T_bg);
    self.x_wg.data, self.y_wg.data, self.theta_wg.data = geo_maths.T_to_xytheta(T_wg)
    
if __name__ == '__main__':
    rospy.init_node('set_vel_py', anonymous=True)
    my_pose=poseGoalBox()

    while not rospy.is_shutdown():  
       my_pose.main()
       my_pose.rate.sleep()
       #rospy.spin()
