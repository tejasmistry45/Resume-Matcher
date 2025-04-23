import os
from langchain_together import Together
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import json

load_dotenv()

# Initialize the Together AI LLM
llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    # model="meta-llama/Llama-2-70b-hf",
    # model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    # model= "mistralai/Mistral-7B-Instruct-v0.1",
    temperature=0.7,
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