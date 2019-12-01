################################################################################################
################################## VARIABLE DEMAND MODEL #######################################
################################################################################################

    
from Results_MY import Plot_Energy_Total, Load_Results, Integer_Time_Series, Print_Results, Energy_Mix
from Model_Creation_MY import Model_Creation
from Model_Resolution_MY import Instance_Creation, Instance_Resolution
from Constraints_MY import Overall_Emissions_Obj
from pyomo.environ import *
from numpy import arange
import matplotlib.pyplot as plt
    
Optimization_Goal = 'Multiobjective'  

Renewable_Penetration = 0  # a number from 0 to 1.
Battery_Independency = 0   # number of days of battery independence

model = AbstractModel() # define type of optimization problem

Model_Creation(model, Renewable_Penetration, Battery_Independency) # Creation of the Sets, parameters and variables.
instance = Instance_Creation(model, Optimization_Goal, Renewable_Penetration, Battery_Independency) # Resolution of the instance

# ## minumum variable costs
instance.ObjectiveFunctionEm.deactivate()
results = Instance_Resolution(instance)
min_varcost = value(results.Total_Variable_Cost_Act)
print("first element of lexicographic matrix costructed. The optimum variable cost is" + str(min_varcost))

# ## minimum emissions
instance.ObjectiveFunctionCost.deactivate()
instance.ObjectiveFunctionEm.activate()

results = Instance_Resolution(instance) 
min_emissions = value(results.Emissions_Obj)
print("secobd element of lexicographic matrix costructed. The optimum emission level is " + str(min_emissions))

# ## maximum emissions
instance.Total_Variable_Cost_Act.fix(min_varcost)

results = Instance_Resolution(instance)
max_emissions = value(results.Emissions_Obj)
print("third element of lexicographic matrix costructed. The upper bound for emissions is " + str(max_emissions))

# ## maximum variable costs
instance.ObjectiveFunctionCost.activate()
instance.ObjectiveFunctionEm.deactivate()
instance.Total_Variable_Cost_Act.unfix()
instance.Emissions_Obj.fix(min_emissions)

results = Instance_Resolution(instance)
max_varcost = value(results.Total_Variable_Cost_Act)
print("fourth element of lexicographic matrix costructed. The upper bound for costs is " + str(max_varcost))

# ## set of Pareto efficient solution generation
n = 5
steps = arange(min_emissions,max_emissions,(max_emissions-min_emissions)/n)

instance.del_component(instance.ObjectiveFunctionCost)
instance.del_component(instance.ObjectiveFunctionEm)

instance.e = Param(initialize=0, mutable=True)
instance.delta = Param(initialize=0.001)
instance.s = Var(within=NonNegativeReals)
instance.Objnew = Objective (expr = instance.Total_Variable_Cost_Act + instance.delta * instance.s, sense=minimize)
instance.C_e = Constraint(expr = instance.Emissions_Obj - instance.s == instance.e)

instance.Total_Variable_Cost_Act.setub(max_varcost)
instance.Total_Variable_Cost_Act.setlb(min_varcost)

print("multi-optimiziation instance constructed. Starting iterations")

cost = []
emissions = []

for i in steps:
    instance.e = i
    results = Instance_Resolution(instance)
    cost.append(value(results.Total_Variable_Cost_Act))
    emissions.append(value(results.Emissions_Obj))
    print("iteration finished")

plt.plot(cost,emissions,'o-.')
plt.title('efficient Pareto-front')
plt.grid(True)
