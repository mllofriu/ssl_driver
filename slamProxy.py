#!/usr/bin/python

import slamstate_pb2 as proto
from google.protobuf.internal import encoder
import socket

from visual_slam_msgs.msg import TrackingState, 
from visualization_msgs import Marker

import rospy

import tf

listener = 0

def process_tracking_state(ts):
	ss = proto.SlamState()

	try:
        (trans,rot) = listener.lookupTransform('/slam/world', 'robot', rospy.Time(0))
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        pass

	ss.state = ts.state
	ss.x = trans.x
	ss.y = trans.y
	# Rotation about z axis
	ss.heading = euler_from_quaternion(rot)[2]

	data = ss.SerializeToString()
	s.sendall(encoder._VarintBytes(len(data)) + data)


if __name__ == "__main__":
    rospy.init_node('SlamStateProxy', log_level=rospy.DEBUG)
    #rospy.init_node('SlamStateProxy')

    listener = tf.TransformListener()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    s.settimeout(None)
    s.connect(("127.0.0.1", 12346))
    rospy.loginfo("Socket initialized")

    rospy.Subscriber("/slam/tracking_state", TrackingState, process_tracking_state)

    
    rospy.spin()
           
