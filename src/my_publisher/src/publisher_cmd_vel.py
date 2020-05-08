#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist, Vector3
import numpy.random as np
from std_msgs.msg import Int32

class VelBase(object):
  _LABEL=''

pub2=rospy.Publisher('chatter', Int32, queue_size=10)
def vel():
    count=0
    rate = rospy.Rate(1000)
    while not rospy.is_shutdown():
        count+=1
	rospy.loginfo(count)
	pub2.publish(count)
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('velocity_publisher_node')
    try:
        vel()
    except rospy.ROSInterruptException:
        pass








'''rospy.init_node('velocity_publisher_node')
pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
rate = rospy.Rate(1000)
while not rospy.is_shutdown():
    linear_x = np.rand()
    angular_z = np.rand()
    var = Twist(Vector3(linear_x,0,0),Vector3(0,0,angular_z))
    pub.publish(var)
    rate.sleep()'''
