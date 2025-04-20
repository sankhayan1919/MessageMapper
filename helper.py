import emoji
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from urlextract import URLExtract
from collections import Counter
extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]    #fetch no. of media messages

    words = []
    links=[]
    for message in df['message']:
        words.extend(message.split())   #fetch no. of words shared
        links.extend(extract.find_urls(message))    #fetch no. of links shared
        emojis = df['message'].apply(lambda x: len([c for c in x if c in emoji.EMOJI_DATA])).sum()   #fetch no. of emojis shared
        stickers = df[df['message'].str.contains('sticker')].shape[0]    #fetch no. of stickers shared
    
    return num_messages, len(words), num_media_messages, len(links), emojis, stickers

def get_chat_age(df):
    # First, remove group notifications
    df_filtered = df[df['user'] != 'group_notification']
    
    # Sort by date in ascending order to get the earliest message
    df_sorted = df_filtered.sort_values('date', ascending=True)
    
    # Get the first message details
    first_message_row = df_sorted.iloc[0]
    first_message_date = first_message_row['date']
    first_message_text = first_message_row['message']
    first_message_user = first_message_row['user']
    
    # Check if the first message is a non-text message
    non_text_patterns = [
        'voice message', 'audio', 'voice note', 'voice recording', 'voice clip', 'voice memo', 'voice file', 'voice msg',
        '<media omitted>', 'image omitted', 'video omitted', 'document omitted', 'sticker omitted',
        'voice call', 'video call', 'missed voice call', 'missed video call',
        'GIF omitted', 'location omitted', 'contact omitted', 'file omitted'
    ]
    
    if any(pattern.lower() in first_message_text.lower() for pattern in non_text_patterns):
        first_message_text = "It's a media message (voice message, call, image, video, etc.)"
    
    # Calculate chat age
    current_date = pd.Timestamp.now()
    chat_age = current_date - first_message_date
    
    years = chat_age.days // 365
    remaining_days = chat_age.days % 365
    months = remaining_days // 30
    days = remaining_days % 30
    
    age_str = ""
    if years > 0:
        age_str += f"{years} year{'s' if years > 1 else ''}, "
    if months > 0:
        age_str += f"{months} month{'s' if months > 1 else ''}, "
    age_str += f"{days} day{'s' if days > 1 else ''}"
    
    return {
        'first_message_date': first_message_date.strftime('%d %B %Y'),
        'chat_age': age_str,
        'first_message': first_message_text,
        'first_message_user': first_message_user
    }

def get_user_first_message(selected_user, df):
    # Filter for the selected user
    df_user = df[df['user'] == selected_user]
    
    # Remove group notifications
    df_user = df_user[df_user['user'] != 'group_notification']
    
    if df_user.empty:
        return {
            'first_message_date': "No messages found",
            'first_message': "No messages found",
            'first_message_user': selected_user
        }
    
    # Sort by date in ascending order to get the earliest message
    df_sorted = df_user.sort_values('date', ascending=True)
    
    # Get the first message details
    first_message_row = df_sorted.iloc[0]
    first_message_date = first_message_row['date']
    first_message_text = first_message_row['message']
    
    # Check if the first message is a non-text message
    non_text_patterns = [
        'voice message', 'audio', 'voice note', 'voice recording', 'voice clip', 'voice memo', 'voice file', 'voice msg',
        '<media omitted>', 'image omitted', 'video omitted', 'document omitted', 'sticker omitted',
        'voice call', 'video call', 'missed voice call', 'missed video call',
        'GIF omitted', 'location omitted', 'contact omitted', 'file omitted'
    ]
    
    if any(pattern.lower() in first_message_text.lower() for pattern in non_text_patterns):
        first_message_text = "It's a media message (voice message, call, image, video, etc.)"
    
    return {
        'first_message_date': first_message_date.strftime('%d %B %Y'),
        'first_message': first_message_text,
        'first_message_user': selected_user
    }

