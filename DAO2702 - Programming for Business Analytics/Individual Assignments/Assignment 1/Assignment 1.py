
# coding: utf-8

# # DAO2702 - Individual Assignment 1 (Zhou Kai Jing - A0171366A)

# # Question 1
# Q1. Understanding demand is always a key issue in business operations. The Hospital.csv 
# contains Singaporeans’ arrivals at the major public hospitals’ emergency departments 
# (EDs) in 2011. To make a staffing plan, which decides the number of nurses and 
# doctors to serve patients, the intra- and inter-day variations in patient arrivals are 
# important descriptive statistics. Please answer the following questions:
# 
# (a) What is the patient arrival pattern within a day? Please draw a proper chart 
# to present your findings. To answer this question, you should divide each day 
# into 24 time intervals (each interval is an hour) and then find out the average 
# number of patient arrivals in an interval. Moreover, you should assume there is 
# no inter-day variability to find the average in part (a). 
# 
# Specifically, you should first create a 31 by 24 table to store the counting 
# results. The first row of the table will be patient arrivals on Oct 01, 2011, in 
# different time periods, say 12 midnight to 1am, 1am to 2am and so on. Then, 
# collapse your rows to have 24 averages and each average represents the average 
# hourly patient arrivals in that time period and visualize your findings.

# Answer for 1(a): We begin by importing all the python packages that are necessary for this assignment. After that, we need to set the seaborn package and obtain the current working directory to ensure that we are working in the same folder that contains our csv data file. We then read the "Hospital.csv" file in Pandas and create new columns to extract the day of the month and hour of the data type through slicing of the corresponding REGIS_DATE and REGIS_TIME columns. We also convert the extracted day/hour columns into integers for boolean comparison when summarizing the data later on.

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns
sns.set()
import os
os.getcwd()

df = pd.read_csv("Hospital.csv")
df['reg_day'] = df.REGIS_DATE.str[0:2].astype(int)
df['reg_hour'] = df.REGIS_TIME.str[0:2].astype(int)


# Next, we are required to create a 31 by 24 table to represent a summary of the patient arrival data across the month and by 1-hour intervals. This was done by the creation of a 2D array (called x), followed by using 2 for loops to obtain the day and hourly indexes respectively, after which we can obtain the intersecting indexes by intersecting the 2 arrays to obtain the patient arrival count for each (day, hour) period and fill it into the 31 by 24 array. The array can then be printed to check the values of the each cell in the table.

# In[2]:


x = np.zeros((31,24), dtype = int)

for i in range(1,df.reg_day.max()+1):
    day_bool = (df.reg_day == i)
    day_ind = np.arange(len(df.reg_day), dtype = int)
    day_ind = day_ind[day_bool]
    for j in range(df.reg_hour.max()+1):
        hour_bool = (df.reg_hour == j)
        hour_ind = np.arange(len(df.reg_hour), dtype = int)
        hour_ind = hour_ind[hour_bool]
        comb_ind = np.intersect1d(day_ind, hour_ind)
        sample_df = df.iloc[comb_ind,:]
        cases_hourly = len(sample_df.reg_hour)
        x[i-1,j] = cases_hourly

hosp_summary = pd.DataFrame(data = x, index = np.arange(1, 32), columns = np.arange(0, 24))
hosp_summary.index.name = "Day"
hosp_summary.columns.name = "Hour:"
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(hosp_summary)


# Finally, we create an array from the summary table for the average patient arrivals per hourly period, and plot the resulting data in a line plot to visualize the trend of average patient arrivals across all 24 1-hour periods for the month of October:

# In[3]:


avg_hourly = np.mean(x, axis = 0)

plt.bar(np.arange(24), avg_hourly)
plt.xlabel("Hour")
plt.ylabel("Number of patients arriving in Hour x")
plt.xticks(np.arange(24))
plt.title("Average number of patients arriving per hourly interval in October")
plt.tight_layout()
plt.show()


