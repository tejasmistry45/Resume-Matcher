import re
import difflib

SECTION_HEADERS = {
    "Job Title": ["Job Title", "Position", "Role"],
    # "Company Description": ["About Us", "Company Description", "Who We Are"],
    "Job Summary": ["Job Summary", "Overview", "Role Overview", "Job Description"],
    "Responsibilities": ["Responsibilities", "Duties", "What You’ll Do", "Key Responsibilities"],
    "Required Qualifications": ["Requirements", "Qualifications", "Skills Required", "Required Qualifications"],
    "Preferred Qualifications": ["Preferred Qualifications", "Desired Skills", "Nice to Have"],
    "Location": ["Location", "Work Location", "Where You’ll Work"],
    # "Benefits": ["Benefits", "Compensation", "What We Offer"],
    "Education": ["Education", "Educational Requirements", "Academic Background"],
    "Experience": ["Experience", "Work Experience", "Professional Experience"],
    "Skills": ["Skills", "Key Skills", "Technical Skills"]
}

import difflib

def extract_jd_sections(jd_text):
    # Initialize output dictionary with all sections set to empty
    cleaned_sections = {section: "" for section in SECTION_HEADERS}
    sections_found = []  # List to store (section, content) pairs
    
    jd_lines = jd_text.splitlines()
    current_section = None
    current_content = []
    
    for line in jd_lines:
        line = line.strip()
        if not line:
            if current_section is not None:
                current_content.append("")  # Preserve empty lines within sections
            continue
        
        # Check if the line is a potential header
        potential_header = line.split(':')[0].strip() if ':' in line else line
        best_ratio = 0
        best_section = None
        
        # Find the best matching section based on similarity
        for section, variants in SECTION_HEADERS.items():
            for variant in variants:
                ratio = difflib.SequenceMatcher(None, potential_header.lower(), variant.lower()).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_section = section
        
        # If similarity is high enough, treat it as a header
        if best_ratio >= 0.8:
            # Save previous section's content if any
            if current_section is not None:
                sections_found.append((current_section, '\n'.join(current_content).strip()))
            # Start new section
            current_section = best_section
            # If line has a colon, take content after it; otherwise, start empty
            current_content = [line.split(':', 1)[1].strip()] if ':' in line else []
        else:
            # Add line to current section's content if a section is active
            if current_section is not None:
                current_content.append(line)
    
    # Save the last section's content
    if current_section is not None:
        sections_found.append((current_section, '\n'.join(current_content).strip()))
    
    # Populate cleaned_sections, concatenating content for multiple occurrences
    for section, content in sections_found:
        if section in cleaned_sections:
            if cleaned_sections[section]:
                cleaned_sections[section] += "\n" + content
            else:
                cleaned_sections[section] = content
    # print("Extracted sections:", sections_found)
    return cleaned_sections