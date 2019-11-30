from pyomo.environ import AbstractModel, value
from numpy import arange

################################################################################################
################################## VARIABLE DEMAND MODEL #######################################
################################################################################################

    
from Results_MY import Plot_Energy_Total, Load_Results, Integer_Time_Series, Print_Results, Energy_Mix
from Model_Creation_MY import Model_Creation
from Model_Resolution_MY import Instance_Creation, Instance_Resolution
from Constraints_MY import Overall_Emissions_Obj
    
Optimization_Goal = 'Multiobjective'  

Renewable_Penetration = 0  # a number from 0 to 1.
Battery_Independency = 0   # number of days of battery independence

model = AbstractModel() # define type of optimization problem

Model_Creation(model, Renewable_Penetration, Battery_Independency) # Creation of the Sets, parameters and variables.
instance = Instance_Creation(model, Optimization_Goal, Renewable_Penetration, Battery_Independency) # Resolution of the instance

# ## minumum variable costs
instance.ObjectiveFunctionEm.deactivate()
results = Instance_Resolution(instance)
min_varcost = value(results.Cost_Obj)

# ## minimum emissions
instance.ObjectiveFunctionCost.deactivate()
instance.ObjectiveFunctionEm.activate()

results = Instance_Resolution(instance) 
min_emissions = value(results.Emissions_Obj)

# ## maximum emissions
instance.Cost_Obj.fix(min_varcost)

results = Instance_Resolution(instance)
max_emissions = value(results.Emission_Obj)


# ## maximum variable costs
instance.ObjectiveFunctionCost.activate()
instance.ObjectiveFunctionEm.deactivate()
instance.Cost_Obj.unfix()
instance.Emissions_Obj.fix(min_emissions)

results = Instance_Resolution(instance)
max_varcost = value(results.Cost_Obj)

# ## set of Pareto efficient solution generation
n = 5
steps = arange(min_emissions,max_emissions,n)

instance.del_component(instance.OBjectiveFunctionCost)
instance.del_component(instance.ObjectiveFunctionEm)

instance.e = Param(initialize=0, mutable=True)
instance.delta = Param(initialize=0.00001)
instance.s = Var(within=NonNegativeReals)
instance.Obj = Var(within=NonNegativeReals)
instance.Em_costr = Constraint(rule=Overall_Emissions_Obj)

instance.Objnew = Objective (expr = model.Obj == model.Cost_Obj + model.delta * model.s, sense=minimize)
instance.C_e = Constraint(expr = model.Emission_Obj - model.s == model.e)

cost = []
emissions = []

for i in steps:
    instance.e = i
    solver.solve(instance)
    cost.append(value(instance.Cost_Obj))
    emissions.append(value(instance.Emission_Obj))

plt.plot(cost,emissions,'o-.')
plt.title('efficient Pareto-front')
plt.grid(True)
