import pandas as pd
import TargetSchemaEncoder
import os
import csv

if __name__ == "__main__":
    # Create FIngerprints for all csv and excel files in the 'errorousFiles' directory
    target_encoder = TargetSchemaEncoder.TargetSchemaEncoder(save_fingerprint=True, save_directory='errorFingerPrints')
    gold_standard_dir = os.path.join(os.path.dirname(__file__), 'csvFiles/errorousFiles')
    for filename in os.listdir(gold_standard_dir):
        if filename.endswith(('.csv', '.xlsx')):
            table_name = os.path.splitext(filename)[0]
            file_path = os.path.join(gold_standard_dir, filename)

            with open(file_path, 'r') as f:
                try:
                    dialect = csv.Sniffer().sniff(f.read(2048))
                    delimiter = dialect.delimiter
                except:
                    delimiter = ','

            try:
                if filename.endswith('.csv'):
                    df = pd.read_csv(
                        file_path,
                        sep=delimiter,
                        engine='python',
                        encoding='utf-8',
                        dayfirst=False,
                        on_bad_lines='warn'
                    )
            except UnicodeDecodeError:
                # Fallback for German/Windows-encoded files
                df = pd.read_csv(
                    file_path,
                    sep=delimiter,
                    engine='python',
                    encoding='latin1',
                    dayfirst=False,
                    on_bad_lines='warn'
                )
            #try:
            #    df = pd.read_excel(file_path, engine=None)
            #except Exception as e:
            #    print(f"Error loading Excel file '{filename}': {e}")
            #    continue
            target_encoder.encode_target_table(table_name, df)
