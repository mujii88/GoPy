import asyncio
import os
import json

async def download_song(song_name: str) -> str:
    print(f"🎵 TOOL FIRED: Hunting for '{song_name}'")

    # 1. Clean the filename (Replacing spaces with underscores is safer for CLI)
    safe_name = "".join(c for c in song_name if c.isalnum() or c in " _-").strip().replace(" ", "_")
    if not safe_name:
        safe_name = "download"

    # 2. Hardcode the absolute Termux path
    base_dir = "/data/data/com.termux/files/home/GoPy"
    
    # FIX: Use %(ext)s in the template so yt-dlp correctly handles the format swap
    # This prevents the dreaded "file.mp3.mp3" bug!
    output_template = f"{base_dir}/{safe_name}.%(ext)s"
    final_file_path = f"{base_dir}/{safe_name}.mp3"

    # 3. Build the exact terminal command with added armor
    command = [
        "yt-dlp",
        "ytsearch1:" + song_name,
        "-x",                                # Extract audio
        "--audio-format", "mp3",             # Convert to mp3 using FFmpeg
        "--audio-quality", "0",              # Gives you the absolute best audio quality
        "-o", output_template,               # Save with our exact template
        "--retries", "15",                   # Retry if network drops
        "--fragment-retries", "15",          # Retry broken chunks
        "--no-playlist",                     # Ensure we only get one song
        "--quiet", "--no-warnings"           # Keep the Termux shell clean
    ]

    try:
        print(f"🚀 Running command: {' '.join(command)}")
        
        # 4. Run it directly in the Termux shell
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # FIX: Bumped timeout to 180 seconds. FFmpeg needs time to convert on mobile!
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=180)

        # 5. Check if the file is actually on the disk
        if os.path.exists(final_file_path):
            print(f"✅ Success! Saved to {final_file_path}")
            return json.dumps({"status": "success", "file": final_file_path})
        else:
            # FIX: Safely decode stderr so weird characters don't crash your script
            error_msg = stderr.decode('utf-8', errors='ignore').strip()
            print(f"❌ yt-dlp failed or file not found. Error: {error_msg}")
            return json.dumps({"status": "error", "message": f"File not found. Log: {error_msg}"})

    except asyncio.TimeoutError:
        print("❌ Command timed out after 180 seconds!")
        try:
            # FIX: Safely kill the process to prevent zombie Termux tasks
            process.kill()
        except ProcessLookupError:
            pass 
        return json.dumps({"status": "error", "message": "Download timed out"})
        
    except Exception as e:
        print(f"❌ System error: {e}")
        return json.dumps({"status": "error", "message": str(e)})

# Test block - run this file directly in Termux to test!
if __name__ == "__main__":
    # Creates the directory if it doesn't exist yet for testing purposes
    os.makedirs("/data/data/com.termux/files/home/GoPy", exist_ok=True)
    result = asyncio.run(download_song("Diljit Dealer song"))
    print(result)
