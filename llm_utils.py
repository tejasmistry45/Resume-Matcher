import os
from langchain_together import Together
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import json
import ollama


load_dotenv()

# Initialize the Together AI LLM
llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    # model="meta-llama/Llama-2-70b-hf",
    # model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    # model= "mistralai/Mistral-7B-Instruct-v0.1",
    temperature=0,
    max_tokens=512,
    together_api_key=os.getenv("TOGETHER_API_KEY"),
)

# Prompt Template
template = """
You are an expert resume analyzer. Extract and return the following details from the resume text:

1. Person Name (if available)
2. Years of Experience (if mentioned in the resume)
3. Key Skills (comma separated)
4. Technologies / Tools mentioned in the resume (comma separated)
5. Estimated Experience Level (Junior, Mid, or Senior)

Resume:
"{resume_text}"

Please provide the information in a structured format in the following way:

Name: [Name or Not Available]
Years of Experience: [Years or Not Available]
Key Skills: [Skills or Not Available]
Technologies / Tools: [Tools or Not Available]
Estimated Experience Level: [Junior/Mid/Senior or Not Available]
"""

prompt = PromptTemplate(
    input_variables=["resume_text"],
    template=template,
)

# Adjusting the response parsing
def extract_resume_info(resume_text):
    # Format the resume text to fit in the prompt
    final_prompt = prompt.format(resume_text=resume_text[:700])  # limit the input size
    
    # Get the response from the LLM
    raw_response = llm.invoke(final_prompt)
    
    # Try to parse the raw response into a structured format
    try:
        response = json.loads(raw_response)  # if response is valid JSON
        name = response.get("Name", "Not Available")
        years = response.get("Years of Experience", "Not Available")
        skills = response.get("Key Skills", "Not Available")
        tech = response.get("Technologies / Tools", "Not Available")
        level = response.get("Estimated Experience Level", "Not Available")
    except json.JSONDecodeError:
        # Fallback for plain text
        response_lines = raw_response.strip().split("\n")
        data = {}
        for line in response_lines:
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()
        
        name = data.get("Name", "Not Available")
        years = data.get("Years of Experience", "Not Available")
        skills = data.get("Key Skills", "Not Available")
        tech = data.get("Technologies / Tools", "Not Available")
        level = data.get("Estimated Experience Level", "Not Available")

    # Return compact HTML with mt-0 on the first <p> to remove top margin
    formatted_html = f"""<div class="space-y-1">
<p class="mt-0"><strong>Name:</strong> {name}</p><p><strong>Years of Experience:</strong> {years}</p><p><strong>Key Skills:</strong> {skills}</p><p><strong>Technologies / Tools:</strong> {tech}</p><p><strong>Estimated Experience Level:</strong> {level}</p></div>"""

    return formatted_html


def extract_jd_info(job_description):
    prompt = f"""
        You are an intelligent AI assistant. Extract the following fields from the provided Job Description text.
        Respond ONLY in the EXACT format given below. No extra text, explanations, or bullet points.

        Format:
        Job Title: ...
        Location: ...
        Years of Experience: ...
        Estimated Experience Level: ...
        Skills: ...
        Required Qualifications: ...

        Job Description:
        \"\"\"
        {job_description}
        \"\"\"
    """

    response = ollama.chat(
        model="llama2",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.get('message', {}).get('content', '').strip()

    # Now, let's parse the content and split it by the fields
    cleaned_sections = {}

    # Split content by lines and match to sections
    lines = content.split('\n')
    
    # Ensure you handle each expected field
    if len(lines) >= 5:
        cleaned_sections["Job Title"] = lines[0].strip()
        cleaned_sections["Location"] = lines[1].strip()
        cleaned_sections["Years of Experience"] = lines[2].strip()
        cleaned_sections["Estimated Experience Level"] = lines[3].strip()
        cleaned_sections["Skills"] = lines[4].strip()
        
        # Optionally, join all remaining lines as required qualifications if any
        cleaned_sections["Required Qualifications"] = "\n".join(lines[5:]).strip()

    return cleaned_sections




# check if the model is running locally
# import ollama

# # Test if you can communicate with the local Ollama model
# response = ollama.chat(
#     model="llama2",  # Replace with the correct model name if different
#     messages=[{"role": "user", "content": "Hello, how are you?"}]
# )
# print(response)