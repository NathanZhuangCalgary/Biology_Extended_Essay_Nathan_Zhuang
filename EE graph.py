import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Define the time intervals and mapped midpoints/labels
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

# Average Relative Growth Data
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

# Standard Deviation Data
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

# Create DataFrames
df_avg = pd.DataFrame(avg_data, index=days)
df_std = pd.DataFrame(std_data, index=days)

# Setup figure and axis
fig, ax = plt.subplots(figsize=(12, 7))

# Plot each treatment with error bars
for treatment in df_avg.columns:
    ax.errorbar(
        x=df_avg.index,
        y=df_avg[treatment],
        yerr=df_std[treatment],
        label=f"{treatment} mg/L -N",
        marker="o",
        capsize=4,
        linewidth=1.8,
    )

# Set titles and axis labels
ax.set_title(
    "Average Relative Growth Rate % over Time by Nitrogen Treatment",
    fontsize=14,
    pad=15,
    fontweight="bold",
)
ax.set_xlabel("Measurement Period (Days)", fontsize=12, labelpad=10)
ax.set_ylabel("Average Relative Growth (%)", fontsize=12, labelpad=10)

# Enable major and minor grid lines
ax.minorticks_on()
ax.grid(visible=True, which="major", color="#666666", linestyle="-", alpha=0.6)
ax.grid(visible=True, which="minor", color="#999999", linestyle=":", alpha=0.4)

# Add horizontal zero-line for reference (growth vs decay)
ax.axhline(0, color="black", linewidth=1, linestyle="--")

# Customize legend and layout
ax.legend(title="Nitrogen Treatment", title_fontsize="11", loc="upper left")
plt.xticks(rotation=45)
plt.tight_layout()

# Display the plot
plt.show()