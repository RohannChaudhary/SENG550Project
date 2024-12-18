import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
file_path = "../../datasets/runtime_trend_per_year.csv" 
df = pd.read_csv(file_path)

# # Plot: Line Chart for Average Runtime
# plt.figure(figsize=(12, 6))
# plt.plot(df['release_year'], df['AverageRuntime'], color="#E50914", linewidth=2, marker='o', markersize=5)

# # Highlight trends with labels and grid
# plt.title("Average Runtime of Titles Over the Years", fontsize=14, color="white", weight="bold")
# plt.xlabel("Release Year", fontsize=12, color="white")
# plt.ylabel("Average Runtime (minutes)", fontsize=12, color="white")
# plt.xticks(fontsize=10, color="white", rotation=45)
# plt.yticks(fontsize=10, color="white")
# plt.grid(color="grey", linestyle="--", alpha=0.5)

# # Style adjustments
# plt.style.use("dark_background")
# plt.tight_layout()

# # Save and show the chart
# plt.savefig("average_runtime_trend_netflix.png", dpi=300, bbox_inches="tight")
# plt.show()

###############
# plt.figure(figsize=(12, 6))
# plt.fill_between(df['release_year'], df['AverageRuntime'], color="#E50914", alpha=0.8)
# plt.plot(df['release_year'], df['AverageRuntime'], color="white", linewidth=2)

# # Add titles and labels
# plt.title("Area Chart of Average Runtime Over the Years", fontsize=14, color="white", weight="bold")
# plt.xlabel("Release Year", fontsize=12, color="white")
# plt.ylabel("Average Runtime (minutes)", fontsize=12, color="white")
# plt.xticks(fontsize=10, color="white", rotation=45)
# plt.yticks(fontsize=10, color="white")
# plt.grid(color="grey", linestyle="--", alpha=0.5)

# # Style adjustments
# plt.style.use("dark_background")
# plt.tight_layout()

# # Save and show the chart
# plt.savefig("average_runtime_area_netflix.png", dpi=300, bbox_inches="tight")
# plt.show()

# Plot: Scatter Plot with Regression Line
# plt.figure(figsize=(12, 6))
# sns.regplot(
#     x='release_year', 
#     y='AverageRuntime', 
#     data=df, 
#     scatter_kws={"color": "#E50914"}, 
#     line_kws={"color": "white", "linewidth": 2}, 
#     ci=None
# )

# # Customize the plot
# plt.title("Scatter Plot of Average Runtime with Trend Line", fontsize=14, color="white", weight="bold")
# plt.xlabel("Release Year", fontsize=12, color="white")
# plt.ylabel("Average Runtime (minutes)", fontsize=12, color="white")
# plt.xticks(fontsize=10, color="white", rotation=45)
# plt.yticks(fontsize=10, color="white")
# plt.grid(color="grey", linestyle="--", alpha=0.5)

# # Style adjustments
# plt.style.use("dark_background")
# plt.tight_layout()

# # Save and show the chart
# plt.savefig("average_runtime_scatter_trend_netflix.png", dpi=300, bbox_inches="tight")
# plt.show()


##############
# df['RollingAverage'] = df['AverageRuntime'].rolling(window=5, center=True).mean()

# # Plot: Line Chart with Rolling Average
# plt.figure(figsize=(12, 6))
# plt.plot(df['release_year'], df['AverageRuntime'], color="grey", alpha=0.6, label="Original", linewidth=1)
# plt.plot(df['release_year'], df['RollingAverage'], color="#E50914", linewidth=2, label="5-Year Rolling Average")

# # Add titles, labels, and legend
# plt.title("Average Runtime with Rolling Average (5-Year)", fontsize=14, color="white", weight="bold")
# plt.xlabel("Release Year", fontsize=12, color="white")
# plt.ylabel("Average Runtime (minutes)", fontsize=12, color="white")
# plt.legend(fontsize=10)
# plt.xticks(fontsize=10, color="white", rotation=45)
# plt.yticks(fontsize=10, color="white")
# plt.grid(color="grey", linestyle="--", alpha=0.5)

# # Style adjustments
# plt.style.use("dark_background")
# plt.tight_layout()

# # Save and show the chart
# plt.savefig("average_runtime_rolling_netflix.png", dpi=300, bbox_inches="tight")
# plt.show()



###############
# Convert release years and runtimes into polar coordinates
theta = np.linspace(0, 2 * np.pi, len(df))  # Angle for each year
runtimes = df['AverageRuntime']

# Plot: Polar Chart
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
ax.plot(theta, runtimes, color="#E50914", linewidth=2, label="Average Runtime")
ax.fill(theta, runtimes, color="#E50914", alpha=0.3)

# Add labels
ax.set_title("Circular Visualization of Average Runtime Trends", fontsize=14, color="white", weight="bold")
ax.set_xticks(theta[::5])  # Adjust tick positions
ax.set_xticklabels(df['release_year'][::5].astype(str), color="white", fontsize=9, rotation=45)
ax.set_yticklabels([], color="white")  # Hide radial ticks for cleaner look
plt.style.use("dark_background")

# Save and show
plt.savefig("average_runtime_polar.png", dpi=300, bbox_inches="tight")
plt.show()