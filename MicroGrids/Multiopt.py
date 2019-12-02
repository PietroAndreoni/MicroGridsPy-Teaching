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
    
Optimization_Goal = 'Multiobjective_NPC' # Multiobjective_NPC for emissions vs NPC, Multiobjective_Operation Cost for emissions vs OPEX 

Renewable_Penetration = 0  # a number from 0 to 1.
Battery_Independency = 0   # number of days of battery independence

model = AbstractModel() # define type of optimization problem

Model_Creation(model, Renewable_Penetration, Battery_Independency) # Creation of the Sets, parameters and variables.
instance = Instance_Creation(model, Optimization_Goal, Renewable_Penetration, Battery_Independency) # Resolution of the instance

# ## minumum variable costs
instance.ObjectiveFunctionEm.deactivate()
results = Instance_Resolution(instance)

if Optimization_Goal == 'Multiobjective_Operation Cost':
    min_cost = value(results.Total_Variable_Cost_Act)
elif Optimization_Goal == 'Multiobjective_NPC':
    min_cost = value(results.Net_Present_Cost)    
print("first element of lexicographic matrix costructed. The optimum variable cost is " + str(min_cost))

# ## minimum emissions
instance.ObjectiveFunctionCost.deactivate()
instance.ObjectiveFunctionEm.activate()

results = Instance_Resolution(instance) 
min_emissions = value(results.Emissions_Obj)
print("secobd element of lexicographic matrix costructed. The optimum emission level is " + str(min_emissions))

# ## maximum emissions
if Optimization_Goal == 'Multiobjective_Operation Cost':
    instance.Total_Variable_Cost_Act.fix(min_cost)
elif Optimization_Goal == 'Multiobjective_NPC':
    instance.Net_Present_Cost.fix(min_cost)

results = Instance_Resolution(instance)
max_emissions = value(results.Emissions_Obj)
print("third element of lexicographic matrix costructed. The upper bound for emissions is " + str(max_emissions))

# ## maximum variable costs
instance.ObjectiveFunctionCost.activate()
instance.ObjectiveFunctionEm.deactivate()
if Optimization_Goal == 'Multiobjective_Operation Cost':
    instance.Total_Variable_Cost_Act.unfix()
elif Optimization_Goal == 'Multiobjective_NPC':
    instance.Net_Present_Cost.unfix()
    
instance.Emissions_Obj.fix(min_emissions)

results = Instance_Resolution(instance)

if Optimization_Goal == 'Multiobjective_Operation Cost':
    max_cost = value(results.Total_Variable_Cost_Act)
elif Optimization_Goal == 'Multiobjective_NPC':
    max_cost = value(results.Net_Present_Cost)  
print("fourth element of lexicographic matrix costructed. The upper bound for costs is " + str(max_cost))

# ## set of Pareto efficient solution generation
n = 5
steps = arange(min_emissions+(max_emissions-min_emissions)/n,max_emissions,(max_emissions-min_emissions)/n)

'''
# method 2: follows paper, buggy. Need fixing
instance.del_component(instance.ObjectiveFunctionCost)
instance.del_component(instance.ObjectiveFunctionEm)
instance.Emissions_Obj.unfix()

instance.e = Param(initialize=0, mutable=True)
instance.delta = Param(initialize=0.00001)
instance.s = Var(within=NonNegativeReals)
instance.Objnew = Objective (expr = instance.Total_Variable_Cost_Act + instance.delta * instance.s, sense=minimize)
instance.C_e = Constraint(expr = instance.Emissions_Obj - instance.s == instance.e)
'''

if Optimization_Goal == 'Multiobjective_Operation Cost':
    instance.Total_Variable_Cost_Act.setub(max_cost)
    instance.Total_Variable_Cost_Act.setlb(min_cost)
elif Optimization_Goal == 'Multiobjective_NPC':
    instance.Net_Present_Cost.setub(max_cost)
    instance.Net_Present_Cost.setlb(min_cost)
print("multi-optimiziation instance constructed. Starting iterations")

cost = [max_cost]
emissions = [min_emissions]

for i in steps:
    instance.Emissions_Obj.fix(i)
#    instance.e = i          #uncomment and comment previous line if ure using method2
    results = Instance_Resolution(instance)    
    if Optimization_Goal == 'Multiobjective_Operation Cost':
        cost.append(value(results.Total_Variable_Cost_Act))
    elif Optimization_Goal == 'Multiobjective_NPC':
        cost.append(value(results.Net_Present_Cost))
    emissions.append(value(results.Emissions_Obj))
    print("iteration finished")

cost.append(min_cost)
emissions.append(max_emissions)
plt.plot(cost,emissions,'o-.')
plt.title('efficient Pareto-front')
plt.grid(True)
plt.savefig("Paretofront.jpg")