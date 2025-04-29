# Tweet Engager Bot

The **Tweet Engager Bot** is a Python-based Twitter automation tool designed to engage with followers through personalized interactions such as sending sleep reminders, thanking new followers, recommending Spotify songs, sharing lyrics, and more.

Originally developed in **June 2022** and deployed on [PythonAnywhere](https://www.pythonanywhere.com/) for continuous operation.

> **Note**: This code was developed using Twitter API **v1.1** via Tweepy. Due to changes in Twitter’s API (e.g., v2 or paid tiers), functionality may require updates. Refer to the [Twitter API documentation](https://developer.twitter.com/en/docs) for latest changes.

---

## 🔧 Features

- **Sleep Reminders**  
  Notifies followers active between 12:00 AM and 5:00 AM (Asia/Colombo time) to encourage healthier sleep patterns.

- **Thanking Followers**  
  Sends personalized thank-you messages to new followers, with wishes or song recommendations based on the time of day.

- **Song Recommendations**  
  Dedicates random Spotify songs (loaded from `Song_Links.txt`) to new followers or users who like a specific tweet.

- **Lyrics Sharing**  
  Shares:
  - English lyrics with users who like a specific tweet.
  - Tamil lyrics with users who retweet it.

- **Motivational Quotes**  
  Sends time-sensitive motivational quotes to users who like a designated tweet.

- **Replying to Thanks**  
  Responds to tweets that include words like “thanks” or “thank” directed at the bot.

- **Tweet Liking**  
  Likes tweets that mention or thank the bot.

- **Nth Follower Request (Discontinued)**  
  Previously responded to tweets like `@BOT_USERNAME hey Aiq <number>` with the user's nth follower. (No longer functional due to Twitter API limitations.)

---

## 🛠️ Technologies Used

- **Language**: Python 3.8  
- **API**: Twitter API v1.1 (via `tweepy`)  
- **Libraries**: `tweepy`, `python-dotenv`, `pytz`  
- **Hosting**: [PythonAnywhere](https://www.pythonanywhere.com/) (free tier)

---

## ⚙️ Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/tweet-engager-bot.git
cd tweet-engager-bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Twitter API
- Create a Twitter Developer account and obtain your API keys:  
  - Consumer Key  
  - Consumer Secret  
  - Access Token  
  - Access Token Secret

- Copy `.env.example` to `.env` and update with your credentials:
```env
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret
```

### 4. Configure the Bot
Edit `config.py` to set:
- `USER_ID`: Your Twitter user ID
- `TWEET_ID`: ID of the tweet used for likes/retweets
- `BOT_USERNAME`: Your bot’s Twitter handle (without the `@`)

Ensure the following files exist in the root directory:
- `Song_Links.txt`: Spotify song URLs (one per line)
- `English_Lyrics.txt`: English lyrics
- `Tamil_Lyrics.txt`: Tamil lyrics

### 5. Run the Bot
```bash
python bot.py
```

---

## 🚀 Deployment on PythonAnywhere

- **Hosting**: Deployed using PythonAnywhere’s free tier with Python 3.8  
- **Scheduled Tasks**: Configured to run `bot.py` every 10 minutes  
- **Environment Variables**: API keys stored securely in PythonAnywhere’s "Web" dashboard  
- **Limitations**: Free tier restricts outbound network access, potentially affecting Twitter API v2 compatibility. Paid plans or alternative hosting may be needed.

---

## 📁 File Structure

- `README.md` – Project overview, setup, and usage  
- `requirements.txt` – Required Python libraries  
- `.env.example` – Template for Twitter API credentials  
- `bot.py` – Main script running the bot logic  
- `utils.py` – Helper functions (e.g., sending reminders, loading lyrics)  
- `config.py` – Configuration and message data  
- `Song_Links.txt` – Spotify URLs for song recommendations  
- `English_Lyrics.txt` – English song lyrics  
- `Tamil_Lyrics.txt` – Tamil song lyrics

---

## ⚠️ Limitations

- **API Compatibility**: Designed for Twitter API v1.1. May need modifications for API v2 or current rate limits.  
- **Nth Follower Feature**: No longer functional due to follower data access restrictions.  
- **Time Zone Specific**: Targeted for Asia/Colombo (UTC+5:30); update logic for other time zones.  
- **Free Hosting Restrictions**: PythonAnywhere’s free tier may block API calls. Consider alternatives like Heroku or AWS.

---

## 📄 License

This project is licensed under the **MIT License**.
