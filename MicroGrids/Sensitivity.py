sens_par_1 = [1,2,3]  # list of ordered values of parameter 1 you want to change
sens_par_2 = [1]      # list of orderer values of parameter 2 you want to change
line_i = 0            # line in which paramater 1 is written in data_MY.dat
line_j = 0            # line in which paramater 2 is written in data_MY.dat

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

        Modify_input(sens_par_1(i),line_i)
        Modify_input(sens_par_2(j),line_j)

        # Optimization model    
        Model_Creation(model, Renewable_Penetration, Battery_Independency) # Creation of the Sets, parameters and variables.
        instance = Model_Resolution(model, Optimization_Goal, Renewable_Penetration, Battery_Independency) # Resolution of the instance

        Data[i][j] = Load_Results(instance, Optimization_Goal)


def Modify_input(value,line):

    #write inputs into 