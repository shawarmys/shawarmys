class CSVProfiler:
    def __init__(self, filepath, embedding_model):
        self.filepath = filepath
        self.embedding_model = embedding_model

        # Step 0: Filename & Metadata Extraction
        self.file_metadata = self._extract_filename_metadata(filepath)
        self.assumed_target = self.file_metadata.get("assumed_report_type")

        # Load raw lines for header check, and a stratified sample dataframe for column checks
        self.raw_head = self._load_raw_lines(filepath, num_lines=15)
        self.df_sample = self._load_stratified_sample(filepath, sample_size=1000)

    def perform_header_check(self):
        """
        Evaluates Row 1 against Rows 2-10 to determine if it is a valid header.
        Returns a confidence score (0.0 to 1.0).
        """
        row_1 = self.raw_head[0]
        sample_rows = self.raw_head[1:10]

        # 1. Character Class Ratios
        r1_alpha_pct = self._calc_alpha_percentage(row_1) # Expect > 90% for headers

        # 2. Token Shape Mapping (e.g., 'Cust_ID' -> 'Xxxx_XX')
        r1_shapes = [self._map_to_shape(cell) for cell in row_1]

        # 3. Type Divergence (Does Row 1 fail numeric casting while sample rows pass?)
        r1_cast_success = self._try_cast_numeric_date(row_1)
        sample_cast_success = self._try_cast_numeric_date(sample_rows)
        divergence_score = self._calculate_divergence(r1_cast_success, sample_cast_success)

        # 4. Length Variance
        r1_avg_len = self._avg_string_length(row_1)
        sample_avg_len = self._avg_string_length(sample_rows)

        # Aggregate into a likelihood score using weighted heuristics
        header_likelihood = self._compute_header_likelihood(
            r1_alpha_pct, divergence_score, r1_avg_len, sample_avg_len
        )

        return {
            "is_header_likelihood": header_likelihood,
            "detected_shapes": r1_shapes,
            "inferred_headers": row_1 if header_likelihood > 0.85 else None
        }

    def perform_column_check(self):
        """
        Profiles the stratified data sample to generate fingerprints for mapping.
        Assumes headers are identified or assigned generic names (Col_1, Col_2).
        """
        column_profiles = {}

        for col_name in self.df_sample.columns:
            col_data = self.df_sample[col_name]
            total_rows = len(col_data)

            # 1. Micro-Profiling (Nulls and Types)
            strict_null_pct = self._detect_strict_nulls(col_data) / total_rows
            type_distribution = self._duck_type_waterfall(col_data) # e.g., {'int': 0.95, 'string': 0.05}

            # 2. Cardinality & Distribution
            unique_vals = col_data.nunique()
            cardinality_ratio = unique_vals / total_rows

            # 3. Information Density (Entropy)
            entropy = self._calculate_shannon_entropy(col_data)

            # 4. Statistical Fingerprint
            stats = self._get_numeric_stats(col_data) if type_distribution.get('int', 0) > 0.5 else None

            # 5. Semantic Vector Embedding (Header + Data Sample)
            top_5_samples = col_data.dropna().unique()[:5]
            semantic_string = f"{col_name}: {', '.join(map(str, top_5_samples))}"
            semantic_embedding = self.embedding_model.encode(semantic_string)

            column_profiles[col_name] = {
                "null_pct": strict_null_pct,
                "type_dist": type_distribution,
                "cardinality": cardinality_ratio,
                "entropy": entropy,
                "stats": stats,
                "semantic_embedding": semantic_embedding
            }

        return column_profiles

    def run_profiler(self):
        """Orchestrates the checks and returns the full profile."""
        header_analysis = self.perform_header_check()

        # Adjust dataframe headers if Row 1 wasn't a real header
        if header_analysis["is_header_likelihood"] < 0.85:
            self._shift_dataframe_headers_to_data()

        column_analysis = self.perform_column_check()

        return {
            "metadata": self.file_metadata,
            "header_analysis": header_analysis,
            "column_profiles": column_analysis
        }
