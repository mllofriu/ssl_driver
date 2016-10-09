#!/usr/bin/python

import rospy
from sensor_msgs.msg import CameraInfo, Image
from camera_info_manager import CameraInfoManager


pub = None 
ci = None
def callback(img):
    cimsg = ci.getCameraInfo()
    cimsg.header.stamp = img.header.stamp 
    pub.publish(cimsg)
    

if __name__ == "__main__":
    rospy.init_node("cam_info_publisher")
    pub = rospy.Publisher("camera/camera_info_orig", CameraInfo, queue_size=15)
    uri = rospy.get_param('~camera_info_url')
    ci = CameraInfoManager(cname='usb_cam',url=uri,namespace='/')
    ci.loadCameraInfo()
    sub = rospy.Subscriber("/camera/image_raw", Image, callback) 
    rospy.spin()  
