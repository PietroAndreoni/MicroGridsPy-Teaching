sens_par_i = [1,2,3]  # list of ordered values of parameter i you want to change
sens_par_j = [1]      

par_i = 0             # name of parameter i
par_j = 0             

line_i = 0            # line in which paramater i is written in data_MY.dat (for multiD parameters it refers to the declaration line "param:  ecc")
line_j = 0           

ind_i = 1             # index of the parameter i for multimensional parameter
ind_j = 1

dim_i = 1             # dimension for the parameter i for multidimensional parameters
dim_j = 1

Data = [ [ [] for j in range(len(sens_par_2)  ] for i in range(len(sens_par_1)  ]

for i in range(len(sens_par_1)):
    for j in range(len(sens_par_2)):

        from pyomo.environ import  AbstractModel

        ################################################################################################
        ################################## VARIABLE DEMAND MODEL #######################################
        ################################################################################################

            
        from Results_MY import Plot_Energy_Total, Load_Results, Integer_Time_Series, Print_Results, Energy_Mix
        from Model_Creation_MY import Model_Creation
        from Model_Resolution_MY import Model_Resolution

            
        Optimization_Goal = 'NPC'  # Options: NPC / Operation cost. 
                                # It allows to switch between a NPC-oriented optimization and a NON-ACTUALIZED Operation Cost-oriented optimization 

        Renewable_Penetration = 0  # a number from 0 to 1.
        Battery_Independency = 0   # number of days of battery independence

        model = AbstractModel() # define type of optimization problem

        Modify_input(par_i,sens_par_i[i],line_i,ind_i,dim_i)
        Modify_input(par_j,sens_par_j[j],line_j,ind_i,dim_i)

        # Optimization model    
        Model_Creation(model, Renewable_Penetration, Battery_Independency) # Creation of the Sets, parameters and variables.
        instance = Model_Resolution(model, Optimization_Goal, Renewable_Penetration, Battery_Independency) # Resolution of the instance

        Data[i][j] = Load_Results(instance, Optimization_Goal)


def Modify_input(variable,value,line,ind,dim):

    f = open('Inputs/data_MY.dat','r')
    lines = f.readlines()

    if dim==1
        lines[line-1] = "param: " + str(variable) + " := " + str(value) + ";"
    elif ind!=dim
        lines[line-1+dim] = str(ind) + "  " +  str(value)
    else
        lines[line-1+dim] = str(ind) + "  " +  str(value) + ";"

    f.close()

    f = open('Inputs/data_MY.dat','w')
    f.writelines(lines)
    f.close()
