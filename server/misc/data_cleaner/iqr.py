import pandas as pd

def iqr(df: pd.DataFrame):
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    return (Q1, Q3, IQR)


def get_outliers(df: pd.DataFrame):
    """
    Detect outliers per column using IQR method.
    Only checks numeric columns.
    Returns dict mapping column names to row indices that are outliers.
    """
    numeric_df = df.select_dtypes(include=['number'])

    if numeric_df.empty:
        return {}

    Q1, Q3, IQR = iqr(numeric_df)
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers_per_column = {}

    for col in numeric_df.columns:
        col_outliers = (numeric_df[col] < lower_bound[col]) | (numeric_df[col] > upper_bound[col])
        outlier_indices = numeric_df[col_outliers].index.tolist()

        if outlier_indices:  # Only include columns with outliers
            outliers_per_column[col] = outlier_indices

    return outliers_per_column
