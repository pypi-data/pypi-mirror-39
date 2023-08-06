import sqlite3 as sq
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import itertools



class HBdataMonitor():
    '''
    Python class to extract data from a SQLite HB database
    requirements
    Python      = 3.6
    numpy       = 1.15.0
    pandas      = 0.23.4
    matplotlib  = 2.2.2
    sqlite      = 3.24.0
    '''
    
    def __init__(self):
        ## default inputVar is zero to check wheter get_DB_info has runned
        self.inputVar = 0
        ## colors
        self.colors = []
        ## linestyle
        self.linestyle = plt.Line2D.filled_markers

    
#    def read_sql_list(self, path, sql_command):
#        # connect withe the myTable database 
#        connection = sq.connect(path) 
#          
#        # cursor object 
#        crsr = connection.cursor() 
#          
#        # execute the command to fetch all the data from the table emp 
#        crsr.execute(sql_command)  
#          
#        # store all the fetched data in the ans variable 
#        data= crsr.fetchall()  
#        return data    

    def read_sql_table(self, path, command):
        '''
        Execute a SQL command and returns the output as DataFrame
        :param str path: path of the databse
        :param str command: SQL command
        :return: DataFrame table: table with the results
        '''

        db = sq.connect(path)
        table = pd.read_sql_query(command, db)
        return table
    

    def read_variables(self,path, columnId, inputvar=True):
        '''
        Returns the sorted unique values for a given variable.
        :param str path: path of the databse
        :param int columnId: ColumnID of the variabele
        :param logical inputvar: switch between input or output variable (True =  inputvariables)
        :return: array var: array with the unique sorted variables
        '''

        if inputvar==True:
            string = 'Input'
        else:
            string = 'Result'
        ## command
        command1 = 'SELECT Value '
        command2 = 'FROM HydroDynamic{}Data '.format(string)
        command3 = 'INNER JOIN HydroDynamicData '
        command4 = 'ON HydroDynamicData.HydroDynamicDataId = HydroDynamic{}Data.HydroDynamicDataId '.format(string)
        command5 = 'WHERE HRD{}columnId={} '.format(string, columnId)
        ## total command
        total_command = command1 + command2 + command3 + command4 + command5
        ## execute command
        values = self.read_sql_table(path , total_command)
        ## unique and sort
        var = np.sort(np.unique(values))
        return var

    def get_variables(self, path):
        '''
        Get the values of the variables
        :param str path: path of the databse
        '''
        ## Read input/output variables
        inputVar = self.read_sql_table(path, 'SELECT * FROM HRDInputVariables')
        resultVar = self.read_sql_table(path, 'SELECT * FROM HRDResultVariables')

        ## link columnname with columndID
        self.inputVar = {}
        for i, item in enumerate(inputVar.ColumnName):
            self.inputVar[item] = inputVar.HRDInputColumnId[i]
        self.resultVar = {}
        for i, item in enumerate(resultVar.ColumnName):
            self.resultVar[item] = resultVar.HRDResultColumnId[i]

        ## input Variabele
        self.inputValues = {}
        for i, item in enumerate(inputVar.ColumnName):
            self.inputValues[item] = self.read_variables(path, inputVar.HRDInputColumnId[i], inputvar=True)
        ## winddirection
        self.inputValues['WindDir'] = np.squeeze(
            self.read_sql_table(path, 'SELECT Direction FROM HRDWindDirections').values)
        ## location
        self.inputValues['loc'] = np.squeeze(self.read_sql_table(path, 'SELECT Name FROM HRDLocations').values)
        ## Closing situations
        self.inputValues['ClosingSituation'] = np.squeeze(
            self.read_sql_table(path, 'SELECT ClosingSituationId FROM closingSituations').values, axis=1)


    def get_DB_info(self,path, fname='Variables.txt'):
        '''
        Read the info from table general.
        :param str path: path of the databse
        :param str fname: name of the asci file
        '''

        ## show general information
        command = "SELECT * FROM General"
        table = self.read_sql_table(path ,command)
        for i, item in enumerate(table.columns):
            print('{}: {}'.format(item, table.iloc[0,i]))
        ## get the variables
        self.get_variables(path)

        ## show input variables
        print('Number of input Variables={}'.format(len(self.inputValues)))
        for i, item in enumerate(self.inputValues.keys()):
            print(item)

        ## show ouput variables
        print('Number of result Variables={}'.format(len(self.resultVar)))
        for i, item in enumerate(self.resultVar):
            print(item)

        ## write variables to file
        with open(fname, 'w') as f:
            f.write('InputVariables\n')
            ## loop through variables
            for row, item in enumerate(self.inputValues.keys()):
                f.write('{};'.format(item))
                ## loop through values
                string = ''
                for col, item in enumerate(self.inputValues[item]):
                    string = string + '{};'.format(item)
                f.write(string + '\n')         


    def HBinput(self,Y,inputX,fname='result.txt'):
        '''
        input function to execute sql command
        1. create a dictionary which can be used to extract the data
        2. extract the data for every combinations
        3. write data to file
        :param str Y: result variabele
        :param dict inputX: dictionary with the variabele and value in a list {'WINDS':[0],'MEERP':[1,2]}
        :param fname: name of asci file
        '''

        ## when get_get_DB_info is not used
        if self.inputVar ==0:
            ## only first databse is selected!
            self.get_variables(inputX['DB'][0])

        ## 1 Determine constant and varying variables
        var_keys = {} 
        con_keys = {}
        for item in inputX.keys():
            ## use all input variables
            if inputX[item] == ['all']:
                inputX[item] = self.inputValues[item]
            if len(inputX[item])>1:
                var_keys[item] = len(inputX[item])
            else:
               con_keys[item] = inputX[item]
        
        ## 2. checks
        for item in self.inputValues.keys():
            ## check if all variables are given
            assert item in inputX.keys(), 'Error: variable {} is missing'.format(item)
            ## check if values exist
            if not all(x in self.inputValues[item] for x in inputX[item]):
                print('Warning: Not all values are present in the database')
        
        ## 3. create new dict with empty lists
        input_data = {}
        for item in inputX.keys():
            input_data[item] = []
        
        ## 4. get all combinations of the variables
        var = list(var_keys.keys()) 
        comb_input = []
        for item in var:
            comb_input.append(inputX[item])
        combinations = list(itertools.product(*comb_input))
        N = len(combinations)
        
        ## 5. fill dict with all combinations
        for i in range(N):
            for item in inputX.keys():
                ## variables which vary
                if item in var_keys.keys():
                    for k,_ in enumerate(var):
                        if item==var[k]:
                            tmp = input_data[item] 
                            tmp.append(combinations[i][k])
                            input_data[item] = tmp
                ## variable which are constant
                else:
                   tmp = input_data[item] 
                   tmp.append(inputX[item][0])
                   input_data[item] = tmp

        ## 6. Write data and execute SQL command
        f = open(fname,'w')
        f.write('constants \n')
        for item in con_keys.keys():
            f.write('{}={}\n'.format(item,con_keys[item][0]))
        f.write('varied \n')
        f.write('{};'.format(Y))
        for item in var:
            f.write('{};'.format(item))
        f.write('\n')
        for i in range(N):
            ##create temporary variable dict of the inputVariables
            tmp = {}
            for item in inputX.keys():
                ## WindDir, loc, DB and closingsituation are not inputVariables
                if item!='WindDir' and item!='loc' and item!='ClosingSituation' and item!='DB':
                    tmp[item] = input_data[item][i]
            y = self.create_sql_command(input_data['DB'][i], Y, input_data['loc'][i], input_data['WindDir'][i], input_data['ClosingSituation'][i], tmp, fig=False)
            if y.empty:
                y.set_value(0, -999)

            if i%10==0:
                print('progress: {} %'.format(np.round(float(i)/N * 100),2))
            ## write data
            for j in range(len(y)):
                f.write('{};'.format(y.iloc[j]))
                for item in var:
                    f.write('{};'.format(input_data[item][i]))
                f.write('\n')
        f.close()


            
                    

    def create_plot(self,Y=0, X=1, Z1=0, Z2=0, fname='result.txt', path='result'):
        '''
        Create a plot from the data points
        :param str Y: variabele on y-axis
        :param str X: variabele on x-axis
        :param str Z1: variabele with different symbols
        :param str Z2: variabele with different colors
        :param str fname: name of asci file
        :param str path: location where the figure is saved
        '''

        ## get data information
        f = open(fname,'r')
        meta = f.readlines()
        f.close()
        constant = ''
        for i,line in enumerate(meta):
            if line[0:6] == 'varied':
                n = i
                break
            if i>0:
                constant = constant + line
        ## get data
        data = pd.read_csv(fname,sep=';',skiprows=n+1,na_values=-999)

        ## checks
        assert len(data.columns)<=5, 'Error: too many columns to plot'
        if len(data.columns)==5:
            assert Z2!=0 and Z1!=0, 'Error: Z1 and Z2 must be specified'
        if len(data.columns)==4:
            assert Z1!=0 and Z2==0, 'Error: Only Z1 can be specified'
        if len(data.columns)==3:
            assert Z1==0 and Z2==0, 'Error: No Z can be specified'


        ## set column indexes
        if X==1:
            Xind = 1
        else:
            Xind = np.where(data.columns == X)[0][0]
        if Y==0:
            Yind =0
        else:
            Yind = np.where(data.columns==Y)[0][0]

        if Z1 !=0:
            Z1ind = np.where(data.columns==Z1)[0][0]
            z1 = np.unique(data.iloc[:, Z1ind])
        else:
            Z1ind = []
            z1 = np.zeros(1)
        if Z2 !=0:
            Z2ind = np.where(data.columns==Z2)[0][0]
            z2 = np.unique(data.iloc[:, Z2ind])
        else:
            Z2ind = []
            z2 = np.zeros(1)

        ## if self.color is empy, use default colormap
        if not self.colors:
            self.colors = cm.rainbow(np.linspace(0, 1, len(z1)))
        assert len(z2)<=15, 'Error: More values in Z2 than symbols'
        ## plot
        fig = plt.figure(figsize=[10,10])
        ax = plt.subplot(1,1,1)
        for i in range(len(z1)):
            for j in range(len(z2)):
                if Z1!=0 and Z2!=0:
                    ind = np.where(np.logical_and(data.iloc[:,Z1ind]==z1[i], data.iloc[:,Z2ind]==z2[j]))[0]
                elif Z1!=0 and Z2==0:
                    ind = np.where(data.iloc[:, Z1ind] == z1[i])[0]
                elif Z1==0 and Z2==0:
                    ind = np.where(data.iloc[:, 0] == data.iloc[:, 0])[0]
                ax.plot(data.iloc[ind,Xind],data.iloc[ind,Yind],linewidth=2,marker=self.linestyle[j],color=self.colors[i])

        ## create labels for legend
        if Z1 != 0:
            lines = ax.get_lines()
            labels_z1 = []
            ind_z1 = []
            for i,item in enumerate(z1):
                labels_z1.append('{}={}'.format(data.columns[Z1ind],item))
                ind_z1.append(i * len(z2))
            legend1 = plt.legend([lines[i] for i in ind_z1], labels_z1, loc=1,
                                 shadow=True, fancybox=True, edgecolor='inherit', framealpha=0.8)
            ax.add_artist(legend1)
        if Z2 !=0:
            labels_z2 = []
            ind_z2 = []
            for i,item in enumerate(z2):
                labels_z2.append('{}={}'.format(data.columns[Z2ind],item))
                ind_z2.append(i)
            legend2 = plt.legend([lines[i] for i in ind_z2], labels_z2, loc=4,
                             shadow=True, fancybox=True, edgecolor='inherit', framealpha=0.8)
            ax.add_artist(legend2)

        ## set x lim. check if x is a string (e.g. loc)
        if type(min(data.iloc[ind,Xind]))==str:
            ax.set_xlim([0, (len(data.iloc[ind, Xind]) -1)*1.5 ])
            plt.xticks(rotation=30)
            bottom = 0.2
        else:
            ax.set_xlim([min(data.iloc[ind, Xind]), max(data.iloc[ind, Xind]) * 1.5])
            bottom = 0.1

        ## figure style
        ax.grid('on',linestyle=':')
        plt.tick_params(labelsize=15)
        plt.subplots_adjust(top=0.8,bottom=bottom)
        plt.xlabel(data.columns[Xind],fontsize=20)
        plt.ylabel(data.columns[Yind],fontsize=20)
        plt.title(constant, fontsize=18)
        ax.grid('on',linestyle=':')
        plt.tick_params(labelsize=15)
        plt.savefig(path +'.png', dpi=500)

        fig.set_size_inches(11.69, 8.27)
        plt.savefig(path + '.pdf', papertype='a4')
        
    
