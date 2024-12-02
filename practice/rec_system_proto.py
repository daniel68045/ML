import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Define a dummy dataset that acts as the Last.fm API
data = pd.DataFrame({
    "Artist": ["Radiohead", "Coldplay", "Nirvana"],
    "Tags": ["rock alternative experimental", "pop alternative soft", "grunge rock 90s"]
})

# Vectorize Tags
vectorizer = TfidfVectorizer()
tag_vectors = vectorizer.fit_transform(data["Tags"])

# Calculate Similarity
similarity_matrix = cosine_similarity(tag_vectors)

# Convert similarity matrix to a DataFrame for better readability
similarity_df = pd.DataFrame(similarity_matrix, index=data["Artist"], columns=data["Artist"])


# Function that actually recommends
def recommend_similar_music(artist_name, top_n=1):
    if artist_name not in similarity_df.index:
        print(f"Artist '{artist_name}' not found in the dataset.")
        return []

    # Sort similar artists by similarity score, exclude the artist itself
    similar_artists = similarity_df.loc[artist_name].sort_values(ascending=False)[1:top_n + 1]
    return similar_artists


# Example usage
print("Similarity Matrix:")
print(similarity_df)

artist = "Radiohead"
recommendations = recommend_similar_music(artist, top_n=2)
print(f"\nArtists similar to '{artist}':")
print(recommendations)

