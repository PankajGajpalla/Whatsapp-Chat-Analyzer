from wordcloud import WordCloud
from collections import Counter
import pandas as pd

import matplotlib.pyplot as plt

import emoji
from urlextract import URLExtract
extract = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    # 1 fetch number of messages
    num_messages = df.shape[0]

    # 2 fetch total number of words in all the messages of selected_user
    words = []
    for message in df['message']:
        words.extend(message.split())  # split with spaces

    # 3 fetch total number of media sent by the selected_user
    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    # 4 fetch number of links shared
    links = []

    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_msg, len(links)

def fetch_most_busy_user(df):
    x = df['users'].value_counts().head()

    df = round((df['users'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={"index":"name","user":"percent(%)"})

    return x, df

def create_wordcloud(selected_user, df):
    f = open("stop_hinglish.txt", 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]

    def remove_stop_words(message):
        words = []
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
        return " ".join(words)


    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    f = open("stop_hinglish.txt", 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group notification']
    temp = temp[temp['message'] != "<Media omitted>\n"]


    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    df = pd.DataFrame(Counter(words).most_common(20))
    return df

def emoji_analysis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    time_line = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(time_line.shape[0]):
        time.append(str(time_line['month'][i]) + " - " + str(time_line['year'][i]))

    time_line['time'] = time
    return time_line


def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()
    return daily_timeline

def weekly_active_day(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    weekly_actd = df["day_name"].value_counts()

    return weekly_actd

def monthly_active(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    busy_month = df["month"].value_counts()

    return busy_month

def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df['users'] == selected_user]

    htmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return htmap



