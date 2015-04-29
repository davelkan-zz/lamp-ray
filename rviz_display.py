#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PolygonStamped, Point32, Point
from visualization_msgs.msg import Marker, MarkerArray

def make_line(points,line_id,color=[0.0,1.0,0.0], offset = 0):
    line = Marker()
    line.header.frame_id = "map"
    line.id = line_id
    line.type = Marker.LINE_STRIP
    line.action = Marker.ADD
    line.scale.x = 2+offset
    line.scale.y = 1
    line.pose.position.x = 0
    line.pose.position.y = 0
    line.pose.position.z = offset
    line.pose.orientation.x = 0.0
    line.pose.orientation.y = 0.0
    line.pose.orientation.z = 0.0
    line.pose.orientation.w = 1.0
    line.color.a = 1.0
    line.color.r = color[0]
    line.color.g = color[1]
    line.color.b = color[2]
    line.points = points
    # pub.publish(line)
    return line

def show_current(pub, current_views):
    array = MarkerArray()
    line_id = 0
    for view_range in current_views:
        a = [view_range[0][0], view_range[0][1], 0]
        b = [view_range[1][0], view_range[1][1], 0]
        line = make_line([Point(*a),Point(*b)],line_id, offset = 3)
        array.markers.append( line )
        line_id += 1
    print "publlishing current view"
    pub.publish(array)

def update_seen(pub, merged_views):
    array = MarkerArray()
    line_id = 0
    for view_range in merged_views:
        a = [view_range[0][0], view_range[0][1], 0]
        b = [view_range[1][0], view_range[1][1], 0]
        line = make_line([Point(*a),Point(*b)],line_id, color = [0.0,0.0,1.0])
        array.markers.append( line )
        line_id += 1
    print "publlishing merged views"
    pub.publish(array)     

def rviz_init(room):
    rospy.init_node('lampbot')

    pub_room = rospy.Publisher('room', PolygonStamped, queue_size=10)
    pub_seen = rospy.Publisher('seen', MarkerArray, queue_size=10)
    pub_seeing = rospy.Publisher('seeing', MarkerArray, queue_size=10)
    rospy.Rate(10)

    rospy.sleep(1)
    layout = PolygonStamped()
    layout.header.frame_id = "map"
    walls = room.get_walls()
    corners = []
    for corner in walls:
        x,y = corner
        corners.append(Point32(x,y,0))
    layout.polygon.points = corners
    print 'publishing room'
    pub_room.publish(layout)
    rospy.sleep(1)
    return pub_seeing, pub_seen
   


if __name__ == '__main__':
    rviz_display(1,1)
    i = 0
    while not rospy.is_shutdown():
        i+=1
        publish_line(pub_seen,[Point(0,0,0),Point(0,i,0),Point(5,i,0)])
        

        rospy.sleep(5) 
    
    

   