def voice_message_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    # Filter messages containing various voice message patterns
    voice_patterns = [
        'voice message',
        'audio',
        'voice note',
        'voice recording',
        'voice clip',
        'voice memo',
        'voice file',
        'voice msg',
        'voice msg.',
        'voice msg:',
        'voice message:',
        'voice note:',
        'voice recording:',
        'voice clip:',
        'voice memo:',
        'voice file:'
    ]
    
    # Create a pattern string for case-insensitive matching
    pattern = '|'.join(voice_patterns)
    voice_messages = df[df['message'].str.contains(pattern, case=False, na=False)]
    
    # Count voice messages per user
    voice_counts = voice_messages['user'].value_counts().reset_index()
    voice_counts.columns = ['User', 'Voice Message Count']
    
    return voice_counts

def most_active_users(df):
    x = df['user'].value_counts().head(5)    #fetch top 5 active users
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'user': 'name', 'count': 'percent'})
    return x, df

def call_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    # Filter messages containing "voice call" or "video call"
    voice_calls = df[df['message'].str.contains('voice call', case=False, na=False)]
    video_calls = df[df['message'].str.contains('video call', case=False, na=False)]

    # Count the number of voice and video calls
    voice_call_count = len(voice_calls)
    video_call_count = len(video_calls)

    # If no calls are found, return a message
    if voice_call_count == 0 and video_call_count == 0:
        return pd.DataFrame(columns=['Call Type', 'Count']), "No calls happened."

    # Create a DataFrame with the counts
    call_data = pd.DataFrame({
        'Call Type': ['Voice Call', 'Video Call'],
        'Count': [voice_call_count, video_call_count]
    })

    return call_data, None

def create_wordcloud(selected_user, df):    #wordcloud
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    stopwords = set(STOPWORDS)
    stopwords.update(['Media', 'omitted', 'https', 'added', 'left', 'group_notification'])  # Add words to exclude
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white', stopwords=stopwords)
    wc = wc.generate(df['message'].str.cat(sep=' '))
    return wc

def emoji_helper(selected_user, df):    #emoji analysis
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    if len(emojis) == 0:  # Check if no emojis are found
        return pd.DataFrame(columns=['Emoji', 'Count'])  # Return an empty DataFrame
    
    emoji_df = pd.DataFrame(Counter(emojis).most_common(10))
    emoji_df.columns = ['Emoji', 'Count']
    return emoji_df

def monthly_timeline(selected_user, df):    #monthly timeline
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    monthly_timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(monthly_timeline.shape[0]):
        time.append(monthly_timeline['month'][i] + '-' + str(monthly_timeline['year'][i]))
    monthly_timeline['time'] = time
    return monthly_timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').size().reset_index(name='message')  # Count messages per day
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()  # Count messages per day of the week

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()  # Count messages per month

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return heatmap  # Create a pivot table for heatmap

def response_time_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    df = df[df['user'] != 'group_notification']

    # Calculate time difference between consecutive messages
    df['time_diff'] = df['date'].diff().dt.total_seconds()

    # Shift the 'user' column to align with the time difference (who replied to whom)
    df['prev_user'] = df['user'].shift()

    # Filter rows where the user is replying to someone else
    df = df[df['user'] != df['prev_user']]

    # Remove any rows with NaN values in time_diff
    df = df.dropna(subset=['time_diff'])

    # If no valid response times found
    if df.empty:
        return pd.DataFrame(columns=['user', 'avg_response_time']), None

    # Group by user and calculate average response time
    response_times = df.groupby('user')['time_diff'].mean().reset_index()
    response_times.rename(columns={'time_diff': 'avg_response_time'}, inplace=True)

    # If no valid response times after grouping
    if response_times.empty:
        return pd.DataFrame(columns=['user', 'avg_response_time']), None

    # Find the fastest responder only if we have valid data
    try:
        fastest_responder = response_times.loc[response_times['avg_response_time'].idxmin()]
    except:
        return response_times, None

    return response_times, fastest_responder