#    def DBinput_old(self,X,Y,loc):
#        ## 1 check location
#        loc = loc
#        
#        xlist = []
#        ylist = []
#        labels = []
#        while True:
#            ## 2 input waardes
#            Xinput = {}
#            for item in self.inputValues.keys():
#                if item !=X:
#                    tmp = float(input('Input {}='.format(item)))
#                    while tmp not in self.inputValues[item]:
#                        tmp = float(input('Bestaat niet! Input {}='.format(item))) 
#                    Xinput[item] = tmp
#            print(Xinput)
#            ## 3 wind
#            windDir = float(input('WindDir ='))
#            
#    
#            x,y = self.create_sql_command(X,Y,loc,windDir,Xinput,fig=False)
#            
#            
#            tmp = input('Volgende reeks (y/n)=')
#            ## label
#            string = 'WindDir={}'.format(windDir)
#            for item in Xinput.keys():
#                string = string + '| {}={}'.format(item,Xinput[item])
#            
#            if tmp=='y':
#                xlist.append(x)
#                ylist.append(y)
#                labels.append(string)
#            else:
#                xlist.append(x)
#                ylist.append(y)
#
#                labels.append(string)
#                break
#
#        
#        plt.figure()
#        for i, item in enumerate(xlist):
#            plt.plot(xlist[i],ylist[i],label=labels[i])
#        plt.title(loc)
#        plt.legend()
#        plt.xlabel(X)
#        plt.ylabel(Y)
#        ##
#        plt.grid('on')
        
        
            

    def create_sql_command(self, path,Y, loc, windDir,closing, Xinput, fig=False):
        '''
        Make SQL command to extract data
        :param str path: location of databse
        :param str Y: result variabele
        :param str loc: location
        :param float windDir: wind direction
        :param int closing: closingcreterium
        :param dict Xinput: dictionary with values for all input variabele
        :param logical fig: switch beteen plotting results (only for testing)
        :return: Pandas.Series with the result variabele given the input variabele
        '''

        
        ## 1. Location
        command = "SELECT HRDLocationId FROM HRDLocations WHERE NAME='{}'".format(loc)
        HRDLocationId = self.read_sql_table(path ,command).values
        HRDLocationId = HRDLocationId[0,0]
        
        ## 2. wind direction
        windDir = str(windDir)
        command = "SELECT HRDWindDirectionId FROM HRDWindDirections WHERE Direction='{}'".format(windDir)
        HRDWindDirectionId = self.read_sql_table(path ,command).values
        HRDWindDirectionId = HRDWindDirectionId[0,0]
        
        ## 3. Closing
        ClosingsituationId = closing
        
        ## 4. Input Variable
        #command = "SELECT HRDInputColumnId FROM HRDInputVariables WHERE ColumnName='{}'".format(X)
        #HRDInputColumnId = self.read_sql_table(path ,command).values
        #HRDInputColumnId = HRDInputColumnId[0,0]
        
        ## 5. Result variable
        command = "SELECT HRDResultColumnId FROM HRDResultVariables WHERE ColumnName='{}'".format(Y)
        HRDResultColumnId = self.read_sql_table(path ,command).values
        HRDResultColumnId = HRDResultColumnId[0,0]
        
        ## get columnId from ColumnName
        Xvalue = {}
        for item in Xinput.keys():
            ColumnId = self.inputVar[item]
            Xvalue[ColumnId] = Xinput[item]
        N = len(Xvalue.keys())
        
        ## SQL command       
        ## Select columns to return
        command1 = 'SELECT HydroDynamicResultData.Value '
        command2 = 'FROM HydroDynamicResultData '
        ## Join hydrodynamic data
        command3 = 'INNER JOIN HydroDynamicData '
        command4 = 'ON HydroDynamicData.HydroDynamicDataID=HydroDynamicResultData.HydroDynamicDataID '
        
        command_total = command1 + command2 + command3 + command4
        
        ## join inputData
        for i in range(N):
            command5 = 'INNER JOIN HydroDynamicInputData I{} '.format(i)
            command6 = 'ON I{}.HydroDynamicDataID=HydroDynamicData.HydroDynamicDataID '.format(i)
            command_total = command_total + command5 + command6
        
        ##  select result variable
        command7 = 'WHERE HydroDynamicResultData.HRDResultColumnId={} '.format(HRDResultColumnId)
        command8 = 'AND '
        command9 = 'HydroDynamicData.HRDLocationID={} AND  HydroDynamicData.ClosingSituationID={} AND HydroDynamicData.HRDWindDirectionID={} '.format(HRDLocationId,ClosingsituationId,HRDWindDirectionId)
        ## Input variable

        command_total = command_total + command7 + command8 + command9
        ## set contrains
        for i,item in enumerate(Xvalue.keys()):
            command11 = 'AND I{}.HRDInputColumnID={} '.format(i,item)
            command12 = 'AND '
            command13 = 'I{}.Value={} '.format(i,Xvalue[item])
            command_total = command_total + command11 + command12 + command13 #+ 'AND '

        value = self.read_sql_table(path ,command_total) 

        ## plot for testing
        if fig==True:
            plt.figure()
            plt.plot(value.iloc[:,1],value.iloc[:,0],'.')
            plt.xlabel(X)
            plt.ylabel(Y)
            plt.title('{} and windDir={}'.format(loc,windDir))
        return value.iloc[:,0]

