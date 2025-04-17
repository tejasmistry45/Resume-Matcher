import time
from flask import Blueprint, render_template, request
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

bp = Blueprint('main', __name__)

# Load model and data
model = SentenceTransformer('all-mpnet-base-v2')
df = pd.read_csv('./data/Final_Resume.csv')
resume_texts = df['resume_text'].tolist()
resume_ids = df['resume_id'].tolist()
embeddings = np.load('./embeddings/resume_embeddings.npy')
index = faiss.read_index('./embeddings/faiss_index.index')

@bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        start_time = time.time()
        job_description = request.form['job_description']
        job_embedding = model.encode([job_description], convert_to_numpy=True)
        distances, indices = index.search(job_embedding, 5)

        matches = []
        for i, idx in enumerate(indices[0]):
            matches.append({
                'rank': i + 1,
                'resume_id': resume_ids[idx],
                'text': resume_texts[idx][:500] + "...",
                'score': round(1 - distances[0][i], 4)
            })
        end_time= time.time()
        print(f"Search completed in {end_time - start_time:.2f} seconds.")
        return render_template('results.html', matches=matches)

    return render_template('index.html')
