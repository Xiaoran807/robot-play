#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64

def read_temperature_sensor_data():
    # Here you read the data from your sensor
    # And you return the real value
    return 30

if __name__ == '__main__':
    rospy.init_node("your_sensor_node")

    # Create a ROS publisher
    data_publisher = rospy.Publisher("/temperature", Float64, queue_size=1)

    # Create a rate
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        msg = Float64()
        msg.data = read_temperature_sensor_data()
        data_publisher.publish(msg)
        rate.sleep()
