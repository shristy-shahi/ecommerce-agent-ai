"""
Data Agent
Executes EDA, cleans data, runs aggregations using Pandas.
"""
import pandas as pd
import numpy as np
from typing import Optional


class DataAgent:
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None

    def load_data(self, filepath: str) -> pd.DataFrame:
        self.df = pd.read_csv(filepath, parse_dates=["date"])
        return self.df

    def clean_data(self) -> pd.DataFrame:
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")
        # Fill numeric nulls with median
        num_cols = self.df.select_dtypes(include=[np.number]).columns
        self.df[num_cols] = self.df[num_cols].fillna(self.df[num_cols].median())
        # Fill categorical nulls with mode
        cat_cols = self.df.select_dtypes(include=["object"]).columns
        for col in cat_cols:
            self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
        return self.df

    def detect_outliers(self, col: str) -> pd.Series:
        Q1 = self.df[col].quantile(0.25)
        Q3 = self.df[col].quantile(0.75)
        IQR = Q3 - Q1
        return (self.df[col] < Q1 - 1.5 * IQR) | (self.df[col] > Q3 + 1.5 * IQR)

    def sales_by_region(self) -> pd.DataFrame:
        return self.df.groupby("region")["sales"].sum().reset_index()

    def sales_trend(self, freq: str = "ME") -> pd.DataFrame:
        return self.df.resample(freq, on="date")["sales"].sum().reset_index()

    def top_products(self, n: int = 10) -> pd.DataFrame:
        return self.df.groupby("product")["sales"].sum().nlargest(n).reset_index()

    def customer_retention(self) -> dict:
        order_counts = self.df.groupby("customer_id")["order_id"].count()
        repeat = (order_counts > 1).sum()
        total = len(order_counts)
        return {"repeat_customers": int(repeat), "total_customers": int(total),
                "retention_rate": round(repeat / total * 100, 2)}

    def run_full_eda(self) -> dict:
        self.clean_data()
        return {
            "shape": self.df.shape,
            "null_count": self.df.isnull().sum().to_dict(),
            "sales_by_region": self.sales_by_region().to_dict("records"),
            "top_products": self.top_products().to_dict("records"),
            "retention": self.customer_retention(),
            "total_revenue": round(self.df["sales"].sum(), 2),
        }
