import pandas as pd
import numpy as np

df = pd.read_csv("day14_users_raw.csv")
def clean_types(df):
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = pd.to_numeric(df[col], errors="ignore")
            df[col] = pd.to_datetime(df[col], errors="ignore")
    return df

def clean_missing(df):
    df = df.copy()
    for col in df.columns:
        df[col] = df[col].fillna(
            df[col].median() if df[col].dtype.kind in "biufc"
            else df[col].mode()[0] if df[col].mode().size > 0
            else "Unknown"
        )
    return df

def handle_outliers(df):
    df = df.copy()
    for col in df.select_dtypes(include="number"):
        Q1, Q3 = df[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        df[col] = df[col].clip(Q1 - 1.5*IQR, Q3 + 1.5*IQR)
    return df

def clean_strings_and_dates(df):
    df = df.copy()
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.strip().str.replace(r"\s+", " ", regex=True)
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df

def validate_cleaned(df):
    return {
        "missing": df.isna().sum().to_dict(),
        "invalid_dates": {c: df[c].isna().sum() for c in df.columns if "date" in c.lower()}
    }

def clean_data(df):
    for func in [clean_types, clean_missing, handle_outliers, clean_strings_and_dates]:
        df = func(df)
    return df, validate_cleaned(df)
print(df)