# (b) Is there any inter-day variation in patient arrivals? Please draw a proper chart 
# to present your findings. However, now you should assume there is inter-day 
# variability in a week (That is, different days in a week can have different 
# arrival patterns of patients) and find out the inter-day-specific average number 
# of patient arrivals. Then, visualize the arrival patterns of patients by different 
# days in a week (from Monday to Sunday).

# Answer for 1(b): Since we are comparing the inter-day variability for patient arrivals, we can first use the datetime module to find out that 1st October 2011 falls on a Saturday.

# In[4]:


import datetime
dt = '1/10/2011'
day, month, year = (int(i) for i in dt.split('/'))    
ans = datetime.date(year, month, day)
print("1st October 2011 falls on a " + ans.strftime("%A"))


# After determining that the first day of the data set is a Saturday (1st October), we use a for-loop to find the "day of the week" summary for the 24 1-hour intervals of patient arrivals across October. For each day of the week, we then plot the graph using different colours, and by using to same y-limits and overlaying the different day's line plots in a single graph, we can get better visual comparability of patient arrival trends across different days of the week.

# In[5]:


weekdays = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
plt_color = ["blue", "cyan", "green", "yellow", "red", "orange", "black"]

for i in range(7):
    day_trend = np.mean(x[i::7], axis = 0, dtype = float)
    plt.plot(np.arange(len(day_trend)), day_trend, color = plt_color[i])

plt.ylim(10, 135)
plt.xlabel("Hour")
plt.ylabel("Number of patients arriving on Hour x")
plt.xticks(range(len(day_trend)))
plt.title ("Average number of patients arriving across different days of the week")
plt.tight_layout()
plt.legend(weekdays)
plt.show()


# From the graph above, we can make the observation that generally across October, the patient arrivals on Mondays are the highest compared to all other days of the week. In addition, the patient arrivals on Sundays are also slightly higher than other days of the week except for Mondays.

# # Question 2

# Q2. The data source is from Taiwan’s Taxation Bureau, which consists of 5 local branches all over Taiwan. In the tables below, we can have a basic understanding of the monthly salary distribution of full-time Taiwanese employees in 2015. Although the total population in Taiwan is estimated over 23.5 million people in 2015, only 5.11 million people’s salary information can be accurately ascertained after considering multiple demographic criteria and checking the accuracy of income records. All of the following statistics in the tables are calculated by Ministry of Finance, Taiwan, using the income data from Taxation Bureau.
# 
# ![table1.PNG](attachment:table1.PNG)
# ![table2.PNG](attachment:table2.PNG)
# 
# From the above tables, you can assume the population data of salaries of full-time Taiwanese employees are available for us to carry out more detailed analytics.
# 
# (a) Although the average monthly salary can be an indicator of central tendency to represent the typical earnings of a Taiwanese, it may not be a good indicator 
# sometimes, due to the impact of extreme income levels in the population. Thus, 
# we also want to know a Taiwanese’s median monthly salary to get a full picture 
# of the salary distribution. However, this piece of information is lacking. Please find out the possible estimate of the median monthly salary by using 
# Python simulation. That is, please use simulation to generate a random sample of size 200 using the population information provided in the above tables. Moreover, we make an explicit distributional assumption on the age-specific salary subpopulations. For example, we assume that for those Taiwanese under 20 years of age, their monthly salary population will be a normal distribution with mean 17,487 and variance 7,4592. Similarly, the salary population of Taiwanese with age between 21 and 30 follows another normal distribution with mean 32,481 and variance 18,2072. All other age-specific salary subpopulations can be defined accordingly. Please use Python to obtain a random sample of size 200 and estimate the sample median monthly salary.
# 
# Note: In your sample, the age-group composition of the sample must be the same (or very close to) the age-group composition of the population. For example, the 21-30 age group constitutes 22.86% (1,170,176/5,118,136) of the population. Hence, in your sample, 46 persons should come from 21-30 age group.

# Answer for 2(a): We begin by importing all the necessary packages, setting seaborn and inputting the given population and sub-population information into the array format in Python. We can display the table to check that all the input information are correct.

# In[6]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns
sns.set()

