import os
import json

from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel
from pypdf import PdfReader
from docx import Document

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables")

client = Groq(api_key=my_api_key)

model = "openai/gpt-oss-20b"


def extract_text(file_path):

    if file_path.lower().endswith(".pdf"):
        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    elif file_path.lower().endswith(".docx"):
        document = Document(file_path)

        return "\n".join(paragraph.text for paragraph in document.paragraphs)

    else:
        raise ValueError("Only PDF and DOCX files are supported.")


resume_path = input("Enter resume path: ").strip()

print("Enter HR requirements. Type END when finished:")

hr_lines = []

while True:
    line = input()

    if line.strip() == "END":
        break

    hr_lines.append(line)

hr_requirements = "\n".join(hr_lines)

resume_text = extract_text(resume_path)

print("\nResume extracted successfully.")


class ResumeAnalysis(BaseModel):
    skills_found: list[str]

    experience_found: list[str]

    projects_found: list[str]

    matched_requirements: list[str]

    missing_requirements: list[str]

    match_percentage: float


schema = ResumeAnalysis.model_json_schema()

system_prompt = f"""
You are an HR resume screening assistant.

Analyze the candidate's resume against the HR requirements.

Extract from the resume:

1. Skills
2. Experience
3. Projects

Then compare them with the HR requirements.

Identify:

- matched requirements
- missing requirements
- overall match percentage

Return the result according to this JSON schema:

{schema}
"""

user_prompt = f"""
HR REQUIREMENTS:

{hr_requirements}


CANDIDATE RESUME:

{resume_text}
"""

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt},
]

response = client.chat.completions.create(
    model=model, messages=messages, response_format={"type": "json_object"}
)

answer = response.choices[0].message.content

print("\nRAW RESPONSE:")
print(answer)

data_file = json.loads(answer)
analysis = ResumeAnalysis(**data_file)


print("\n========== RESUME ANALYSIS ==========")

print("\nSkills found:")
for skill in analysis.skills_found:
    print("-", skill)

print("\nExperience found:")
for experience in analysis.experience_found:
    print("-", experience)

print("\nProjects found:")
for project in analysis.projects_found:
    print("-", project)

print("\nMatched requirements:")
for requirement in analysis.matched_requirements:
    print("-", requirement)

print("\nMissing requirements:")
for requirement in analysis.missing_requirements:
    print("-", requirement)

print(f"\nMatch percentage: {analysis.match_percentage}%")

print("\n====================================")
