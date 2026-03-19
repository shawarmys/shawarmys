import pandas as pd

from misc.data_cleaner.CsvExcelReader import CsvExcelReader


def get_file_extension(file_path: str) -> str:
    filename = file_path.split('/')[-1]  # Get the last part of the path
    if '.' in filename:
        return filename.split('.')[-1].lower()  # Return the extension in lowercase
    else:
        return ''  # No extension found

def clean_csv(file_path: str):
    # Implement CSV cleaning logic here
    print(f"Cleaning CSV file: {file_path}")
    # Read the CSV file, perform cleaning operations, and save the cleaned data
    df: pd.DataFrame = CsvExcelReader(file_path).read_csv()

def clean_data(file_path: str):
    # Step 1: Identify the file type
    file_extension = get_file_extension(file_path)

    # Step 2: Clean the data based on
    if file_extension == 'csv':
        clean_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")
