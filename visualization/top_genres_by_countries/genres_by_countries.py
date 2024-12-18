import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =============================
# Step 1: Load the Data
# =============================

# Path to your CSV file
file_path = "../../datasets/common_top3_genres.csv"  # Update this to correct path
output_image_path = "./top_genres_pie_chart_final.png"  # Path to save the image

# Read the CSV file
df = pd.read_csv(file_path)

# =============================
# Step 2: Prepare Data
# =============================

# Extract Genre and CountryCount
labels = df['Genre']
sizes = df['CountryCount']

# Define Netflix-themed color palette
netflix_colors = [
    "#E50914", "#B81D24", "#7E0E14", "#FF5733", "#C70039", "#900C3F", "#581845", 
    "#D7263D", "#A83333", "#8C1C1C", "#6B0F0F", "#5B0E0E", "#4A0808", "#300404", "#1E0202"
]

# =============================
# Step 3: Create Full Pie Chart with Better Arrows
# =============================

# Create figure and axes
fig, ax = plt.subplots(figsize=(12, 12), facecolor="black")

# Plot the pie chart
wedges, texts = ax.pie(
    sizes,
    labels=None,                       # No labels inside the chart
    colors=netflix_colors[:len(sizes)],  # Netflix color scheme
    startangle=140,                    # Rotate start angle
    wedgeprops=dict(edgecolor="black", linewidth=1.5)  # Add black borders
)

# Add labels outside with better arrows
for i, (p, label) in enumerate(zip(wedges, labels)):
    # Calculate label position
    ang = (p.theta2 - p.theta1) / 2 + p.theta1  # Mid angle of the slice
    x = 1.15 * np.cos(np.radians(ang))
    y = 1.15 * np.sin(np.radians(ang))

    # Label position (slightly farther out)
    ax.annotate(
        f"{label} ({sizes[i]})",      # Label with genre and count
        xy=(x, y),                    # Arrow end point
        xytext=(1.7 * x, 1.7 * y),    # Label position farther out
        arrowprops=dict(
            arrowstyle="wedge,tail_width=0.5", color="white", lw=1.5
        ),  # Better arrows
        ha="center", va="center", fontsize=10, color="white"
    )

# Add title
plt.title(
    "Number of countries that have the Genre in their top 3", 
    fontsize=20, color="white", pad=150
)

# Adjust layout for better spacing
plt.subplots_adjust(top=0.85, left=0.1, right=0.9, bottom=0.1)
plt.tight_layout()

# =============================
# Step 4: Save and Show Chart
# =============================

# Save the pie chart as PNG
plt.savefig(output_image_path, dpi=300, facecolor="black", bbox_inches="tight")
print(f"Pie chart saved as '{output_image_path}'")

# Show the chart
plt.show()
