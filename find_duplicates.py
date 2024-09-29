import pandas as pd
from sklearn.cluster import DBSCAN
import numpy as np
from fuzzywuzzy import fuzz
from scipy.spatial.distance import pdist, squareform

# Step 1: Load the CSV file
df = pd.read_csv('names.csv')

# Step 2: Preprocess the names (lowercase, strip spaces)
df['name_cleaned'] = df['name'].str.lower().str.strip()

# Step 3: Define a function to compute string similarity using FuzzyWuzzy
def fuzzy_similarity(x, y):
    return fuzz.partial_ratio(x, y)

# Step 4: Create a similarity matrix (pairwise fuzzy matching)
names = df['name_cleaned'].tolist()
similarity_matrix = np.zeros((len(names), len(names)))

# Compute pairwise similarity between all names
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        similarity = fuzzy_similarity(names[i], names[j])
        # Convert to a distance (1 - similarity/100)
        similarity_matrix[i, j] = 1 - (similarity / 100)
        similarity_matrix[j, i] = similarity_matrix[i, j]

# Step 5: Use DBSCAN with precomputed similarity distance
# eps: Controls how similar names need to be to be clustered (you can adjust this threshold)
dbscan = DBSCAN(eps=0.4, min_samples=2, metric='precomputed')
df['cluster'] = dbscan.fit_predict(similarity_matrix)

# Step 6: For each cluster, determine the most representative common name
# This will be the name from the original data with the highest average similarity to all other names in the cluster
def get_common_name(cluster):
    # Get all names in the current cluster
    cluster_names = df[df['cluster'] == cluster]
    if cluster_names.empty:
        return None
    
    # Original names (from the input file)
    original_names = cluster_names['name'].tolist()

    # Find the name with the highest average similarity to others in the cluster
    best_name = None
    best_similarity_score = -1

    for name in original_names:
        total_similarity = 0
        for other_name in original_names:
            if name != other_name:
                total_similarity += fuzzy_similarity(name, other_name)
        
        # Compute average similarity for this name
        avg_similarity = total_similarity / (len(original_names) - 1) if len(original_names) > 1 else 0
        
        # Choose the name with the highest average similarity
        if avg_similarity > best_similarity_score:
            best_similarity_score = avg_similarity
            best_name = name

    return best_name

# Apply the function to get common names from the original names
df['common_name'] = df['cluster'].apply(get_common_name)

# Step 7: Output the duplicates and their common name
output_df = df[['name', 'common_name']].copy()
output_df.columns = ['Duplicate Name', 'Common Name']

# Save the result to a new CSV
output_df.to_csv('output_names.csv', index=False)

print("Similar company names have been grouped and saved to 'output_names.csv'.")
