from pyomo import value
from pyomo.environ import AbstractModel
from numpy import arange

################################################################################################
################################## VARIABLE DEMAND MODEL #######################################
################################################################################################

    
from Results_MY import Plot_Energy_Total, Load_Results, Integer_Time_Series, Print_Results, Energy_Mix
from Model_Creation_MY import Model_Creation
from Model_Resolution_MY import Instance_Creation, Instance_Resolution
   
    
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

n = 5
steps = arange(min_emissions,max_emissions,n)

for i in steps:
    