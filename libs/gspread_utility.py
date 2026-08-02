import sys
import os
import json
from typing import Optional, Any

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

import gspread
import pandas as pd
from gspread.client import Client
from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, date
from decimal import Decimal
from gspread.exceptions import APIError

BASE_FILE_PATH = "/tmp"

def get_gspread_client() -> Client:
    local_file_path = "praxis-acolyte-504305-u4-3f02001b458a.json"
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        local_file_path, scope
    )
    print("Credential: ", credentials)
    try:
        # OAuth 인증 수행
        gspread_client = gspread.authorize(credentials)
        print("OAuth 인증 성공: ", gspread_client)
    except Exception as e:
        # 인증 실패한 경우 예외 처리
        print(f"OAuth 인증 실패: {str(e)}")
    return gspread_client


def get_gspread_spreadsheet(
    gspread_client: Client,
    gspread_key: str,
) -> Optional[Spreadsheet]:
    # gc = get_gspread_client()
    # print("Client: ", gc)
    try:
        # 시트 오픈
        target_spreadsheet = gspread_client.open_by_key(key=gspread_key)
        print(f"API 호출 성공: {target_spreadsheet}")
    except APIError as e:
        # API 호출 실패한 경우 예외 처리
        print(f"API 호출 실패: {str(e)}")
        print(f"API 응답 정보: {e.response}")
    return target_spreadsheet


def get_gspread_worksheet(
    gspread_client: Client = get_gspread_client(),
    gspread_spreadsheet_key: str = None,
    gspread_worksheet_key: int = 0,
) -> Optional[Worksheet]:
    try:
        sh = gspread_client.open_by_key(key=gspread_spreadsheet_key)
        worksheet = sh.get_worksheet_by_id(gspread_worksheet_key)
        print(f"API 호출 성공: {worksheet}")
    except APIError as e:
        # API 호출 실패한 경우 예외 처리
        print(f"API 호출 실패: {str(e)}")
        print(f"API 응답 정보: {e.response}")
        return None
    return worksheet


def get_sheet_dimensions(query_results: list):
    row_num = len(query_results)
    col_num = len(query_results[0])
    return {"col": col_num, "row": row_num}


def create_gspread_worksheet(
    gspreadsheet: Spreadsheet, title: str, rows: int = 100, cols: int = 100
):
    worksheet = gspreadsheet.add_worksheet(title=title, rows=rows, cols=cols)
    return {
        "worksheet_id": get_gspread_worksheet_id(title, gspreadsheet),
        "worksheet_name": title,
    }


def get_gspread_worksheet_id(
    target_sheet_name: str,
    spread_sheet: Spreadsheet = None,
    gspread_key: str = None,
) -> Optional[int]:
    if spread_sheet is None:
        spread_sheet = get_gspread_spreadsheet(gspread_key=gspread_key)

    worksheet_list = spread_sheet.worksheets()
    for ws in worksheet_list:
        if target_sheet_name == ws.title:
            return ws.id
    return None


def get_gspread_worksheet_headers(
    worksheet: Worksheet = None, row_number: int = 1
) -> list:
    headers_list = worksheet.row_values(row_number)
    return headers_list


def get_cell_point(row_num, col_num):
    letters = []
    while col_num > 0:
        col_num, remainder = divmod(col_num - 1, 26)
        letters.append(chr(65 + remainder))
    letters.reverse()
    return f"{''.join(letters)}{row_num}"


def get_duplicated_gspread_worksheet_id(
    spread_sheet: Spreadsheet,
    reference_sheet_id: int,
    new_sheet_name: str,
    insert_sheet_index: int = 2,
    row_clear_start_index: int = 0,
) -> int:
    work_sheet = spread_sheet.duplicate_sheet(
        source_sheet_id=reference_sheet_id,
        new_sheet_name=new_sheet_name,
        insert_sheet_index=insert_sheet_index,
    )
    if row_clear_start_index > 0:
        last_cell_point = get_cell_point(row_clear_start_index, work_sheet.col_count)
        work_sheet.delete_rows(
            start_index=row_clear_start_index, end_index=work_sheet.row_count - 1
        )
        work_sheet.update(
            f"A{row_clear_start_index}:{last_cell_point}", [[""] * work_sheet.col_count]
        )
    else:
        pass  # 설정없음 Clear 작업 스킵
    print(f"Duplicate worksheet from {reference_sheet_id} to {work_sheet.id}")
    return work_sheet.id


def transform_dtypes_in_tuple(import_data: list) -> list:
    if not import_data:
        return []

    # 각 셀의 실제 값 타입으로 직접 변환한다.
    # (헤더행을 샘플로 컬럼 타입을 추론하면 헤더가 문자열이라 Decimal/bool 감지에 실패한다)
    export_data = list()
    for row in import_data:
        export_row = list()
        for value in row:
            if value is None:
                export_value = ""
            elif isinstance(value, bool):
                export_value = "TRUE" if value else "FALSE"
            elif isinstance(value, datetime):
                export_value = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, date):
                export_value = value.strftime("%Y-%m-%d")
            elif isinstance(value, Decimal):
                export_value = float(value)
            else:
                export_value = value
            export_row.append(export_value)
        export_data.append(export_row)
    return export_data


if __name__ == "__main__":
    gc = get_gspread_client()
    print(type(gc), gc)
    sh = get_gspread_spreadsheet(gc, "1hqZzKbPofKQuEHkP6or3ggnlKNZy2ulqCH5eWSyA1_E")
    worksheet = sh.worksheet("Sheet1")
    records = worksheet.get_all_records()
    # df = pd.DataFrame(records)
    # df = df[df['Name'].str.strip() != '']
    # print(df)
    with open("viewing_use.json", "w", encoding = "utf-8") as f:
        json.dump(records, f, indent = 2, ensure_ascii=False)