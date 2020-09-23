#!/usr/bin/env python
# coding: utf-8

# In[3]:


"""1. This project is designed to take in a CSV file of numeric data and output it with certain statistical summaries. The format matches the preferred style of the Clinical Addictions
Research Lab at UChicago. I created an object that takes in a dataframe and can split it by Active and Control groups, run the stats and put them in their proper place, and export the data.

2. I selected this project because it would be helpful for our lab. Takes much less time and can be more reliable than human error working on Excel. I also realized I was incompetent working with Pandas 
and dataframes in Python, so this was a good learning opportunity.

3. The use of Pandas and math were both important. Pandas provides a nice way to work with Dataframes, and math allowed for necessary statistical computations. 
I also took advantage of comprehensions, f strings, and object creation.

4. What I would have done differently is require user inputs when running the class CARLData. I relied on inputs from the user many times, which could be made more effecient by requiring inputs on the front end.
In addition, I would have given myself more time for customizability. For example, the object is restricted to binary splits (i.e. active and control). It would be cool to allow for many splits.

5. Upload the Affect CSV as a pd df. create an object using CARLData. Use the methods of the object to produce the stats. Use comments as a guide. 

6. The project was challenging, yes. I did not know what to expect, but manipulating rows and indexing was the biggest learning curve. Overall, it was a fun challenge.

7. I referred to the Pandas module documentation quite a bit. Other than that, I cited a few sources within the code comments.

8. I am not sure if this work qualifies for EC. perhaps some of the indexing techniques stand out."""



import pandas as pd
import numpy as np
import math


#Affect data consists of numeric data. These numbers correspond to participants' markings on a 100 millimeter scale for various types of moods at different time points. 
affect = pd.read_csv("Affect Data .csv", index_col = None)


# In[4]:


#affect.rename(columns = {"Grp" : "Group"}, inplace = True)
affect.head()


# In[6]:


