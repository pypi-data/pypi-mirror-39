"""
Test of agent
"""
import numpy as np
import pandas as pd
import networkx as nx
import navipy.moving.agent as naviagent
import navipy.database as navidb
from navipy import Brain
import pkg_resources
import warnings

import unittest

version = float(nx.__version__)


class BrainTest(Brain):
    def __init__(self, renderer=None):
        Brain.__init__(self, renderer=renderer)
        convention = 'zyx'
        tuples = [('location', 'x'), ('location', 'y'),
                  ('location', 'z'), (convention, 'alpha_0'),
                  (convention, 'alpha_1'), (convention, 'alpha_2')]
        index = pd.MultiIndex.from_tuples(tuples,
                                          names=['position',
                                                 'orientation'])
        self.__posorient_col = index
        tuples_vel = [('location', 'x'), ('location', 'y'),
                      ('location', 'z'), (convention, 'alpha_0'),
                      (convention, 'alpha_1'), (convention, 'alpha_2'),
                      ('location', 'dx'), ('location', 'dy'),
                      ('location', 'dz'), (convention, 'dalpha_0'),
                      (convention, 'dalpha_1'), (convention, 'dalpha_2')]
        index_vel = pd.MultiIndex.from_tuples(tuples_vel,
                                              names=['position',
                                                     'orientation'])
        self.__velocity_col = index_vel
        self.__posorient_vel_col = self.__velocity_col.copy()
        # self.__posorient_vel_col.extend(self.__velocity_col)

    def velocity(self):
        return pd.Series(data=0, index=self.__posorient_vel_col)


