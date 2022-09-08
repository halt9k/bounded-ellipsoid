import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.figure import Figure


class PointsDrawer:
    pts_cloud: np.array
    fig: Figure
    ax3D: Axes
    pt_average: np.array
    pt_foci_1: np.array
    pt_foci_2: np.array
    stg = 0
    _pts_animations: np.array

    prev_pt_highlights = None
    prev_quivers = None

    def __init__(self, pts, stg, foci_1, foci_2, _pts_animations):
        self.pts_cloud = pts
        self.pt_average = (foci_1 + foci_2) / 2
        self.pt_foci_1 = foci_1
        self.pt_foci_2 = foci_2
        self.stg = stg
        self._pts_animations = _pts_animations

    def draw_point(self, pt, color, label, size=5):
        return self.ax3D.scatter(pt[0], pt[1], pt[2], s=size, c=color, marker="o", label=label)

    def draw_el_curve(self, axis1, axis2, a, b, foci_len, transform_mtr, vec_translate):
        # ax3 = avg
        vec_zero = np.array([0, 0, 0]).astype(np.float64)
        t = np.linspace(0, 2 * np.pi, 100)
        vec = np.transpose([vec_zero] * len(t))

        # idea - calculating for xz plane and then 
        # applying rotation transform matrix based on where x-axis will go
        phi = 0
        vec[axis1] += a * np.cos(t) * np.cos(phi) - b * np.sin(t) * np.sin(phi)
        vec[axis2] += a * np.cos(t) * np.sin(phi) + b * np.sin(t) * np.cos(phi)

        vec = np.add(np.array([[foci_len / 2], [0], [0]]), vec)
        vec = np.dot(transform_mtr, vec)
        vec = np.add(vec_translate.reshape(3, 1), vec)

        plt.plot(vec[0], vec[1], vec[2])

    # rotates from [1,0,0] to vec_to
    def mtr_rotation_from_x(self, vec_to):
        un_z = np.array([0, 0, 1])

        mtr_ex = vec_to / np.linalg.norm(vec_to)
        mtr_y = np.cross(un_z, vec_to)
        mtr_ey = mtr_y / np.linalg.norm(mtr_y)
        mtr_z = np.cross(mtr_ex, mtr_ey)
        mtr_ez = mtr_z / np.linalg.norm(mtr_z)

        transform_mtr = np.array([mtr_ex, mtr_ey, mtr_ez])
        return transform_mtr.T

    def draw_ellipsoid_bounds(self):
        f1, f2, stg, avg = self.pt_foci_1, self.pt_foci_2, self.stg, self.pt_average
        # for tests
        # stg = (2*2*3 + 1)**0.5
        # f2 = np.array([2,2,2])
        # f1 = np.array([0,0,0])

        voc_foci = f2 - f1
        voc_foci_len = np.linalg.norm(voc_foci)

        a = stg / 2  # Semi-major axis
        b = np.sqrt(stg ** 2 - voc_foci_len ** 2) / 2  # Semi-minor axis

        transform_mtr = self.mtr_rotation_from_x(voc_foci)

        self.draw_el_curve(0, 1, a, b, voc_foci_len, transform_mtr, f1)
        self.draw_el_curve(0, 2, a, b, voc_foci_len, transform_mtr, f1)
        self.draw_el_curve(1, 2, b, b, voc_foci_len, transform_mtr, f1)

    def plot_static_objects(self):
        ax3D = self.ax3D
        ax3D.clear()

        data = self.pts_cloud.transpose()
        ax3D.scatter(data[0], data[1], data[2], s=5, c='black', marker="s", label='cloud')

        self.draw_point(self.pt_foci_1, 'b', 'f1', 40)
        self.draw_point(self.pt_foci_2, 'b', 'f2', 40)
        self.draw_point(self.pt_average, 'b', 'avg')
        self.draw_ellipsoid_bounds()

    def plot_animations(self, i):
        avg = self.pt_average

        if self.prev_pt_highlights is not None:
            self.prev_pt_highlights.remove()
        if self.prev_quivers is not None:
            self.prev_quivers.remove()

        cur_pt = self._pts_animations[i][0]
        self.prev_pt_highlights = self.draw_point(cur_pt, 'r', 'cur_pt', 30)

        cur_foc = self._pts_animations[i][1]
        self.prev_quivers = self.ax3D.quiver(avg[0], avg[1], avg[2], cur_foc[0], cur_foc[1], cur_foc[2])

    def draw(self):
        self.fig, self.ax3D = plt.subplots(subplot_kw=dict(projection="3d"))

        self.plot_static_objects()

        def update(i):
            self.plot_animations(i)

        len_pts = len(self.pts_cloud)
        ani = FuncAnimation(self.fig, update, frames=len_pts, interval=10 / len_pts)

        limits = np.array([getattr(self.ax3D, f'get_{axis}lim')() for axis in 'xyz'])
        self.ax3D.set_box_aspect(np.ptp(limits, axis=1))

        plt.show()
