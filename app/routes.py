import time
from flask import Blueprint, render_template, request, jsonify,Response
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from llm_utils import extract_resume_info
import ollama
from llm_utils import extract_resume_info, extract_jd_info
 
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
    jd_fields = {
        "job_title": "",
        "location": "",
        "years_exp": "",
        "skills": "",
        "qualifications": ""
    }
 
    if request.method == 'POST':
        # Capture fields from form
        for field in jd_fields:
            jd_fields[field] = request.form.get(field, "").strip()
 
        # Create a combined string for embedding
        job_text = f"{jd_fields['job_title']} | {jd_fields['location']} | {jd_fields['years_exp']} yrs exp | Skills: {jd_fields['skills']} | Qualifications: {jd_fields['qualifications']}"
 
        # Encode the job description into an embedding
        job_embedding = model.encode([job_text])
 
        # Search for the top 5 matching resumes using FAISS
        D, I = index.search(np.array(job_embedding).astype(np.float32), k=5)
 
        # Get the top matching resumes
        matches = []
        for i, idx in enumerate(I[0]):
            match = {
                "resume_id": resume_ids[idx],
                "score": D[0][i],
                # "name": df.iloc[idx]["name"],  # Assuming your CSV has a 'name' column for the resume
            }
            matches.append(match)
        # Sort matches by score in descending order (highest score first)
        matches.sort(key=lambda x: x['score'], reverse=True)
 
    return render_template("index.html", matches=matches, jd_fields=jd_fields)
 
 
 
@bp.route('/insights/<resume_id>', methods=['GET'])
def get_resume_insights(resume_id):
    try:
        # Ensure both resume_id and list items are strings
        resume_id_str = str(resume_id)
        resume_ids_str = [str(rid) for rid in resume_ids]
 
        if resume_id_str not in resume_ids_str:
            return "Resume ID not found.", 404
 
        resume_index = resume_ids_str.index(resume_id_str)
        resume_text = resume_texts[resume_index]
       
        start_time = time.time()
        llm_response = extract_resume_info(resume_text)
        end_time = time.time()
        print(f"LLM Response completed in {end_time - start_time:.2f} seconds.")
 
        return llm_response.strip(), 200, {'Content-Type': 'text/plain'}
 
    except Exception as e:
        import traceback
        return f"Failed to extract insights: {str(e)}", 500
 
 
@bp.route('/clean-jd', methods=['POST'])
def extract_fields_from_jd():
    data = request.get_json()  # Get the JSON payload
    job_description = data.get('job_description', '').strip()  # Extract job description
 
    if not job_description:
        return Response('Error: Job description is missing.', status=400, mimetype='text/plain')
 
    try:
        start_time = time.time()
        content = extract_jd_info(job_description)
        end_time = time.time()
 
        print(f"JD Extraction completed in {end_time - start_time:.2f} seconds.")
 
        if not content:
            return Response('Error: Failed to extract information.', status=500, mimetype='text/plain')
 
        return jsonify({"cleaned_sections": content})  # Return the content as JSON
 
    except Exception as e:
        return Response(f'Error: {str(e)}', status=500, mimetype='text/plain')