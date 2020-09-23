#!/usr/bin/env python
# coding: utf-8



# In[18]:


#THIS IS A BETTER VERSION OF ABOVE AND MORE FLEXIBLE

from scipy.integrate import simps
from numpy import trapz
import pandas as pd
import numpy as np
import scipy as sp
import glob
from itertools import islice

class DynamoFlex():

    def __init__(self):
        self.AllCSVs = []
            
    def AUC(self, ColPerSession):
        
       
        TempList = []
        
        pathlist = [file for file in sorted(glob.glob('/Users/nathandidier/Desktop/DynamoData/*.csv'))]
        for filepath in filelist:
            self.AllCSVs.append(pd.read_csv(filepath, index_col = None)) 
        
        ticker = 1
        for item in self.AllCSVs:
            if ("Post" in pathlist[ticker-1] or "Pre" in pathlist[ticker-1]) and len(item.columns) != 6:
                #dummy columns that ensure the correct amount of columns for the file
                if len(item.columns) == 2:
                    item.insert(0, "dummy1", [0])
                    item.insert(0, "dummy2", [0])
                    item.insert(0, "dummy3", [0])
                    item.insert(0, "dummy4", [0])
                if len(item.columns) == 4:
                    item.insert(0, "dummy1", [0])
                    item.insert(0, "dummy2", [0])
            if "SLP" in pathlist[ticker-1] and len(item.columns) != 2:
                print("SLP file invalid columns")
                break
                
            for col in item.columns[1::2]:
                y = item[[col]].to_numpy()
                y = y[~np.isnan(y)]
                AUC = np.trapz(y, dx = 0.1)
                TempList.append(AUC)
            ticker += 1
        
        DataList = [TempList[i * ColPerSession:(i + 1) * ColPerSession] for i in range((len(TempList) + ColPerSession - 1) // ColPerSession)] 
            
            
        ABlist = ["A", "B"] * int((len(self.AllCSVs)/6))
        
        
        Dynamo = pd.DataFrame(data = DataList, columns = ["AUCWaterPre", "AUCFoodPre", "AUCCigPre", "AUCWaterPost", "AUCFoodPost", "AUCCigPost", "AUCSLP"], index = None)
        Dynamo["AUCWaterDelta"] = Dynamo["AUCWaterPost"] - Dynamo["AUCWaterPre"]
        Dynamo["AUCFoodDelta"] = Dynamo["AUCFoodPost"] - Dynamo["AUCFoodPre"]
        Dynamo["AUCCigDelta"] = Dynamo["AUCCigPost"] - Dynamo["AUCCigPre"]
        
    
        return Dynamo
        
        
        
            


# In[19]:


work2 = DynamoFlex()


# In[20]:


work2.AUC(7)


# In[ ]:





# In[ ]:




