This file describes the different files in this Github repository.

The Drone, Weapons, gbad files are the basic classes that are used to define and 
store the different variables of the environment. 
For example, the Drone class file will be used to store and update the important elements of each drone such as its position,
speed, threat value, etc. On the other hand, the MIP_Assignment.py, MIP_for_comparison.py and 
Sim_MIP.py files are basic simulators that use the greedy algorithm to solve the WTA problem.
The Sim_dynamic files (in several versions v1, v2, v3, v4) are also simulators but they have a
dynamic aspect as explained in the thesis through different versions of the value function.
All versions of the value function are defined and updated in the Value_function.py file.
Sim_almost_MDP.py is the first attempt at a simulator using the Markov decision process.

Finally, the Stats.py file brings together several simulators to compare the performances
through graphs drawn using the matplotlib.pyplot library of Python.
