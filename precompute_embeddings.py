# this script precomputes the embeddings for resumes and saves them to a FAISS index.

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os

# Load data
df = pd.read_csv('./data/Final_Resume.csv')
resumes = df['resume_text'].tolist()

# Load SBERT model
model = SentenceTransformer('all-mpnet-base-v2')

# Encode all resumes into embeddings
print("Encoding resumes...")

if "resume_embeddings.npy" in os.listdir('./embeddings'):
    print("Embeddings already exist. Loading...")
    embeddings = np.load('./embeddings/resume_embeddings.npy')
else:
    print("Creating new embeddings...")
    embeddings = model.encode(resumes, convert_to_numpy=True, show_progress_bar=True)

# Save embeddings
os.makedirs('./embeddings', exist_ok=True)
np.save('./embeddings/resume_embeddings.npy', embeddings)

# Create and save FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, './embeddings/faiss_index.index')
print("FAISS index saved.")
