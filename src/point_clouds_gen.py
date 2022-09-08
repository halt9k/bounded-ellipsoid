import numpy as np


class Sample:
    # np.random.seed()
    @staticmethod
    def rand_vec(length):
        return np.random.rand(1, 3) * length + 0.5

    @staticmethod
    def sphere(pts_count, ndim=3):
        vec = np.random.randn(ndim, pts_count)
        vec /= np.linalg.norm(vec, axis=0)
        return np.transpose(vec)

    @staticmethod
    def ball(pts_count, ndim=3):
        vec = np.random.randn(ndim, pts_count)
        return np.transpose(vec)

    @staticmethod
    def cube(pts_count):
        vec = np.random.rand(pts_count, 3) - [0.5, 0.5, 0.5]
        for n in range(pts_count):
            vec[n][np.random.randint(3)] = np.random.randint(2) - 0.5
        return vec * 10

    @staticmethod
    def spheres(pts_count, count):
        spheres = np.array([], dtype=np.float).reshape(0, 3)
        for n in range(count):
            sph = Sample.sphere(pts_count) + Sample.rand_vec(20) - 5
            spheres = np.vstack([spheres, sph])
        return spheres

    @staticmethod
    def line(pts_count):
        a, b = Sample.rand_vec(10), Sample.rand_vec(10)
        pts = a + np.transpose(np.transpose(b - a) * np.random.rand(pts_count))
        pts += np.random.rand(pts_count, 3)
        return pts

    @staticmethod
    def rnd_transform(pts: np.array):
        mtr = np.random.rand(3, 3) * [[2, 0, 0], [0, 1, 1], [0, 1, 1]]
        return pts @ mtr
