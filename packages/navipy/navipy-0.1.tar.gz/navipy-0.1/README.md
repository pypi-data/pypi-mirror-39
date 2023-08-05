# About navipy

Navipy is a package providing method to simulate a navigating agent in realistic environment. Navipy make use of the blender rendering engine and its python API. Therefore any environment that can be realised with blender, can be used by navipy. Blender rendering may however be too slow to test different model of navigation or the different parameters of a given model. To speed up the simulation, the scene at relevant location in the environment can be stored in a database. Then, instead of rendering the scene again, it is simply loaded from the database. The agent can, thus, jump from relevant location to the next (i.e. move on a grid) without the need to use the blender API. Moreover, certain models of navigation do not depend on the history of the agent, but instead associate a moving direction to the current agent location. With such model, a graph can be created from the moving direction at each location on a grid of relevant places. The graph make use of the package networkx, thus attracting points or loop can be found, the possible connection from one point on the grid to another can be assessed, the number of independent sub graph can be calculated, etc.

# Goals

The navigation toolbox aims to bring in an intuitive python toolbox different methods to model the visual navigation of a virtual agent. 
-    Keep the interface simple
-    Allow complex environments and realistic world scenario
-    Implement the most popular model of insect navigation
-    Avoid re-rendering by using grid constrained motion.

# How to install the navigation toolbox
The rendering from the insect point of view is done with the blender rendering engine. Thus, you will need to first install Blender
https://www.blender.org/

## Windows
We recommend using Anaconda (https://www.anaconda.com/) and create a virtual environment within it before installing the toolbox. 

Start the Anaconda Prompt, and then enter
```
conda update conda
```
Upadate any packages if necessary by typing y to proceed

Then, create a virtual environment for your project
```
conda create -n yourenvname python=x.x anaconda
```
here `yourenvname` is the name of your project (without special characters and spaces), and `python=x.x` the version of python
to use, for example `python=3.5.3` (see table below to install a version matching with blender)

You can now activate your environment. 
```
activate yourenvname
```

and install navipy by going the root folder of the toolbox (use cd to change directory and dir to list the content of a directory), and typing
```
python setup.py install
```

You can now use the navigation toolbox. 

## Linux (Ubuntu)
From the terminal 
```
pip install update
```
Upadate any packages if necessary by typing y to proceed

Then, create a virtual environment for your project
```
mkvirtualenv yourenvname
```
here `yourenvname` is the name of your project (without special characters and spaces)

You can now activate your environment. 
```
workon yourenvname
```

and install navipy by going the root folder of the toolbox (use cd to change directory and ls to list the content of a directory), and typing
```
python setup.py install
```

## Blender-python version
Navipy can be interfaced with blender. It is highly recommended to use the same version of packages of blender when doing so, in order to reduce problem of compatibility.
To determine the packages that you will need, you can run the script: `navipy/script/check_blender_versions_pip.py` in blender or via commandline:

```
blender -b -P check_blender_versions_pip.py
```

It will create a textfile containing all packages used by blender. They can be installed in your virtualenvironment (prior to navipy) by doing:
```
pip install -r requirement.txt
```

| Blender version | Python version |
| --------------- | -------------- |
| 2.79b           | 3.5.3          |



# Code of conduct

In the interest of fostering an open and welcoming environment, we as users and developers pledge to making participation with this project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.