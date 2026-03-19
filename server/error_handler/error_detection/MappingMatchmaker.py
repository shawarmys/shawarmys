import numpy as np
from scipy.optimize import linear_sum_assignment
from sklearn.metrics.pairwise import cosine_similarity

class MappingMatchmaker:
    def __init__(self, weights=None):
        # Default weights: Semantics are high, Type mismatches are expensive
        self.weights = weights or {
            "semantic": 0.5,
            "entropy": 0.2,
            "type": 0.3
        }

    def calculate_cost(self, incoming_col_profile, target_col_profile):
        """Calculates a scalar cost between 0 (identical) and 1+ (very different)"""
        cost = 0

        # 1. Semantic Distance (1 - Cosine Similarity)
        # Reshape for sklearn similarity: [[vec]]
        sem_sim = cosine_similarity(
            [incoming_col_profile['semantic_embedding']],
            [target_col_profile['semantic_embedding']]
        )[0][0]
        cost += self.weights['semantic'] * (1 - sem_sim)

        # 2. Entropy Difference
        ent_diff = abs(incoming_col_profile['entropy'] - target_col_profile['entropy'])
        # Normalize: assuming entropy usually falls between 0-10 for columns
        cost += self.weights['entropy'] * min(ent_diff / 5.0, 1.0)

        # 3. Type Compatibility
        # Penalty if the 'top' detected type doesn't exist in target's expected types
        inc_type = max(incoming_col_profile['type_dist'], key=incoming_col_profile['type_dist'].get)
        if target_col_profile['expected_types'].get(inc_type, 0) < 0.1:
            cost += self.weights['type'] * 1.0 # Significant penalty

        return cost

    def find_best_mapping(self, incoming_profiles, target_profiles):
        """
        incoming_profiles: dict of {col_name: fingerprint}
        target_profiles: dict of {col_name: fingerprint}
        """
        inc_keys = list(incoming_profiles.keys())
        tgt_keys = list(target_profiles.keys())

        # Initialize Cost Matrix [Rows = Incoming, Cols = Target]
        matrix = np.zeros((len(inc_keys), len(tgt_keys)))

        for i, inc_key in enumerate(inc_keys):
            for j, tgt_key in enumerate(tgt_keys):
                matrix[i, j] = self.calculate_cost(
                    incoming_profiles[inc_key],
                    target_profiles[tgt_key]
                )

        # Apply Hungarian Algorithm
        # row_ind: indices of incoming_profiles
        # col_ind: the corresponding optimal target_profile index
        row_ind, col_ind = linear_sum_assignment(matrix)

        results = []
        for r, c in zip(row_ind, col_ind):
            mapping_cost = matrix[r, c]
            results.append({
                "incoming_col": inc_keys[r],
                "target_col": tgt_keys[c],
                "confidence": 1.0 - min(mapping_cost, 1.0),
                "cost": mapping_cost
            })

        return results
