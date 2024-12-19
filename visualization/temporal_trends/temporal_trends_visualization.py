import pandas as pd
import matplotlib.pyplot as plt


# Load the dataset
file_path = "../../datasets/temporal_trends.csv"
df = pd.read_csv(file_path)
df = df[df["release_year"] >= 1990]


# Group by release_year and calculate total titles
yearly_totals = df.groupby("release_year")["TotalTitles"].sum().reset_index()


plt.style.use("dark_background")

# Plot: Total Titles over the Years
plt.figure(figsize=(12, 6))
plt.plot(
    yearly_totals["release_year"],
    yearly_totals["TotalTitles"],
    marker="o",
    linestyle="-",
    color="#E50914", 
    linewidth=2,    
    markerfacecolor="#FF5733",  
    markeredgecolor="white",   
    markersize=8
)

# Customizing titles and labels
plt.title("Total Number of Titles Released Over Time", fontsize=14, color="white", weight="bold")
plt.xlabel("Release Year", fontsize=12, color="white")
plt.ylabel("Total Titles", fontsize=12, color="white")

# Customizing grid lines
plt.grid(color="grey", linestyle="--", linewidth=0.5)

# Adjust the ticks to white
plt.tick_params(axis="x", colors="white")
plt.tick_params(axis="y", colors="white")

# Save the plot as an image
plt.savefig("total_titles_over_time.png") 
plt.close()

###################
# # Group by year and country, summing up the titles
# country_yearly_totals = df.groupby(["release_year", "Country"])["TotalTitles"].sum().reset_index()

# # Filter Top 5 countries with most titles overall
# top_countries = country_yearly_totals.groupby("Country")["TotalTitles"].sum().nlargest(5).index
# top_countries_data = country_yearly_totals[country_yearly_totals["Country"].isin(top_countries)]

# # Pivot the data for visualization
# pivot_data = top_countries_data.pivot(index="release_year", columns="Country", values="TotalTitles").fillna(0)

# # Set Netflix-like theme
# plt.style.use("dark_background")  # Use a dark background

# netflix_colors = ["#E50914", "#FF5733", "#900C3F", "#221F1F", "#C70039"]

# # Plot: Stacked Area Chart
# plt.figure(figsize=(12, 6))
# pivot_data.plot(kind="area", stacked=True, color=netflix_colors, linewidth=0.5)

# # Customize titles and labels
# plt.title("Top 5 Countries by Title Contribution Over Time", fontsize=14, color="white", weight="bold")
# plt.xlabel("Release Year", fontsize=12, color="white")
# plt.ylabel("Total Titles", fontsize=12, color="white")
# plt.legend(title="Country", facecolor="#221F1F", edgecolor="white", labelcolor="white")
# plt.grid(color="grey", linestyle="--", linewidth=0.5)


# plt.savefig("top_countries_over_time_netflix.png", dpi=300, bbox_inches="tight") 
# plt.close()


###################
# # Pivot the data for heatmap
# heatmap_data = df.pivot_table(index="Country", columns="release_year", values="TotalTitles", aggfunc="sum").fillna(0)

# # Filter Top 10 countries with the most titles
# top_countries_heatmap = heatmap_data.loc[heatmap_data.sum(axis=1).nlargest(10).index]

# # Set Netflix-like dark theme
# plt.style.use("dark_background")

# # Define a custom Netflix-themed colormap
# netflix_cmap = sns.light_palette("#E50914", as_cmap=True)  # Netflix Red-based gradient

# # Plot: Heatmap
# plt.figure(figsize=(15, 8))
# sns.heatmap(
#     top_countries_heatmap, 
#     cmap=netflix_cmap,   # Custom Netflix colormap
#     linewidths=0.5, 
#     annot=True, 
#     fmt=".0f", 
#     linecolor="black"    # Gridlines in black for contrast
# )

# # Customize titles and labels
# plt.title("Heatmap of Titles by Top 10 Countries and Release Year", fontsize=14, color="white", weight="bold")
# plt.xlabel("Release Year", fontsize=12, color="white")
# plt.ylabel("Country", fontsize=12, color="white")

# # Adjust tick colors
# plt.xticks(color="white")
# plt.yticks(color="white", rotation=0)  # Keep country names horizontal
# # Save the heatmap to a file
# plt.savefig("titles_heatmap.png")  # Save the figure
# plt.close()