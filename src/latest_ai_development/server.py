from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from crew import LatestAiDevelopment  # import your crew class

app = FastAPI()

# Allow Netlify frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in prod use ["https://your-netlify-app.netlify.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    topic: str
    chat_id: str
    bot_user_id: str

@app.post("/crew/message")
async def run(data: InputData):
    inputs = data.dict()

    # Split into visible and hidden
    visible_dict = {k: v for k, v in inputs.items() if k == "topic"}
    hidden_dict = {k: v for k, v in inputs.items() if k != "topic"}

    # Call your Crew
    result = LatestAiDevelopment(hidden_inputs=hidden_dict).crew().kickoff(inputs=visible_dict)

    return {
        "chat_id": data.chat_id,
        "response": str(result),  # make sure it's serializable
        "is_bot": True
    }
