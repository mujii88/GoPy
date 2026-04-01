
Markdown
<div align="center">

# 🎧 Bulletproof Termux Music Bot
**A high-performance Telegram YouTube Downloader engineered for Android.**

![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Termux](https://img.shields.io/badge/Termux-000000?style=for-the-badge&logo=termux&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)

*Bypass Azure/AWS IP bans by turning your spare Android phone into an unblockable, residential media server.*

</div>

---

## 🛑 The Problem: Cloud IP Bans & Mobile Timeouts
Hosting YouTube downloaders on cloud providers (Azure, AWS, DigitalOcean) is a nightmare. YouTube actively flags and blocks Datacenter IPs, instantly breaking your bots. 

If you try to move standard `yt-dlp` scripts to a mobile device (Termux), they usually crash due to spotty cell service, 60-second timeouts, and memory leaks.

## ⚡ The Solution: Mobile-First Architecture
This project is a custom Go/Python hybrid gateway specifically designed to run on **Termux**. By using your phone's Residential/Mobile IP, the bot becomes invisible to YouTube's security blocks, while the aggressive network armor prevents mobile connection drops.

### ✨ Core Features
* 🛡️ **Zero Mobile Timeouts:** Hardcoded 180-second timeouts with 15-retry chunk network armor.
* 🎵 **True V0 MP3 Quality:** Forces FFmpeg to extract and encode at the highest Variable Bitrate without the dreaded `file.mp3.mp3` double-extension bug.
* 🧹 **Scorched-Earth Process Management:** Includes a custom `start.sh` script that hunts down and kills zombie Go/Python processes to prevent Termux memory leaks.
* 💸 **Zero Cloud Costs:** Runs 100% locally on your device.

---

## 🛠️ Installation & Setup

<details>
<summary><b>Step 1: Termux Preparation</b> (Click to expand)</summary>

First, ensure your Termux is updated and has access to your phone's internal storage so it can save the music.

```bash
pkg update && pkg upgrade -y
termux-setup-storage
</details>

<details>
<summary><b>Step 2: Install Dependencies</b> (Click to expand)</summary>

Install the required languages and media encoding engines.

Bash
pkg install python ffmpeg golang git -y
pip install yt-dlp
</details>

<details>
<summary><b>Step 3: Clone & Configure</b> (Click to expand)</summary>

Pull this repository and set up your Telegram Bot Token.

Bash
git clone [https://github.com/mujii88/GoPy.git](https://github.com/mujii88/GoPy.git)
cd GoPy

# Create your environment file
echo "BOT_TOKEN=your_telegram_bot_token_here" > .env
(Note: Replace your_telegram_bot_token_here with the token you get from BotFather on Telegram).

</details>

🚀 Running the Bot
Do not run the Go and Python files manually. Use the provided startup script. This script automatically wipes out old ghost sessions, compiles the latest Go binary, and safely starts the system.

Bash
cd ~/GoPy
chmod +x start.sh
./start.sh
📂 Where does the music go?
Downloaded .mp3 files are saved directly to the absolute Termux path (/data/data/com.termux/files/home/GoPy) before being securely transmitted back to you via the Telegram API.

⚠️ Disclaimer
This tool is provided for educational purposes and personal archiving only. Please respect the terms of service of the platforms you interact with and only download content you have the right to access.

<div align="center">
<i>Engineered for stability. Built to bypass the bans.</i>
</div>
