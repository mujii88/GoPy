package main

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"strings"
	"html"
	"net/url"


	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
	"github.com/joho/godotenv"
)

// --- Define the Structures to match Python's JSON ---
type NewsItem struct {
	Title       string `json:"title"`
	URL         string `json:"url"`
	Time        string `json:"time"`
	Description string `json:"description"`
}

type GopyReport struct {
	Category    string     `json:"category"`
	NewsUpdates []NewsItem `json:"news_updates"`
	DailyAdvice string     `json:"daily_advice"`
}


type LeetCodeBriefing struct{
	QuestionTitle string `json:"question_title"`
	QuestionDifficulty string `json:"question_difficulty"`
	QuestionContent string `json:"question_content"`
}


type MusicResponse struct {
    Status  string `json:"status"`
    File    string `json:"file"`
    Message string `json:"message"`
}

func main() {

	err := godotenv.Load("/home/one/GoPy/.env")
	if err != nil {
		log.Println("error in loading the env file")
	}

	bottoken := os.Getenv("TELEGRAM_BOT_TOKEN")
	if bottoken == "" {
		log.Fatal("telegram bot token is empty in env file")
	}

	bot, err := tgbotapi.NewBotAPI(bottoken)
	if err != nil {
		log.Panic(err)
	}

	log.Printf("Gateway online......")

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60

	updates := bot.GetUpdatesChan(u)

	for update := range updates {
		if update.Message == nil {
			continue
		}

		if !update.Message.IsCommand() {
			continue
		}

		// Prepare the default response message object
		msg := tgbotapi.NewMessage(update.Message.Chat.ID, "")

		switch update.Message.Command() {
		case "start":
			msg.Text = "Hello Buddy! your GOPY is ready so send the tasks you need to be done"

		case "report":
			// 1. Send the "waiting" message immediately so the user knows it's working
			waitMsg := tgbotapi.NewMessage(update.Message.Chat.ID, "📡 Pinging the Python Brain... Grab a cup of coffee...")
			bot.Send(waitMsg)

			// 2. Fetch data from the Python Brain
			resp, err := http.Get("http://localhost:8000/brief")

			if err != nil {
				msg.Text = "❌ Error: Could not reach the Python Brain."
			} else {
				defer resp.Body.Close()
				body, _ := io.ReadAll(resp.Body)

				// 3. Parse the JSON into our Go structs
				var report GopyReport
				err = json.Unmarshal(body, &report)
				if err != nil {
					msg.Text = "❌ Gopy encountered an error formatting the report."
				} else {
					// 4. Build the beautiful HTML string
					var finalMsg string
					finalMsg += "⚡ <b>" + strings.ToUpper(report.Category) + "</b> ⚡\n\n"

					if len(report.NewsUpdates) > 0 {
						finalMsg += "🗞 <b>LATEST TECH & AI NEWS</b>\n"
						for _, item := range report.NewsUpdates {
							finalMsg += "▪️ <b><a href=\"" + item.URL + "\">" + item.Title + "</a></b>\n"
							finalMsg += "<i>" + item.Description + "</i>\n\n"
						}
					} else {
						finalMsg += "🗞 <i>No new updates right now.</i>\n\n"
					}

					finalMsg += "💡 <b>DAILY ADVICE</b>\n"
					finalMsg += "<i>" + report.DailyAdvice + "</i>"

					// 5. Apply the HTML formatting to the Telegram message
					msg.Text = finalMsg
					msg.ParseMode = "HTML"
					msg.DisableWebPagePreview = true
				}
			}


		
		case "leetcode":

			waitmsg:=tgbotapi.NewMessage(update.Message.Chat.ID,"📡 Getting the data for your daily leetcode dose.....")
			bot.Send(waitmsg)

			resp,err:=http.Get("http://localhost:8000/leetcode")
			if err!=nil{
				msg.Text="❌ Error: Could not reach the Python Brain."
			}else{
				defer resp.Body.Close()
				body,_:=io.ReadAll(resp.Body)

				var leetcode LeetCodeBriefing
				err=json.Unmarshal(body,&leetcode)
				if err!=nil{
					msg.Text="❌ Gopy encountered an error formatting the report."
				}else{
					var finalMsg string
					finalMsg+="⚡ "+strings.ToUpper(leetcode.QuestionTitle)+" ⚡\n\n"
					finalMsg+="💡 <b>"+leetcode.QuestionDifficulty+"</b>\n"
					finalMsg += html.EscapeString(leetcode.QuestionContent)
					

					// 5. Apply the HTML formatting to the Telegram message
					msg.Text = finalMsg
					msg.ParseMode = "HTML"
					msg.DisableWebPagePreview = true
				}
			}


		case "play":
			songName := update.Message.CommandArguments()
            if songName == "" {
                msg.Text = "❌ Please provide a song name! Example: /play Linkin Park Numb"
                bot.Send(msg)
                continue
            }

            waitMsg := tgbotapi.NewMessage(update.Message.Chat.ID, "🎧 Hijacking YouTube stream... Give me a few seconds!")
            bot.Send(waitMsg)

            // Encode the URL (Turns "Anarkali disco chali" into "Anarkali+disco+chali")
            safeSongName := url.QueryEscape(songName)

            // Ping the Python Brain
            resp, err := http.Get("http://localhost:8000/music?song=" + safeSongName)
            if err != nil {
                msg.Text = "❌ Error: Could not reach the Python Brain."
                bot.Send(msg)
                continue
            }
            defer resp.Body.Close()

            body, _ := io.ReadAll(resp.Body)
            var musicRes MusicResponse
            json.Unmarshal(body, &musicRes)

            if musicRes.Status == "success" {
                // Send the local MP3 file directly as a Telegram Audio track
                audioMsg := tgbotapi.NewAudio(update.Message.Chat.ID, tgbotapi.FilePath(musicRes.File))
				audioMsg.Title = songName        
                audioMsg.Performer = "GoPy API"
                bot.Send(audioMsg)

                // CRITICAL: Delete the file from your computer immediately after sending!
                os.Remove(musicRes.File)
                
                // We successfully sent an audio message, so we continue the loop to avoid sending a blank text message at the bottom
                continue 
            } else {
                msg.Text = "❌ Failed to rip audio: " + musicRes.Message
            }

		default:
			msg.Text = "Unknown command. Use /start, /report, /leetcode, or /play <song_name>"
		}
		// Send the final compiled message (either an error or the formatted report)
		if _, err := bot.Send(msg); err != nil {
			log.Println(err)
		}

	}
}
