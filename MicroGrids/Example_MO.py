# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 12:50:26 2019

@author: someone on the internet

EXAMPLE SCRIPT FOR EPSILON AUGMENTED METHOD (w/o lexicographic optimization?)
"""

from pyomo.environ import *
import matplotlib.pyplot as plt

# max f1 = X1 <br>
# max f2 = 3 X1 + 4 X2 <br>
# st  X1 <= 20 <br>
#     X2 <= 40 <br>
#     5 X1 + 4 X2 <= 200 <br>

model = AbstractModel()

model.X1 = Var(within=NonNegativeReals)
model.X2 = Var(within=NonNegativeReals)

model.C1 = Constraint(expr = model.X1 <= 20)
model.C2 = Constraint(expr = model.X2 <= 40)
model.C3 = Constraint(expr = 5 * model.X1 + 4 * model.X2 <= 200)

model.f1 = Var()
model.f2 = Var()
model.C_f1 = Constraint(expr= model.f1 == model.X1)
model.C_f2 = Constraint(expr= model.f2 == 3 * model.X1 + 4 * model.X2)
model.O_f1 = Objective(expr= model.f1  , sense=maximize)
model.O_f2 = Objective(expr= model.f2  , sense=maximize)

instance = model.create_instance()

# ## max f1
instance.O_f2.deactivate()

solver = SolverFactory('gurobi')
solver.solve(instance);

f1_max = value(instance.f1)

# ## max f2

instance.O_f2.activate()
instance.O_f1.deactivate()

solver.solve(instance);

f2_max = value(instance.f2)

# ## min f1
instance.O_f2.deactivate()
instance.O_f1.activate()

instance.f2.fix(f2_max)

f1_min = value(instance.f1)


# ## min f2 
instance.O_f2.activate()
instance.O_f1.deactivate()

instance.f2.unfix()
instance.f1.fix(f1_max)

solver.solve(instance)

f2_min = value(instance.f2)

print('Each iteration will keep f2 lower than some values between f2_min and f2_max, so [' + str(f2_min) + ', ' + str(f2_max) + ']')


# ## apply normal $\epsilon$-Constraint

instance.O_f1.activate()
instance.O_f2.deactivate()
instance.f1.unfix()

instance.e = Param(initialize=0, mutable=True)

n = 4
step = int((f2_max - f2_min) / n)
steps = list(range(int(f2_min),int(f2_max+step),step)) 

# ## apply augmented $\epsilon$-Constraint

# max   f2 + delta*epsilon <br>
#  s.t. f2 - s = e

instance.del_component(instance.O_f1)
instance.del_component(instance.O_f2)

instance.delta = Param(initialize=0.00001)

instance.s = Var(within=NonNegativeReals)

instance.O_f1 = Objective(expr = instance.f1 + instance.delta * instance.s, sense=maximize)

instance.C_e = Constraint(expr = instance.f2 - instance.s == instance.e)


x1_l = []
x2_l = []
for i in steps:
    instance.e = i
    instance.f1.setlb(f1_min)
    instance.f1.setub(f1_max)
    solver.solve(instance);
    x1_l.append(value(instance.X1))
    x2_l.append(value(instance.X2))
plt.plot(x1_l,x2_l,'o-.');
plt.title('efficient Pareto-front');
plt.grid(True);
