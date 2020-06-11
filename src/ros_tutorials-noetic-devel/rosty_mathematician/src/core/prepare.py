import math
import rospy
from geometry_msgs.msg import Twist

# Draws axis x.
#
# @param pub Publisher instance
def prepare(pub):
  # Size of the field the robot is in divided by two.
  r = 7

  # Moves the turtle forward, drawing one half of the x axis.
  move(pub, r, 4)

  # Moves the turtle backwards twice the length, putting it to the left edge.
  move(pub, 2 * r, -4)

# Moves by certain distance by given speed.
#
# @param pub Publisher instance
# @param distance The distance relative to the enviroment to move by
# @param speed How many units per tick do we take
def move(pub, distance, speed):
  message = Twist()
  message.linear.x = speed

  while not rospy.is_shutdown():
    traveled = 0
    t0 = rospy.Time.now().to_sec()

    # Absolute value so that we can move backwards.
    while (math.fabs(traveled) < distance):
      pub.publish(message)

      # Calculates the distance traveled based on time lapsed in the while.
      t1 = rospy.Time.now().to_sec()
      traveled = speed * (t1 - t0)

    # Stops the robot.
    message.linear.x = 0
    pub.publish(message)

    break
