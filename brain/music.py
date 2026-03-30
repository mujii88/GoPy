import yt_dlp
import asyncio
import os

async def download_song(song_name: str) -> str:
    print(f"🎵 TOOL FIRED: Hunting for '{song_name}' on YouTube...")
    
    # 1. Sanitize the name! Remove weird characters like / or \ that break Linux file systems
    safe_name = "".join(c for c in song_name if c.isalnum() or c in " -_").strip()
    if not safe_name:
        safe_name = "downloaded_song" # Failsafe just in case
    
    ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192', 
            }],
            'outtmpl': f'brain/{safe_name}.%(ext)s', 
            'restrictfilenames': False, 
            'noplaylist': True,        
            'quiet': True,             
            'no_warnings': True,       
            
            # --- THE NEW ARMOR: ANTI-THROTTLING & NETWORK FIXES ---
            'retries': 15,          # If the connection drops, try again up to 15 times
            'fragment_retries': 15, # If a specific chunk of the song fails, retry just that chunk
            'socket_timeout': 30,   # Wait up to 30 seconds for YouTube to respond before calling it a timeout
            'http_headers': {       # Disguise the bot as a normal Windows/Chrome user
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        }

    def _download():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # We don't need to extract the ID anymore! 
            # yt-dlp will automatically name it whatever we put in outtmpl.
            ydl.extract_info(f"ytsearch1:{song_name}", download=True)

    try:
        # Run the download
        await asyncio.to_thread(_download)
        
        # 3. Construct the exact path we know it saved to
        final_file = f"/home/one/GoPy/brain/{safe_name}.mp3"
        
        if os.path.exists(final_file):
            print(f"✅ Download Complete! Saved at: {final_file}")
            return final_file
        else:
            print("❌ File downloaded, but could not be found on disk.")
            return ""
            
    except Exception as e:
        print(f"❌ yt-dlp Crashed: {str(e)}")
        return ""

# Test block - run this file directly to test!
if __name__ == "__main__":
    result = asyncio.run(download_song("Diljit Dealer song"))
