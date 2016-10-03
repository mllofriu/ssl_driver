#!/usr/bin/python

import slamstate_pb2 as proto
from google.protobuf.internal import encoder
import socket

from visual_slam_msgs.msg import TrackingState

import rospy

def process_tracking_state(ts):
  ss = proto.SlamState()

  ss.state = ts.state
  ss.x = 0
  ss.y = 0
  ss.heading = 0

  data = ss.SerializeToString()
  s.sendall(encoder._VarintBytes(len(data)) + data)
  

if __name__ == "__main__":
    rospy.init_node('SlamStateProxy', log_level=rospy.DEBUG)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    s.settimeout(None)
    s.connect(("127.0.0.1", 12346))
    rospy.loginfo("Socket initialized")

    rospy.Subscriber("/slam/tracking_state", TrackingState, process_tracking_state)
    
    rospy.spin()
           
