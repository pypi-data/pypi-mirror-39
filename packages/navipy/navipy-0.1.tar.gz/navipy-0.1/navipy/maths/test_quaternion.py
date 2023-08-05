import unittest
import numpy as np
import navipy.maths.homogeneous_transformations as ht
import navipy.maths.quaternion as quat
import navipy.maths.random as random


class TestQuaternions(unittest.TestCase):
    def test_quaternion_from_euler(self):
        quaternion = quat.from_euler(1, 2, 3, 'yxz')
        self.assertTrue(np.allclose(quaternion,
                                    [0.435953, 0.310622,
                                     -0.718287, 0.444435]))

    def test_about_axis(self):
        quaternion = quat.about_axis(0.123, [1, 0, 0])
        self.assertTrue(np.allclose(quaternion,
                                    [0.99810947, 0.06146124, 0, 0]))

    def test_matrix(self):
        quaternion = np.random.rand(4)
        quaternion /= np.sqrt(np.sum(quaternion**2))
        matrix = quat.matrix(quaternion)
        quaternion_fm = quat.from_matrix(matrix)
        np.testing.assert_allclose(quaternion_fm, quaternion)

    def test_matrix_identity(self):
        matrix = quat.matrix([1, 0, 0, 0])
        self.assertTrue(np.allclose(matrix, np.identity(4)))

    def test_matrix_diagonal(self):
        matrix = quat.matrix([0, 1, 0, 0])
        self.assertTrue(np.allclose(matrix, np.diag([1, -1, -1, 1])))

    def test_from_matrix_identity(self):
        quaternion = quat.from_matrix(np.identity(4))
        self.assertTrue(np.allclose(quaternion, [1, 0, 0, 0]))

    def test_from_matrix_diagonal(self):
        quaternion = quat.from_matrix(np.diag([1, -1, -1, 1]))
        self.assertTrue(np.allclose(quaternion, [0, 1, 0, 0])
                        or np.allclose(quaternion, [0, -1, 0, 0]))

    def test_from_matrix_rotation(self):
        rotation = random.rotation_matrix()
        quaternion = quat.from_matrix(rotation)
        ht.testing_is_same_transform(
            rotation, quat.matrix(quaternion))

    def test_inverse(self):
        quaternion_0 = random.quaternion()
        quaternion_1 = quat.inverse(quaternion_0)
        self.assertTrue(np.allclose(
            quat.multiply(quaternion_0, quaternion_1),
            [1, 0, 0, 0]))


if __name__ == '__main__':
    unittest.main()
