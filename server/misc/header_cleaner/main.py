import argparse
import os
import json
import tempfile
import pandas as pd

from FileNameMatcher import FileNameMatcher
from CsvExcelReader import CsvExcelReader
from TableSchemaEncoder import TableSchemaEncoder
from HeaderValidator import HeaderValidator
from BertSemanticMatcher import BertSemanticMatcher
from pdf_handler.TextExtractor import TextExtractor
from pdf_handler.Mapper import Mapper
from SaveBert import download_and_save_bert

def main(file_path):
  # Get the gold standard fingerprint for the file type
  matcher = FileNameMatcher()
  target_fingerprint_name = matcher.match_file_name(os.path.basename(file_path))

  # Find the corresponding gold fingerprint JSON file
  gold_fingerprint_path = os.path.join("server\misc\header_cleaner\goldFingerPrints", f"{target_fingerprint_name}_fingerprint.json")

  # Check file type
  if file_path.endswith('.pdf'):
    # Extract text from PDF
    extracted_text = TextExtractor(file_path)
    raw_text = extracted_text.extract_text()

    # Map extracted text to structured format
    mapper = Mapper()
    mapper.load_schema("pdf_handler/FileSchemas/nursing_config.json")

    incoming_df = mapper.map_values_to_dataframe(raw_text)

    store_temp_file({"df": incoming_df, "errors": "valid"})

  else:
    print("CSV/XLSX file detected. Validating header and performing matchmaking if needed...")
    # Load the gold fingerprint
    with open(gold_fingerprint_path, 'r') as f:
        gold_fingerprint = json.load(f)

    # Read incoming file and create fingerprint
    incoming_df = CsvExcelReader(file_path)
    encoder = TableSchemaEncoder()
    incoming_fingerprint = encoder.encode_target_table(os.path.basename(file_path), incoming_df)

    print("Gold fingerprint and incoming fingerprint created. Validating header...")

    # Validate header and get errors
    header_validator = HeaderValidator(gold_fingerprint)
    matchmaking_required, message = header_validator.validate_header(incoming_fingerprint)

    print("Header validation completed. Matchmaking required:", matchmaking_required, "Message:", message)

    # Match columns and reorder/rename incoming dataframe
    if matchmaking_required:
      # Check if BERT model is available, if not download and save it
      if not os.path.exists("server/misc/header_cleaner/bert_model"):
          download_and_save_bert("server/misc/header_cleaner/bert_model")

      matchmaker = BertSemanticMatcher()
      matches = matchmaker.match_columns(gold_fingerprint, incoming_fingerprint)

      # Reorder/rename incoming dataframe based on matches
      predictions = matchmaker.reorder_and_rename(incoming_df, matches)
      print("Matchmaking predictions obtained. Unzipping predictions and rearranging dataframe...")

      # Unzip predictions and rearrange columns of dataframe with column names as predicted
      unziped_predictions = matchmaker.unzip_predictions(predictions)
      matchmaker_logic = MatchmakerLogic()
      reordered_df = matchmaker_logic.reorder_dataframe(incoming_df, unziped_predictions, list(gold_fingerprint.keys()))

      print("Matchmaking completed. Columns have been reordered/renamed based on gold standard fingerprint.")
      return {"df": reordered_df, "errors": message}

    print("No matchmaking needed. Header is valid.")
    return {"df": incoming_df, "errors": message}

class MatchmakerLogic:
  def unzip_predictions(self, predictions):
      return {item['incoming']: item['target'] for item in predictions}

  def reorder_dataframe(self, incoming_df, mapping, target_order):
    # Create a reverse mapping for easy lookup: {target: incoming}
    reverse_mapping = {v: k for k, v in mapping.items()}

    # Only take target columns that actually exist in our mapping
    cols_to_extract = [reverse_mapping[t_col] for t_col in target_order if t_col in reverse_mapping]

    # Slice and Reorder: This creates a new DF with only matched cols in target order
    reordered_df = incoming_df[cols_to_extract].copy()

    # Rename columns to target names
    reordered_df.rename(columns=mapping, inplace=True)

    return reordered_df

def store_temp_file(out):
  df = out["df"]
  errors = out["errors"]
  if errors is not None:
    with tempfile.NamedTemporaryFile(
      mode="w",
      encoding="utf-8",
      suffix=".json",
      prefix="errors_",
      delete=False,
    ) as tmp_json:
     json.dump({errors}, tmp_json, ensure_ascii=False, indent=2, default=str)
    errors_path = tmp_json.name

    csv_path = None
    if df is not None:
      with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".csv",
        prefix="cleaned_",
        delete=False,
        newline=""
      ) as tmp_csv:
        df.to_csv(tmp_csv.name, index=False)
        csv_path = tmp_csv.name
    else:
      csv_path = args.file_path

    print(csv_path + ";" + errors_path)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    description="Clean and validate EPAC/Labs/Device CSV/XLSX files"
  )
  parser.add_argument(
        "--file_path",
        type=str,
        help="Path to CSV to clean"
    )

  args = parser.parse_args()

  main(args.file_path)
# Usage example
# python main.py --file_path "C:\Users\marti\Documents\shawarmys\server\misc\header_cleaner\csvFiles\split_data_pat_case_altered\clinic_1_labs.csv
# python main.py --file_path "C:\Users\marti\Documents\shawarmys\server\misc\header_cleaner\pdf_handler\clinic_4_nursing.pdf"
