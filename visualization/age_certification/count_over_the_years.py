import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "../../datasets/age_certification_per_year.csv"
df = pd.read_csv(file_path)

# Filter data starting from 1990
df = df[df["release_year"] >= 1990]

# Pivot the data for a stacked area chart
pivot_data = df.pivot_table(index="release_year", columns="age_certification", values="TitleCount", aggfunc="sum").fillna(0)

# Create Netflix-themed plot
plt.figure(figsize=(14, 8))
pivot_data.plot(kind="area", stacked=True, figsize=(14, 8), color=["#E50914", "#B81D24", "#221F1F", "#FFFFFF", "#666666", "#FF5733"])

# Netflix-style customization
plt.title("Age Certification Trends (1990-Present)", fontsize=18, fontweight="bold", color="#E50914")
plt.xlabel("Release Year", fontsize=14, fontweight="bold", color="#FFFFFF")
plt.ylabel("Title Count", fontsize=14, fontweight="bold", color="#FFFFFF")
plt.legend(title="Age Certification", fontsize=12, title_fontsize=14, loc="upper left", facecolor="#333333", edgecolor="#333333")
plt.grid(color="#444444", linestyle="--", linewidth=0.5)
plt.gca().set_facecolor("#221F1F")
plt.tick_params(colors="#000000", labelsize=12)
plt.savefig("age_certification_trends.png")  # Save the figure
plt.close()

print("Stacked area chart saved as 'age_certification_trends.png'.")



# Filter for recent years (2015 onward)
recent_years_data = df[df["release_year"] >= 2000]
recent_years_data = df[df["release_year"] <= 2021]


# Group by release_year and age_certification, summing TitleCount
recent_pivot = recent_years_data.pivot_table(index="release_year", columns="age_certification", values="TitleCount", aggfunc="sum").fillna(0)

# Use a high-contrast color palette
palette = sns.color_palette("Set1", n_colors=len(recent_pivot.columns))  # Distinct colors

# Plot Netflix-themed line chart
plt.figure(figsize=(14, 8))
for idx, column in enumerate(recent_pivot.columns):
    plt.plot(recent_pivot.index, recent_pivot[column], label=column, color=palette[idx], linewidth=2)

# Netflix-style customization
plt.title("Recent Age Certification Trends (2000-Present)", fontsize=18, fontweight="bold", color="#E50914")
plt.xlabel("Release Year", fontsize=14, fontweight="bold", color="#CCCCCC")  # Light gray labels
plt.ylabel("Title Count", fontsize=14, fontweight="bold", color="#CCCCCC")  # Light gray labels
plt.legend(title="Age Certification", fontsize=12, title_fontsize=14, loc="upper left", facecolor="#333333", edgecolor="#333333")
plt.grid(color="#444444", linestyle="--", linewidth=0.5)
plt.gca().set_facecolor("#221F1F")
plt.tick_params(colors="#000000", labelsize=12)  # Light gray tick labels

# Save the figure
plt.savefig("netflix_recent_age_certifications_fixed.png", bbox_inches="tight", facecolor="#221F1F")
plt.close()




# Group and pivot the data
type_age_data = df.groupby(["type", "age_certification"])["TitleCount"].sum().reset_index()
pivot_type_age_heatmap = type_age_data.pivot(index="age_certification", columns="type", values="TitleCount").fillna(0)

# Plot heatmap
plt.figure(figsize=(12, 8))
plt.style.use("dark_background")
sns.heatmap(
    pivot_type_age_heatmap,
    annot=True,
    fmt=".0f",
    cmap="Reds",
    linewidths=0.5,
    linecolor="black",
    cbar_kws={"label": "Title Count"},
)

# Customize the chart for a black background
plt.title("Heatmap of Age Certification Distribution by Content Type", fontsize=16, fontweight="bold", color="white")
plt.xlabel("Content Type", fontsize=12, color="white")
plt.ylabel("Age Certification", fontsize=12, color="white")

# Adjust the figure background and tick labels
plt.gca().set_facecolor("black")
plt.xticks(color="white", fontsize=10)
plt.yticks(color="white", fontsize=10)

plt.savefig("age_certification_by_type.png")  # Save the figure
plt.close()