class CARLData():
    def __init__(self, df):
        try:
            self.df = df
            self.Active = []
            self.Control = []
            self.ActiveStatsRun = False
            self.ControlStatsRun = False
        except Exception as e:
            print(f"Missing Dataframe: {e}.")
                 
    def splitbygroup(self, df):
        
        #This is a binary split of data for Active and Control expiremental data. 
        if "Grp" not in df.columns:
            for col in self.df.columns:
                print(col) 
            groupcolumn = str(input("What is the column name for group?"))
            df.rename(columns = {groupcolumn : "Grp"}, inplace = True)
        self.Active = df[df["Grp"] == 1]
        self.Control = df[df["Grp"] == 0]
        self.Active.reset_index(drop=True, inplace=True)
        self.Control.reset_index(drop=True, inplace=True)
 
        
    #Getters
    def GetActive(self):
        if len(self.Active) == 0:
            print("No data. Original Data has probably not been split by group yet.")
        else:
            print("Here is a peak at Active group.")
            return self.Active.tail()
            
    def GetControl(self):
        if len(self.Control) == 0:
            print("No data. Original Data has probably not been split by group yet.")
        else:
            print("Here is a peak at the Control group.")
            return self.Control.head()
            
    def GetOriginal(self):
            print("Here is a peak at the Original data.")
            return self.df.head()
            
    #Hear is where the meat is
    def RunActiveStats(self):
        
        #for easy referencing 
        for col in self.df.columns: 
            print(self.df.columns.get_loc(col), col)     
            
        #We want to ignore running stats for SubID, Group, and Sex (and perhaps other demographics) so this allow for that
        startcolumn = int(input("Which column do you want to start runnning stats for? Enter column #:"))
        stopyesno = str(input("Do you want to stop running stats at a certain column? Enter Y or N:"))
        
        #The default is to run the stats from startcolumn through the end
        stopcolumn = len(list(self.df.columns))
        
        #but in case we do want to stop at a certain column...
        if stopyesno == "Y":
            stopcolumn = int(input("Which column would you like to stop at? Enter column #:"))
            confirmation = str(input(f"Run stats from column {startcolumn} through {stopcolumn}? Enter Y or N:"))
        else:
            confirmation = str(input(f"Run stats from {startcolumn} until the end of the dataset? Enter Y or N:"))
        while confirmation == "N":
            break  
        
        #Making a new dataframe to work with
        #found this helpful: https://stackoverflow.com/questions/11285613/selecting-multiple-columns-in-a-pandas-dataframe
        ActiveStats = self.Active.iloc[:, startcolumn:stopcolumn]
        
        #The data we don't want to run stats for - let's save this so we can stitch this back in later
        SeveredFrontActive = self.Active.iloc[:, 0:startcolumn] 
        
        #In case we don't run stats all the way through, we'll keep the back end for later stitching too
        if stopyesno == "Y":
            SeveredBackActive = self.Active.iloc[:, stopcolumn:]
        
        #Here is where we begin running stats. My P.I. likes counts, means, SDs, and Standard Error at the bottom of each column
        Counts = ActiveStats.count(axis = 0)
        Means = ActiveStats.mean(axis = 0, skipna = True)
        SDs = ActiveStats.std(axis = 0, skipna = True)
        
        CountList = []
        MeanList = []
        SDList = []
        SEList = []
        
        for val in Counts:
            CountList.append(val) 
        for val in Means:
            MeanList.append(val)
        for val in SDs:
            SDList.append(val)
        
        
        countandstd = dict(zip(SDList, CountList))
        #for calculating SE below, i needed to loop through two lists. So instead I created this above dict out of two lists and looped through that 
        for std,count in countandstd.items():
            SEList.append((std/(math.sqrt(count))))
        
        #Most people work with columns. Appending rows was tricky. 
        #Found this helpful: https://stackoverflow.com/questions/29079408/python-create-a-data-frame-with-one-row-by-a-list
                                                                                            #PLEASE notice the list comprehension tucked in here ;)
        TempStatDf = pd.DataFrame(data = [CountList, MeanList, SDList, SEList], columns = list(col for col in ActiveStats.columns), index = ["Count", "Mean", "Standard Dev", "Standard Error"])
        ActiveStats = ActiveStats.append(TempStatDf, ignore_index = None)
        
        #Stitch back together with this slick for loop. 
        for col in SeveredFrontActive.columns:
                                #found this helpful: https://discuss.codecademy.com/t/can-we-add-a-new-column-at-a-specific-position-in-a-pandas-dataframe/355842
            ActiveStats.insert(SeveredFrontActive.columns.get_loc(col), col, SeveredFrontActive[col])
                                #index to identify where to insert, column name, column data
                
        #Stitch the back end on if needed
        if stopyesno == "Y":
            for col in SeveredBackActive.columns:
                                    #use len to index back end of df
                ActiveStats.insert(len(ActiveStats.columns), col, SeveredBackActive[col])
                
        self.Active = ActiveStats
        self.ActiveStatsRun = True
        return ActiveStats
    
    #Same code here except for Control group
    def RunControlStats(self):
        for col in self.df.columns: 
            print(self.df.columns.get_loc(col), col)     
            
        
        startcolumn = int(input("Which column do you want to start runnning stats for? Enter column #:"))
        
        stopyesno = str(input("Do you want to stop running stats at a certain column? Enter Y or N:"))
        stopcolumn = len(list(self.df.columns))
        if stopyesno == "Y":
            stopcolumn = int(input("Which column would you like to stop at? Enter column #:"))
            confirmation = str(input(f"Run stats from column {startcolumn} through {stopcolumn}? Enter Y or N:"))
        else:
            confirmation = str(input(f"Run stats from {startcolumn} until the end of the dataset? Enter Y or N:"))
        while confirmation == "N":
            break  
        
        ControlStats = self.Control.iloc[:, startcolumn:stopcolumn]
        SeveredFrontControl = self.Control.iloc[:, 0:startcolumn] 
        if stopyesno == "Y":
            SeveredBackControl = self.Control.iloc[:, stopcolumn:]
        
        Counts = ControlStats.count(axis = 0)
        Means = ControlStats.mean(axis = 0, skipna = True)
        SDs = ControlStats.std(axis = 0, skipna = True)
        
        CountList = []
        MeanList = []
        SDList = []
        SEList = []
        
        for val in Counts:
            CountList.append(val) 
        for val in Means:
            MeanList.append(val)
        for val in SDs:
            SDList.append(val)
        
        
        countandstd = dict(zip(SDList, CountList))
        for std,count in countandstd.items():
            SEList.append((std/(math.sqrt(count))))
        
        TempStatDf = pd.DataFrame(data = [CountList, MeanList, SDList, SEList], columns = list(col for col in ControlStats.columns), index = ["Count", "Mean", "Standard Dev", "Standard Error"])
        ControlStats = ControlStats.append(TempStatDf, ignore_index = None)
        
        for col in SeveredFrontControl.columns:
            ControlStats.insert(SeveredFrontControl.columns.get_loc(col), col, SeveredFrontControl[col])
    
        if stopyesno == "Y":
            for col in SeveredBackControl.columns:
                ControlStats.insert(len(ControlStats.columns), col, SeveredBackControl[col])
                
        self.Control = ControlStats
        self.ControlStatsRun = True
        return ControlStats
    
    
    def Round(self, digits):
        if self.ControlStatsRun == True and self.ActiveStatsRun == True:
            self.Active = self.Active.round(digits)
            self.Control = self.Control.round(digits)
            return self.Active.head(), self.Control.tail()
        else:    
            print("Stats have not been run for Active and Control.")
            
    def ExportActive(self, title):
        self.Active.to_csv(title + ".csv")
        
    def ExportControl(self, title):
        self.Control.to_csv(title + ".csv")
    
    
    def SumRowsActive(self):
        sums = self.Active.sum(axis=1)
        SumList = []
        for val in sums:
            SumList.append(val)
        TempSumDf = pd.DataFrame({"Sums": SumList})
        self.Active.insert(len(self.Active.columns), "Sums", TempSumDf["Sums"])
        return self.Active
    
    def SumRowsControl(self):
        sums = self.Control.sum(axis=1)
        SumList = []
        for val in sums:
            SumList.append(val)
        TempSumDf = pd.DataFrame({"Sums": SumList})
        self.Control.insert(len(self.Control.columns), "Sums", TempSumDf["Sums"])
        return self.Control
    
    def RunCatStatsControl(self):
        #This portion of the code is same as prior stats
        for col in self.df.columns: 
            print(self.df.columns.get_loc(col), col)
        startcolumn = int(input("Which column do you want to start runnning stats for? Enter column #:"))
        stopyesno = str(input("Do you want to stop running stats at a certain column? Enter Y or N:"))
        stopcolumn = len(list(self.df.columns))
        if stopyesno == "Y":
            stopcolumn = int(input("Which column would you like to stop at? Enter column #:"))
            confirmation = str(input(f"Run stats from column {startcolumn} through {stopcolumn}? Enter Y or N:"))
        else:
            confirmation = str(input(f"Run stats from {startcolumn} until the end of the dataset? Enter Y or N:"))
        while confirmation == "N":
            break  
        ControlStats = self.Control.iloc[:, startcolumn:stopcolumn]
        SeveredFrontControl = self.Control.iloc[:, 0:startcolumn] 
        if stopyesno == "Y":
            SeveredBackControl = self.Control.iloc[:, stopcolumn:]
            
        #Here are where modifications begin
        df1 = pd.DataFrame()
        list1 = []
        ticker = 0
        for col in ControlStats.columns:
            uniquenames = ControlStats[col].unique().tolist()
            valuecounts = ControlStats[col].value_counts().tolist()
            dictcollector = dict(zip(uniquenames, valuecounts))
            list1.append(dictcollector)
            #df1[col] = dictcollector
        
        list2 = []
        mainlist = []
        
        #convert list of dicts into list of string
        for item in list1:
            for key,val in item.items():
                list2.append(f"{key}" + " : " + f"{val}")
            mainlist.append(list2)
            list2 = []
        
        #create dataframe with string-based value counts 
        for col in ControlStats.columns:
            df1[col] = pd.Series(mainlist[ticker])
            ticker += 1
            
        
    
        ControlStats = ControlStats.append(df1, ignore_index = None)
        
        self.Control = ControlStats
        return ControlStats
        
    


# In[7]:


#work1.GetControl()
        
            
work1 = CARLData(affect)
work1.splitbygroup(affect) 


# In[ ]:


work1.RunStatsControl()


# In[ ]:


work1.RunActiveStats()


# In[ ]:


work1.Round(2)


# In[ ]:


work1.ExportActive("Active10")


# In[ ]:


work1.ExportControl("Control11")


# In[ ]:


work1.SumRows()


# In[ ]:



    

