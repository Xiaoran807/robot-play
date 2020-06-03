#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import TwistStamped, Twist, Pose
from gazebo_msgs.msg import ModelState
from gazebo_msgs.srv import SetModelState


class currentController():

    def callback(self, data):
        global lin_x
        self.lin_x=data.twist.linear.x;
        return self.lin_x

    def __init__(self):
        try:
            rospy.wait_for_service('/gazebo/set_model_state', timeout=20)
        except rospy.ROSException:
            print 'Current velocity services not available! Closing node...'
            sys.exit(-1)
        self.setCurrent = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
        self.modelstate=ModelState()
        self.modelstate.model_name='simple_box'
        self.modelstate.reference_frame = "world";
        self.model_twist=Twist();
        self.model_twist.linear.x = 0;
        self.model_twist.linear.y = 0;
        self.model_twist.linear.z = 0;
        self.model_twist.angular.x = 0;
        self.model_twist.angular.y = 0.0;
        self.model_twist.angular.z = 0.0;
        self.model_pose=Pose();
        self.model_pose.position.x=0;
        self.model_pose.position.y=0;
        self.model_pose.position.z=0;
        self.model_pose.orientation.x=0;
        self.model_pose.orientation.y=0;
        self.model_pose.orientation.z=0;
        self.model_pose.orientation.w=0;
        self.modelstate.twist=self.model_twist;
        self.modelstate.pose=self.model_pose;
        #self.periodicUpdate = rospy.Timer(rospy.Duration(10.0), self.updateCurrent)
        self.lin_x=0;

    def updateCurrent(self, event):
        self.modelstate=ModelState()
        self.modelstate.model_name='simple_box'
        self.modelstate.reference_frame = "world";
        self.model_twist=Twist();
        self.model_twist.linear.x = self.lin_x;
        self.model_twist.linear.y = 0;
        self.model_twist.linear.z = 0;
        self.model_twist.angular.x = 0;
        self.model_twist.angular.y = 0.0;
        self.model_twist.angular.z = 0.0;
        self.model_pose=Pose();
        self.model_pose.position.x=-5;
        self.model_pose.position.y=0;
        self.model_pose.position.z=0;
        self.model_pose.orientation.x=0;
        self.model_pose.orientation.y=0;
        self.model_pose.orientation.z=0;
        self.model_pose.orientation.w=0;
        self.modelstate.twist=self.model_twist;
        self.modelstate.pose=self.model_pose;
        self.setCurrent(self.modelstate)
        
    def listener(self):
        rospy.Subscriber('cmd_vel', 1, self.callback)

if __name__ == '__main__':
    try:
        rospy.init_node('currentController', log_level=rospy.DEBUG)

    except rospy.ROSInterruptException as error:
        print('pubs error with ROS: ', error)
        exit(1)

    curCon = currentController()
    rospy.spin()



