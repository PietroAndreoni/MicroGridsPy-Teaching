from Results_MY import Plot_Energy_Total, Load_Results, Integer_Time_Series, Print_Results, Energy_Mix, Modify_input
from Model_Creation_MY import Model_Creation
from Model_Resolution_MY import Model_Resolution
from pyomo.environ import  AbstractModel

#USER INPUTS
flag = 0               # set to 1 if you are performing sensitivity over two parameters, zero otherwise
res = 0                # set to 1 if you want to receive all the excel file from all run in results
sens_par_i = [1,2]     # list of ordered values of parameter i you want to change
sens_par_j = ['none']  # list of ordered values of parameter j you want to change (set to ['none'] if there's no second parameter)
   
par_i = "Value_Of_Lost_Load"             # name of parameter i
par_j = " "                              # name of parameter i
var_out = " "                            # name of output variable

# FOR MULTIDIMENSIONAL PARAMETERS
mdi = 0                 # set to 1 if parameter uno is multidimensional

   
Optimization_Goal = 'NPC'  # Options: NPC / Operation cost. 
                        # It allows to switch between a NPC-oriented optimization and a NON-ACTUALIZED Operation Cost-oriented optimization 

Renewable_Penetration = 0  # a number from 0 to 1.
Battery_Independency = 0   # number of days of battery independence

if res == 1
    Result = [[] for i in range(0,len(sens_par_i)) ]

model = AbstractModel() # define type of optimization problem        
Model_Creation(model, Renewable_Penetration, Battery_Independency) # Creation of the Sets, parameters and variables.        
instance = Instance_Creation(model, Optimization_Goal, Renewable_Penetration, Battery_Independency) # Resolution of the instance

opt = SolverFactory('gurobi') # Solver use during the optimization
opt.set_options('Method=2 Crossover=0 BarConvTol=1e-4 OptimalityTol=1e-4 FeasibilityTol=1e-4 IterationLimit=1000') # !! only works with GUROBI solver   
#    opt.set_options('Method=2 BarHomogeneous=1 Crossover=0 BarConvTol=1e-4 OptimalityTol=1e-4 FeasibilityTol=1e-4 IterationLimit=1000') # !! only works with GUROBI solver   
print('Model_Resolution: solver called')

instance.exec(par_i).mutable(True) 
instance.exec(par_j).mutable(True) 
output = []

k = 0
for i in sens_par_i:
    for j in sens_par_j:
        
        instance.exec(par_i) = i
        if flag==1
            instance.exec(par_j) = j 
        results = opt.solve(instance, tee=True) # Solving a model instance 
        print('Model_Resolution: instance solved')
        output.append(value(results.exec(var_out)))
        
        if res == 1:        
            instance.solutions.load_from(results)
            Result[k].append( Load_Results(instance, Optimization_Goal, par_i + "=val:" + str(i) "_" + par_j + "=val:" + str(j))) 
        
    k += 1