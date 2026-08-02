from datetime import date, datetime

def convert_to_datetime_1(input_string: str):
    """
    "%Y/%m/%d" form
    """
    date_object = datetime.strptime(input_string, "%Y/%m/%d")
    return date_object