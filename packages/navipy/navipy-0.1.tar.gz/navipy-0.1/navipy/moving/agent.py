"""
+-------------------------------------------+\
--------------+-------------+
|Agent class                                |\
Type of agent | Rendering   |
+===========================================+\
==============+=============+
|:class:`navipy.moving.agent.CyberBeeAgent` |\
Close loop    |Online       |
+-------------------------------------------+\
              +-------------+
|:class:`navipy.moving.agent.GraphAgent`    |\
              |Pre-rendered |
+-------------------------------------------+\
--------------+             +
|:class:`navipy.moving.agent.GridAgent`     |\
Open loop     |             |
+-------------------------------------------+\
--------------+-------------+


"""
import numpy as np
import pandas as pd
import copy
import networkx as nx
import multiprocessing
from multiprocessing import Queue, JoinableQueue, Process
import inspect
import navipy.moving.maths as navimomath
from navipy.database import DataBase
import time
import os

version = float(nx.__version__)


def defaultcallback(*args, **kwargs):
    """default call back"""
    raise NameError('No Callback')


class DefaultBrain():
    def __init__(self):
        pass

    def update(self, posorient):
        raise NameError('No Callback')

    def velocity(self):
        raise NameError('No Callback')


def posorient_columns(convention):
    return [('location', 'x'),
            ('location', 'y'),
            ('location', 'z'),
            (convention, 'alpha_0'),
            (convention, 'alpha_1'),
            (convention, 'alpha_2')]


def velocities_columns(convention):
    return [('location', 'dx'),
            ('location', 'dy'),
            ('location', 'dz'),
            (convention, 'dalpha_0'),
            (convention, 'dalpha_1'),
            (convention, 'dalpha_2')]


class AbstractAgent():
    def __init__(self, convention='zyx'):
        self._brain = DefaultBrain()
        self._alter_posorientvel = defaultcallback
        tuples = posorient_columns(convention)
        index = pd.MultiIndex.from_tuples(tuples,
                                          names=['position',
                                                 'orientation'])
        self._posorient_col = index

        tuples_vel = velocities_columns(convention)
        index_vel = pd.MultiIndex.from_tuples(tuples_vel,
                                              names=['position',
                                                     'orientation'])
        tuples_posvel = tuples
        tuples_posvel.extend(tuples_vel)
        index_posvel = pd.MultiIndex.from_tuples(tuples_posvel,
                                                 names=['position',
                                                        'orientation'])
        self._velocity_col = index_vel
        self._posorient_vel_col = index_posvel
        self._posorient_vel = pd.Series(
            index=self._posorient_vel_col,
            data=np.nan)

    @property
    def posorient(self):
        return self._posorient_vel.loc[self._posorient_col].copy()

    @posorient.setter
    def posorient(self, posorient):
        if isinstance(posorient, pd.Series) is False:
            raise TypeError('posorient should be a pandas Series')
        for col in self._posorient_col:
            if col not in posorient.index:
                raise KeyError(
                    'posorient should have {} as index'.format(col))
        self._posorient_vel.loc[self._posorient_col] = \
            posorient.loc[self._posorient_col]

    @property
    def velocity(self):
        return self._posorient_vel.loc[self._velocity_col].copy()

    @velocity.setter
    def velocity(self, velocity):
        if isinstance(velocity, pd.Series) is False:
            raise TypeError('velocity should be a pandas Series')
        for col in self._velocity_col:
            if col not in velocity.index:
                raise KeyError(
                    'velocity should have {} as index'.format(col))
        self._posorient_vel.loc[self._velocity_col] = \
            velocity.loc[self._velocity_col]

    @property
    def posorient_vel(self):
        return self._posorient_vel.copy()

    @posorient_vel.setter
    def posorient_vel(self, posorient_vel):
        self.posorient = posorient_vel
        self.velocity = posorient_vel

    @property
    def brain(self):
        return inspect.getsourcelines(self._brain)

    @brain.setter
    def brain(self, brain):
        self._brain = brain

    @property
    def alter_posorientvel(self):
        return inspect.getsourcelines(self._alter_posorientvel)

    def move(self):
        self._brain.update(self.posorient)
        self.velocity = self._brain.velocity()
        alteredpos = self._alter_posorientvel(self._posorient_vel)
        self.posorient = alteredpos
        self.velocity = alteredpos

    def fly(self, max_nstep, return_tra=False):
        """move cyberbee until max step has been performed
        """
        if return_tra:
            trajectory = pd.DataFrame(index=range(0, max_nstep),
                                      columns=self._posorient_vel_col)
            trajectory.loc[0, :] = self._posorient_vel.copy()
        for stepi in range(1, max_nstep):
            self.move()
            if return_tra:
                trajectory.loc[stepi, :] = self._posorient_vel.copy()
        if return_tra:
            return trajectory
        else:
            return None


