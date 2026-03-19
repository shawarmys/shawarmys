import numpy as np
import pandas as pd
from statsmodels.stats.stattools import medcouple


def adjusted_boxplot(df: pd.DataFrame):
    numeric_df = df.select_dtypes(include=["number"])
    if numeric_df.empty:
        return {}

    q1 = numeric_df.quantile(0.25)
    q3 = numeric_df.quantile(0.75)
    iqr = q3 - q1

    mc = numeric_df.apply(
        lambda s: float(medcouple(s.dropna().to_numpy())) if s.notna().sum() >= 3 else 0.0
    ).astype("float64")

    mc_np = mc.to_numpy(dtype=np.float64)

    lower_factor = pd.Series(
        np.where(mc_np >= 0, np.exp(-4.0 * mc_np), np.exp(-3.0 * mc_np)),
        index=mc.index,
        dtype="float64",
    )
    upper_factor = pd.Series(
        np.where(mc_np >= 0, np.exp(3.0 * mc_np), np.exp(4.0 * mc_np)),
        index=mc.index,
        dtype="float64",
    )

    lower_bound = q1 - 1.5 * lower_factor * iqr
    upper_bound = q3 + 1.5 * upper_factor * iqr

    outliers_per_column = {}
    for col in numeric_df.columns:
        mask = (numeric_df[col] < lower_bound[col]) | (numeric_df[col] > upper_bound[col])
        idx = numeric_df.index[mask].tolist()
        if idx:
            outliers_per_column[col] = idx

    return outliers_per_column