pop_param = np.array([[105770,1170176,1797410,1256255,692903,88260,7362],[17487,32481,47044,56863,59514,76572,114779],[7459,18207,37225,65919,103232,137916,360839]])
sal_summary = pd.DataFrame(data = pop_param, index = ["No. of people", "Mean salary", "S.d."], columns = ["<=20", "21-30", "31-40", "41-50", "51-60", "61-65", ">=66"])
sal_summary.columns.name = "Age:"
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(sal_summary)


# From the population information given, we can then calculate the proportion information from the array containing the number of people in each age sub-category of the population. Using the given proportions, we can find the required number of people in each subcategory for the sample size by multiplying 200 and rounding. Here, we define a sample check function [sam_check(x, y)] for 3 purposes. Firstly, to prevent non-representation of any age groups, a while-loop in included to increase the sub-category count of any non-represented age groups by 1. Furthermore, to ensure that the sample size is exactly at 200, we can use 2 more while-loops to increase the number of the least represented age group if the total sample size is under 200 or reduce the number of the most represented age group if the total sample size is over 200. We can then print to check that the total sample size is 200 and that all age groups are represented in the sample proportion.

# In[7]:


pop_prop = pop_param[0,:]/(np.sum(pop_param[0,:]))

sam_prop = np.round(pop_prop*200,0).astype(int)

def sam_check(propn, sam_size):
    while np.min(propn) == 0:
        propn[np.argmin(propn)] += 1 
    while np.sum(propn) < sam_size:
        propn[np.argmin(propn)] += 1
    while np.sum(propn) > sam_size:
        propn[np.argmax(propn)] -= 1

sam_check(sam_prop, 200)   
print(np.sum(sam_prop),"\n",sam_prop)


# After obtaining the sample proportion, we can begin our simulation using a for-loop. Through a for-loop, we can generate simulated salary following the mean salary and standard deviation of each age group from given data source from Taiwan's Taxation Bureau. Within each for loop, another while loop is included to check that all simulated salary are not negative (since it is not realistic to have a negative salary). After ensuring all simulated salary data are positive, we can then concatenate them into the population sample array (named simulate_x) which will contain the simulated salary for all 200 sample salaries. The simulated sample is then sorted and printed to ensure that all salaries are non-negative. Finally, we can find the median of simulate_x using the np.median function.

# In[8]:


simulate_x = np.array([0])
for i in range(len(sam_prop)):
    N = sam_prop[i]
    pop_mean = pop_param[1,i]
    pop_sd = pop_param[2,i]
    simul_xpos = np.random.normal(pop_mean,pop_sd,N)
    for j in range(len(simul_xpos)):
        while simul_xpos[j] < 0:
            simul_xpos[j] = np.random.normal(pop_mean,pop_sd,1)
    simulate_x = np.concatenate((simulate_x, simul_xpos))
simulate_x = np.delete(simulate_x,0).astype(int)
simulate_x = np.sort(simulate_x)
# print(simulate_x)

median_x = np.median(simulate_x)
print("Median salary of sample size " + str(len(simulate_x)) + " from the simulated population is: " + str(median_x))


# (b) Please perform repeated random sampling of size 200 from Taiwanese population and figure out the sampling distribution of sample median monthly salary. (The sampling distribution must be constructed with 5000 repeated sampling outcomes and you need to visualize the sampling distribution simulated as your answers).

# Answer for 2(b): To repeat the sampling 5000 times to obtain 5000 sample medians, we can use another for-loop to generate 5000 sampling medians and store them in an array (named store_median).

# In[9]:


repeat = 5000
store_median = np.empty(repeat, dtype = float)

for i in range(repeat):
    simulate_rep = np.array([0])
    for j in range(len(sam_prop)):
        N = sam_prop[j]
        pop_mean = pop_param[1,j]
        pop_sd = pop_param[2,j]
        simul_pos = np.random.normal(pop_mean,pop_sd,N)
        for k in range(len(simul_pos)):
            while simul_pos[k] < 0:
                simul_pos[k] = np.random.normal(pop_mean,pop_sd,1)
        simulate_rep = np.concatenate((simulate_rep, simul_pos))
    simulate_rep = np.delete(simulate_rep,0).astype(int)
    simulate_rep = np.sort(simulate_rep)
    med_rep = np.median(simulate_rep)
    store_median[i] = med_rep


