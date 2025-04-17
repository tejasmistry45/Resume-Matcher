# This file is extra and not use in this project
# This script matches resumes to a job description using precomputed embeddings and FAISS for efficient similarity search.

import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Load data and precomputed files
df = pd.read_csv('./data/Final_Resume.csv')
resume_texts = df['resume_text'].tolist()
resume_ids = df['resume_id'].tolist()

embeddings = np.load('./embeddings/resume_embeddings.npy')
index = faiss.read_index('./embeddings/faiss_index.index')

# Load model
model = SentenceTransformer('all-mpnet-base-v2')

# Get job description input
job_description = input("Enter job description:\n")
job_embedding = model.encode([job_description], convert_to_numpy=True)

# Search for top N similar resumes
k = 10  
distances, indices = index.search(job_embedding, k)

# Print top matches
print("\nTop Matching Resumes:\n")
for i, idx in enumerate(indices[0]):
    print(f"{i+1}. Resume ID: {resume_ids[idx]}")
    print(f"   Text: {resume_texts[idx][:200]}...")
    print(f"   Similarity Score: {1 - distances[0][i]:.4f}")
    print("-" * 50)
