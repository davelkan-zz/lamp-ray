import los

vis = los.Visibility()

walls = [(0.0,0.0),(5.0,0.0),(5.0,6.0),(10.0,6.0),(10.0,10.0),(0.0,10.0)]
vis.setup(walls)
walls_seen = vis.run((3,3))
print walls_seen
