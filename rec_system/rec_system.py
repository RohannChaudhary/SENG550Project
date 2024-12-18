from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# =============================
# Step 1: Load the Prepared Dataset
# =============================
df = pd.read_csv("rec_system/prepared_dataset.csv")

# =============================
# Step 2: Vectorization
# =============================
# Initialize the CountVectorizer
vectorizer = CountVectorizer(stop_words='english')

# Transform the 'soup' column into a sparse matrix
count_matrix = vectorizer.fit_transform(df['soup'])

# Output the shape of the matrix
print("Count matrix shape:", count_matrix.shape)

# =============================
# Step 3: Compute Cosine Similarity
# =============================
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# Output the shape of the cosine similarity matrix
print("Cosine similarity matrix shape:", cosine_sim.shape)

# =============================
# Step 4: Define Recommendation Function
# =============================
# Create a reverse mapping of indices and titles
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

def get_recommendations(title, cosine_sim):
    try:
        # Get the index of the title that matches the input
        idx = indices[title]

        # Get pairwise similarity scores of all titles with the input title
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort titles based on similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the top 10 most similar titles
        sim_scores = sim_scores[1:11]  # Skip the first one (self-match)

        # Get the indices of the top 10 similar titles
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar titles
        return df['title'].iloc[movie_indices]
    except KeyError:
        return f"Title '{title}' not found in the dataset."

# =============================
# Step 5: Test the Recommendation System
# =============================
test_title = 'Five Feet Apart'  # Replace with an actual title from your dataset
recommendations = get_recommendations(test_title, cosine_sim)

print(f"Recommendations for '{test_title}':")
print(recommendations)
