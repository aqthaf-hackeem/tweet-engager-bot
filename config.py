import os
import tweepy
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Twitter API credentials
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

# Bot configuration
USER_ID = 'your_twitter_user_id'  # Replace with your Twitter user ID
TWEET_ID = 'your_tweet_id'  # Replace with the tweet ID for likes/retweets
BOT_USERNAME = 'your_bot_username'  # Replace with your bot's Twitter handle (without @)

# Message lists
thanking_list = [
    'Oh nice! Thanks for following me❤️ ',
    'Oh Wow!! Thanks for following me ❤️ ',
    'Oh, that\'s wonderful! Thank you for following me❤️ ',
    'That\'s amazing! Thank you for following me🥳 ',
    'Oh, that\'s wonderful. I appreciate your interest in following my timeline🤓, ',
    'Oh, great move! Thank you for following me😎 ',
    'You could have picked millions of people to follow… GREAT choice. Thank you! ',
    'Thanks for following, Hope you enjoy my tweets! ',
    'Hey there, thank you for the follow. Glad to have you here, and hope to make it worth your time. Cheers!🥳 ',
    'You could have picked millions of people to follow…GREAT choice🤪 Thank you! '
]

good_morning_wishes = [
    "Wishing a lovely morning! May your day be filled with much joy and success.",
    "Life is not about the past. Life is not about the future. Life is about the present. Life is about today. So have a nice day, Good Morning!",
    # ... (other good morning wishes from your code)
]

good_night_wishes = [
    "Good Night, Hope you are ending your day with happy thoughts and gratitude.",
    "Hope you are looking forward to a morning that is as wonderful as you. Good Night, Friend!",
    # ... (other good night wishes from your code)
]

wishes = [
    "All the best for all your future endeavors! Hoping that your hard work always brings out the best results for you.",
    "I pray for a happy, healthy, and prosperous life for you. May God always bless you and help you. Best wishes!",
    # ... (other general wishes from your code)
]

welcoming_messages = [
    "You're welcome!",
    "I'm glad that you're enjoyed.",
    "You're very welcome!",
    "It's my pleasure."
]

follow_me_message = "Keep in touch by following me on twitter😴🤖"

# Motivational quotes (placeholder, as Morning Quotes.txt not provided)
motivational_quotes = [
    "The only limit to our realization of tomorrow is our doubts of today.",
    "Success is not the absence of obstacles, but the courage to push through them.",
    # Add more quotes as needed
]

def get_twitter_client():
    """Initialize and return a Tweepy client for Twitter API v1.1."""
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    return tweepy.API(auth, wait_on_rate_limit=True)
