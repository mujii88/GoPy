
package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"net/url"
	"os"
	"regexp"
	"strings"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

type MusicResponse struct {
	Status  string `json:"status"`
	File    string `json:"file"`
	Message string `json:"message"`
}

func main() {
	// The Brute Force Token
	token := "Put_your_Telegram_Bot_token_here"

	// 5-Minute Timeout for slow uploads
	client := &http.Client{
		Timeout: 300 * 1000000000, 
	}

	bot, err := tgbotapi.NewBotAPIWithClient(token, tgbotapi.APIEndpoint, client)
	if err != nil {
		log.Panic(err)
	}

	bot.Debug = false
	log.Printf("✅ Authorized on account: @%s", bot.Self.UserName)
	log.Println("🚀 GoPy Music Gateway is LIVE on Termux!")

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60
	updates := bot.GetUpdatesChan(u)

	for update := range updates {
		if update.Message == nil || !update.Message.IsCommand() {
			continue
		}

		chatID := update.Message.Chat.ID
		command := update.Message.Command()
		args := update.Message.CommandArguments()

		switch command {

		case "start":
			msg := tgbotapi.NewMessage(chatID, "👋 Welcome to the GoPy Music Bot!\n\n🎧 Just type `/play <song name>` and I will fetch it for you.")
			bot.Send(msg)

		case "play":
			if strings.TrimSpace(args) == "" {
				bot.Send(tgbotapi.NewMessage(chatID, "⚠️ Please tell me what to play! Example: `/play faded`"))
				continue
			}

			statusMsg := tgbotapi.NewMessage(chatID, fmt.Sprintf("🔍 Searching for: *%s*...\n⏳ Please wait a moment!", args))
			statusMsg.ParseMode = "Markdown"
			sentStatus, _ := bot.Send(statusMsg)

			apiURL := fmt.Sprintf("http://127.0.0.1:8000/music?song=%s", url.QueryEscape(args))
			resp, err := http.Get(apiURL)

			if err != nil {
				bot.Send(tgbotapi.NewEditMessageText(chatID, sentStatus.MessageID, "❌ Gateway Error: Could not connect to the Python Brain."))
				continue
			}
			defer resp.Body.Close()

			var musicResp MusicResponse
			if err := json.NewDecoder(resp.Body).Decode(&musicResp); err != nil {
				bot.Send(tgbotapi.NewEditMessageText(chatID, sentStatus.MessageID, "❌ Gateway Error: Invalid response from Brain."))
				continue
			}

			if musicResp.Status != "success" {
				bot.Send(tgbotapi.NewEditMessageText(chatID, sentStatus.MessageID, fmt.Sprintf("❌ Could not download: %s", musicResp.Message)))
				continue
			}

			bot.Send(tgbotapi.NewEditMessageText(chatID, sentStatus.MessageID, "☁️ Song downloaded! Uploading to Telegram..."))

			// 🕵️‍♂️ THE "MESSY PYTHON" FIX
			// If Python sends a dictionary inside the file variable, extract the real path!
			actualPath := musicResp.File
			if strings.Contains(actualPath, `"file"`) {
				re := regexp.MustCompile(`"file":\s*"([^"]+)"`)
				match := re.FindStringSubmatch(actualPath)
				if len(match) > 1 {
					actualPath = match[1] // Grab just the clean file path
				}
			}
			actualPath = strings.TrimSpace(actualPath)

			// Upload using the clean path
			audio := tgbotapi.NewAudio(chatID, tgbotapi.FilePath(actualPath))
			audio.Caption = fmt.Sprintf("🎧 Enjoy your track: %s", args)
			
			_, err = bot.Send(audio)
			if err != nil {
				log.Printf("Upload failed: %v", err)
				bot.Send(tgbotapi.NewMessage(chatID, fmt.Sprintf("❌ Upload failed: %v", err)))
			} else {
				bot.Send(tgbotapi.NewDeleteMessage(chatID, sentStatus.MessageID))
				os.Remove(actualPath) // Clean up the file so your phone doesn't run out of storage!
			}

		default:
			bot.Send(tgbotapi.NewMessage(chatID, "❓ I don't know that command. Try `/play`."))
		}
	}
}
