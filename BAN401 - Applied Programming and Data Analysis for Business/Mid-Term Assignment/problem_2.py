# Import Required packages
import numpy as np

# Insert given unemployment information into a dictionary
unemp = {'Australia': 5.92,
         'Brazil': 12.77,
         'China': 3.90,
         'Finland': 8.53,
         'Norway': 4.22,
         'South Africa': 27.45,
         'Iran': 11.81}

# Retrieve Norway's unemployment rate using a key
print(unemp['Norway'])

# Find out the position of the countries with the highest and lowest unemployment
highest_ue_pos = np.argmax(list(unemp.values()), axis = None)
lowest_ue_pos = np.argmin(list(unemp.values()), axis = None)

# Extract the countries with the highest and lowest unemployment
highest_country = list(unemp.keys())[highest_ue_pos]
lowest_country = list(unemp.keys())[lowest_ue_pos]

# Print the results of which country has highest/lowest unemployment
print(lowest_country,
      "has the lowest and",
      highest_country,
      "has the highest unemployment rate.")