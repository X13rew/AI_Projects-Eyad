"""
Day 11 Activity: Outlier Strategies
Tasks:
1) Load numeric data with outliers
2) Implement percentile capping (winsorization)
3) Implement removal strategy
4) Compare summary stats before/after
"""

import pandas as pd
import numpy as np

# income = [
#     20074.66, 43519.44, 22388.46, 12655.25, 37727.56, 13362.66, 26191.16, 31052.51,
#     10000000.0, 20000000.0, 50000000.0
# ]



# df = pd.DataFrame({"income": income})

df = pd.read_csv("day11_income.csv")

def winsorize_series(s, lower_q=0.01, upper_q=0.99):
    lower = s.quantile(lower_q)
    upper = s.quantile(upper_q)
    return s.clip(lower, upper)

def remove_upper_tail(s, upper_q=0.99):
    upper = s.quantile(upper_q)
    return s[s <= upper]

original_stats = df["income"].describe()

winsorized = winsorize_series(df["income"], 0.01, 0.99)
winsorized_stats = winsorized.describe()

removed = remove_upper_tail(df["income"], 0.99)
removed_stats = removed.describe()

print("\n===== ORIGINAL DATA =====")
print(original_stats)

print("\n===== AFTER WINSORIZATION =====")
print(winsorized_stats)

print("\n===== AFTER REMOVAL STRATEGY =====")
print(removed_stats)
