from pydantic import BaseModel,Field
from typing import List

class NewsItem(BaseModel):
    title: str
    url: str
    time: str
    description:str=Field("A Brief overview of the news")

class EmailItem(BaseModel):
    subject: str
    sender: str
    summary: str # Gopy will summarize the snippet for you

class GopyBriefing(BaseModel):
    category: str
    news_updates: List[NewsItem]
    daily_advice: str # A custom note for Mujii


class LeetCodeBriefing(BaseModel):
    question_title:str
    question_difficulty:str
    question_content:str