"""
Data Tools
Reusable Pandas utilities for cleaning, aggregation, and EDA.
"""
import pandas as pd
import numpy as np
from typing import List, Optional


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Impute nulls, cast types, normalize column names."""
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    num_cols = df.select_dtypes(include=[np.number]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    cat_cols = df.select_dtypes(include=["object"]).columns
    for col in cat_cols:
        df[col] = df[col].fillna(df[col].mode()[0])
    return df


def detect_outliers_iqr(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Flag outliers using IQR method. Returns df with 'is_outlier' column."""
    Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
    IQR = Q3 - Q1
    df = df.copy()
    df["is_outlier"] = (df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)
    return df


def aggregate_sales(df: pd.DataFrame, group_by: List[str],
                    metric: str = "sales", agg: str = "sum") -> pd.DataFrame:
    """Generic aggregation helper."""
    return df.groupby(group_by)[metric].agg(agg).reset_index()


def compute_growth_rate(current: float, previous: float) -> float:
    """Calculate percentage growth rate."""
    if previous == 0:
        return 0.0
    return round((current - previous) / previous * 100, 2)


def get_summary_stats(df: pd.DataFrame, col: str) -> dict:
    """Return descriptive stats for a numeric column."""
    return {
        "mean": round(df[col].mean(), 2),
        "median": round(df[col].median(), 2),
        "std": round(df[col].std(), 2),
        "min": round(df[col].min(), 2),
        "max": round(df[col].max(), 2),
        "q1": round(df[col].quantile(0.25), 2),
        "q3": round(df[col].quantile(0.75), 2),
    }