# (c) Please repeat your repeated sampling in (b), but now you need to increase the sample size from 200 to 500 and 1000. Comment on the shape of the sampling distribution of the median monthly salary. When the sample size increases, is the sampling distribution of the median monthly salary approaching a normal distribution? (Please draw a panel of histograms to present your visualization).

# Answer for 2(c): Using a similar method as above, we can also simulate 5000 sample medians from sample sizes of 500, and store it in a separate array (named store_med_y).

# In[10]:


sam_prop_y = np.round(pop_prop*500,0).astype(int)

sam_check(sam_prop_y, 500)
print(np.sum(sam_prop_y),"\n",sam_prop_y)

store_med_y = np.empty(repeat, dtype = float)

for i in range(repeat):
    simulate_y = np.array([0])
    for j in range(len(sam_prop_y)):
        N = sam_prop_y[j]
        pop_mean = pop_param[1,j]
        pop_sd = pop_param[2,j]
        simul_ypos = np.random.normal(pop_mean,pop_sd,N)
        for k in range(len(simul_ypos)):
            while simul_ypos[k] < 0:
                simul_ypos[k] = np.random.normal(pop_mean,pop_sd,1)
        simulate_y = np.concatenate((simulate_y, simul_ypos))
    simulate_y = np.delete(simulate_y,0).astype(int)
    simulate_y = np.sort(simulate_y)
    median_y = np.median(simulate_y)
    store_med_y[i] = median_y


# Similarly, for the last simulation with sample sizes 1000, we can run the same simulation as the above and change the sample size to 1000 accordingly. Then, we store it in a third array (named store_med_z). Finally, we plot the 3 different distribution curves, using the 3 generated arrays containing each set of simulation data, together in a 3-by-1 subplot to compare the differences in the shapes of the 3 curves.

# In[11]:


sam_prop_z = np.round(pop_prop*1000,0).astype(int)

sam_check(sam_prop_z, 1000)
print(np.sum(sam_prop_z),"\n",sam_prop_z)

store_med_z = np.empty(repeat, dtype = float)

for i in range(repeat):
    simulate_z = np.array([0])
    for j in range(len(sam_prop_z)):
        N = sam_prop_z[j]
        pop_mean = pop_param[1,j]
        pop_sd = pop_param[2,j]
        simul_zpos = np.random.normal(pop_mean,pop_sd,N)
        for k in range(len(simul_zpos)):
            while simul_zpos[k] < 0:
                simul_zpos[k] = np.random.normal(pop_mean,pop_sd,1)
        simulate_z = np.concatenate((simulate_z, simul_zpos))
    simulate_z = np.delete(simulate_z,0).astype(int)
    simulate_z = np.sort(simulate_z)
    median_z = np.median(simulate_z)
    store_med_z[i] = median_z

sample_sizes = [200,500,1000]
sam_plots = [store_median, store_med_y, store_med_z]

plt.figure(figsize=(6,6))
for i in range(len(sample_sizes)):
    plt.subplot(len(sample_sizes),1,i+1)
    sns.distplot(sam_plots[i], color = 'blue', label = "Size " + str(sample_sizes[i]))
    plt.xlim(42500,60000)
    plt.ylim(0,0.00030)
    plt.xlabel("Median monthly salary of samples")
    plt.title("Distribution of sample median monthly salary")
    plt.legend()

plt.tight_layout()
plt.show()


# From the panel of histograms above, we can see that as the sample size increases, there is less spread and hence, lower variance for the sample median distribution graphs from 200, to 500 and 1000. As the size increases, we can also observe the trend that the sample median distribution curve experiences a higher peak around the mean values and less spread, giving a taller normal distribution curve. Hence, we can say that as the sample size increases, the sample distribution of the median monthly salary tend towards a normal distribution.
