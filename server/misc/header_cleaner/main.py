import argparse
import os
import json
import tempfile
import pandas as pd

from misc.header_cleaner.FileNameMatcher import FileNameMatcher
from misc.header_cleaner.CsvExcelReader import CsvExcelReader
from misc.header_cleaner.TableSchemaEncoder import TableSchemaEncoder
from misc.header_cleaner.HeaderValidator import HeaderValidator
from misc.header_cleaner.BertSemanticMatcher import BertSemanticMatcher
from misc.header_cleaner.pdf_handler.TextExtractor import TextExtractor
from misc.header_cleaner.pdf_handler.Mapper import Mapper
from misc.header_cleaner.SaveBert import download_and_save_bert

def main(file_path):
  # Get the gold standard fingerprint for the file type
  matcher = FileNameMatcher()
  target_fingerprint_name = matcher.match_file_name(os.path.basename(file_path))

  # Find the corresponding gold fingerprint JSON file
  _dir = os.path.dirname(os.path.abspath(__file__))
  gold_fingerprint_path = os.path.join(_dir, "goldFingerPrints", f"{target_fingerprint_name}_fingerprint.json")

  # Check file type
  if file_path.endswith('.pdf'):
    # Extract text from PDF
    extracted_text = TextExtractor(file_path)
    raw_text = extracted_text.extract_text()

    # Map extracted text to structured format
    mapper = Mapper()
    mapper.load_schema(os.path.join(_dir, "pdf_handler", "FileSchemas", "nursing_config.json"))

    incoming_df = mapper.map_values_to_dataframe(raw_text)

    store_temp_file({"df": incoming_df, "errors": "valid"})

  else:
    # Load the gold fingerprint
    with open(gold_fingerprint_path, 'r') as f:
        gold_fingerprint = json.load(f)

    # Read incoming file and create fingerprint
    reader = CsvExcelReader(file_path)
    incoming_df = reader.read_csv() if file_path.endswith('.csv') else reader.read_excel()

    encoder = TableSchemaEncoder()
    incoming_fingerprint = encoder.encode_target_table(os.path.basename(file_path), incoming_df)


    # Validate header and get errors
    header_validator = HeaderValidator(gold_fingerprint)
    matchmaking_required, message = header_validator.validate_header_row(incoming_fingerprint, )

    # Match columns and reorder/rename incoming dataframe
    if matchmaking_required:
      # 1. Handle BERT loading
      base_dir = os.path.dirname(os.path.abspath(__file__))
      model_dir = os.path.join(base_dir, "models", "bert_local")

      # if not os.path.exists(model_dir):
      download_and_save_bert()

      matchmaker = BertSemanticMatcher(model_dir=model_dir)

      # 2. Get matches (Ensure you pass the nested 'column_fingerprints')
      gold_cols = gold_fingerprint.get("column_fingerprints", gold_fingerprint)
      inc_cols = incoming_fingerprint.get("column_fingerprints", incoming_fingerprint)

      matches = matchmaker.match_columns(gold_cols, inc_cols)

      # 3. Transform data using MatchmakerLogic
      matchmaker_logic = MatchmakerLogic()

      # Convert list of matches into a simple {incoming: target} dictionary
      unziped_predictions = matchmaker_logic.unzip_predictions(matches)

      # Use the order defined in the gold standard (table_metadata)
      target_order = gold_fingerprint.get("table_metadata", {}).get("ordered_headers", list(gold_cols.keys()))

      reordered_df = matchmaker_logic.reorder_dataframe(incoming_df, unziped_predictions, target_order)

      store_temp_file({"df": reordered_df, "errors": message})
      return {"df": reordered_df, "errors": message}

    store_temp_file({"df": incoming_df, "errors": message})
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
     json.dump(errors, tmp_json, ensure_ascii=False, indent=2, default=str)
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
# python main.py --file_path "C:\Users\marti\Documents\shawarmys\server\misc\header_cleaner\csvFiles\split_data_pat_case_altered\clinic_1_labs.csv"
# python main.py --file_path "C:\Users\marti\Documents\shawarmys\server\misc\header_cleaner\pdf_handler\clinic_4_nursing.pdf"
