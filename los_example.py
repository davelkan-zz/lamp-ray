import los
import follow_path

vis = los.Visibility()

walls_L = [[(0.0,0.0),(5.0,0.0)],
          [(5.0,0.0),(5.0,6.0)],
          [(5.0,6.0),(10.0,6.0)],
          [(10.0,6.0),(10.0,10.0)],
          [(10.0,10.0),(0.0,10.0)],
          [(0.0,10.0),(0.0,0.0)]]
walls_block = [[(0.0,0.0),(10.0,0.0)],
              [(10.0,0.0),(10.0,10.0)],
              [(10.0,10.0),(0.0,10.0)],
              [(0.0,10.0),(0.0,0.0)],
              [(4.0,4.0),(4.0,6.0)],
              [(4.0,6.0),(6.0,6.0)],
              [(6.0,6.0),(6.0,4.0)],
              [(6.0,4.0),(4.0,4.0)]]

path = [(1.0,1.0),(5.0,1.0),(9.0,1.0)]


vis.setup(walls_block)
print len(walls_block)


print 'single run'
current_position = (5.0,1.0)
walls_seen = vis.run(current_position)
for w in walls_seen: print w

print 'following path'
room = follow(path,vis)
room.merge_visible()
for v in room.visable: print v, room.visable[v]
print room.percentage()
