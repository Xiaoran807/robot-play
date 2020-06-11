import math
import rospy
from geometry_msgs.msg import Twist

class Subscriber:

  # @param pub Publisher instance to send message with
  def __init__(self, pub):
    self.pub = pub
    # By default position on x axis is 0.
    self.x = 0
    # The initial state of the robot is perpetual to the x axis.
    self.delta = 0

  # Main program tick that calculates the changes.
  # @param dx The difference in distance on axis x in each tick
  # @param f The function to render
  def tick(self, dx, f):
    # Calculates the change on axis y.
    dy = f(self.x + dx) - f(self.x)

    # Calculates the hypotenuse of the dx dy right triangle.
    change = math.sqrt(dx * dx + math.pow(dy, 2))

    # The between dx and hypotenuse.
    delta = math.asin(dy / change)

    message = Twist()
    message.linear.x = change
    # The difference between new delta and old delta is the
    # angle the robot to turns by.
    message.angular.z = delta - self.delta

    # Sends the command velocity to the turtle bot node.
    self.pub.publish(message)

    # Update the state.
    self.x += dx
    self.delta = delta
