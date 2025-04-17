import os
from langchain_together import Together
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import json

load_dotenv()

# Initialize the Together AI LLM
llm = Together(
    model="mistralai/Mistral-7B-Instruct-v0.1",
    # model="deepseek-ai/DeepSeek-R1",
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

def extract_resume_info(resume_text):
    # Format the resume text to fit in the prompt
    final_prompt = prompt.format(resume_text=resume_text[:1500])
    
    # Get the response from the LLM
    raw_response = llm.invoke(final_prompt)
    
    # Try to parse the raw response into a structured format
    try:
        # If the response is in JSON format, try to parse it
        response = json.loads(raw_response)
    except json.JSONDecodeError:
        # If the response is not JSON, handle it as a raw string
        response = raw_response

    # If response is a string, we parse the response to extract details
    if isinstance(response, str):
        formatted_response = response
    else:
        # Extract and format response based on structured fields (if JSON)
        formatted_response = f"""
        Name: {response.get('Person Name', 'Not Available')},
        Years of Experience: {response.get('Years of Experience', 'Not Available')},
        Key Skills: {response.get('Key Skills', 'Not Available')},
        Technologies / Tools: {response.get('Technologies / Tools', 'Not Available')},
        Estimated Experience Level: {response.get('Estimated Experience Level', 'Not Available')}
        """

    return formatted_response