"""
Visualization Tools
Plotly chart generators for the analytics dashboard.
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional


DARK_TEMPLATE = dict(
    paper_bgcolor="#0A0D12",
    plot_bgcolor="#111620",
    font=dict(color="#E8ECF4"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
)

COLORS = ["#00E5A0", "#6C63FF", "#FF6B6B", "#FFB347", "#38BDF8", "#A78BFA"]


def plot_sales_by_region(df: pd.DataFrame, title: str = "Sales by Region") -> go.Figure:
    data = df.groupby("region")["sales"].sum().reset_index()
    fig = px.bar(data, x="region", y="sales", title=title,
                 color="region", color_discrete_sequence=COLORS)
    fig.update_layout(**DARK_TEMPLATE)
    return fig


def plot_sales_trend(df: pd.DataFrame, freq: str = "ME",
                     title: str = "Sales Trend") -> go.Figure:
    trend = df.resample(freq, on="date")["sales"].sum().reset_index()
    fig = px.line(trend, x="date", y="sales", title=title,
                  color_discrete_sequence=[COLORS[0]])
    fig.update_traces(line_width=2.5)
    fig.update_layout(**DARK_TEMPLATE)
    return fig


def plot_top_products(df: pd.DataFrame, n: int = 10) -> go.Figure:
    top = df.groupby("product")["sales"].sum().nlargest(n).reset_index()
    fig = px.bar(top, x="sales", y="product", orientation="h",
                 title=f"Top {n} Products by Revenue",
                 color_discrete_sequence=[COLORS[1]])
    fig.update_layout(**DARK_TEMPLATE)
    return fig


def plot_customer_segments(df: pd.DataFrame) -> go.Figure:
    counts = df.groupby("customer_id")["order_id"].count()
    segments = pd.cut(counts, bins=[0, 1, 3, 10, float("inf")],
                      labels=["One-time", "Occasional", "Regular", "VIP"])
    seg_counts = segments.value_counts().reset_index()
    seg_counts.columns = ["segment", "count"]
    fig = px.pie(seg_counts, values="count", names="segment",
                 title="Customer Segments", color_discrete_sequence=COLORS)
    fig.update_layout(**DARK_TEMPLATE)
    return fig
