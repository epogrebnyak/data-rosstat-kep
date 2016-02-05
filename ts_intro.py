# we have two time series of power and oil production by month in Russia in 2014, TWh (млрд. кВтч) and mln t

""" Electricty production by month, TWh 
2014-01-31    102.0
2014-02-28     93.5
2014-03-31     94.3
2014-04-30     84.4
2014-05-31     79.6
2014-06-30     74.6
2014-07-31     77.5
2014-08-31     78.8
2014-09-30     80.1
2014-10-31     92.8
2014-11-30     96.0
2014-12-31    104.0
"""

z = """Oil production by month, mln t 
2014-01-31    42.6
2014-02-28    38.3
2014-03-31    42.3
2014-04-30    41.0
2014-05-31    42.5
2014-06-30    41.3
2014-07-31    42.3
2014-08-31    42.4
2014-09-30    41.4
2014-10-31    42.5
2014-11-30    41.4
2014-12-31    42.5
"""

import pandas as pd

# datapoints as vector
power_prod_vector = [102.0, 93.5, 94.3, 84.4, 79.6, 74.6, 77.5, 78.8, 80.1, 92.8, 96.0, 104.0]
oil_prod_vector = [42.6, 38.3, 42.3, 41.0, 42.5, 41.3, 42.3, 42.4, 41.4, 42.5, 41.4, 42.5]

assert len(power_prod_vector) == 12
assert len(oil_prod_vector) == 12

#creating Series objects
ts_power = pd.Series(power_prod_vector)
ts_oil   = pd.Series(oil_prod_vector)

# this data does not have time labels, which is essential for time sereis

# background: a single date in python  -----------------------------------------------------------
#
#             To be able to compare dates, work with date ranges and print in varios formats, etc
#             one must represent dates as a special type of variable, not just text like '2015-01-31' 
#
#             Standard date represntation in Python in datetime.date  
from datetime import date
d1 = date(1978, 4, 15) 
d2 = date(2014, 4, 15)
# check we can comapre dates
assert d2 > d1 
# print some output
# some date + .today() method will give today's date
print("Today is", date(1917, 11, 7).today().isoformat())

#             In pandas there is even a more convenient date type called Timestamp
#             Actually, it is a high precision date and time datastructure, but its can be 
#             used to  handle dates too.  

# Timestamp can be constructed from many inputs 
p1 = pd.Timestamp('1978-04-15')
p2 = pd.Timestamp(d2)
assert p2 > p1
print("Today is", p1.today().date().isoformat())
# end 'a single date in python'
# ---------------------------------------------------------------------------------------------------

# we can generate time index using pandas function date_range()
# in example below it will gerentate an array(index) of end of month dates in 
# for little dicsussion: why end-of-month is better as a time marker for monthly data?
time_index = pd.date_range('1/1/2014', periods=12, freq='M')

# recreating time series with time index
ts_power = pd.Series(power_prod_vector, time_index)
# alternatinely can assign index
ts_oil.index = time_index

#congratulations, ts_power and ts_oil are valid Timeseries variables now

# can plot a variable:
ts_power.plot()


# time series can be handled together as dataframe, which is a basic 
# data structure for dealing with several time series

prod_df = pd.DataFrame({'power' : ts_power,
           'oil'   : ts_oil})
print(prod_df)

prod_df.plot()

# todo: нарисовать отклонения от cреднегодового уровня обоих прееменны