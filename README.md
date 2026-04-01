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

### 📱 Step 1: Prepare Your Termux Environment
Before installing the bot, we need to ensure your Termux is updated and has access to your phone's internal storage so it can save the music.

**1. Update the package lists and upgrade existing software:**
*(This makes sure you have the latest, most secure versions of everything).*
```bash
pkg update && pkg upgrade -y

```

### 2. Grant storage permissions:
(A popup will appear on your phone asking for permission. Click "Allow" so the bot can save MP3s).

```bash
termux-setup-storage
```
⚙️ Step 2: Install the Core Engines
This bot relies on a few heavy-duty tools to process audio and handle the Telegram gateway. We will install them in stages.

1. Install Git and Go:
(Git lets you download this repository, and Go is required to compile the high-speed Telegram gateway).

```Bash
pkg install git golang -y
```
2. Install Python and FFmpeg:
(Python runs the download scripts, and FFmpeg is the engine that converts the raw video into a high-quality V0 MP3).

```Bash
pkg install python ffmpeg -y
```
3. Install the Downloader Library:
(This installs yt-dlp, the core python library we use to communicate with YouTube).

```Bash
pip install yt-dlp
```
🔗 Step 3: Download & Configure the Bot
1. Clone the repository to your phone:

```Bash
git clone https://github.com/mujii88/GoPy.git
```
2. Navigate into the new folder:

```Bash
cd GoPy
```
💡 PRO TIP: Adding Your Bot Token safely
To avoid environment variable (.env) loading errors on Termux, the safest method is to hardcode your token directly into the Go script.

Type nano gateway/main.go to open the file in the terminal editor.

Find the token placeholder and replace it with your actual Telegram Bot Token from BotFather.

Press CTRL + X, then type Y, and hit Enter to save and exit.

🚀 Running the Bot
⚠️ IMPORTANT: Do not run the Go and Python files manually!

We have included a custom startup script (start.sh) that acts as your system's process manager. It automatically wipes out old ghost sessions, compiles the latest Go binary, and safely starts the system without memory leaks.
1. Make the script executable:
(You only have to run this command once)

```Bash
chmod +x start.sh
```
2. Launch the Bot:
(Run this command whenever you want to turn the bot on)

```Bash
./start.sh
```
📂 Where does the music go?
Downloaded .mp3 files are saved directly to this absolute Termux path:
/data/data/com.termux/files/home/GoPy

They are stored here temporarily before being securely transmitted back to you via the Telegram API, after which they are automatically cleaned up.

⚠️ Disclaimer
This tool is provided for educational purposes and personal archiving only. Please respect the terms of service of the platforms you interact with and only download content you have the right to access.