class TestNavipyMovingAgent(unittest.TestCase):
    def setUp(self):
        self.mydb_filename = pkg_resources.resource_filename(
            'navipy', 'resources/database.db')
        self.mydb = navidb.DataBase(self.mydb_filename, mode='r')
        self.convention = 'zyx'
        self.brain = BrainTest(self.mydb)
        tuples = [('location', 'x'), ('location', 'y'),
                  ('location', 'z'), (self.convention, 'alpha_0'),
                  (self.convention, 'alpha_1'), (self.convention, 'alpha_2')]
        index = pd.MultiIndex.from_tuples(tuples,
                                          names=['position',
                                                 'orientation'])
        self.__posorient_col = index
        tuples_vel = [('location', 'x'), ('location', 'y'),
                      ('location', 'z'), (self.convention, 'alpha_0'),
                      (self.convention, 'alpha_1'),
                      (self.convention, 'alpha_2'),
                      ('location', 'dx'), ('location', 'dy'),
                      ('location', 'dz'), (self.convention, 'dalpha_0'),
                      (self.convention, 'dalpha_1'),
                      (self.convention, 'dalpha_2')]
        index_vel = pd.MultiIndex.from_tuples(tuples_vel,
                                              names=['position',
                                                     'orientation'])
        self.__velocity_col = index_vel
        self.__posorient_vel_col = self.__posorient_col
        # self.__posorient_vel_col.extend(self.__velocity_col)
    #
    # AbstractAgent
    #

    def test_move_abstractagent(self):
        agent = naviagent.AbstractAgent()
        with self.assertRaises(NameError):
            agent.move()

    def test_fly_abstractagent(self):
        agent = naviagent.AbstractAgent()
        with self.assertRaises(NameError):
            agent.fly(max_nstep=10)

    #
    # GridAgent
    #
    def test_move_gridagent(self):
        agent = naviagent.GridAgent(self.brain)
        initposorient = None
        with warnings.catch_warnings(record=True):
            initposorient = self.brain.posorients.loc[13, :]
        initposovel = pd.Series(data=0,
                                index=self.__posorient_vel_col)
        initposovel.loc[initposorient.index] = initposorient
        agent.posorient = initposovel
        with self.assertRaises(AttributeError):
            agent.move()
        tuples = [('location', 'dx'), ('location', 'dy'),
                  ('location', 'dz')]
        index = pd.MultiIndex.from_tuples(tuples,
                                          names=['position',
                                                 'orientation'])
        mode_move = {'mode': 'on_cubic_grid',
                     'param': {'grid_spacing':
                               pd.Series(data=1,
                                         index=index)}}
        agent.mode_of_motion = mode_move
        with warnings.catch_warnings(record=True):
            agent.move()
        obtained = agent.posorient
        self.assertTrue(np.allclose(
            obtained, initposorient.loc[obtained.index]))

    def test_fly_gridagent(self):
        agent = naviagent.GridAgent(self.brain, self.convention)
        initposorient = None
        with warnings.catch_warnings(record=True):
            initposorient = self.brain.posorients.loc[13, :]
        initposovel = pd.Series(data=0,
                                index=self.__posorient_vel_col)
        initposovel.loc[initposorient.index] = initposorient
        agent.posorient = initposovel
        with self.assertRaises(AttributeError):
            agent.fly(max_nstep=10)
        tuples = [('location', 'dx'), ('location', 'dy'),
                  ('location', 'dz')]
        index = pd.MultiIndex.from_tuples(tuples,
                                          names=['position',
                                                 'orientation'])
        mode_move = {'mode': 'on_cubic_grid',
                     'param': {'grid_spacing':
                               pd.Series(data=1,
                                         index=index)}}
        agent.mode_of_motion = mode_move
        agent.fly(max_nstep=10)
        obtained = agent.posorient
        self.assertTrue(np.allclose(obtained,
                                    initposorient.loc[obtained.index]))

    #
    # GraphAgent
    #

    def test_init_graphagent(self):
        mode_of_motion = dict()
        mode_of_motion['mode'] = 'on_cubic_grid'
        mode_of_motion['param'] = dict()
        mode_of_motion['param']['grid_spacing'] = 0.5
        agent = None
        with warnings.catch_warnings(record=True):
            agent = naviagent.GraphAgent(self.brain, mode_of_motion)
        if version < 2:
            graph_nodes = list(agent.graph.nodes())
        else:
            graph_nodes = list(agent.graph.nodes)
        self.assertEqual(sorted(graph_nodes),
                         sorted(list(self.mydb.posorients.index)),
                         'Init of graph failed. Node missmatch')

    def test_graph_setter(self):
        mode_of_motion = dict()
        mode_of_motion['mode'] = 'on_cubic_grid'
        mode_of_motion['param'] = dict()
        mode_of_motion['param']['grid_spacing'] = 0.5
        agent = None
        with warnings.catch_warnings(record=True):
            agent = naviagent.GraphAgent(self.brain, mode_of_motion)
        if version < 2:
            graph_nodes = list(agent.graph.nodes())
        else:
            graph_nodes = list(agent.graph.nodes)
        graph_edges = list()
        for gnode in graph_nodes[1:]:
            graph_edges.append((gnode, graph_nodes[0]))

        graph = nx.DiGraph()
        graph.add_nodes_from(graph_nodes)
        graph.add_edges_from(graph_edges)
        agent.graph = graph

        graph_edges.append((graph_nodes[2], graph_nodes[1]))
        graph = nx.DiGraph()
        graph.add_nodes_from(graph_nodes)
        graph.add_edges_from(graph_edges)
        with self.assertRaises(ValueError):
            agent.graph = graph

    def test_catchment_area(self):
        """
        1 Test all node to first
        2 Test 11 nodes to first, 14 to 12th
        3 Two loops attractors
        """
        # Test all node to first
        mode_of_motion = dict()
        mode_of_motion['mode'] = 'on_cubic_grid'
        mode_of_motion['param'] = dict()
        mode_of_motion['param']['grid_spacing'] = 0.5
        agent = None
        with warnings.catch_warnings(record=True):
            agent = naviagent.GraphAgent(self.brain, mode_of_motion)

        if version < 2:
            graph_nodes = list(agent.graph.nodes())
        else:
            graph_nodes = list(agent.graph.nodes)
        graph_edges = list()
        for gnode in graph_nodes[1:]:
            graph_edges.append((gnode, graph_nodes[0]))

        graph = nx.DiGraph()
        graph.add_nodes_from(graph_nodes)
        graph.add_edges_from(graph_edges)
        agent.graph = graph
        attractors = agent.find_attractors()
        self.assertEqual(len(attractors), 1, 'Too many or too few attractors')
        attractors = agent.find_attractors_sources(attractors)
        catchment_area = agent.catchment_area(attractors)
        self.assertEqual(catchment_area, [len(graph_nodes)],
                         'Too big or too short catchment area')

        # Test 11 nodes to first, 14 to 12th
        graph_edges = list()
        for gnode in graph_nodes[1:11]:
            graph_edges.append((gnode, graph_nodes[0]))
        for gnode in graph_nodes[11:]:
            graph_edges.append((gnode, graph_nodes[11]))

        graph = nx.DiGraph()
        graph.add_nodes_from(graph_nodes)
        graph.add_edges_from(graph_edges)
        agent.graph = graph
        attractors = agent.find_attractors()
        self.assertEqual(len(attractors), 2, 'Too many or too few attractors')
        attractors = agent.find_attractors_sources(attractors)
        catchment_area = agent.catchment_area(attractors)
        self.assertEqual(sorted(catchment_area), [11, 14],
                         'Too big or too short catchment area')

        # Two loops attractors
        graph_edges = list()
        for snode, enode in zip(graph_nodes[:11],
                                np.roll(graph_nodes[:11], 1)):
            graph_edges.append((snode, enode))
        for snode, enode in zip(graph_nodes[11:],
                                np.roll(graph_nodes[11:], 1)):
            graph_edges.append((snode, enode))

        graph = nx.DiGraph()
        graph.add_nodes_from(graph_nodes)
        graph.add_edges_from(graph_edges)
        agent.graph = graph
        attractors = agent.find_attractors()
        self.assertEqual(len(attractors), 2, 'Too many or too few attractors')
        attractors = agent.find_attractors_sources(attractors)
        catchment_area = agent.catchment_area(attractors)
        self.assertEqual(sorted(catchment_area), [11, 14],
                         'Too big or too short catchment area')

    def test_neighboring_nodes(self):
        """ Counting neighnoring nodes for 3 situations
        1. Local maxima
        2. Saddle points
        3. Local minima
        """
        # Init the agent
        mode_of_motion = dict()
        mode_of_motion['mode'] = 'on_cubic_grid'
        mode_of_motion['param'] = dict()
        mode_of_motion['param']['grid_spacing'] = 0.5
        agent = None
        with warnings.catch_warnings(record=True):
            agent = naviagent.GraphAgent(self.brain, mode_of_motion)

        # Local maxima
        if version < 2:
            graph_nodes = list(agent.graph.nodes())
        else:
            graph_nodes = list(agent.graph.nodes)
        graph_edges = list()
        graph_edges.append((graph_nodes[0],
                            graph_nodes[1]))

        graph = nx.DiGraph()
        graph.add_nodes_from(graph_nodes)
        graph.add_edges_from(graph_edges)
        agent.graph = graph
        neighbors = agent.neighboring_nodes(graph_nodes[0])
        expected_nbh = []
        obtained_nbh = [a for a in neighbors]
        self.assertEqual(sorted(expected_nbh),
                         sorted(obtained_nbh),
                         'Problem neighbors maxima')

        # Saddle points
        graph_edges.append((graph_nodes[1],
                            graph_nodes[2]))

        graph = nx.DiGraph()
        graph.add_nodes_from(graph_nodes)
        graph.add_edges_from(graph_edges)
        agent.graph = graph
        neighbors = agent.neighboring_nodes(graph_nodes[1])
        expected_nbh = [graph_nodes[0]]
        obtained_nbh = [a for a in neighbors]
        self.assertEqual(sorted(expected_nbh),
                         sorted(obtained_nbh),
                         'Problem neighbors saddle')

        # Local maxima points
        graph_edges.append((graph_nodes[3],
                            graph_nodes[2]))

        graph = nx.DiGraph()
        graph.add_nodes_from(graph_nodes)
        graph.add_edges_from(graph_edges)
        agent.graph = graph
        neighbors = agent.neighboring_nodes(graph_nodes[2])
        expected_nbh = [graph_nodes[3], graph_nodes[1]]
        obtained_nbh = [a for a in neighbors]
        self.assertEqual(sorted(expected_nbh),
                         sorted(obtained_nbh),
                         'Problem neighbors minima')


if __name__ == '__main__':
    unittest.main()
