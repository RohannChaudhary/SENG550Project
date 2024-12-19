import pandas as pd
import plotly.graph_objects as go
import pycountry

# =============================
# Step 1: Load the Dataset
# =============================

# Define the file path
file_path = "../../datasets/country_ratings_avg.csv"  # Update this path as needed

# Load the dataset
df = pd.read_csv(file_path)

# =============================
# Step 2: Clean and Prepare Data
# =============================

# Rename columns for clarity
df = df.rename(columns={"country": "Country", "overall_average_rating": "Rating"})

# Function to convert ISO-2 country codes to ISO-3 codes
def iso2_to_iso3(iso2_code):
    try:
        return pycountry.countries.get(alpha_2=iso2_code.upper()).alpha_3
    except AttributeError:
        return None

# Add ISO-3 country codes
df['ISO-3'] = df['Country'].apply(iso2_to_iso3)

# Drop rows with invalid country codes or missing ratings
df = df.dropna(subset=['ISO-3', 'Rating'])

# =============================
# Step 3: Create the Choropleth Map
# =============================

# Choropleth trace
choropleth = go.Choropleth(
    locations=df['ISO-3'],                 # ISO-3 country codes
    z=df['Rating'],                        # Ratings column
    hovertemplate=(                        # Hover tooltip
        "<b>%{text}</b><br>"
        "Average Rating: %{z:.1f}<br>"     # Display rating with one decimal place
    ),
    colorscale="Reds",                     # Netflix-themed color scheme
    marker_line_color="white",             # White borders between countries
    colorbar_title="Average Rating",
    colorbar_tickformat=".1f"              # Format colorbar ticks to one decimal place
)

# =============================
# Step 4: Customize the Layout
# =============================

# Create the figure with only the Choropleth trace
fig = go.Figure(data=[choropleth])

# Update layout
fig.update_layout(
    geo=dict(
        projection_type="natural earth",   # Natural Earth projection
        bgcolor="black",                   # Black background for the map
        showland=True,                     # Highlight land areas
        landcolor="black",                 # Black land color for Netflix theme
        showcountries=True,                # Show country borders
        countrycolor="white",              # White country borders
    ),
    title=dict(
        text="Global Average Ratings by Country",
        font=dict(size=20, color="white"),
        x=0.5  # Center the title
    ),
    paper_bgcolor="black",                 # Black background for the figure
    margin=dict(l=10, r=10, t=50, b=10)    # Adjust margins for better visuals
)


# =============================
# Step 5: Save and Show the Map
# =============================

# Save the map as an interactive HTML file
fig.write_html("country_ratings_avg_with_ratings_labels.html")

# Save the map as a static image
fig.write_image("country_ratings_avg_with_ratings_labels.png", format="png", scale=2)

# Show the interactive map
fig.show()
