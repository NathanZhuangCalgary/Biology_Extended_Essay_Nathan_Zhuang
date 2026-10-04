import numpy as np
import pandas as pd
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# 1. Dataset Reconstruction
days = [
    "D1-2",
    "D2-3",
    "D3-4",
    "D4-5",
    "D5-6",
    "D6-7",
    "D7-8",
    "D8-9",
    "D9-10",
    "D10-11",
    "D11-12",
    "D12-13",
    "D13-14",
]
treatments = [0.00, 50.00, 100.00, 150.00, 200.00, 400.00]

avg_data = {
    0.00: [
        24.43,
        9.13,
        12.13,
        -7.00,
        7.98,
        -2.54,
        -5.47,
        13.96,
        -8.29,
        10.20,
        -11.26,
        47.09,
        -32.87,
    ],
    50.00: [
        81.72,
        0.50,
        6.70,
        -7.65,
        5.71,
        1.14,
        -8.07,
        12.17,
        -9.50,
        21.73,
        -22.29,
        136.16,
        -62.79,
    ],
    100.00: [
        61.38,
        7.40,
        8.08,
        -2.13,
        2.97,
        -7.16,
        -5.83,
        7.76,
        -12.24,
        18.43,
        0.69,
        63.34,
        -52.17,
    ],
    150.00: [
        52.65,
        6.92,
        5.37,
        -4.17,
        5.73,
        -1.99,
        -5.79,
        -0.10,
        -11.92,
        35.15,
        -41.23,
        221.73,
        -58.00,
    ],
    200.00: [
        53.76,
        4.89,
        11.39,
        -7.92,
        4.36,
        -3.53,
        -3.83,
        -1.32,
        -10.18,
        27.53,
        -27.92,
        140.48,
        -52.64,
    ],
    400.00: [
        67.00,
        3.78,
        3.87,
        -7.15,
        6.99,
        -14.91,
        -3.53,
        -2.87,
        -21.56,
        64.26,
        10.81,
        132.07,
        -45.52,
    ],
}

std_data = {
    0.00: [
        27.02,
        3.38,
        0.76,
        4.63,
        5.99,
        4.62,
        6.88,
        14.72,
        6.25,
        9.25,
        19.15,
        74.82,
        22.65,
    ],
    50.00: [
        18.20,
        10.48,
        2.00,
        8.27,
        4.56,
        4.54,
        5.94,
        6.37,
        3.77,
        4.78,
        4.89,
        29.52,
        10.49,
    ],
    100.00: [
        15.41,
        2.51,
        1.41,
        4.83,
        5.39,
        7.59,
        10.25,
        3.63,
        2.93,
        8.05,
        23.72,
        35.62,
        12.53,
    ],
    150.00: [
        9.61,
        2.31,
        5.17,
        3.01,
        6.07,
        3.58,
        3.61,
        10.96,
        6.04,
        16.52,
        18.72,
        174.69,
        11.60,
    ],
    200.00: [
        8.28,
        3.65,
        4.18,
        5.96,
        5.63,
        3.95,
        3.13,
        5.46,
        5.25,
        16.30,
        22.65,
        108.35,
        6.87,
    ],
    400.00: [
        1.41,
        18.00,
        3.04,
        5.00,
        6.46,
        13.11,
        5.36,
        4.79,
        10.66,
        7.57,
        26.36,
        54.43,
        236.08,
    ],
}

z_base = np.array([-2, -1, 0, 1, 2], dtype=float)
z_norm = z_base / np.std(z_base, ddof=1)

rows = []
for tr in treatments:
    for i, day in enumerate(days):
        mean_val = avg_data[tr][i]
        std_val = std_data[tr][i]
        replicates = mean_val + z_norm * std_val
        for rep in replicates:
            rows.append(
                {"Treatment": f"{tr} mg/L", "Day": day, "Growth": rep}
            )

df = pd.DataFrame(rows)

# 2. Loop Through EVERY Day and Run Tukey HSD
all_results = {}
significant_comparisons = []

for day in days:
    df_day = df[df["Day"] == day]
    tukey = pairwise_tukeyhsd(
        endog=df_day["Growth"], groups=df_day["Treatment"], alpha=0.05
    )
    all_results[day] = tukey

    # Extract significant results (reject == True)
    tukey_df = pd.DataFrame(
        data=tukey._results_table.data[1:],
        columns=tukey._results_table.data[0],
    )
    sig_rows = tukey_df[tukey_df["reject"] == True]

    for _, row in sig_rows.iterrows():
        significant_comparisons.append(
            {
                "Day": day,
                "Comparison": f"{row['group1']} vs {row['group2']}",
                "Mean Diff": round(row["meandiff"], 2),
                "p-adj": round(row["p-adj"], 4),
            }
        )

# 3. Print Summary of Significant Results Across All Days
print("=== SIGNIFICANT PAIRWISE DIFFERENCES ACROSS ALL DAYS (p < 0.05) ===")
sig_df = pd.DataFrame(significant_comparisons)
if not sig_df.empty:
    print(sig_df.to_string(index=False))
else:
    print("No pairwise comparisons reached p < 0.05 on individual days.")

# 4. Print Full Day-by-Day Tukey Tables
print("\n" + "=" * 60)
print("FULL DAY-BY-DAY TUKEY HSD TABLES")
print("=" * 60)

for day in days:
    print(f"\n--- {day} ---")
    print(all_results[day])