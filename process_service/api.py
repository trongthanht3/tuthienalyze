import re
from typing import Annotated
from fastapi import FastAPI, File, UploadFile
import fitz
import pandas as pd
import json

app = FastAPI()

def process_data(data):
    # Regex pattern to identify valid date (dd/mm/yyyy)
    date_pattern = re.compile(r'\d{2}/\d{2}/\d{4}')
    
    # Initialize empty list for cleaned rows
    cleaned_data = []
    current_row = {"Date": None, "ID": None, "Amount": None, "Content": ""}
    
    # Iterate through the data
    for row in data:
        if row[0] and date_pattern.match(row[0]):  # New date found
            if current_row["Date"]:  # Add current row before starting a new one
                cleaned_data.append(current_row.copy())
            current_row["Date"] = row[0]
            current_row["ID"] = None
            current_row["Amount"] = None
            current_row["Content"] = ""
        elif row[0] and not row[1]:  # ID found
            current_row["ID"] = row[0]
        if row[1]:  # Amount found
            current_row["Amount"] = row[1]
        if row[2]:  # Content found
            current_row["Content"] += row[2] + " "
    
    # Add the last row
    if current_row["Date"]:
        cleaned_data.append(current_row.copy())
    
    # Create DataFrame
    new_df = pd.DataFrame(cleaned_data)
    
    # Display the reformatted DataFrame
    return new_df

def process_balance(input_text):
    input_text = input_text.strip()
    input_text = input_text.split(' ')[0]
    input_text = input_text.replace('.', '')
    input_text = input_text.strip()
    return int(input_text)

# httpoption check for haproxy
@app.options("/")
async def options():
    return {"status": "ok"}

@app.post("/uploadfile/")
async def upload_file(file_input: UploadFile = File(...)):
    # f = open(file_input.file)
    doc = fitz.open(stream=file_input.file.read(), filetype='pdf') # open a document
    page = doc[0]
    clip_rect = [0, 0, 800, 750]

    df_raw = pd.DataFrame(columns=['Date', 'ID', 'Amount', 'Content'])

    tabs = page.find_tables(clip=clip_rect, strategy='text', min_words_vertical=4, min_words_horizontal=1)
    
    old_column_names = tabs[0].header.names
    
    tab = tabs[0]
    df = tab.to_pandas()
    try:
        df.columns = ['Col1', 'Col2', 'Col3']
        df.loc[-1] = old_column_names  # Add new row at index -1
        df.index = df.index + 1        # Shift index
        df = df.sort_index()           # Sort index to make the new row the first one
        new_df = process_data(df.values)
        df_raw = pd.concat([df_raw, new_df], ignore_index=True)
    except Exception as e:
        print(df)
        for i,tab in enumerate(tabs):  # iterate over all tables
            for cell in tab.header.cells:
                page.draw_rect(cell,color=fitz.pdfcolor["red"],width=0.3)
            page.draw_rect(tab.bbox,color=fitz.pdfcolor["green"])
            print(f"Table {i} column names: {tab.header.names}, external: {tab.header.external}")
            old_column_names = tab.header.names
            print(old_column_names)
    return json.loads(df_raw.to_json(orient='records'))
