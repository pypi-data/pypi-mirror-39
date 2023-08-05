"""
Close-loop agent
~~~~~~~~~~~~~~~~
A standard method to move an agent is to update:

1. update the sensory information at the current agent location :math:`x`
2. deduce the agent motion :math:`vdt` from this information
3. displace the agent by motion ( :math:`x\\rightarrow x + vdt`)


The use of a close loop model including visual rendering is \
sometimes too slow to efficiently test several models or tune the \
parameters of a given models. The GridAgent solves this problem by \
restricting the agent motion on locations with rendered scene. The \
agent moves thus on a grid, and its next position is always \
snapped to the closest grid location. The finer the grid is, the \
larger the database storing all sceneries and grid location is; \
but also the more accurate the agent motion is. The grid size \
depend on the storage space, the time you can wait for the \
database creation, and how sensitive to exact location your model is.

This iterative method can be used with a wide range of models. \
In :navipy: differents classes of agents exist. \
They differ by the method use to update the sensory information:

+----------------+----------------------------------------------------+
|Agent class     |Sensory update                                      |
+================+====================================================+
|:CyberBeeAgent: |:Cyberbee: update within blender.                   |
+----------------+----------------------------------------------------+
|:GridAgent:     |:DataBase: update from a pre-rendered database. |
+----------------+----------------------------------------------------+

To deduce the agent motion from the current state of the agent \
(e.g. position, orientation, sensory information, memories, ...) all \
classes of agents use callback function, which is a custom function \
defined by the user. This function takes as input argument, the \
agent position-orientation and its velocities, and the currently \
seen scene. The function should return a the agent motion. \

Once the agent sensory method and motion method have been configured, \
the agent can:

1. move (perform a one step motion), or
2. fly (move until its velocity is null, or until n-steps).

Agent on a graph
~~~~~~~~~~~~~~~~
As mentioned above, in every model of navigation the agent motion \
is derived from its current external state, its position \
orientation as well as the derivatives, and its internal state. \
However, when the agent motion is only derived from its current \
position orientation, and what is seen from this location, the \
simulation of an agent can be drastically simplified. Indeed, \
not only the scene at relevant location can be pre-rendered, but \
the motion of the agent from those locations as well.

The agent being restricted to move from relevant locations to \
relevant locations, a graph of interconnected locations can be built.\
The nodes of the graph are the relevant locations, and the directed \
edges the motion of the agent from one location to the next. \
:GraphAgent: can build such graph by simply using a database of \
pre-rendered scenery at relevant locations, and a function \
giving the motion of the agent from a scene and the agent \
position orientation. Once the graph has been generated, \
attractors can be found, the number of locations converging to \
those (i.e. the catchment area or volume), if two locations are \
connected, etc.

To speed up certain calculations, additional values can stored \
at each graph node and access from the callback function. It is \
worth mentioning a warning here. The size of the graph can be \
incredibly large. Thus, not too much information can be stored \
at each node. To assess the memory size of the graph before \
creating it, one can use the tool agent.tools.assess_graphmemsize.
"""
