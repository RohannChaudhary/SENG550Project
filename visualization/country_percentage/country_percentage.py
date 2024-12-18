import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = "../../datasets/percentage_share_of_titles_per_country.csv"  # Replace with the correct path
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

# Plot: Pie Chart
plt.figure(figsize=(10, 8))
plt.pie(
    combined_df["percentage_share"], 
    labels=combined_df["country"], 
    autopct="%.2f%%", 
    startangle=140, 
    textprops={'fontsize': 10}
)
plt.title("Percentage Contribution of Top 6 Countries and Others")
plt.savefig("countries_pie_chart.png")  # Save the figure
plt.close()
