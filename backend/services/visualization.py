import pandas as pd
import decimal
import datetime
import re


def detect_requested_chart(question: str) -> str:
    """
    Detect user requested chart type from the question.
    """
    if not question:
        return None

    q = question.lower()
    if re.search(r"\b(line chart|trend|over time|monthly|daily|weekly)\b", q):
        return "line"
    if re.search(r"\b(bar chart|compare|top|ranking)\b", q):
        return "bar"
    if re.search(r"\b(pie chart|percentage|share|distribution|breakdown)\b", q):
        return "pie"
    if re.search(r"\b(kpi|total|sum|number of|count of)\b", q):
        return "kpi"
    if re.search(r"\b(table|list|rows)\b", q):
        return "table"
    return None


def generate_chart_config(results: list, question: str = None):
    """
    Semantic + directive-aware BI visualization engine.

    Chart Types:
    - KPI
    - Line
    - Bar
    - Stacked Bar
    - Grouped Bar
    - Pie (true distribution only)
    - Table fallback
    """

    if not results:
        return {"type": "table", "data": []}

    df = pd.DataFrame(results)

    # ----------------------------
    # Normalize data types
    # ----------------------------
    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].apply(
                lambda x: float(x) if isinstance(x, decimal.Decimal) else x
            )

    for col in df.columns:
        if isinstance(df[col].iloc[0], (datetime.date, datetime.datetime)):
            df[col] = pd.to_datetime(df[col])

    # ----------------------------
    # Identify column types
    # ----------------------------
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    numeric_cols = [c for c in numeric_cols if not c.lower().endswith("id")]

    datetime_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    categorical_cols = [c for c in df.columns if c not in numeric_cols and c not in datetime_cols]

    row_count = len(df)

    # ----------------------------
    # Detect requested chart from question
    # ----------------------------
    requested_chart = detect_requested_chart(question)

    # ----------------------------
    # Single row → KPI
    # ----------------------------
    if row_count == 1 and numeric_cols:
        primary_metric = numeric_cols[0]
        return {
            "type": "kpi",
            "value": df.iloc[0][primary_metric],
            "label": primary_metric,
            "context": {col: df.iloc[0][col] for col in categorical_cols} if categorical_cols else None
        }

    # ----------------------------
    # Explicit directive overrides
    # ----------------------------
    if requested_chart == "line" and datetime_cols and numeric_cols:
        x_col = datetime_cols[0]
        y_col = numeric_cols[0]
        return {
            "type": "line",
            "x": df[x_col].dt.strftime("%Y-%m-%d").tolist(),
            "y": df[y_col].tolist(),
            "x_label": x_col,
            "y_label": y_col
        }

    if requested_chart == "pie" and categorical_cols and numeric_cols:
        cat_col = categorical_cols[0]
        num_col = numeric_cols[0]
        return {
            "type": "pie",
            "labels": df[cat_col].astype(str).tolist(),
            "values": df[num_col].tolist(),
            "label_field": cat_col,
            "value_field": num_col
        }

    if requested_chart == "table":
        return {"type": "table", "data": df.to_dict(orient="records")}

    # ----------------------------
    # Time Series Inference → Line
    # ----------------------------
    if len(datetime_cols) == 1 and len(numeric_cols) == 1:
        x_col = datetime_cols[0]
        y_col = numeric_cols[0]
        return {
            "type": "line",
            "x": df[x_col].dt.strftime("%Y-%m-%d").tolist(),
            "y": df[y_col].tolist(),
            "x_label": x_col,
            "y_label": y_col
        }

    # ----------------------------
    # Pie / Distribution inference
    # ----------------------------
    distribution_keywords = ["share", "distribution", "percentage", "contribution", "breakdown"]
    is_distribution_intent = any(k in (question.lower() if question else "") for k in distribution_keywords)

    if (
        is_distribution_intent
        and len(categorical_cols) == 1
        and len(numeric_cols) == 1
        and 2 <= row_count <= 8
    ):
        cat_col = categorical_cols[0]
        num_col = numeric_cols[0]
        return {
            "type": "pie",
            "labels": df[cat_col].astype(str).tolist(),
            "values": df[num_col].tolist(),
            "label_field": cat_col,
            "value_field": num_col
        }

    # ----------------------------
    # Stacked Bar → 2 categories + 1 numeric
    # ----------------------------
    if len(categorical_cols) >= 2 and len(numeric_cols) == 1:
        primary = categorical_cols[0]
        secondary = categorical_cols[1]
        value_col = numeric_cols[0]
        grouped = df.groupby([primary, secondary])[value_col].sum().reset_index()
        pivot_df = grouped.pivot(index=primary, columns=secondary, values=value_col).fillna(0)
        return {
            "type": "stacked_bar",
            "categories": pivot_df.index.astype(str).tolist(),
            "series": [{"name": str(col), "data": pivot_df[col].tolist()} for col in pivot_df.columns],
            "x_label": primary,
            "y_label": value_col
        }

    # ----------------------------
    # Grouped Bar → 1 category + multiple numeric
    # ----------------------------
    if len(categorical_cols) == 1 and len(numeric_cols) > 1:
        cat_col = categorical_cols[0]
        return {
            "type": "grouped_bar",
            "categories": df[cat_col].astype(str).tolist(),
            "series": [{"name": metric, "data": df[metric].tolist()} for metric in numeric_cols],
            "x_label": cat_col,
            "y_label": "Values"
        }

    # ----------------------------
    # Ranking / Comparison → Bar
    # ----------------------------
    if len(categorical_cols) == 1 and len(numeric_cols) == 1:
        cat_col = categorical_cols[0]
        num_col = numeric_cols[0]
        return {
            "type": "bar",
            "x": df[cat_col].astype(str).tolist(),
            "y": df[num_col].tolist(),
            "x_label": cat_col,
            "y_label": num_col
        }

    # ----------------------------
    # Fallback → Table
    # ----------------------------
    return {"type": "table", "data": df.to_dict(orient="records")}