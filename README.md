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
This project is a custom Go/Python hybrid gateway specifically designed to run natively on **Termux**. By using your phone's Residential/Mobile IP network, the bot becomes invisible to YouTube's security blocks, while the custom network armor prevents mobile connection drops.

### ✨ Core Features
* 🛡️ **Zero Mobile Timeouts:** Hardcoded 180-second timeouts with 15-retry chunk network armor.
* 🎵 **True V0 MP3 Quality:** Forces FFmpeg to extract and encode at the highest Variable Bitrate without the dreaded double-extension bug.
* 🧹 **Scorched-Earth Process Management:** Includes a custom `start.sh` script that hunts down and kills zombie Go/Python processes to prevent Termux memory leaks.
* 💸 **Zero Cloud Costs:** Runs 100% locally on your device.

---

## 🛠️ Installation & Setup

### 📱 Step 1: Termux Preparation
First, ensure your Termux is updated and has access to your phone's internal storage so it can save the music.
```bash
pkg update && pkg upgrade -y
termux-setup-storage
⚙️ Step 2: Install Dependencies
Install the required programming languages and media encoding engines.

Bash
pkg install python ffmpeg golang git -y
pip install yt-dlp
🔗 Step 3: Clone & Configure
Pull this repository directly to your device and navigate into the folder:

Bash
git clone [https://github.com/mujii88/GoPy.git](https://github.com/mujii88/GoPy.git)
cd GoPy
💡 PRO TIP: Adding Your Bot Token
To avoid environment variable (.env) loading errors in Termux, the safest method is to hardcode your token.
Open gateway/main.go using a terminal editor like nano and replace the token placeholder directly with your actual Telegram Bot Token from BotFather!

🚀 Running the Bot
⚠️ IMPORTANT: Do not run the Go and Python files manually!

Use the provided startup script. This script acts as your system's process manager: it automatically wipes out old ghost sessions, compiles the latest Go binary, and safely starts the system without memory leaks.

Bash
cd ~/GoPy
chmod +x start.sh
./start.sh
📂 Where does the music go?
Downloaded .mp3 files are saved directly to the absolute Termux path:
/data/data/com.termux/files/home/GoPy

They are stored here temporarily before being securely transmitted back to you via the Telegram API.

⚠️ Disclaimer
This tool is provided for educational purposes and personal archiving only. Please respect the terms of service of the platforms you interact with and only download content you have the right to access.

<div align="center">
<i>Engineered for stability. Built to bypass the bans.</i>
</div>
