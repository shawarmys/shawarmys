import torch
import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from scipy.optimize import linear_sum_assignment

class BertSemanticMatcher:
    def __init__(self, model_dir="./models/bert_local"):
        # Load directly from the local directory
        print(f"Loading BERT from {model_dir}...")
        self.tokenizer = BertTokenizer.from_pretrained(model_dir)
        self.model = BertModel.from_pretrained(model_dir)
        self.model.eval()

    def _stringify_fingerprint(self, col_name, fp):
        """Converts the fingerprint DNA into a descriptive sentence for BERT."""
        main_type = max(fp['expected_types'], key=fp['expected_types'].get)

        desc = (
            f"Header: {col_name}. "
            f"Type: {main_type}. "
            f"Entropy: {fp['entropy']:.2f}. "
            f"Unique Ratio: {fp['cardinality_ratio']:.2f}. "
            f"Mean Length: {fp['length_stats']['mean']:.1f}."
        )
        return desc

    def get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
        with torch.no_grad():
            outputs = self.model(**inputs)
        # Using the [CLS] token representation
        return outputs.last_hidden_state[:, 0, :].numpy()

    def match_columns(self, target_fp_dict, incoming_fp_dict):
        tgt_cols = list(target_fp_dict.keys())
        inc_cols = list(incoming_fp_dict.keys())

        # Generate embeddings (Local CPU/GPU inference)
        tgt_embeddings = np.vstack([self.get_embedding(self._stringify_fingerprint(n, target_fp_dict[n])) for n in tgt_cols])
        inc_embeddings = np.vstack([self.get_embedding(self._stringify_fingerprint(n, incoming_fp_dict[n])) for n in inc_cols])

        # Cost Matrix (1 - Similarity)
        sim_matrix = cosine_similarity(inc_embeddings, tgt_embeddings)
        cost_matrix = 1 - sim_matrix

        # Optimization
        row_ind, col_ind = linear_sum_assignment(cost_matrix)

        return [
            {
                "incoming": inc_cols[r],
                "target": tgt_cols[c],
                "confidence": float(sim_matrix[r, c])
            }
            for r, c in zip(row_ind, col_ind)
        ]


# --- Example Usage ---
if __name__ == "__main__":
    import json
    from CsvExcelReader import CsvExcelReader
    # Test case: Use two different datasets with different column labels but similar data distributions and see if the matchmaker can correctly identify the matches based on the fingerprints
    # Use the TableSchemaEncoder to create gold metadata and incoming metadata for two different datasets, then use the MappingMatchmaker to find the best matches and reorder/rename the incoming dataframe to match the gold standard. Evaluate the results based on how well the columns were matched and reordered/renamed.
    from TableSchemaEncoder import TableSchemaEncoder

    encoder = TableSchemaEncoder()
    input_file = "C:\\Users\\marti\\Documents\\shawarmys\\server\\misc\\header_cleaner\\error_detection\\csvFiles\\split_data_pat_case_altered\\clinic_1_nursing.csv"
    reader = CsvExcelReader(input_file)
    incoming_df = reader.read_csv()
    incoming_metadata = encoder.encode_target_table("incoming_table", incoming_df)

    with open("C:\\Users\\marti\\Documents\\shawarmys\\server\\misc\\header_cleaner\\error_detection\\goldFingerPrints\\synthetic_nursing_daily_reports_en_fingerprint.json") as f:
        gold_metadata = json.load(f)

    # Start the matching process
    matchmaker = BertSemanticMatcher()
    matches = matchmaker.match_columns(gold_metadata["column_fingerprints"], incoming_metadata["column_fingerprints"])
    print("Matches found:")
    for match in matches:
        print(f"Incoming Column: {match['incoming']} --> Target Column: {match['target']} (Confidence: {match['confidence']:.2f})")
