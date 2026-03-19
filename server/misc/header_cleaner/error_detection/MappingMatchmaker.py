import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.metrics.pairwise import cosine_similarity

class MappingMatchmaker:
    def __init__(self, gold_metadata, incoming_metadata, incoming_df):
        self.gold_metadata = gold_metadata
        self.incoming_metadata = incoming_metadata

    def match_wrong_ordered_headers(self):
        self.gold_headers_order = self.gold_metadata["table_metadata"]["ordered_headers"]
        self.incoming_headers_order = self.incoming_metadata["table_metadata"]["ordered_headers"]

        # Sort incoming dataframe by gold_headers_order
        self.incoming_df = self.incoming_df.reindex(columns=sorted(self.incoming_df.columns, key=lambda x: self.gold_headers_order.index(x) if x in self.gold_headers_order else float('inf')))
        return self.incoming_df

    def match_wrong_labels(self):
        self.gold_fingerprints = self.gold_metadata["table_metadata"]["column_fingerprints"]
        self.incoming_fingerprints = self.incoming_metadata["table_metadata"]["column_fingerprints"]

        # Group incoming columns and gold columns by their data types
        self.gold_groups = self._group_by_data_type(self.gold_fingerprints)
        self.incoming_groups = self._group_by_data_type(self.incoming_fingerprints)

        # For each data type group, compute similarity and find best matches
        self.matches = {}

        # For integers compare their distributions
        for data_type in self.gold_groups:
            if data_type in self.incoming_groups:
                gold_cols = self.gold_groups[data_type]
                incoming_cols = self.incoming_groups[data_type]

                # Compute similarity matrix based on distributions
                similarity_matrix = np.zeros((len(gold_cols), len(incoming_cols)))
                for i, gold_col in enumerate(gold_cols):
                    for j, incoming_col in enumerate(incoming_cols):
                        gold_dist = self.gold_fingerprints[gold_col]["distribution"]
                        incoming_dist = self.incoming_fingerprints[incoming_col]["distribution"]
                        similarity_matrix[i, j] = cosine_similarity([gold_dist], [incoming_dist])[0][0]

                # Use Hungarian algorithm to find best matches
                row_ind, col_ind = linear_sum_assignment(-similarity_matrix)  # Maximize similarity
                for i, j in zip(row_ind, col_ind):
                    self.matches[gold_cols[i]] = incoming_cols[j]


    def _group_by_data_type(self, fingerprints):
        groups = {}
        for col, fingerprint in fingerprints.items():
            data_type = fingerprint["expected_types"]
            if data_type not in groups:
                groups[data_type] = []
            groups[data_type].append(col)
        return groups


if __name__ == "__main__":
    # Example usage
