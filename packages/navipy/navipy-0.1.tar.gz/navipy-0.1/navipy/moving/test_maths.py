"""
Test of maths
"""
import numpy as np
import pandas as pd
import navipy.moving.maths as navimaths
import unittest


class TestNavipyMovingMaths(unittest.TestCase):
    """ A class to test some mathy function of the toolbox
    """

    def test_motion_vec_pandas(self):
        """ Test that a TypeError is correctly raised
        """
        motion_vec = 'NotPandas'
        move_mode = 'on_cubic_grid'
        mode_param = dict()
        mode_param['grid_spacing'] = 1
        with self.assertRaises(TypeError):
            navimaths.next_pos(motion_vec,
                               move_mode,
                               move_mode)

    def test_notsupported_mofm(self):
        """ Test that a TypeError is correctly raised
        """
        tuples = [('location', 'x'), ('location', 'y'),
                  ('location', 'z'), ('location', 'dx'),
                  ('location', 'dy'), ('location', 'dz')]
        index = pd.MultiIndex.from_tuples(tuples,
                                          names=['position',
                                                 'orientation'])
        motion_vec = pd.Series(data=0,
                               index=index)
        move_mode = 'NotSupportedMode'
        mode_param = dict()
        mode_param['grid_spacing'] = 1
        with self.assertRaises(KeyError):
            navimaths.next_pos(motion_vec,
                               move_mode,
                               move_mode)

    def test_null_velocity(self):
        """ Test null velocity

        When the agent has a null velocity, the next postion
        should be equal to the current position. Here, we
        test this by series equality.
        """
        # Test if stay at same position.
        tuples = [('location', 'x'), ('location', 'y'),
                  ('location', 'z'), ('location', 'dx'),
                  ('location', 'dy'), ('location', 'dz')]
        index = pd.MultiIndex.from_tuples(tuples,
                                          names=['position',
                                                 'orientation'])
        motion_vec = pd.Series(data=0,
                               index=index)
        move_mode = 'on_cubic_grid'
        mode_param = dict()
        mode_param['grid_spacing'] = 1
        new_pos = navimaths.next_pos(motion_vec, move_mode, mode_param)
        self.assertTrue(new_pos.equals(motion_vec),
                        'At null velocity the agent should not move')

    def test_closest_cubic(self):
        """ Test if the snaping to cubic is correct

        When the agent move on the grid, its position has to be snapped
        to the grid position. On a cubic grid, the instability is at
        22.5 degrees modulo 45 degrees. We therefore test the functions
        close to each instability.
        """
        tuples = [('location', 'x'), ('location', 'y'),
                  ('location', 'z')]
        index = pd.MultiIndex.from_tuples(tuples,
                                          names=['position',
                                                 'orientation'])
        positions = pd.DataFrame(data=[[0, 0, 0],
                                       [0, 1, 0],
                                       [0, 2, 0],
                                       [1, 0, 0],
                                       [1, 1, 0],
                                       [1, 2, 0],
                                       [2, 0, 0],
                                       [2, 1, 0],
                                       [2, 2, 0]],
                                 columns=index,
                                 dtype=np.float)
        move_mode = 'on_cubic_grid'
        move_param = dict()
        tuples = [('location', 'dx'), ('location', 'dy'),
                  ('location', 'dz')]
        index = pd.MultiIndex.from_tuples(tuples,
                                          names=['position', 'orientation'])
        move_param['grid_spacing'] = pd.Series(data=1,
                                               index=index)
        expected_dict = dict()
        expected_dict[-22] = 7  # [2,1]
        expected_dict[22] = 7
        expected_dict[24] = 8  # [2,2]
        expected_dict[67] = 8
        expected_dict[68] = 5  # [1,2]
        expected_dict[112] = 5
        expected_dict[113] = 2  # [0,2]
        expected_dict[157] = 2
        expected_dict[158] = 1  # [0, 1]
        expected_dict[202] = 1
        expected_dict[204] = 0  # [0, 0]
        expected_dict[247] = 0
        expected_dict[248] = 3  # [1, 0]
        expected_dict[292] = 3
        expected_dict[293] = 6  # [2, 0]
        expected_dict[337] = 6
        expected_dict[338] = 7  # equivalent to -22
        tuples2 = [('location', 'x'), ('location', 'y'),
                   ('location', 'z'), ('location', 'dx'),
                   ('location', 'dy'), ('location', 'dz')]
        index2 = pd.MultiIndex.from_tuples(tuples2,
                                           names=['position', 'orientation'])

        for angle, exp_i in expected_dict.items():
            alpha = np.deg2rad(angle)
            motion_vec = pd.Series(
                data=[1, 1, 0,
                      np.cos(alpha), np.sin(alpha), 0],
                index=index2,
                dtype=np.float)
            newpos = navimaths.next_pos(motion_vec,
                                        move_mode,
                                        move_param)
            snappos = navimaths.closest_pos(newpos, positions)
            self.assertEqual(snappos.name, exp_i,
                             'closest pos is not correctly snapped')


if __name__ == '__main__':
    unittest.main()
