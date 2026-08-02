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
from sqlalchemy import create_engine, text

import libs.gspread_utility as gspread
from libs.pandas_utility import clean_empty_rows

# 1. Define Database Connection URL
# Format: postgresql+psycopg2://username:password@host:port/database_name
DB_URL = "postgresql://eddancho:slurpuff@localhost:5432/dont_forget"

# Create the SQLAlchemy Engine
engine = create_engine(DB_URL)

def create_table(dataframe, 
                 engine,
                 table_name: str):
    dataframe.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",  
        index=False           # Do not save Pandas DataFrame index as a column
    )
    print(f"Made table with table name '{table_name}'")

if __name__ == "__main__":
    gc = gspread.get_gspread_client()
    sh = gspread.get_gspread_spreadsheet(gc, "1hqZzKbPofKQuEHkP6or3ggnlKNZy2ulqCH5eWSyA1_E")
    worksheet = sh.worksheet("USD")
    df_worksheet = pd.DataFrame(worksheet.get_all_records())
    df_worksheet = clean_empty_rows(df_worksheet)
    print(df_worksheet)

    create_table(df_worksheet,
                 engine,
                 "us_dollars")