class CyberBeeAgent(AbstractAgent, Process):
    """
    A CyberBeeAgent uses the rendering method of cyberbee. \
CyberBeeAgent is a close loop agent and need to be run within blender \
(see :doc:`rendering`).

    Single process
    Here come example of how to use it

    Multi process
    CyberBeeAgent inherit from the Process \
    class of the multiprocessing module of the standard python \
    library. Thus, several GridAgents can safely be run in parallel.

    """

    def __init__(self, brain, convention,
                 posorients_queue=None,
                 results_queue=None):
        if convention is None:
            raise Exception("a convention must be specified")
        if (posorients_queue is not None) and (results_queue is not None):
            multiprocessing.Process.__init__(self)
        AbstractAgent.__init__(self, convention)
        AbstractAgent._alter_posorientvel = \
            lambda motion_vec: navimomath.next_pos(motion_vec,
                                                   move_mode='free_run')
        self._alter_posorientvel = \
            lambda motion_vec: navimomath.next_pos(motion_vec,
                                                   move_mode='free_run')
        self.brain = brain
        self._posorients_queue = posorients_queue
        self._results_queue = results_queue

    def run(self):
        """ Only supported when multiprocess"""
        if self._posorients_queue is None or self._results_queue is None:
            raise NameError('Single agent class has not be inititialised '
                            + 'with multiprocessing suppport')
        proc_name = self.name
        print('Process {} started'.format(proc_name))
        while True:
            start_posorient = self._posorients_queue.get(timeout=1)
            if start_posorient is None:
                # Poison pill means shutdown)
                break
            common_id = list(set(start_posorient.index).intersection(
                self._posorient_vel.index))
            self._posorient_vel.loc[common_id] = start_posorient.loc[common_id]
            self._posorient_vel.name = start_posorient.name
            self.move()
            posorient_vel = self._posorient_vel
            self._posorients_queue.task_done()
            self._results_queue.put(posorient_vel)
        self._posorients_queue.task_done()
        print('Process {} done'.format(proc_name))


class GridAgent(AbstractAgent, Process):
    """
    A GridAgent fetches the scene from a pre-rendered database. \
(see :doc:`database`)
GridAgent is a close loop agent here its position is snap to a grid.

    Single process
    Here come example of how to use it

    Multi process
    GridAgent inherit from the Process \
    class of the multiprocessing module of the standard python \
    library. Thus, several GridAgents can safely be run in parallel.


    """

    def __init__(self, brain,
                 posorients_queue=None,
                 results_queue=None):
        if not isinstance(brain.renderer, DataBase):
            msg = 'GridAgent only works with a brain having '
            msg += 'a renderer of type DataBase'
            raise TypeError(msg)
        convention = brain.renderer.rotation_convention
        if (posorients_queue is not None) and (results_queue is not None):
            multiprocessing.Process.__init__(self)
        AbstractAgent.__init__(self, convention)
        self._alter_posorientvel = self.snap_to_grid
        self.brain = brain
        self._posorients_queue = posorients_queue
        self._results_queue = results_queue

    @property
    def mode_of_motion(self):
        """
        """
        toreturn = self._mode_move
        toreturn['describe'] = \
            navimomath.mode_moves_supported()[
                self._mode_move['mode']]['describe']
        return toreturn

    @mode_of_motion.setter
    def mode_of_motion(self, mode):
        """

        """
        if not isinstance(mode, dict):
            raise TypeError('Mode is not a dictionary')
        if 'mode' not in mode:
            raise KeyError("'mode' is not a key of mode")
        if 'param' not in mode:
            raise KeyError("'param' is not a key of mode")
        if mode['mode'] in navimomath.mode_moves_supported().keys():
            for param in navimomath.mode_moves_supported()[
                    mode['mode']]['param']:
                if param not in mode['param']:
                    raise KeyError(
                        "'{}' is not in mode['param']".format(param))
            self._mode_move = mode
        else:
            raise ValueError('mode is not supported')

    def snap_to_grid(self, posorient_vel):
        posorient_vel = navimomath.next_pos(
            posorient_vel,
            move_mode=self._mode_move['mode'],
            move_param=self._mode_move['param'])
        tmppos = self._brain.posorients
        tmp = navimomath.closest_pos(
            posorient_vel, tmppos)  # self._brain.posorients)
        posorient_vel.loc[self._posorient_col] = \
            tmp.loc[self._posorient_col]
        posorient_vel.name = tmp.name
        return posorient_vel

    def move(self):
        if hasattr(self, '_mode_move'):
            AbstractAgent.move(self)
        else:
            raise AttributeError(
                'GridAgent object has no attribute _mode_move\n' +
                'Please set the mode of motion')

    def fly(self, max_nstep, return_tra=False):
        if hasattr(self, '_mode_move'):
            return AbstractAgent.fly(self, max_nstep, return_tra)
        else:
            raise AttributeError(
                'GridAgent object has no attribute _mode_move\n' +
                'Please set the mode of motion')

    def run(self):
        """ Only supported when multiprocess"""
        if self._posorients_queue is None or self._results_queue is None:
            raise NameError('Single agent class has not be inititialised '
                            + 'with multiprocessing suppport')
        proc_name = self.name
        print('Process {} started'.format(proc_name))
        while True:
            start_posorient = self._posorients_queue.get(timeout=1)
            if start_posorient is None:
                # Poison pill means shutdown)
                break
            common_id = list(set(start_posorient.index).intersection(
                self._posorient_vel.index))
            self._posorient_vel.loc[common_id] = start_posorient.loc[common_id]
            self.move()
            next_posorient = self._posorient_vel
            self._posorients_queue.task_done()
            self._results_queue.put((start_posorient, next_posorient))
        self._posorients_queue.task_done()
        print('Process {} done'.format(proc_name))


