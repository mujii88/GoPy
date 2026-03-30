import os
from dotenv import load_dotenv
from pydantic_ai import Agent, RunContext
from schemas import GopyBriefing,LeetCodeBriefing
from tools import fetch_news
from tools import daily_leetcode


# 1. Load your .env file
dotenv_path = os.path.join(base_dir, "..", ".env")

load_dotenv(dotenv_path)
# 2. Route Pydantic-AI to GitHub's free servers (No Tor proxies!)
os.environ["OPENAI_API_KEY"] = os.getenv('GITHUB_TOKEN')
os.environ["OPENAI_BASE_URL"] = "https://models.inference.ai.azure.com"

# 3. Initialize the Agent using the stable GPT-4o engine
gopy_agent = Agent(
    model='openai:gpt-4o', 
    output_type=GopyBriefing, 
    system_prompt=(
        "You are Gopy, Mujii's Personal AI. Your MANDATORY workflow is: "
        "1. Call 'get_latest_news' to fetch the latest updates on AI, tech, and engineering. "
        "2. Generate the GopyBriefing. Populate the news_updates array and provide daily_advice. "
        "3. Leave the inbox_highlights array strictly empty, as you do not have email access right now. "
        "CONTEXT: Mujii is an EE student at NUST building open-source agentic systems. Curate the news to match his heavy coding and hardware interests."
    )
)

@gopy_agent.tool
async def get_latest_news(ctx: RunContext[None]):
    return await fetch_news()


leetCode_agent=Agent(
    model='openai:gpt-4o',
    output_type=LeetCodeBriefing,
    system_prompt=(
        "You are LeetCode Agent, Mujii's Personal AI. Your MANDATORY workflow is: "
        "1. first get the daily leetcode question using the fetch_daily_leetcode tool "
        "2. then generate the LeetCodeBriefing. "
    )
)

@leetCode_agent.tool
async def fetch_daily_leetcode(ctx: RunContext[None]):
    return await daily_leetcode()
