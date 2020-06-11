#!/usr/bin/env python
import rospy
#import utils.geo_maths as geo_maths
from std_msgs.msg import Float32
from geometry_msgs.msg import TwistStamped, Twist, Pose
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState
from ros_turtlebot_control.srv import *
from nav_msgs.msg import Odometry

pose_x=Float32();
pose_y=Float32();
theta=Float32();
def callback(data):
    pose_x.data=data.pose.pose.position.x;
    pose_y.data=data.pose.pose.position.y;
    theta.data=0;

def main():
    rospy.init_node('set_vel_py')
    rate=rospy.Rate(5)
    rospy.Subscriber('/ground_truth/state', Odometry, callback)
    while not rospy.is_shutdown():  
       x=pose_x.data;
       y=pose_y.data;
       the_ta=0;
       moveToPose=MoveToPoseRequest()
       moveToPose.x=x;
       moveToPose.y=y;
       moveToPose.theta=the_ta;
       rate.sleep()
       rospy.wait_for_service('/turtle/move_to_pose')
       try:
           set_state = rospy.ServiceProxy('/turtle/move_to_pose', MoveToPose)
           resp = set_state(moveToPose)
       except rospy.ServiceException, e:
          print "Service call failed: %s" % e

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
