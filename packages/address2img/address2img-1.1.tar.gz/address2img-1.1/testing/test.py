import mapnik
stylesheet = 'world_style.xml'
image = 'world_style.png'
m = mapnik.Map(400, 100)
mapnik.load_map(m, stylesheet)

extent = mapnik.Box2d(-180, 0, 180, 90) # (min lon, min lat, max lon, max lat
m.zoom_to_box(extent)
mapnik.render_to_file(m, image)
print "rendered image to '%s'" % image