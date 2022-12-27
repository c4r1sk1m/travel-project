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
print(result)

