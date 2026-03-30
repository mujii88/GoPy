from dotenv import load_dotenv
import os 
import httpx
import asyncio 
import httplib2
import google_auth_httplib2 # The missing bridge
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import urllib.request
import json
import re
import html


dotenv_path = os.path.join(base_dir, "..", ".env")

load_dotenv(dotenv_path)
news_api=os.getenv("NEWS_API_KEY")

async def fetch_news(query="AI"):
    print("📡 TOOL FIRED: Fetching Latest News...")
    url = f"https://newsdata.io/api/1/latest?apikey={news_api}&q={query}"
    
    # trust_env=False is the magic wand here. 
    # It tells httpx to IGNORE the Tor proxy and just use normal internet!
    async with httpx.AsyncClient(trust_env=False) as client:
        try:
            response = await client.get(url)
            print(f"📡 News API Status Code: {response.status_code}") 
            response.raise_for_status()
            data = response.json()
            
            results = data.get('results', [])
            print(f"📡 Found {len(results)} news articles!")
            return results
            
        except Exception as e:
            print(f"❌ News Tool Crashed: {str(e)}")
            return {"error": f"Unexpected error: {str(e)}"}
def format_leetcode_content(raw_html):
    if not raw_html:
        return ""
    
    # 1. Destroy hidden tabs and carriage returns
    text = raw_html.replace('\t', '').replace('\r', '')
    
    # --- THE FIX: Rescue Math Tags Before Nuking HTML ---
    text = re.sub(r'<sup>(.*?)</sup>', r'^\1', text)  # Turns 10<sup>5</sup> into 10^5
    text = re.sub(r'<sub>(.*?)</sub>', r'_\1', text)  # Turns nums<sub>i</sub> into nums_i
    # ----------------------------------------------------
    
    # 2. Targeted Emoji Replacements
    text = re.sub(r'<strong[^>]*>Example (\d+):?</strong>', r'\n\n💡 Example \1:', text)
    text = re.sub(r'<strong>Input:?</strong>', r'\n🔸 Input:', text)
    text = re.sub(r'<strong>Output:?</strong>', r'\n🔹 Output:', text)
    text = re.sub(r'<strong>Explanation:?</strong>', r'\nExplanation:', text)
    text = re.sub(r'<strong[^>]*>Constraints:?</strong>', r'\n\n⚙️ Constraints:', text)
    text = re.sub(r'\n*<li>', r'\n  ▪️ ', text)
    
    # 3. Strip all remaining HTML tags FIRST (The Nuke)
    text = re.sub(r'<[^>]+>', '', text)
    
    # 4. Translate HTML codes (&lt; to <) AFTER the tags are gone!
    text = html.unescape(text)
    
    # 5. The Final Vacuum (Whitespace Cleanup)
    text = re.sub(r'^[ \t]+$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()

async def daily_leetcode():
    
    query = """
    query questionOfToday {
      activeDailyCodingChallengeQuestion {
        date
        question {
          questionFrontendId
          title
          difficulty
          content
        }
      }
    }
    """

    url = "https://leetcode.com/graphql"


    async with httpx.AsyncClient() as client:
        try:
            print("Getting the data for your daily leetcode dose.....")
            res = await client.post(url, json={"query": query})
            print(f"Status Code={res.status_code}")
            response=res.json()
            q_data = response['data']['activeDailyCodingChallengeQuestion']['question']
            
            title = q_data['questionFrontendId'] + ". " + q_data['title']
            difficulty = q_data['difficulty']
            clean_content = format_leetcode_content(q_data['content'])

            return {
                "title": title,
                "difficulty": difficulty,
                "content": clean_content
            }


        except Exception as e:
            print(f"❌ Leetcode Tool Crashed: {str(e)}")
            return {"error": f"Unexpected error: {str(e)}"}















if __name__ == "__main__":
    data=asyncio.run(fetch_daily_leetcode())

# async def fetch_gmail_unread():
#     token_path='token.json'

#     if not os.path.exists(token_path):
#         return {
#             "error":"token not found first run the auth_gmail.py to generate the token"
#         }

#     try:
#         creds=Credentials.from_authorized_user_file(token_path)
#         custom_http=httplib2.Http(timeout=45)


#         authorized_http=google_auth_httplib2.AuthorizedHttp(creds,http=custom_http)
#         service=build('gmail','v1',http=authorized_http)
#         print("Connection Secured now GoPy is fetching your emails....")
#         result=service.users().messages().list(
#             userId='me',
#             q='is:unread',
#             maxResults=10
#         ).execute()

#         messages=result.get('messages',[])
#         email_briefs=[]

#         for msg in messages:
#             m = service.users().messages().get(userId='me', id=msg['id']).execute()
#             headers = m.get('payload', {}).get('headers', [])
#             subject = next((h['value'] for h in headers if h['name'] == 'Subject'), "No Subject")
#             sender = next((h['value'] for h in headers if h['name'] == 'From'), "Unknown")
            
#             email_briefs.append({
#                 "subject": subject,
#                 "sender": sender,
#                 "snippet": m.get('snippet', '')
#             })
            
       
#         return email_briefs

#     except Exception as e:
#         print(f"❌ Handshake failed: {e}")
#         return {"error": f"Gmail request failed: {str(e)}"}


# if __name__=="__main__":
#     data=asyncio.run(fetch_gmail_unread())
#     print(data)
