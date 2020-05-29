#!/usr/bin/env python

import rospy
from std_msgs.msg import Float64

class TemperatureSensor:

    def read_temperature_sensor_data(self):
        # Here you read the data from your sensor
        # And you return the real value
        self.temperature = 30.0

    def __init__(self):
        # Create a ROS publisher
        self.temperature_publisher = rospy.Publisher("/temperature", Float64, queue_size=1)

        # Initialize temperature data
        self.temperature = 0

    def publish_temperature(self):
        msg = Float64()
        msg.data = self.temperature
        self.temperature_publisher.publish(msg)

if __name__ == '__main__':
    rospy.init_node("your_sensor_node")

    # Create an instance of Temperature sensor
    ts = TemperatureSensor()

    # Create a rate
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        ts.read_temperature_sensor_data()
        ts.publish_temperature()
        rate.sleep()
