'''
Add PIPESIM PLC Parser into the pyfas library
'''

import os
import re
import numpy as np
import pandas as pd

class NetworkSimulationProfile:
    
    def __init__(self, directory):
        #Get PLC files and test to make sure there are PLC files in the directory
        self._directory = directory
        self._listdir = os.listdir(directory)
        self._plctest = any([file.endswith('.plc') for file in self._listdir])
        self._plcfiles = [file for file in self._listdir if file.endswith('.plc')]
        self.branchnames = [file[0:-4] for file in self._plcfiles]
        if not self._plctest:
            raise ValueError(f"There are no .plc files in {directory}")
        
        self.varnames = {}
        self.varcount = {}
        self.pointcount = {}
        for branch in self.branchnames:
            self.varnames[branch] = []
            self.varcount[branch] = 0
            self.pointcount[branch] = 0
        for i , file in enumerate(self._plcfiles):
            
            with open(os.path.join(directory, file), 'r') as fobj:
                
                for idx, line in enumerate(fobj):
                    
                    if '*CHEAD' in line:
                        fixedline = [j.strip() for j in line.split(',')]
                        varname = fixedline[1]
                        self.varnames[self.branchnames[i]].append(varname)
                        self.varcount[self.branchnames[i]] +=1
                    elif '*POINT ' in line:
                        self.pointcount[self.branchnames[i]] += 1
        
        self.linesperpoint = {}
        self.results1d = {}
        self.results2d = {}
        self.results= {}
        for branch in self.branchnames:
            self.linesperpoint[branch] = np.ceil(self.varcount[branch] / 10)
            self.results1d[branch] = []
            self.results2d[branch] = 0
            self.results[branch] = 0
        
    def extractResults(self):
        
        for i , file in enumerate(self._plcfiles):
            
            with open(os.path.join(self._directory,file), 'r') as fobj:
                
                for idx , line in enumerate(fobj):
                    
                    if '*POINT' in line:
                        fixedline = [j.strip() for j in line.split(',')] #Split string at the commas and eliminate whitespace
                        if fixedline[-1] == '&':
                            _ = fixedline.pop() #We don't want the & point
                        values = map(lambda string: float(re.findall(r"[-+]?\d*\.\d*E?[-+]?\d*" , string)[0]),fixedline) #convert to floats
                        for value in values:
                            self.results1d[self.branchnames[i]].append(value)
                            
                self.results1d[self.branchnames[i]] = np.array(self.results1d[self.branchnames[i]])
                
        #Restructure the 1D Data
        for branch in self.branchnames:
            
            self.results2d[branch] = self.results1d[branch].reshape((self.pointcount[branch] , self.varcount[branch]))
            self.results[branch] = pd.DataFrame(data=self.results2d[branch], columns=self.varnames[branch])
