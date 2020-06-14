#include <ros/ros.h>
#include <geometry_msgs/TwistStamped.h>
// Here we are including all the headers necessary to use the most common public
// pieces of the ROS system. Always we create a new C++ file, we will need to
// add this include.

/* this can also be done in command window
rostopic pub -r 10 /cmd_velBox geometry_msgs/TwistStamped  '{header: {stamp: now, frame_id: base_link}, twist: {linear:  {x: -0.1, y: 0, z: 0.0}, angular: {x: 0.0,y: 0.0,z: 0.0}}}'*/


int main(int argc, char** argv) {// We start the main C++ program

    ros::init(argc, argv, "move_forward");// We initiate a ROS node called topic_publisher
    ros::NodeHandle nh;// We create a handler for the node. This handler will actually do the initialization of the node.

    ros::Publisher pub = nh.advertise<geometry_msgs::TwistStamped>("cmd_velBox", 1000); //We create a publisher called counter which uses std_msgs of Int32 type to publish 1000
    ros::Rate loop_rate(2);// We create a Rate object of 2Hz

    geometry_msgs::TwistStamped move;//We initializing count variable.
    move.twist.linear.x = .1;// we are setting Count data to zero
    move.twist.linear.y = .1;// we are setting Count data to zero
    move.twist.linear.z = 0;// we are setting Count data to zero
    move.twist.angular.x = 0;
    move.twist.angular.y = 0;
    move.twist.angular.z = 0.1;
    while (ros::ok())//Endless loop to publish the count variable
    {
        pub.publish(move);// Publish the message within the 'count' variable
        ros::spinOnce();
        loop_rate.sleep();// Make sure the publish rate maintains at 2 Hz
    }

    return 0;
}
