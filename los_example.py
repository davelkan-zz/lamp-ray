import los

vis = los.Visibility()

walls = [[(0.0,0.0),(5.0,0.0)],
         [(5.0,0.0),(5.0,6.0)],
         [(5.0,6.0),(10.0,6.0)],
         [(10.0,6.0),(10.0,10.0)],
         [(10.0,10.0),(0.0,10.0)],
         [(0.0,10.0),(0.0,0.0)]]

vis.setup(walls)

print 'merp'
current_position = (1.0,1.0)
walls_seen = vis.run(current_position)
print walls_seen
# for s in vis.segments: print s


