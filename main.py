from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Request Model
class UserPrompt(BaseModel):
    message: str


# System Prompt
SYSTEM_PROMPT = """
You are CareerGuide AI, an intelligent and friendly career guidance assistant.

Your role is to help students and job seekers make informed career decisions.

Responsibilities:
- Suggest career paths based on interests and skills.
- Recommend courses and certifications.
- Explain job roles and future opportunities.
- Provide resume and interview tips.
- Help with higher studies and internships.

Always provide:
1. Career Recommendation
2. Why It Fits
3. Skills Required
4. Learning Resources
5. Future Opportunities
6. Next Steps

Keep responses professional, supportive, and easy to understand.
"""


# Home Route
@app.get("/")
def home():
    return {"message": "Career Guidance AI API is Running!"}


# Chat Route
@app.post("/chat")
def chat(user_input: UserPrompt):

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_input.message
            }
        ],
        temperature=0.7,
        max_tokens=1024
    )

    answer = response.choices[0].message.content

    return {
        "response": answer
    }


# Run Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )