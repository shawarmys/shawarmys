import argparse
import os
import json
import tempfile
import pandas as pd

from data_cleaner.file_name_matcher import FileNameMatcher
from CsvExcelReader import CsvExcelReader
from TableSchemaEncoder import TableSchemaEncoder
from HeaderValidator import HeaderValidator
from LLMMatchmaker import LLMMatchmaker
from pdf_handler.TextExtractor import TextExtractor
from pdf_handler.Mapper import Mapper
from pdf_handler.FreetextExtractor import FreetextExtractor
from SaveBert import download_and_save_bert
from server.misc.data_cleaner.data_cleaner import DataCleaner

def main(file_path):
  # Get the gold standard fingerprint for the file type
  matcher = FileNameMatcher()
  target_fingerprint_name = matcher.match_file_name(os.path.basename(file_path))

  # Find the corresponding gold fingerprint JSON file
  gold_fingerprint_path = os.path.join("server\misc\header_cleaner\goldFingerPrints", f"{target_fingerprint_name}_fingerprint.json")

  # Check file type
  if file_path.endswith('.pdf'):
    # Extract text from PDF
    text_extractor = TextExtractor()
    extracted_text = text_extractor.extract_text(file_path)

    free_text_extractor = FreetextExtractor()
    free_text_extractor.extract_free_text(extracted_text)

    # Map extracted text to structured format
    mapper = Mapper()
    incoming_df = mapper.map_text_to_dataframe(extracted_text, target_fingerprint_name)

    # Save the mapped dataframe as CSV for further processing with ; delimiter
    store_temp_file(incoming_df)

  else:
    # Load the gold fingerprint
    with open(gold_fingerprint_path, 'r') as f:
        gold_fingerprint = json.load(f)

    # Read incoming file and create fingerprint
    incoming_df = CsvExcelReader(file_path)
    encoder = TableSchemaEncoder()
    incoming_fingerprint = encoder.encode_target_table(os.path.basename(file_path), incoming_df)

    # Validate header and get errors
    header_validator = HeaderValidator(gold_fingerprint)
    matchmaking_required, message = header_validator.validate_header(incoming_fingerprint)

    # Match columns and reorder/rename incoming dataframe
    if matchmaking_required:
      # Check if BERT model is available, if not download and save it
      if not os.path.exists("server/misc/header_cleaner/bert_model"):
          download_and_save_bert("server/misc/header_cleaner/bert_model")

      matchmaker = LLMMatchmaker()
      matches = matchmaker.match_columns(gold_fingerprint, incoming_fingerprint)

      # Reorder/rename incoming dataframe based on matches
      reordered_df = matchmaker.reorder_and_rename(incoming_df, matches)

      return {"df": reordered_df, "errors": message}

    return {"df": incoming_df, "errors": message}

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
  df, errors = main(args.file_path)
