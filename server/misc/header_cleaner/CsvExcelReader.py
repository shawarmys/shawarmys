import pandas as pd
import csv
import os

class CsvExcelReader:
  def __init__(self, file_path):
    self.file_path = file_path

  def read_csv(self):
    try:
      df = pd.read_csv(self.file_path, delimiter=self.check_delimiter(self.file_path), engine='python', encoding='utf-8', on_bad_lines='warn')
      return df
    except Exception as e:
      raise ValueError(f"Error reading CSV file: {e}")

  def read_excel(self):
    try:
      df = pd.read_excel(self.file_path, engine=None)
      return df
    except Exception as e:
      raise ValueError(f"Error reading Excel file: {e}")

  def check_delimiter(self, file_path):
    with open(file_path, 'r') as f:
      try:
        dialect = csv.Sniffer().sniff(f.read(2048))
        delimiter = dialect.delimiter
      except:
        delimiter = ','
    return delimiter
