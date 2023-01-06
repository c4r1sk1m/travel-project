'''/****************************************************************************************************************************************************************
  Author:
  Kaya Celebi

  Written by Kaya Celebi, March 2022
****************************************************************************************************************************************************************/'''

from typing import overload
import numpy as np
import pandas as pd
from tqdm import tqdm 
import json
import os
from scraping import *

result = scrape_data('JFK', 'IST', '2023-05-20', '2023-06-10')
#print(result)
#print(pd.DataFrame.from_dict(result))

# Check type of columns in dataframe
print([(c, type(pd.DataFrame.from_dict(result)[c][0])) for c in pd.DataFrame.from_dict(result).columns])
res_df = pd.to_datetime(pd.DataFrame.from_dict(result))

## Cleaning dataframe columns

# Convert date columns to datetime type
res_df['Leave Date'] = pd.to_datetime(res_df['Leave Date'])
res_df['Return Date'] = pd.to_datetime(res_df['Return Date'])

# Convert 'Travel Time' column to int
res_df['Travel Time_hour_to_min'] = res_df['Travel Time'].apply(lambda x: int(str(x).split('hr')[0].strip())*60 )
res_df['Travel Time_min'] = res_df['Travel Time'].apply(lambda x: int(str(x).split('min')[0].split('hr')[1].strip()) if 'min' in str(x) else 0 )
res_df['Travel Time Converted'] = res_df['Travel Time_hour_to_min'] + res_df['Travel Time_min']

