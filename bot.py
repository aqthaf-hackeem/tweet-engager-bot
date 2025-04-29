import time
import tweepy
from datetime import datetime
from dotenv import load_dotenv
import os
from utils import (
    load_lyrics, thank_followers, send_lyrics, send_motivational_quote,
    send_sleep_reminder, reply_to_thanks, like_mentions, respond_to_nth_follower
)
from config import (
    USER_ID, TWEET_ID, BOT_USERNAME, get_twitter_client
)

# Load environment variables
load_dotenv()

def main():
    """Main function to run the Twitter bot."""
    # Initialize Twitter API clients
    client1 = get_twitter_client()  # For actions like tweeting, liking
    client2 = get_twitter_client()  # For fetching data (followers, likes, etc.)

    # Load lyrics from files
    english_lyrics, tamil_lyrics = load_lyrics()

    # Initialize state tracking
    replied_followers = []
    replied_likes = []
    replied_retweets = []
    replied_thanks = []
    replied_thanks_users = []
    replied_nth_tweets = []
    sleep_reminder_tweets = []
    sleep_reminder_users_once = []
    sleep_reminder_users_twice = []

    while True:
        try:
            # Get current time in Asia/Colombo
            current_hour = datetime.now().astimezone(pytz.timezone('Asia/Colombo')).hour

            # Thank new followers
            replied_followers = thank_followers(
                client2, USER_ID, current_hour, replied_followers
            )

            # Send lyrics to users who like or retweet the specific tweet
            english_lyrics, tamil_lyrics, replied_likes, replied_retweets = send_lyrics(
                client1, client2, TWEET_ID, english_lyrics, tamil_lyrics,
                replied_likes, replied_retweets, USER_ID
            )

            # Send motivational quotes to users who like the quote tweet
            send_motivational_quote(client1, client2, current_hour)

            # Send sleep reminders to active followers
            sleep_reminder_tweets, sleep_reminder_users_once, sleep_reminder_users_twice = (
                send_sleep_reminder(
                    client1, client2, USER_ID,
                    sleep_reminder_tweets, sleep_reminder_users_once,
                    sleep_reminder_users_twice
                )
            )

            # Reply to users thanking the bot
            replied_thanks, replied_thanks_users = reply_to_thanks(
                client1, client2, BOT_USERNAME, replied_thanks, replied_thanks_users
            )

            # Like tweets mentioning the bot
            like_mentions(client1, BOT_USERNAME)

            # Respond to nth follower requests
            replied_nth_tweets = respond_to_nth_follower(
                client1, client2, BOT_USERNAME, replied_nth_tweets
            )

            # Save remaining lyrics to files
            save_lyrics(english_lyrics, tamil_lyrics)

            # Wait before the next iteration
            print("Waiting for next check...")
            time.sleep(60)

        except Exception as e:
            print(f"Error: {e}. Waiting before retry...")
            time.sleep(60)

def save_lyrics(english_lyrics, tamil_lyrics):
    """Save remaining lyrics to their respective files."""
    with open('English_Lyrics.txt', 'w') as f:
        f.write('\n'.join(english_lyrics))
    with open('Tamil_Lyrics.txt', 'w') as f:
        f.write('\n'.join(tamil_lyrics))

if __name__ == "__main__":
    main()
