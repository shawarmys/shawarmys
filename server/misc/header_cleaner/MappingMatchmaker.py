import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.metrics.pairwise import cosine_similarity

class MappingMatchmaker:
    def __init__(self, gold_metadata, incoming_metadata, incoming_df):
        self.gold_metadata = gold_metadata
        self.incoming_metadata = incoming_metadata
        self.incoming_df = incoming_df

    def match_wrong_ordered_columns(self):
        gold_order = self.gold_metadata["table_metadata"]["ordered_headers"]
        existing_columns = [col for col in gold_order if col in self.incoming_df.columns]

        # Reorder the dataframe directly
        self.incoming_df = self.incoming_df[existing_columns]

        return self.incoming_df

    def match_wrong_labels(self):
        # 1. Grab fingerprints from the correct top-level JSON key
        self.gold_fingerprints = self.gold_metadata["column_fingerprints"]
        self.incoming_fingerprints = self.incoming_metadata["column_fingerprints"]

        gold_cols = list(self.gold_fingerprints.keys())
        incoming_cols = list(self.incoming_fingerprints.keys())

        # 2. Build a Similarity Matrix
        # This creates a grid of size (Number of Gold Cols) x (Number of Incoming Cols)
        similarity_matrix = np.zeros((len(gold_cols), len(incoming_cols)))

        for i, g_col in enumerate(gold_cols):
            for j, i_col in enumerate(incoming_cols):
                similarity_matrix[i, j] = self._compute_similarity(
                    self.gold_fingerprints[g_col],
                    self.incoming_fingerprints[i_col]
                )

        # 3. Use Hungarian algorithm to find the optimal global match
        # We make the matrix negative because the algorithm minimizes cost,
        # but we want to MAXIMIZE similarity.
        row_ind, col_ind = linear_sum_assignment(-similarity_matrix)

        # 4. Create the rename mapping (Incoming Name -> Gold Name)
        rename_mapping = {}
        for r, c in zip(row_ind, col_ind):
            gold_name = gold_cols[r]
            incoming_name = incoming_cols[c]
            rename_mapping[incoming_name] = gold_name

        # 5. Apply the mapping to the dataframe
        self.incoming_df.rename(columns=rename_mapping, inplace=True)

        # 6. Reorder the columns to match the Gold Standard order
        self.incoming_df = self.match_wrong_ordered_columns()

        return self.incoming_df

    def _compute_similarity(self, fp1, fp2):
        """Calculates a similarity score between 0.0 and 1.0 for two column fingerprints."""

        # --- A. Data Type Similarity (Dot Product) ---
        types1 = fp1.get("expected_types", {})
        types2 = fp2.get("expected_types", {})
        all_type_keys = set(types1.keys()) | set(types2.keys())
        # Multiplies probabilities: e.g., (1.0 * 1.0) + (0.0 * 0.0) = 1.0
        type_sim = sum(types1.get(k, 0.0) * types2.get(k, 0.0) for k in all_type_keys)

        # --- B. Entropy Similarity ---
        e1, e2 = fp1.get("entropy", 0.0), fp2.get("entropy", 0.0)
        max_e = max(e1, e2)
        ent_sim = 1.0 - (abs(e1 - e2) / max_e) if max_e > 0 else 1.0

        # --- C. Cardinality Similarity ---
        c1, c2 = fp1.get("cardinality_ratio", 0.0), fp2.get("cardinality_ratio", 0.0)
        max_c = max(c1, c2)
        card_sim = 1.0 - (abs(c1 - c2) / max_c) if max_c > 0 else 1.0

        # --- D. Physical Length (Mean) Similarity ---
        l1 = fp1.get("length_stats", {}).get("mean", 0.0)
        l2 = fp2.get("length_stats", {}).get("mean", 0.0)
        max_l = max(l1, l2)
        len_sim = 1.0 - (abs(l1 - l2) / max_l) if max_l > 0 else 1.0

        # Calculate final weighted score
        # 40% Types | 20% Entropy | 20% Cardinality | 20% Length
        total_score = (type_sim * 0.40) + (ent_sim * 0.20) + (card_sim * 0.20) + (len_sim * 0.20)

        return total_score


    def _group_by_data_type(self, fingerprints):
        groups = {}
        for col, fingerprint in fingerprints.items():
            data_type = fingerprint["expected_types"]
            if data_type not in groups:
                groups[data_type] = []
            groups[data_type].append(col)
        return groups


if __name__ == "__main__":
    import json
    from CsvExcelReader import CsvExcelReader
    """
    # Test case: Reorder 9 columns in the incoming dataframe and see if the matchmaker can reorder them back to match the gold standard
    with open("C:\\Users\\marti\\Documents\\shawarmys\\server\\misc\\header_cleaner\\error_detection\\goldFingerPrints\\epaAC-Data-1_fingerprint.json") as f:
        gold_metadata = json.load(f)
    incoming_metadata = gold_metadata.copy()
    reader = CsvExcelReader("C:\\Users\\marti\\Documents\\shawarmys\\server\\misc\\header_cleaner\\error_detection\\csvFiles\\goldStandard\\epaAC-Data-1.csv")
    df = reader.read_csv()
    # Reorder 9 dataframe columns for testing
    df_reordered = df.iloc[:, [0, 2, 1, 4, 3, 6, 5, 8, 7]]
    # Reorder incoming metadata to match the reordered dataframe
    incoming_metadata["table_metadata"]["ordered_headers"] = [incoming_metadata["table_metadata"]["ordered_headers"][i] for i in [0, 2, 1, 4, 3, 6, 5, 8, 7]]
    print("original columns:", df.columns.tolist())
    print("reordered columns:", df_reordered.columns.tolist())
    matchmaker = MappingMatchmaker(gold_metadata, incoming_metadata, df_reordered)
    matched_df = matchmaker.match_wrong_ordered_columns()
    print("matched columns:", matched_df.columns.tolist())
    """
    # Test case: Use two different datasets with different column labels but similar data distributions and see if the matchmaker can correctly identify the matches based on the fingerprints
    # Use the TableSchemaEncoder to create gold metadata and incoming metadata for two different datasets, then use the MappingMatchmaker to find the best matches and reorder/rename the incoming dataframe to match the gold standard. Evaluate the results based on how well the columns were matched and reordered/renamed.
    from TableSchemaEncoder import TableSchemaEncoder

    encoder = TableSchemaEncoder()
    input_file = "C:\\Users\\marti\\Documents\\shawarmys\\server\\misc\\header_cleaner\\error_detection\\csvFiles\\errorousFiles\\NoHeader_synth_device_raw_1hz_motion_fall.csv"
    reader = CsvExcelReader(input_file)
    incoming_df = reader.read_csv()
    incoming_metadata = encoder.encode_target_table("incoming_table", incoming_df)

    with open("C:\\Users\\marti\\Documents\\shawarmys\\server\\misc\\header_cleaner\\error_detection\\goldFingerPrints\\synthetic_nursing_daily_reports_en_fingerprint.json") as f:
        gold_metadata = json.load(f)

    # Start the matching process
    matchmaker = MappingMatchmaker(gold_metadata, incoming_metadata, incoming_df)
    matched_df = matchmaker.match_wrong_labels()
