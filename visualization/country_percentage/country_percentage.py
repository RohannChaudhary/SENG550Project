import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import pycountry
import numpy as np
from plotly.io import write_image
import plotly.graph_objects as go

# Load the dataset
file_path = "../../datasets/percentage_share_of_titles_per_country.csv" 
df = pd.read_csv(file_path)

# # Sort by percentage share in descending order
# df = df.sort_values(by="percentage_share", ascending=False)

# # Separate the top 6 countries
# top_countries = df[:6]

# # Calculate "Others"
# num_others = len(df) - 6  # Total number of countries in "Others"
# others = pd.DataFrame({
#     "country": [f"Others ({num_others} countries)"],
#     "title_count": [df["title_count"][6:].sum()],
#     "percentage_share": [df["percentage_share"][6:].sum()]
# })

# # Combine top countries and "Others"
# combined_df = pd.concat([top_countries, others])

# # Define Netflix-themed colors (red and darker tones)
# netflix_colors = ["#E50914", "#B81D24", "#900C3F", "#FF5733", "#C70039", "#7E0E14", "#404040"]

# # Set the dark background style
# plt.style.use("dark_background")

# # Plot: Netflix-Themed Pie Chart
# plt.figure(figsize=(10, 8))
# wedges, texts, autotexts = plt.pie(
#     combined_df["percentage_share"], 
#     labels=combined_df["country"], 
#     autopct="%.2f%%", 
#     startangle=140,
#     colors=netflix_colors,       # Apply Netflix-themed colors
#     textprops={'fontsize': 10, 'color': "white"},  # White text for contrast
#     wedgeprops={'edgecolor': "black", 'linewidth': 1}  # Add black edges for clarity
# )

# # Customize percentage text to be bold
# for autotext in autotexts:
#     autotext.set_color("white")
#     autotext.set_fontweight("bold")

# # Title with white text
# plt.title("Percentage Contribution of Top 6 Countries and Others", fontsize=14, color="white", weight="bold")

# # Save the Netflix-themed pie chart
# plt.savefig("countries_pie_chart.png", dpi=300, bbox_inches="tight")
# plt.close()


# Function to convert ISO-2 to ISO-3
def iso2_to_iso3(iso2_code):
    try:
        return pycountry.countries.get(alpha_2=iso2_code.upper()).alpha_3
    except AttributeError:
        return None  # Return None for invalid codes

# Convert country column to ISO-3 codes
df['ISO-3'] = df['country'].apply(iso2_to_iso3)

# Drop rows where conversion failed (e.g., invalid country codes)
df = df.dropna(subset=['ISO-3'])

# Rename columns for clarity
df = df.rename(columns={"percentage_share": "PercentageShare"})


df['LogPercentageShare'] = np.log1p(df['PercentageShare'])  # log(1 + x) to handle 0 values gracefully

# Create the Choropleth Map
choropleth = go.Choropleth(
    locations=df['ISO-3'],
    z=df['LogPercentageShare'],
    text=df['country'],
    hoverinfo="location+z+text", 
    colorscale="Reds",
    marker_line_color="white"
)

# Add scattergeo for labels with black text and smaller font size
scattergeo = go.Scattergeo(
    locations=df['ISO-3'],
    text=df['country'] + "<br>" + df['PercentageShare'].round(2).astype(str) + "%", 
    mode="text",
    textfont=dict(size=7, color="black"), 
)

# Combine both traces
fig = go.Figure(data=[choropleth, scattergeo])

# Update layout
fig.update_layout(
    geo=dict(
        projection_type="natural earth",
        bgcolor="black",
        showland=True,
        landcolor="black",
        showcountries=True,
        countrycolor="white",
    ),
    title="Netflix-Themed Choropleth Map with Smaller Labels",
    title_font=dict(size=20, color="white"),
    paper_bgcolor="black",
)

# Save the interactive map as HTML
fig.write_html("netflix_log_percentage_share_map.html")

# Save the map as PNG
fig.write_image("netflix_log_percentage_share_map", format="png", scale=2)

# Show the map
fig.show()