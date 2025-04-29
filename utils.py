import random
import tweepy
from datetime import datetime, timedelta
import pytz
from config import (
    thanking_list, good_morning_wishes, good_night_wishes, wishes,
    welcoming_messages, follow_me_message, motivational_quotes
)

def load_lyrics():
    """Load English and Tamil lyrics from their respective files."""
    def clean_lyrics(file_path):
        with open(file_path, 'r') as f:
            lyrics = [line.strip().lower().replace('  ', ' ') for line in f]
        return [lyric if '...🎶' in lyric else lyric + '...🎶' for lyric in lyrics]

    english_lyrics = clean_lyrics('English_Lyrics.txt')
    tamil_lyrics = clean_lyrics('Tamil_Lyrics.txt')
    return english_lyrics, tamil_lyrics

def load_song_links():
    """Load Spotify song URLs from Song_Links.txt."""
    with open('Song_Links.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def thank_followers(client, user_id, current_hour, replied_followers):
    """Thank new followers with a time-sensitive message."""
    followers = client.get_users_followers(id=user_id, user_fields=['id', 'name'])
    followers_data = {user.id: {'username': user.username, 'name': user.name} for user in followers.data}

    # Load song links
    song_links = load_song_links()

    for follower_id in followers_data:
        if follower_id in replied_followers:
            continue

        # Choose message based on time of day
        if 5 < current_hour < 12:
            message = random.choice(good_morning_wishes)
        elif 12 <= current_hour < 20:
            message = random.choice([random.choice(wishes), f"I'm dedicating a song for you!\n{random.choice(song_links)}"])
        else:
            message = random.choice([random.choice(good_night_wishes), random.choice(wishes), f"I'm dedicating a song for you!\n{random.choice(song_links)}"])

        # Construct thank-you tweet
        username = followers_data[follower_id]['username']
        statement = f"{random.choice(thanking_list)}@{username}\n\n{message}"
        print(statement)
        # Uncomment to tweet: client.create_tweet(text=statement)

        replied_followers.append(follower_id)

    return replied_followers

def send_lyrics(client1, client2, tweet_id, english_lyrics, tamil_lyrics, replied_likes, replied_retweets, user_id):
    """Send English lyrics to likers and Tamil lyrics to retweeters of a specific tweet."""
    # Get followers for checking if users follow the bot
    followers = client2.get_users_followers(id=user_id, user_fields=['username'])
    follower_usernames = [user.username for user in followers.data]

    # Get users who liked the tweet
    likers = client2.get_liking_users(id=tweet_id)
    liked_users = [user.username for user in likers.data]

    # Get users who retweeted the tweet
    retweeters = client2.get_retweeters(id=tweet_id)
    retweeted_users = [user.username for user in retweeters.data] if retweeters.data else []

    # Send English lyrics to likers
    for username in liked_users:
        if username in replied_likes or not english_lyrics:
            continue

        lyric = random.choice(english_lyrics)
        english_lyrics.remove(lyric)
        statement = f"@{username}\n{lyric}"
        if username not in follower_usernames:
            statement += f"\n\n{follow_me_message}"
        if username in replied_retweets:
            statement = f"@{username}\nI hope you enjoyed Tamil lyric🙌🏻\n\n{lyric}"
        print(statement)
        # Uncomment to tweet: client1.create_tweet(in_reply_to_tweet_id=tweet_id, text=statement)

        replied_likes.append(username)

    # Send Tamil lyrics to retweeters
    for username in retweeted_users:
        if username in replied_retweets or not tamil_lyrics:
            continue

        lyric = random.choice(tamil_lyrics)
        tamil_lyrics.remove(lyric)
        statement = f"@{username}\n{lyric}"
        if username not in follower_usernames:
            statement += f"\n\n{follow_me_message}"
        if username in replied_likes:
            statement = f"@{username}\nI hope you enjoyed English lyric🙌🏻\n\n{lyric}"
        print(statement)
        # Uncomment to tweet: client1.create_tweet(in_reply_to_tweet_id=tweet_id, text=statement)

        replied_retweets.append(username)

    return english_lyrics, tamil_lyrics, replied_likes, replied_retweets

def send_motivational_quote(client1, client2, current_hour):
    """Send a motivational quote to users who like a specific tweet."""
    quote_tweet_id = '1528247071324549121'
    greeting = (
        "Good Morning" if current_hour < 12 else
        "Good Afternoon" if current_hour < 16 else
        "Good Evening"
    )

    likers = client2.get_liking_users(id=quote_tweet_id)
    liked_users = {user.username: user.name for user in likers.data}
    replied_users = []

    for username in liked_users:
        if username in replied_users or not motivational_quotes:
            continue

        quote = random.choice(motivational_quotes)
        motivational_quotes.remove(quote)
        statement = (
            f"Hey @{username}\nIf you are from GMT+5:30, {greeting}! "
            f"I'm dedicating this motivational quote for you. Enjoy your quote of the day❤️\n\n{quote}"
        )
        print(statement)
        # Uncomment to tweet: client1.create_tweet(in_reply_to_tweet_id=quote_tweet_id, text=statement)

        replied_users.append(username)

def send_sleep_reminder(client1, client2, user_id, replied_tweets, replied_once, replied_twice):
    """Send sleep reminders to followers active between 12:00 AM and 5:00 AM Asia/Colombo."""
    # Get current time in Asia/Colombo
    colombo_tz = pytz.timezone('Asia/Colombo')
    now = datetime.now(colombo_tz)
    current_hour = now.hour

    # Only proceed if current time is between 12:00 AM and 5:00 AM
    if not (0 <= current_hour < 5):
        return replied_tweets, replied_once, replied_twice

    # Calculate UTC time window for 12:00 AM to 5:00 AM Asia/Colombo today
    today = now.date()
    start_time = colombo_tz.localize(datetime(today.year, today.month, today.day, 0, 0))
    end_time = colombo_tz.localize(datetime(today.year, today.month, today.day, 5, 0))
    start_time_utc = start_time.astimezone(pytz.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time_utc = end_time.astimezone(pytz.UTC).strftime('%Y-%m-%dT%H:%M:%SZ')

    # Get followers
    followers = client2.get_users_followers(id=user_id, user_fields=['id', 'name'])
    followers_data = {user.id: {'username': user.username, 'name': user.name} for user in followers.data}

    for follower_id in followers_data:
        # Fetch tweets posted in the time window
        tweets = client2.get_users_tweets(
            id=str(follower_id), start_time=start_time_utc, end_time=end_time_utc,
            tweet_fields=['lang', 'created_at', 'author_id']
        )
        if not tweets.data:
            continue

        for tweet in tweets.data:
            if tweet.id in replied_tweets:
                continue

            username = followers_data[follower_id]['username']
            name = followers_data[follower_id]['name']

            # Log tweet data for debugging
            log_data = f"{username}\n{tweet.text}\n{tweet.id}\n\n"
            print(log_data)  # Replace with file logging if needed

            if follower_id in replied_once:
                if follower_id in replied_twice:
                    continue
                statement = f"Hello! @{username}\nI already told you to sleep and you are still here :("
                replied_twice.append(follower_id)
            else:
                statement = (
                    f"Hello, @{username}\n\n"
                    f"I know you are a follower of Professor and I identify that now you are on Twitter instead of sleeping.\n\n"
                    f"\"Sleeping is more important than Twitter.\"\n\n"
                    f"Go and Sleep {name}\n\nGood Night😴"
                )
                replied_once.append(follower_id)

            print(statement)
            # Uncomment to tweet: client1.create_tweet(reply_settings='following', text=statement)

            replied_tweets.append(tweet.id)

    return replied_tweets, replied_once, replied_twice

def reply_to_thanks(client1, client2, bot_username, replied_thanks, replied_thanks_users):
    """Reply to tweets thanking the bot."""
    query = f"(thanks OR thank) (to:{bot_username})"
    response = client2.search_recent_tweets(
        query=query, max_results=10, tweet_fields=['text', 'created_at'], expansions=['author_id']
    )

    users = {u['id']: u for u in response.includes['users']}
    for tweet in response.data:
        user = users.get(tweet.author_id)
        if not user or user.id in replied_thanks_users or tweet.id in replied_thanks:
            continue

        statement = f"{user.name}, {random.choice(welcoming_messages)}"
        print(statement)
        # Uncomment to tweet: client1.create_tweet(in_reply_to_tweet_id=str(tweet.id), text=statement)
        # Uncomment to like: client1.like(tweet_id=str(tweet.id))

        replied_thanks.append(tweet.id)
        replied_thanks_users.append(user.id)

    return replied_thanks, replied_thanks_users

def like_mentions(client1, bot_username):
    """Like tweets mentioning the bot."""
    query = f"@{bot_username}"
    response = client2.search_recent_tweets(
        query=query, max_results=10, tweet_fields=['text', 'created_at'], expansions=['author_id']
    )

    for tweet in response.data:
        print(f"Liking tweet {tweet.id}")
        # Uncomment to like: client1.like(tweet_id=str(tweet.id))

def respond_to_nth_follower(client1, client2, bot_username, replied_tweets):
    """Respond to tweets requesting the nth follower."""
    query = f"@{bot_username} hey Aiq"
    response = client2.search_recent_tweets(
        query=query, max_results=10, tweet_fields=['text', 'created_at'], expansions=['author_id']
    )

    users = {u['id']: u for u in response.includes['users']}
    for tweet in response.data:
        if tweet.id in replied_tweets or 'RT ' in tweet.text:
            continue

        user = users.get(tweet.author_id)
        if not user:
            continue

        tweet_text = tweet.text
        numbers = [int(s) for s in tweet_text.split() if s.isdigit()]
        total_requests = len(numbers)

        if not numbers:
            statement = f"Hello {user.name}! Seems like you haven't asked me anything. Btw nice to meet you :)"
        else:
            which_follower = numbers[0]
            number_suffix = (
                "th" if 4 <= which_follower % 100 <= 20 else
                {1: "st", 2: "nd", 3: "rd"}.get(which_follower % 10, "th")
            )

            followers = client2.get_users_followers(id=str(user.id), user_fields=['username'])
            follower_usernames = [u.username for u in followers.data]

            if which_follower == 0:
                statement = f"Hello {user.name}! Are you testing me or what? Btw your zeroth follower is me."
            elif which_follower > len(follower_usernames):
                statement = (
                    f"Oops! you have only {len(follower_usernames)} followers. "
                    f"Once a wise man said, \"aasepadelam perasepade koodathu\""
                )
            else:
                index = len(follower_usernames) - which_follower
                follower = follower_usernames[index]
                statement = f"Hello {user.name}! your {which_follower}{number_suffix} follower is @{follower}"
                if total_requests > 1:
                    statement += " Seems like you have requested more than one. Try again next time!"

        print(statement)
        # Uncomment to tweet: client1.create_tweet(in_reply_to_tweet_id=str(tweet.id), text=statement)
        # Uncomment to like: client1.like(tweet_id=str(tweet.id))

        replied_tweets.append(tweet.id)

    return replied_tweets