def first_message_of_day(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    # Remove group notifications
    df = df[df['user'] != 'group_notification']
    # Extract the date part of the timestamp
    df['only_date'] = df['date'].dt.date

    # Find the first message of each day
    first_messages = df.groupby('only_date').first().reset_index()

    # Count the occurrences of each user in the first messages
    first_message_counts = first_messages['user'].value_counts().reset_index()
    first_message_counts.columns = ['user', 'first_message_count']

    return first_message_counts

def late_night_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    # Remove group notifications
    df = df[df['user'] != 'group_notification']
    # Filter messages sent between 12 AM and 3 AM
    late_night_messages = df[(df['hour'] >= 0) & (df['hour'] < 3)]

    # Count the number of messages sent by each user during this time
    late_night_counts = late_night_messages['user'].value_counts().reset_index()
    late_night_counts.columns = ['user', 'late_night_message_count']

    return late_night_counts

def longest_streaks(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    # Group messages by date and count the number of messages for each day
    daily_activity = df.groupby('only_date').size().reset_index(name='message_count')

    # Sort by message count in descending order
    top_days = daily_activity.sort_values(by='message_count', ascending=False).head(10)

    return top_days

def text_length_analysis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # Filter out group notifications
    df = df[df['user'] != 'group_notification']
    
    if df.empty:
        return pd.DataFrame(columns=['User', 'Average Message Length'])
    
    # Calculate average message length for each user
    if selected_user == 'Overall':
        avg_length = df.groupby('user')['message'].apply(
            lambda x: sum(len(msg) for msg in x) / len(x)
        ).reset_index()
        avg_length.columns = ['User', 'Average Message Length']
    else:
        # For individual user, calculate their average message length
        avg_length = pd.DataFrame({
            'User': [selected_user],
            'Average Message Length': [sum(len(msg) for msg in df['message']) / len(df['message'])]
        })
    
    return avg_length

def analyze_deleted_messages(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    deleted_messages = df[df['message'].str.contains('This message was deleted', case=False, na=False)]
    
    # Count deletions per user
    deletion_counts = deleted_messages['user'].value_counts().reset_index()
    deletion_counts.columns = ['User', 'Deleted Messages']
    
    # Calculate percentage of total messages
    total_messages = df.groupby('user')['message'].count()
    deletion_percentages = (deleted_messages['user'].value_counts() / total_messages * 100).round(2)
    deletion_counts['Deletion Rate (%)'] = deletion_counts['User'].map(deletion_percentages)
    
    return deletion_counts

def analyze_group_dynamics(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    # Check if it's a group chat (more than 2 users excluding group_notification)
    unique_users = df[df['user'] != 'group_notification']['user'].nunique()
    if unique_users <= 2:
        return None, None, "This is not a group chat"

    # Analyze mentions (@username)
    mentions = []
    mention_by = []
    for _, row in df.iterrows():
        message = row['message']
        sender = row['user']
        # Find all @mentions in the message
        if '@' in message:
            mentioned_users = [word.strip('@') for word in message.split() if word.startswith('@')]
            for mentioned in mentioned_users:
                mentions.append(mentioned)
                mention_by.append(sender)

    # Create mentions DataFrame
    mentions_df = pd.DataFrame({
        'Mentioned_by': mention_by,
        'Mentioned_user': mentions
    })
    mentions_summary = mentions_df.groupby('Mentioned_by').size().reset_index(name='Mention_count')
    mentions_summary = mentions_summary.sort_values('Mention_count', ascending=False)

    # Analyze reply patterns
    replies = []
    for i in range(1, len(df)):
        current_user = df.iloc[i]['user']
        prev_user = df.iloc[i-1]['user']
        if current_user != prev_user and current_user != 'group_notification' and prev_user != 'group_notification':
            replies.append({
                'From': current_user,
                'To': prev_user
            })

    # Create reply patterns DataFrame
    replies_df = pd.DataFrame(replies)
    if not replies_df.empty:
        reply_summary = replies_df.groupby(['From', 'To']).size().reset_index(name='Reply_count')
        reply_summary = reply_summary.sort_values('Reply_count', ascending=False)
    else:
        reply_summary = pd.DataFrame(columns=['From', 'To', 'Reply_count'])

    return mentions_summary, reply_summary, None


