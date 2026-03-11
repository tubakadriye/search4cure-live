import json
from vertexai.generative_models import GenerativeModel
import re

model = GenerativeModel("gemini-1.5-flash")

def extract_entities_with_llm(text):

    prompt = f"""
You are extracting entities from a biomedical research paper.

Return ONLY JSON. No explanations.

Schema:

{{
"authors": [],
"methods": [],
"datasets": [],
"diseases": [],
"biomarkers": [],
"drugs": [],
"genes": [],
"outcomes": []
}}

Rules:
- methods = ML models, algorithms, statistical methods
- datasets = dataset names
- diseases = diseases studied
- biomarkers = lab measurements
- drugs = medications
- genes = gene symbols like TCF7L2, PPARG
- outcomes = clinical outcomes (mortality, glucose control, progression)
- Return unique entities
- Use canonical names
- Avoid duplicates
- Do not hallucinate entities


Text:
{text[:12000]}
"""

    response = model.generate_content(prompt)

    raw = response.text.strip()

    # remove markdown formatting
    raw = re.sub(r"```json|```", "", raw)

    try:
        for _ in range(3):
            try:
                return json.loads(raw)
            except:
                continue

    except Exception:

        print("LLM returned invalid JSON. Attempting repair.")

        try:
            fixed = raw[raw.index("{"):raw.rindex("}")+1]
            return json.loads(fixed)
        except:
            return {
                "authors": [],
                "methods": [],
                "datasets": [],
                "diseases": [],
                "biomarkers": [],
                "drugs": [],
                "genes": [],
                "outcomes": []
            }
