import time
from flask import Blueprint, render_template, request, jsonify
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from llm_utils import extract_resume_info

bp = Blueprint('main', __name__, template_folder='templates', static_folder='static')

# Load model and data
model = SentenceTransformer('all-mpnet-base-v2')
df = pd.read_csv('./data/Final_Resume.csv')
resume_texts = df['resume_text'].tolist()
resume_ids = df['resume_id'].astype(str).tolist()  # Ensure resume_ids are strings
embeddings = np.load('./embeddings/resume_embeddings.npy')
index = faiss.read_index('./embeddings/faiss_index.index')

@bp.route('/', methods=['GET', 'POST'])
def home():
    matches = []
    job_description = ""

    if request.method == 'POST':
        start_time = time.time()
        job_description = request.form['job_description']
        job_embedding = model.encode([job_description], convert_to_numpy=True)
        distances, indices = index.search(job_embedding, 5)

        for i, idx in enumerate(indices[0]):
            resume_text = resume_texts[idx]
            matches.append({
                'rank': i + 1,  # Sequential rank (1, 2, 3, ...)
                'resume_id': resume_ids[idx],  # String ID
                'score': round(1 - distances[0][i], 4),
            })
        end_time = time.time()
        print(f"Search completed in {end_time - start_time:.2f} seconds.")

    return render_template('index.html', matches=matches, job_description=job_description)

@bp.route('/insights/<resume_id>', methods=['GET'])
def get_resume_insights(resume_id):
    try:
        # print(f"[DEBUG] Received resume_id: {resume_id}")

        # Ensure both resume_id and list items are strings
        resume_id_str = str(resume_id)
        resume_ids_str = [str(rid) for rid in resume_ids]

        if resume_id_str not in resume_ids_str:
            # print(f"[ERROR] Resume ID not found: {resume_id_str}")
            return "Resume ID not found.", 404

        resume_index = resume_ids_str.index(resume_id_str)
        resume_text = resume_texts[resume_index]
        # print(f"[DEBUG] Resume text: {resume_text[:100]}...")  # Log only first 100 chars

        llm_response = extract_resume_info(resume_text)
        # print(f"[DEBUG] LLM response: {llm_response[:100]}...")  # Avoid printing large response

        return llm_response.strip(), 200, {'Content-Type': 'text/plain'}

    except Exception as e:
        import traceback
        # print(f"[ERROR] Unexpected failure:\n{traceback.format_exc()}")
        return f"Failed to extract insights: {str(e)}", 500
