#!/usr/bin/env python

# import rospy

import location
# import rviz_display
import pickle
# import wall_tracer

# fl = wall_tracer.cornerFinder()
# walls = fl.run()
# pickle.dump(walls,open('walls.p','wb'))
walls = pickle.load(open('walls.p','rb'))

start = (10.0,10.0)

# walls = [[(0.0,0.0),(5.0,0.0)],[(5.0,0.0),(5.0,6.0)],[(5.0,6.0),(10.0,6.0)],[(10.0,6.0),(10.0,10.0)],[(10.0,10.0), (0.0,10.0)],[(0.0,10.0),(0.0,0.0)]]  

print "Walls: ",walls

path, room, vis = location.main(start, walls)
pickle.dump([path,room,vis], open('save.p', 'wb'))
path, room, vis = pickle.load(open('save.p', 'rb'))


# current_pub, overall_pub = rviz_display.rviz_init(room)

# room.clear()

# for point in path:
#     seeing_now = room.extend_path(point,vis)
#     rviz_display.update_seen(overall_pub, room.get_merged())
#     rviz_display.show_current(current_pub, seeing_now)
#     rospy.sleep(5)


#     # display visable, wait, move on