class GraphAgent():
    """
    A GraphAgent uses, to build a graph,

1. pre-rendered scene from a database to derive \
the agent motion, or
2. pre-computed agent-motion


    """

    def __init__(self, brain, mode_of_motion):
        self._brain = copy.copy(brain)
        # Init the graph
        self._graph = nx.DiGraph()
        if not isinstance(self._brain.renderer, DataBase):
            msg = 'GraphAgent only works with a brain having '
            msg += 'a renderer of type DataBase'
            raise TypeError(msg)
        for row_id, posor in self._brain.posorients.iterrows():
            posor.name = row_id
            self._graph.add_node(row_id,
                                 posorient=posor)
        self.mode_of_motion = mode_of_motion
        # Create a dataframe to store the velocities
        convention = self._brain.renderer.rotation_convention
        tuples_posvel = posorient_columns(convention)
        tuples_posvel.extend(velocities_columns(convention))
        index_posvel = pd.MultiIndex.from_tuples(tuples_posvel,
                                                 names=['position',
                                                        'orientation'])
        self.velocities = pd.DataFrame(columns=index_posvel,
                                       index=list(self._graph.nodes()))

    @property
    def graph(self):
        return self._graph

    @graph.setter
    def graph(self, graph):
        if isinstance(graph, nx.DiGraph) is False:
            raise TypeError('graph is not a nx.DiGraph')
        self._graph = graph.copy()
        self.check_graph()

    def compute_velocities(self,
                           ncpu=5,
                           timeout=1,
                           filename=None,
                           blocksize=100):
        if os.path.exists(filename):
            self.velocities = pd.read_hdf(filename)
        nodes_tocompute = self.velocities.isna().any(axis=1)
        nodes_tocompute = nodes_tocompute[nodes_tocompute].index
        # Build a list of nodes
        posorients_queue = JoinableQueue()
        results_queue = Queue()
        for node in nodes_tocompute:
            posorients_queue.put(self._graph.nodes[node]['posorient'])

        # Start ndatabase loader
        convention = self._brain.renderer.rotation_convention
        num_agents = ncpu
        agents = [CyberBeeAgent(copy.copy(self._brain),
                                convention=convention,
                                posorients_queue=posorients_queue,
                                results_queue=results_queue)
                  for _ in range(num_agents)]
        for w in agents:
            w.start()

        # Add a poison pill for each agent
        for _ in range(num_agents):
            posorients_queue.put(None)

        # Wait for all of the tasks to finish
        # posorients_queue.join()
        nline = 0
        prev_nline = nline
        t_start = time.time()
        nbnodes = nodes_tocompute.shape[0]
        for _ in range(nbnodes):
            res = results_queue.get(timeout=timeout)
            self.velocities.loc[res.name, res.index] = res
            if (nline-prev_nline) > blocksize:
                t_elapse = time.time()-t_start
                t_peritem = t_elapse/nline
                remain = nbnodes-nline
                print('Computed {} in {}'.format(nline, t_elapse))
                print('Remain {}, done in {}'.format(remain, remain*t_peritem))
                if filename is not None:
                    self.velocities.to_hdf(filename, key='velocities')
                prev_nline = nline
            nline += 1
        return self.velocities.copy()

    def build_graph(self, movemode, moveparam):
        """
        Connect edges with a given velocity
        """
        if self.velocities.dropna().shape[0] == 0:
            raise NameError('compute_velocities should be called first')
        edges = pd.Series(data=np.nan, index=self.velocities.index)
        # Make sure that the velocity start at the correct location
        posorients = self._brain.posorients
        myvelocities = self.velocities.copy()
        myvelocities = myvelocities.swaplevel(axis=1)
        myvelocities.x = posorients.x
        myvelocities.y = posorients.y
        myvelocities.z = posorients.z
        myvelocities.alpha_0 = posorients.alpha_0
        myvelocities.alpha_1 = posorients.alpha_1
        myvelocities.alpha_2 = posorients.alpha_2
        myvelocities = myvelocities.swaplevel(axis=1)
        for ii, row in myvelocities.iterrows():
            if np.any(np.isnan(row)):
                continue
            # Move according to user mode of motion
            nposorient = navimomath.next_pos(row, movemode, moveparam)
            # Snap to the closest point
            nextpos_index = navimomath.closest_pos(
                nposorient, myvelocities)
            edges[ii] = nextpos_index.name
        # Format for graph
        validedges = edges.dropna()
        results_edges = np.vstack(
            [validedges.index,
             validedges.values]).transpose()
        # Add to graph
        self._graph.add_edges_from(results_edges)
        self.check_graph()

    def check_graph(self):
        self.check_single_target()

    def check_single_target(self):
        if version < 2:
            graph_nodes = list(self._graph.nodes())
        else:
            graph_nodes = list(self._graph.nodes)
        for node in graph_nodes:
            # not connected -> loop not ran
            for count, _ in enumerate(self._graph.neighbors(node)):
                # count == 0 -> connected to one node
                # count == 1 -> connected to two nodes
                if count > 0:
                    raise ValueError(
                        'Node {} leads to several locations'.format(node))

    def find_attractors(self):
        """Return a list of node going to each attractor in a graph
        """
        attractors = list()
        for attractor in nx.attracting_components(self._graph):
            att = dict()
            att['attractor'] = attractor
            attractors.append(att)
        return attractors

    def find_attractors_sources(self, attractors=None):
        """Find all sources going to each attractors
        """
        if attractors is None:
            attractors = self.find_attractors()

        if isinstance(attractors, list) is False:
            raise TypeError('Attractors should be a list of dict')
        elif len(attractors) == 0:
            raise ValueError('No attractors found')

        # Check attractor
        for att in attractors:
            keyatt = att.keys()
            if 'attractor' not in keyatt:
                raise ValueError(
                    'Each attractors should contain the key attractor')

        # Calculate connection
        for att_i, att in enumerate(attractors):

            # [0] because one node of the attractor is enough
            # all other node of the attractor are connected to this one
            target = list(att['attractor'])[0]
            attractors[att_i]['paths'] = nx.shortest_path(
                self.graph, target=target)
            attractors[att_i]['sources'] = list(
                attractors[att_i]['paths'].keys())
        return attractors

    def catchment_area(self, attractors=None):
        """Return the catchment area for attractors
        """
        if attractors is None:
            attractors = self.find_attractors_sources()

        if isinstance(attractors, list) is False:
            raise TypeError('Attractors should be a list of dict')
        elif len(attractors) == 0:
            raise ValueError('No attractors found')

        # Check attractor
        for att in attractors:
            keyatt = att.keys()
            if 'sources' not in keyatt:
                raise ValueError(
                    'Each attractors should contains a list of sources')

        return [len(att['sources']) for att in attractors]

    def reach_goals(self, goals):
        """ Return all paths to the goals """
        return nx.shortest_path(self._graph, target=goals)

    def neighboring_nodes(self, target):
        """ Return the nodes going to the target """
        # Reverse graph because nx.neighbors give the end node
        # and we want to find the start node going to target
        # not where target goes.
        tmpgraph = self._graph.reverse(copy=True)
        neighbors = tmpgraph.neighbors(target)
        return neighbors
