import re
import difflib

import ollama  

# You need to replace this with your local Ollama setup if needed
OLLAMA_API_URL = 'http://localhost:11434/v1/ollama'  # Replace with the correct URL for Ollama local setup

# Define the job description as a string (this will be dynamic in real-world use)
job_description = """
Machine Learning Engineer
At Company ABC, we are solving cutting-edge problems in the field of AI and ML. You will work with talented engineers to build innovative systems.

Responsibilities:
- Develop machine learning models for predictive analysis
- Collaborate with cross-functional teams for system integration

Required Qualifications:
- Bachelor’s degree in Computer Science, AI, or related field
- 1-3 years of experience in Machine Learning
- Proficient in Python, TensorFlow, and Scikit-learn

Technologies / Tools: TensorFlow, PyTorch, SQL
Experience Level: Junior
"""

# Define function to extract job details using regex (fallback)
def extract_jd_details(jd_text):
    # Patterns to capture the fields
    patterns = {
        "Name": r"^(.*?Engineer|.*?Developer|.*?Scientist|.*?Specialist)",  # Capture job title (e.g., "Machine Learning Engineer")
        "Years of Experience": r"(\d+-\d+ years|\d+ years|Not Available)",  # Experience format
        "Key Skills": r"Skills: (.*)",  # Capture skills
        "Technologies / Tools": r"Technologies? / Tools?: (.*)",  # Capture technologies
        "Estimated Experience Level": r"(Junior|Mid|Senior|Not Available)"  # Capture experience level
    }

    # Extract data using regex
    job_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, jd_text, re.IGNORECASE)
        if match:
            job_data[field] = match.group(1).strip()
        else:
            job_data[field] = "Not Available"  # Fallback value if not found

    return job_data

# Define function to send to Ollama model for structured extraction
def extract_using_llm(jd_text):
    # Define the prompt for the LLM to extract job details
    prompt = f"""
    Extract the following details from the job description below:

    Name: [Job Role or "Not Available"]
    Years of Experience: [Years or "Not Available"]
    Key Skills: [Skill list or "Not Available"]
    Technologies / Tools: [List or "Not Available"]
    Estimated Experience Level: [Junior/Mid/Senior or "Not Available"]

    Job Description:
    {jd_text}
    """

    # Send the prompt to the LLM model using Ollama's correct method (try the appropriate call)
    response = ollama.invoke(model="phi-2", input=prompt)

    # Process the response to extract structured information
    return response.strip()


# Main logic to extract the job description details
def main(jd_text):
    print("Using LLM for extraction...")
    job_data_llm = extract_using_llm(jd_text)
    print("Extracted job details using LLM:\n", job_data_llm)

# Run the script
if __name__ == "__main__":
    main(job_description)
