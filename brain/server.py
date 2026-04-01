from fastapi import FastAPI
from music import download_song
import os


# Force Python to use the Tor tunnel for all external web requests


app=FastAPI()



@app.get('/music')
async def get_music(song: str = "jhalla wallah"):
    try:
        # Trigger the tool directly (No agent needed!)
        file_path = await download_song(song)
        
        if file_path and file_path != "":
            return {
                "status": "success", 
                "file": file_path
            }
        else:
            return {
                "status": "error", 
                "message": "Failed to locate the song on disk."
            }
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="0.0.0.0",port=8000)
