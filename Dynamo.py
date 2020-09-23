#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from __future__ import print_function

from scipy.integrate import simps
from numpy import trapz
import pandas as pd
import numpy as np
import scipy as sp


preA = "/Users/nathandidier/Desktop/DynamoData/VIP19 SA Pre.csv"
postA = "/Users/nathandidier/Desktop/DynamoData/VIP19 SA Post.csv"
slpA = "/Users/nathandidier/Desktop/DynamoData/VIP19 SA SLP.csv"

preB = "/Users/nathandidier/Desktop/DynamoData/VIP19 SB Pre.csv"
postB = "/Users/nathandidier/Desktop/DynamoData/VIP19 SB Post.csv"
slpB = "/Users/nathandidier/Desktop/DynamoData/VIP19 SB SLP.csv"


class Dynamo6():
    
    """Creating an object that has a customizable # of data entries is the next step. This would involve the object to NOT require 6 files
    to be substantiated with the object, but entered into the object after substantiation. Various Try-Except commands will be important in the case 
    where a column of data is missing, for example. """
    

    def __init__(self, preA, postA, slpA, preB, postB, slpB):
        try:
            self.preA = pd.read_csv(preA, index_col = None)
            self.postA = pd.read_csv(postA, index_col = None)
            self.slpA = pd.read_csv(slpA, index_col = None)
            self.preB = pd.read_csv(preB, index_col = None)
            self.postB = pd.read_csv(postB, index_col = None)
            self.slpB = pd.read_csv(slpB, index_col = None)
            self.VIP = str(input("VIP#"))
            self.prepost = [self.preA, self.postA, self.slpA, self.preB, self.postB, self.slpB]
            
        except:
            print("File paths not entered properly. Should be entered in this order: preA, postA, slpA, preB, postB, slpB")
   
    def runprepost(self):
        
        listA = []
        listB = []
        ticker = 0
        for item in self.prepost:
            #water - except if ticker == 2 or ticker == 5. In those cases, this is SLPcig. 
            
            #should these next 5 lines be defined as a function 
            #alternative method here is create a definition and then do another for loop
            #this for loop would consist of "for col in col.columns and a defined function for getting trapoizadol area"
                
            xw = item[["Latest: Time (s)"]].to_numpy()
            xw = xw[~np.isnan(xw)]
            yw = item[["Latest: Force (N)"]].to_numpy()
            yw = yw[~np.isnan(yw)]
            areaw = np.trapz(yw, dx=0.1)
            
            
            #2 and 5 indicate where in the prepost list is SLP data (where this is only one column of data)
            if ticker != 2 and ticker != 5:    
                #food
                xf = item[["Run 1: Time (s)"]].to_numpy()
                xf = xf[~np.isnan(xf)]
                yf = item[["Run 1: Force (N)"]].to_numpy()
                yf = yf[~np.isnan(yf)]
            
                areaf = np.trapz(yw, dx=0.1)
            
                #cig
                xc = item[["Run 2: Time (s)"]].to_numpy()
                xc = xc[~np.isnan(xc)]
                yc = item[["Run 2: Force (N)"]].to_numpy()
                yc = yc[~np.isnan(yc)]
            
                areac = np.trapz(yc, dx=0.1)
           
            
            if ticker == 0 or ticker == 1:
                listA.append(areaw)
                listA.append(areaf)
                listA.append(areac)
            if ticker == 2:
                listA.append(areaf)
                
            if ticker == 3 or ticker == 4:
                listB.append(areaw)
                listB.append(areaf)
                listB.append(areac)
            if ticker == 5:
                listB.append(areaw)
            
            
            ticker += 1
    
        listA.insert(0, "A")
        listA.insert(0, self.VIP)
        #delta scores
        listA.append(listA[5] - listA[2])
        listA.append(listA[6] - listA[3])
        listA.append(listA[7] - listA[4])
        
        listB.insert(0, "B")
        listB.insert(0, self.VIP)
        #delta scores
        listB.append(listB[5] - listB[2])
        listB.append(listB[6] - listB[3])
        listB.append(listB[7] - listB[4])
        
        Dynamo = pd.DataFrame(data = [listA, listB], columns = ["VIP#", "Session", "AUCWaterPre", "AUCFoodPre", "AUCCigPre", "AUCWaterPost", "AUCFoodPost", "AUCCigPost", "AUCSLP", "AUCWaterDelta", "AUCFoodDelta", "AUCCigDelta"], index = None)
        #Dynamo.to_csv("DynamoCollector.csv", mode = "a")
        #Dynamo.to_csv("DynamoCollector.csv", mode = "a", header = False)
    
        
        return Dynamo
        
        
            


# run1 = Dynamo(preA, postA, slpA, preB, postB, slpB)
# 

# In[ ]:


run1 = Dynamo6(preA, postA, slpA, preB, postB, slpB)
run1.runprepost()


# In[18]:


#THIS IS A BETTER VERSION OF ABOVE AND MORE FLEXIBLE

from __future__ import print_function

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




