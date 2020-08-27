# Import required packages
import numpy as np

# Create the function
def roe_func(net_income, beg_equity, end_equity):
    # Compute the Average Shareholder's Equity for the year
    avg_equity = (beg_equity+end_equity)/2

    # Compute the Return on Equity according to the given equation
    roe = net_income/avg_equity

    # Return ROE rounded off to 2 decimal places
    return round(roe, 2)

# Print ROE of Apple in the console
apple_ROE = (roe_func(59500000000, 134000000000, 107100000000))
print('ROE of Apple for 2018 is ' + str(apple_ROE))