#USER INPUTS
sens_par_i = [1,2]   # list of ordered values of parameter i you want to change
sens_par_j = ['none']  # list of ordered values of parameter i you want to change (set to ['none'] if there's no second parameter)
   
par_i = "Value_Of_Lost_Load"             # name of parameter i
par_j = " "                              # name of parameter i

line_i = 29            # line in which paramater i is written in data_MY.dat (for multiD parameters it refers to the declaration line "param:  ecc")
line_j = 0           

ind_i = 1             # index of the parameter i for multimensional parameter (needs to be <= than corresponding dim)
ind_j = 1

dim_i = 1             # dimension for the parameter i for multidimensional parameters (set to 1 for 1D parameters)
dim_j = 1

#MODEL RESOLUTION
Result = [[] for i in range(0,len(sens_par_i)) ]

from Results_MY import Plot_Energy_Total, Load_Results, Integer_Time_Series, Print_Results, Energy_Mix, Modify_input
from Model_Creation_MY import Model_Creation
from Model_Resolution_MY import Model_Resolution
from pyomo.environ import  AbstractModel
   
Optimization_Goal = 'NPC'  # Options: NPC / Operation cost. 
                        # It allows to switch between a NPC-oriented optimization and a NON-ACTUALIZED Operation Cost-oriented optimization 

Renewable_Penetration = 0  # a number from 0 to 1.
Battery_Independency = 0   # number of days of battery independence

for i in range(len(sens_par_i)):
    for j in range(len(sens_par_j)):

        Modify_input(par_i,sens_par_i[i],line_i,ind_i,dim_i)
        if sens_par_j[0] != 'none':
            Modify_input(par_j,sens_par_j[j],line_j,ind_i,dim_i)
            
        # Optimization model   

        model = AbstractModel() # define type of optimization problem        
        Model_Creation(model, Renewable_Penetration, Battery_Independency) # Creation of the Sets, parameters and variables.        
        instance = Model_Resolution(model, Optimization_Goal, Renewable_Penetration, Battery_Independency) # Resolution of the instance

        Result[i].append( Load_Results(instance, Optimization_Goal, par_i + "=val:" + str(sens_par_i[i])) "_" + par_j + "=val:" + str(sens_par_j[j])) 
        
        '''
        some sintax: for 1D variables you access by instance.variable_name.value
        for multiD variables instance.variable_name.get_values()
        '''

