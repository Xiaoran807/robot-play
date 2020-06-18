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
  
  def main(self):
    self.moveToPose.x=1;
    self.moveToPose.y=1;
    self.moveToPose.theta=1;
    resp = self.set_state(self.moveToPose) 

if __name__ == '__main__':
    rospy.init_node('set_vel_py', anonymous=True)
    my_pose=poseGoalBox()

    while not rospy.is_shutdown():  
       my_pose.main()
       my_pose.rate.sleep()
       rospy.spin()
