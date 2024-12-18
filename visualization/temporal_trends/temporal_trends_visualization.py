import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "../../datasets/temporal_trends.csv"
df = pd.read_csv(file_path)

# # Group by year and country, summing up the titles
# country_yearly_totals = df.groupby(["release_year", "Country"])["TotalTitles"].sum().reset_index()

# # Filter Top 5 countries with most titles overall
# top_countries = country_yearly_totals.groupby("Country")["TotalTitles"].sum().nlargest(5).index
# top_countries_data = country_yearly_totals[country_yearly_totals["Country"].isin(top_countries)]

# # Pivot the data for visualization
# pivot_data = top_countries_data.pivot(index="release_year", columns="Country", values="TotalTitles").fillna(0)

# # Plot: Stacked Area Chart
# plt.figure(figsize=(12, 6))
# pivot_data.plot(kind="area", stacked=True, colormap="tab10", linewidth=0.5)
# plt.title("Top 5 Countries by Title Contribution Over Time")
# plt.xlabel("Release Year")
# plt.ylabel("Total Titles")
# plt.legend(title="Country")
# plt.grid()
# plt.savefig("top_countries_over_time.png")  # Save the figure
# plt.close()


# Filter data starting from 1984
df = df[df["release_year"] >= 1994]

# Pivot the data for heatmap
heatmap_data = df.pivot_table(index="Country", columns="release_year", values="TotalTitles", aggfunc="sum").fillna(0)

# Filter Top 10 countries with the most titles
top_countries_heatmap = heatmap_data.loc[heatmap_data.sum(axis=1).nlargest(10).index]

# Plot: Heatmap
plt.figure(figsize=(15, 8))
sns.heatmap(top_countries_heatmap, cmap="YlGnBu", linewidths=0.5, annot=True, fmt=".0f")
plt.title("Heatmap of Titles by Top 10 Countries and Release Year")
plt.xlabel("Release Year")
plt.ylabel("Country")

# Save the heatmap to a file
plt.savefig("titles_heatmap.png")  # Save the figure
plt.close()