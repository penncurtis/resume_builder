import os, json, re
from typing import Dict, Tuple, Any
from openai import OpenAI

JSON_TAG_OPEN  = "<RESUME_DATA_JSON>"
JSON_TAG_CLOSE = "</RESUME_DATA_JSON>"

SYSTEM_PROMPT = f"""
You are a resume-building assistant. Extract information from user messages and update the resume data.

RESPONSE FORMAT:
1) Acknowledge what you've added/updated
2) A JSON object between {JSON_TAG_OPEN} and {JSON_TAG_CLOSE} with only the fields that changed

SIMPLE RULES:
- Extract ALL information from each message
- Don't ask for information already provided
- If user gives experience, don't ask for it again
- If user gives contact info, don't ask for it again
- If user gives name/title, don't ask for it again
- Create summaries from provided information
- Only ask for what's actually missing
- Be proactive and drive the conversation forward
- Don't wait for user to ask "what next?" - suggest next steps

Schema:
{{
  "name": str,
  "title": str,
  "contact": {{
    "email": str, "phone": str, "location": str, "linkedin": str, "github": str
  }},
  "summary": str,
  "experience": [
    {{
      "title": str,
      "company": str,
      "location": str,
      "start_date": str,
      "end_date": str,
      "bullets": [str, ...],
      "technologies": [str, ...]
    }}
  ],
  "education": [
    {{
      "school": str, "degree": str, "location": str,
      "start_date": str, "end_date": str, "details": [str, ...]
    }}
  ],
  "skills": {{
    "design": [str, ...],
    "frontend": [str, ...],
    "backend": [str, ...],
    "data_ai": [str, ...],
    "tools": [str, ...],
    "other": [str, ...]
  }}
}}

Guidelines:
- Extract ALL information from user messages
- When user gives experience details, extract title, company, dates, bullets, and technologies
- When user gives contact info, extract email, phone, LinkedIn, GitHub, location
- Convert raw text into crisp bullets; prefer action > metric > outcome
- Keep resume bullets short (<= 1 line each)
- If information is missing, ask for ONLY the missing pieces
"""

class ChatHandler:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def process_message(self, user_input: str, current_resume_data: Dict) -> Tuple[str, Dict[str, Any]]:
        """Returns (assistant_text, resume_delta)"""
        try:
            # Give AI context about what's already in the resume
            context = f"Current resume data: {json.dumps(current_resume_data, indent=2)}"
            
            msg = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{context}\n\nUser message: {user_input}"},
            ]
            rsp = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=msg,
                temperature=0.5,
                max_tokens=700,
            )
            text = rsp.choices[0].message.content or ""

            # split conversational reply and JSON delta
            delta = {}
            m = re.search(re.escape(JSON_TAG_OPEN) + r"(.*?)" + re.escape(JSON_TAG_CLOSE), text, re.S)
            if m:
                json_str = m.group(1).strip()
                try:
                    delta = json.loads(json_str)
                except Exception:
                    delta = {}
                # remove the JSON block from the assistant text
                text = text.replace(m.group(0), "").strip()

            return text, delta

        except Exception as e:
            return f"Sorry—ran into an error parsing that. Could you rephrase? [{e}]", {}