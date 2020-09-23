# Data-Analysis-Univ-Chicago
Data Formatting and Summarization
For Numeric Data:
    Count, Mean, Standard Deviation and Standard Error on the bottom of each column
        I have already created a version of code that accomplishes this
    Optional: create a column of Sums of data across rows
           This would be applicable for surveys that are scored with Totals
    Optional: highlight data that is 2 SDs away from the mean
          We may want to add flexibility here, like coloring and other parameters for which cells should be highlighted
For categorical data:
    Counts of each unique response on the bottom of each column
    Here is an example for Education:
        Some High School: 14
        High School/GED: 25
        Some College: 43
        Completed College: 72
        Etc.
    I have already created a version of code that accomplishes this
    
For all data:
    Bolded column names (i.e. variables)
    Footer of Date, File Name, and initials of creator
    Downloadable as Excel file
    A variable key
    A variable key is usually on its own sheet within a workbook. It includes information about each variable and what they mean for easy reference. We would         probably want to create a "library" of variable names and definitions for the variables that are applicable to research in CARL (Clinical Addictions Research Lab). We could also store information here about the Query that was used to produce the workbook
    
Data Table Visualization
    Demographic / Sample Characteristic Table
        This is a table that usually has two or more columns
          E.g. Experimental group(s), control group, and total sample
          E.g. Current Smokers vs. Former Smokers 
        The rows consist of variables (e.gs. Race, Education, Cigarettes smoked/day)
        For numeric data, the cells contain Mean and Standard Deviation
          e.g. 14.2 (1.13)
        For categorical variables, the cells contain Count and percentage of group
          e.g. 76 (52%)
        These tables include a Title on top and a Note on the bottom
        There are also a column that consists of P values; this involves a T-Test between groups 
        I will share an example table of what this looks like
        Oftentimes, these table are made step by step on Excel
        I have created demographic tables on R rather easily; would working with R be compatible with this project? I assume not
        More types of tables may be desirable eventually. 
  Graphical Visualization
  Bar Graphs
  Scatterplots
  Box and Whisker
  Line Graphs
