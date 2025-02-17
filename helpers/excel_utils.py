import os
from openpyxl import Workbook

DATA_DIR = "data"
EXCEL_FILE = os.path.join(DATA_DIR, "trending_topics.xlsx")

def save_to_excel(topics):
    """
    Saves trending topics to an Excel file.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    wb = Workbook()
    ws = wb.active
    ws.title = "Trending Topics"
    ws.append(["Topic"])

    for topic in topics:
        ws.append([topic])

    wb.save(EXCEL_FILE)
