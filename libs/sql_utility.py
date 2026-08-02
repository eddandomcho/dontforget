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

# 1. Define Database Connection URL
# Format: postgresql+psycopg2://username:password@host:port/database_name
DB_URL = "postgresql://eddancho:slurpuff@localhost:5432/dont_forget"

# Create the SQLAlchemy Engine
engine = create_engine(DB_URL)

def run_sql_query(query, engine):
    df = pd.read_sql_query(query, con = engine)
    return df

if __name__ == "__main__":
    sql_query = """
    select sum("Amount (₩)")
    from korean_won
    """
    df = run_sql_query(sql_query, engine)
    print(df)