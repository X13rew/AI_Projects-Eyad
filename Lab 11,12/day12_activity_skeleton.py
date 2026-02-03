"""
Day 12 Activity: String & Date Cleaning
Tasks:
1) Clean city strings (strip, lower, remove punctuation)
2) Map synonyms to canonical values
3) Parse mixed-format timestamps and localize to UTC
"""

import pandas as pd
import numpy as np
import re



df = pd.read_csv("day12_users.csv")

def standardize_city(df):
    df["city_clean"] = (
        df["city"]
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w\s]", "", regex=True)  
    )

    mapping = {
        "new york": "new york",
        "nyc": "new york",
        "san francisco": "san francisco",
        "sanfrancisco": "san francisco",
    }

    df["city_standardized"] = df["city_clean"].map(mapping).fillna(df["city_clean"])
    return df

def parse_and_localize(df):
    def try_parse(x):
        try:
            return pd.to_datetime(x, errors="raise")
        except:
            return pd.NaT

    df["signup_parsed"] = df["signup_time"].apply(try_parse)

    df["signup_utc"] = df["signup_parsed"].dt.tz_localize("UTC")
    return df

df = standardize_city(df)
df = parse_and_localize(df)

print(df[["user_id", "city", "city_standardized", "signup_time", "signup_utc"]])