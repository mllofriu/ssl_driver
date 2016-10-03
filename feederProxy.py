#!/usr/bin/python

import feeders_pb2 as proto
from google.protobuf.internal import encoder
import socket

from ar_track_alvar_msgs.msg import AlvarMarker

import rospy
import tf 

max_wait = 2
cam_frame = "/base"
marker_frame = "/ar_marker_0"

if __name__ == "__main__":
    #rospy.init_node('FeederProxy')
    rospy.init_node('FeederProxy', log_level=rospy.DEBUG)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    s.settimeout(None)
    s.connect(("127.0.0.1", 12345))
    rospy.loginfo("Socket initialized")
    
    tf_listener = tf.TransformListener()

    r = rospy.Rate(3) # 10hz
    while not rospy.is_shutdown():
        now = rospy.Time.now()
        markers = []
        try:
          lastT = tf_listener.getLatestCommonTime(cam_frame, marker_frame)
          if now - lastT < rospy.Duration(.3):
            (t, rot) = tf_listener.lookupTransform(cam_frame, marker_frame, lastT)
            rospy.logdebug("Marker (id, x, y): ({},{},{})".format(1, t[0],  t[1]))
            markers += [(0, t[0], t[1])]
        except:
          pass
          
        fs = proto.Feeders()
        for m in markers:
          f = fs.feeders.add()
          f.id = m[0]
          f.x = m[1]
          f.y = m[2]
          rospy.logdebug("Sending Marker (id, x, y): ({},{},{})".format(m[0], m[1],  m[2]))
        #s.sendall(fs.SerializeToString())
        data = fs.SerializeToString()
        s.sendall(encoder._VarintBytes(len(data)) + data)
        
        r.sleep()    
           
