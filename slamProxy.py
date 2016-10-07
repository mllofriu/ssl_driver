#!/usr/bin/python

import slamstate_pb2 as proto
from google.protobuf.internal import encoder
import socket

from visual_slam_msgs.msg import TrackingState 
from visualization_msgs.msg import Marker

import rospy

import tf

listener = 0

def process_tracking_state(ts):
    ss = proto.SlamState()
    ss.state = ts.state
    ss.x = 0
    ss.y = 0
    ss.heading = 0
    try:
        (trans,rot) = listener.lookupTransform('/slam/world', 'robot', rospy.Time(0))
        ss.x = trans[0]
        ss.y = trans[1]
        # Rotation about z axis
        ss.heading = tf.transformations.euler_from_quaternion(rot)[2]

    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            pass
   
    data = ss.SerializeToString()
	
    s.sendall(encoder._VarintBytes(len(data)) + data)


if __name__ == "__main__":
    rospy.init_node('SlamStateProxy', log_level=rospy.DEBUG)
    #rospy.init_node('SlamStateProxy')

    listener = tf.TransformListener()
   
    connected = False
    while not connected: 
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
            s.settimeout(None)
            s.connect(("127.0.0.1", 12346))
            rospy.loginfo("Socket initialized")
            connected = True 
        except socket.error:
            rospy.logerr("Connection to 12346 refused, retrying...")
            rospy.sleep(3)    
            

    rospy.Subscriber("/slam/tracking_state", TrackingState, process_tracking_state)

    
    rospy.spin()
           
