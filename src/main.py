import numpy as np

from bounded_ellipsoid_alg import find_ellipsoid
from point_clouds_gen import Sample
from visuals import PointsDrawer

np.random.seed()
pts = Sample.spheres(50, 2)
# pts = Sample.sphere(400)
# pts = Sample.ball(200)
# pts = Sample.cube(400)
# pts = Sample.line(200)

# unnecessary random transform of point cloud to spice it
# pts = Sample.rnd_transform(pts)

foci_1, foci_2, elp_string, _pts_animation = find_ellipsoid(pts)
print(foci_1, foci_2, elp_string)

cd = PointsDrawer(pts, elp_string, foci_1, foci_2, _pts_animation)
cd.draw()
