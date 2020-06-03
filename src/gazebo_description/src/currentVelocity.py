#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import TwistStamped, Twist, Pose
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState

lin_x=Float32();
def callback(data):
    lin_x.data=data.twist.linear.x;

def main():
    rospy.init_node('set_vel')

    modelstate=ModelState()
    modelstate.model_name='simple_box'
    modelstate.reference_frame = "world";
    model_twist=Twist();
    model_twist.linear.x = lin_x.data;
    model_twist.linear.y = 0;
    model_twist.linear.z = 0;
    model_twist.angular.x = 0;
    model_twist.angular.y = 0.0;
    model_twist.angular.z = 0.0;
    model_pose=Pose();
    model_pose.position.x=-5;
    model_pose.position.y=0;
    model_pose.position.z=-8;
    model_pose.orientation.x=0;
    model_pose.orientation.y=0;
    model_pose.orientation.z=0;
    model_pose.orientation.w=0;
    modelstate.twist=model_twist;
    modelstate.pose=model_pose;

    rospy.wait_for_service('/gazebo/set_model_state')
    try:
        set_state = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        resp = set_state( modelstate )

    except rospy.ServiceException, e:
        print "Service call failed: %s" % e


        rospy.Subscriber('cmd_vel', 1, callback)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
