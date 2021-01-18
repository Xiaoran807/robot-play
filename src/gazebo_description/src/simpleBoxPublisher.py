#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import TwistStamped

class VelBaseBox(object):
  _LABEL=''

pub2=rospy.Publisher('cmd_velBox', TwistStamped, queue_size=10)
def vel_box():
    t = rospy.get_time()
    rate = rospy.Rate(500)
    msg=TwistStamped()

    while not rospy.is_shutdown():
        if rospy.get_time()>5 and rospy.get_time()<=20:
            msg.twist.linear.x=0.2
            msg.twist.linear.y=0.2
            msg.twist.linear.z=0
            msg.twist.angular.x=0
            msg.twist.angular.y=0
            msg.twist.angular.z=0
        elif rospy.get_time()>20 and rospy.get_time()<=35:
            msg.twist.linear.x=0.2
            msg.twist.linear.y=-0.2
            msg.twist.linear.z=0
            msg.twist.angular.x=0
            msg.twist.angular.y=0
            msg.twist.angular.z=0
        elif rospy.get_time()>35 and rospy.get_time()<=50:
            msg.twist.linear.x=-0.2
            msg.twist.linear.y=-0.2
            msg.twist.linear.z=-0
            msg.twist.angular.x=0
            msg.twist.angular.y=0
            msg.twist.angular.z=0
        elif rospy.get_time()>50 and rospy.get_time()<=65:
            msg.twist.linear.x=-0.2
            msg.twist.linear.y=0.2
            msg.twist.linear.z=-0.2
            msg.twist.angular.x=0
            msg.twist.angular.y=0
            msg.twist.angular.z=0
        else:
            msg.twist.linear.x=0
            msg.twist.linear.y=0
            msg.twist.linear.z=0
            msg.twist.angular.x=0
            msg.twist.angular.y=0
            msg.twist.angular.z=0






       	pub2.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('velocity_publisher_node')
    try:
        vel_box()
    except rospy.ROSInterruptException:
        pass
