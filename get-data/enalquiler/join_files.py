# from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
import datetime as dt
import pandas as pd
import numpy as np
import os, re

# Load Data
PATH = os.getcwd()
DATA_PATH = "/data/enalquiler/"
filename = "enalquiler_01.csv"
full_path = PATH + DATA_PATH + filename

data = pd.read_csv(full_path)
length = len(data)

for i in range (2,89):
    if i < 10:
        filename = "enalquiler_0" + str(i) + ".csv"
    else:
        filename = "enalquiler_" + str(i) + ".csv"
    file = PATH + DATA_PATH + filename
    temp_data = pd.read_csv(file)
    length += len(temp_data)

    data = pd.concat([data,temp_data], axis=0)

data.reset_index(inplace=True, drop=True)

if length == data.shape[0]:
    print("Data has been correctly loaded")
    print("It has {} rows and {} columns".format(data.shape[0], data.shape[1]))
else:
    print("Some data might be missed when loading")

# Clean date
ref_day = "2020-04-15"
ref_day = dt.datetime.strptime(ref_day, "%Y-%m-%d")

# Change Date string from `Hace 5 años/meses` to `2015-01-01` or `2019-11-01`
# - Floor day of month if year is 2019
# - Floor year if year is older than 2019
data["Aproximate Date"] = np.nan

for i in range(0, len(data)):
    string = str(data.iloc[i,2])
    try:
        if re.match(".*meses.*", string):
            num = int(''.join(filter(str.isdigit, string)))
            date = ref_day - relativedelta(months=num)
            date = date.replace(day=1)
            data.at[i,"Aproximate Date"] = date
        elif re.match(".*año.*", string):
            num = int(''.join(filter(str.isdigit, string)))
            date = ref_day - relativedelta(years=num)
            date = date.replace(month=1, day=1)
            data.at[i,"Aproximate Date"] = date
        else:
            data.at[i,"Aproximate Date"] = None
    except:
        data.at[i,"Aproximate Date"] = None

data['Aproximate Date'] =  pd.to_datetime(data['Aproximate Date'], format='%Y%m%d').dt.to_period('M').dt.to_timestamp()

# Save data
data = data[['User Name', 'User Category', 'Aproximate Date', 'Question Body']]

data.to_csv(PATH+DATA_PATH+"enalquiler_all.csv", index=False)
