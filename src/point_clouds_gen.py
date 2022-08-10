import numpy as np
import typing

class Sample:
    # np.random.seed()
    @staticmethod
    def rand_vec(length):
        return np.random.rand(1, 3) * length + 0.5

    @staticmethod
    def sphere(npoints, ndim=3):
        vec = np.random.randn(ndim, npoints)
        vec /= np.linalg.norm(vec, axis=0)
        return np.transpose(vec)

    @staticmethod
    def ball(npoints, ndim=3):
        vec = np.random.randn(ndim, npoints)    
        return np.transpose(vec)

    @staticmethod
    def cube(npoints):
        vec = np.random.rand(npoints, 3) - [0.5, 0.5, 0.5]
        for n in range(npoints):
             vec[n][np.random.randint(3)] = np.random.randint(2)-0.5
        return  vec * 10

    @staticmethod
    def spheres(npoints, count):
        spheres = np.array([], dtype=np.float).reshape(0,3)
        for n in range(count):
            sph = Sample.sphere(npoints) + Sample.rand_vec(20) - 5
            spheres = np.vstack([spheres, sph])
        return spheres

    @staticmethod
    def line(npoints):
        a, b = Sample.rand_vec(10), Sample.rand_vec(10)
        pts = a + np.transpose( np.transpose(b - a) * np.random.rand(npoints))
        pts += np.random.rand(npoints, 3)
        return pts

    @staticmethod
    def rnd_transform(pts: np.array):
        mtr = np.random.rand(3, 3) * [[2, 0, 0], [0, 1, 1], [0, 1, 1]]
        return pts @ mtr

        
        