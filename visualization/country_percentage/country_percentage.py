import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = "../../datasets/percentage_share_of_titles_per_country.csv" 
df = pd.read_csv(file_path)

# Sort by percentage share in descending order
df = df.sort_values(by="percentage_share", ascending=False)

# Separate the top 6 countries
top_countries = df[:6]

# Calculate "Others"
num_others = len(df) - 6  # Total number of countries in "Others"
others = pd.DataFrame({
    "country": [f"Others ({num_others} countries)"],
    "title_count": [df["title_count"][6:].sum()],
    "percentage_share": [df["percentage_share"][6:].sum()]
})

# Combine top countries and "Others"
combined_df = pd.concat([top_countries, others])

# Define Netflix-themed colors (red and darker tones)
netflix_colors = ["#E50914", "#B81D24", "#900C3F", "#FF5733", "#C70039", "#7E0E14", "#404040"]

# Set the dark background style
plt.style.use("dark_background")

# Plot: Netflix-Themed Pie Chart
plt.figure(figsize=(10, 8))
wedges, texts, autotexts = plt.pie(
    combined_df["percentage_share"], 
    labels=combined_df["country"], 
    autopct="%.2f%%", 
    startangle=140,
    colors=netflix_colors,       # Apply Netflix-themed colors
    textprops={'fontsize': 10, 'color': "white"},  # White text for contrast
    wedgeprops={'edgecolor': "black", 'linewidth': 1}  # Add black edges for clarity
)

# Customize percentage text to be bold
for autotext in autotexts:
    autotext.set_color("white")
    autotext.set_fontweight("bold")

# Title with white text
plt.title("Percentage Contribution of Top 6 Countries and Others", fontsize=14, color="white", weight="bold")

# Save the Netflix-themed pie chart
plt.savefig("countries_pie_chart.png", dpi=300, bbox_inches="tight")
plt.close()