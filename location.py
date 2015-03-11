import los

vis = los.Visibility()

walls = [(0.0,0.0),(5.0,0.0),(5.0,6.0),(10.0,6.0),(10.0,10.0),(0.0,10.0)]
vis.setup(walls)
while running:
    current_position = (3,3)
    walls_seen = vis.run(current_position)
    print walls_seen
