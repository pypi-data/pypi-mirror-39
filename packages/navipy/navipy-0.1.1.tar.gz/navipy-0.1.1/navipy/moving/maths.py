"""
Mathematical computation are done in this module. Those involve mostly
geometry, and predefined grids shapes
"""
import numpy as np
import pandas as pd


def mode_moves_supported():
    return {
        'on_cubic_grid': {
            'param':
            ['grid_spacing'],
            'describe':
            "Agent restricted to move on a grid"},
        'free_run': {
            'param': [],
            'describe':
            "Freely moving agent, pos(t+dt)=pos+speed (dt=1)"}}


def next_pos(motion_vec, move_mode, move_param=None):
    """return the future position knowing speed and current position

    :param motion_vec: the position and speed of the agent
(pandas Series with columns ['x','y','z','dx','dy','dz'])
    :param grid_spacing: the spacing between two grid points
(only relevant for regular grids)
    :param grid_mode: the type of grid.

    ..todo: add literal include for supported_grid_mode
    """
    if isinstance(motion_vec, pd.Series) is False:
        raise TypeError('motion vector must be a pandas Series')
    if move_mode not in mode_moves_supported().keys():
        raise KeyError(
            'move mode must is not supported {}'.format(move_mode))
    tuples = [('location', 'dx'), ('location', 'dy'),
              ('location', 'dz')]
    index = pd.MultiIndex.from_tuples(tuples,
                                      names=['position',
                                             'orientation'])
    speed = pd.Series(index=index)
    speed.loc[('location', 'dx')] = motion_vec[('location', 'dx')]
    speed.loc[('location', 'dy')] = motion_vec[('location', 'dy')]
    speed.loc[('location', 'dz')] = motion_vec[('location', 'dz')]
    # speed = motion_vec.loc[['dx', 'dy', 'dz']]
    if move_mode == 'on_cubic_grid':
        # speed in spherical coord
        epsilon = np.arctan2(speed['location']['dz'],
                             np.sqrt(speed['location']['dx']**2 +
                                     speed['location']['dy']**2))
        phi = np.arctan2(speed['location']['dy'], speed['location']['dx'])
        radius = np.sqrt(np.sum(speed**2))
        if np.isclose(radius, 0):
            # scaling = 0
            speed = 0 * speed
        else:
            tuples = [('location', 'dx'), ('location', 'dy'),
                      ('location', 'dz')]
            index = pd.MultiIndex.from_tuples(tuples,
                                              names=['position',
                                                     'orientation'])
            deltas = pd.Series(index=index)
            deltas['location']['dz'] = float(epsilon > (np.pi / 8) -
                                             epsilon < (np.pi / 8))
            edgecases = np.linspace(-np.pi, np.pi, 9)
            case_i = np.argmin(np.abs(phi - edgecases))
            if case_i == 8 or case_i == 0 or case_i == 1 or case_i == 7:
                deltas['location']['dx'] = -1
            elif case_i == 3 or case_i == 4 or case_i == 5:
                deltas['location']['dx'] = 1
            else:
                deltas['location']['dx'] = 0

            if case_i == 1 or case_i == 2 or case_i == 3:
                deltas['location']['dy'] = -1
            elif case_i == 5 or case_i == 6 or case_i == 7:
                deltas['location']['dy'] = 1

            else:
                deltas['location']['dy'] = 0
            # scaling = 1
            speed = move_param['grid_spacing'] * deltas
    elif move_mode is 'free_run':
        pass
        # scaling = 1  # <=> dt = 1, user need to scale speed in dt units
    else:
        raise ValueError('grid_mode is not supported')
    toreturn = motion_vec.copy()
    toreturn.loc[('location', 'x')] += speed['location']['dx']
    toreturn.loc[('location', 'y')] += speed['location']['dy']
    toreturn.loc[('location', 'z')] += speed['location']['dz']
    return toreturn


def closest_pos(pos, positions):
    """Return the closest position from a list of positions

    :param pos: the position to find (a pandas Series with ['x','y','z']
    :param positions: the possible closest positions
    (a pandas dataframe with
    [['location','x'],['location','y'],['location','z']])
    """

    euclidian_dist = np.sqrt(
        (pos['location']['x'] - positions['location']['x'])**2
        + (pos['location']['y'] - positions['location']['y'])**2
        + (pos['location']['z'] - positions['location']['z'])**2)
    return positions.loc[euclidian_dist.idxmin()]


def closest_pos_memory_friendly(pos, database):
    """Return the closest position from a list of positions

    :param pos: the position to find (a pandas Series with ['x','y','z']
    :param database: the possible closest positions
    (a pandas dataframe with ['x','y','z'])
    """
    raise NameError('Not implemated')
