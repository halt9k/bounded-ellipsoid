import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, draw, show
from matplotlib.animation import FuncAnimation
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.patches import Ellipse
from math import pi
import typing

class PointsDrawer:    
    pts_cloud: np.array
    fig: Figure
    ax3D: Axes    
    pt_average: np.array; pt_foci_1: np.array; pt_foci_2: np.array
    stg = 0
    _pts_animations: np.array

    prev_pt_highlights = None
    prev_quivers  = None

    def __init__(self, pts, stg, foci_1, foci_2, _pts_animations):
        self.pts_cloud = pts
        self.pt_average =  (foci_1 + foci_2)/2
        self.pt_foci_1 = foci_1
        self.pt_foci_2 = foci_2
        self.stg = stg
        self._pts_animations = _pts_animations


    def draw_pt(self, pt, acolor, alabel, asize = 5):        
        return self.ax3D.scatter(pt[0], pt[1], pt[2], s=asize, c=acolor, marker="o", label=alabel)

    def draw_el(self):
        f1, f2, stg, avg = self.pt_foci_1, self.pt_foci_2, self.stg, self.pt_average
        
        a = stg / 2                       # Semimajor axis
        f = np.linalg.norm((f1 - f2) / 2)
        b = np.sqrt(a**2 - f**2)          # Semiminor axis
        t = np.linspace(0, 2*np.pi, 100)

        def draw_plane_el(ax1, ax2):
            vec = np.transpose([avg] * len(t))
            phi = np.arctan2((f2[ax2] - f1[ax2]), (f2[ax1] - f1[ax1]))
            vec[ax1] += a * np.cos(t) * np.cos(phi) - b * np.sin(t) * np.sin(phi)
            vec[ax2] += a * np.cos(t) * np.sin(phi) + b * np.sin(t) * np.cos(phi)
            plt.plot(vec[0], vec[1], vec[2])
        draw_plane_el(0, 1)
        draw_plane_el(1, 2)
        draw_plane_el(0, 2)


    def plot3D(self):
        ax3D = self.ax3D
        ax3D.clear()

        data = self.pts_cloud.transpose()    
        ax3D.scatter(data[0], data[1], data[2], s=5, c='black', marker="s", label='cloud')
   
        self.draw_pt(self.pt_foci_1, 'b', 'f1', 30)
        self.draw_pt(self.pt_foci_2, 'b', 'f2', 30)
        self.draw_pt(self.pt_average, 'b', 'avg')
        self.draw_el()



    def plot3D_update(self, i):
        avg = self.pt_average

        if self.prev_pt_highlights is not None:
            self.prev_pt_highlights.remove()
        if self.prev_quivers is not None:
            self.prev_quivers.remove()

        cur_pt = self._pts_animations[i][0]
        self.prev_pt_highlights = self.draw_pt(cur_pt, 'r', 'cur_pt', 30)

        cur_foc = self._pts_animations[i][1]
        self.prev_quivers = self.ax3D.quiver(avg[0], avg[1], avg[2], cur_foc[0], cur_foc[1], cur_foc[2])    

    def draw(self):
        self.fig, self.ax3D = plt.subplots(subplot_kw=dict(projection="3d"))

        self.plot3D()
        def update(i):
            self.plot3D_update(i)

        len_pts = len(self.pts_cloud)
        ani = FuncAnimation(self.fig, update, frames=len_pts, interval=10/len_pts)
       
        limits = np.array([getattr(self.ax3D, f'get_{axis}lim')() for axis in 'xyz'])
        self.ax3D.set_box_aspect(np.ptp(limits, axis = 1))

        plt.show()