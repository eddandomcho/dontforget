import sys
import os
import json
from datetime import date 
from typing import Optional, Any

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd

def clean_empty_rows(df):
    df = df.loc[df['ID'] != '']
    return df


def rename_headers(df):
    print("renaming headers")
    # lower case
    # remove special characters


def column_dt_to_date(df, 
                      column_name, 
                      date_format = "%Y/%m/%d"):
    print("changing column dt to date")