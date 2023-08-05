import unittest
import numpy as np
import navipy.maths.random as random
from navipy.maths.tools import vector_norm


class TestRandom(unittest.TestCase):
    def test__rotation_matrix(self):
        rotation = random.rotation_matrix()
        self.assertTrue(np.allclose(np.dot(rotation.T, rotation),
                                    np.identity(4)))

    def test_random_quaternion(self):
        quaternion = random.quaternion()
        self.assertTrue(np.allclose(1, vector_norm(quaternion)))


if __name__ == '__main__':
    unittest.main()
