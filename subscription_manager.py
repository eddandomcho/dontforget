import sys
import os
import json

from datetime import date 
from typing import Optional, Any

project_root = os.path.dirname(os.path.abspath(__file__))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import libs.gspread_utility as gspread
from libs.common_utility import convert_to_datetime_1

def get_upcoming_due_dates(records, time_frame_days: int):
    new_list = list()
    for record in records:
        if record.get("Days to Action") <= time_frame_days and record.get("Days to Action") >= 0 :
            new_list.append(
                {
                    "Name" : record.get("Name"),
                    "Amount" : record.get("Amount"),
                    "Days to Action" : record.get("Days to Action")
                }
            )
    return new_list


def main(gspread_client,
         spreadsheet_key):
    sh = gspread.get_gspread_spreadsheet(gspread_client, spreadsheet_key)
    worksheet = sh.worksheet("KRW")
    records = worksheet.get_all_records()
    records = gspread.filter_empty_rows(records)
    with open("viewing_use.json", "w", encoding = "utf-8") as f:
        json.dump(records, f, indent = 2, ensure_ascii=False)
    
    # today = date.today()
    # print(today)

    print(get_upcoming_due_dates(records, 19))

if __name__ == "__main__":
    gc = gspread.get_gspread_client()
    sh_key = "1hqZzKbPofKQuEHkP6or3ggnlKNZy2ulqCH5eWSyA1_E"
    main(gc, sh_key)