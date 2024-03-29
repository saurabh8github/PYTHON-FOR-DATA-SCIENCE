# -*- coding: utf-8 -*-
"""whatsapp_chat_analyzer.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1L5SlFLoOsFtpUa-_9pRX_EbsxmZ5dwCp

##                                   Welcome to Whatsapp_Chat_analyzer


---
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import the chat history
chat_history = pd.read_csv('WhatsApp Chat with DSGRG Pitchers Startup.txt')

# Create a new column that indicates whether the message was sent by the specific person
chat_history['sent_by_specific_person'] = chat_history['author'] == 'specific_person'

# Use a time series analysis to find the patterns in the data
sent_by_specific_person = chat_history['sent_by_specific_person'].values
time = chat_history['time'].values

# Visualize the results using a graph
plt.plot(time, sent_by_specific_person)
plt.show()



"""#installation of essential libraries"""

!pip install streamlit

!pip install streamlit
!pip install urlextract
!pip install wordcloud

!pip install preprocessor

import re
import pandas as pd

# Read the text file
path = "WhatsApp Chat with DSGRG Pitchers Startup.txt"
f = open(path, 'r', encoding='utf-8')
data = f.read()
print(type(data))

# Regular expression to find the dates
pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s'

# Pass the pattern and data to split it to get the list of messages
messages = re.split(pattern, data)[1:]

# Extract all dates
dates = re.findall(pattern, data)

# Clean the time data by removing non-printable characters and special characters
dates = [re.sub(r'[^\x00-\x7F]', '', date).strip('- ') for date in dates]

# Create dataframe
df = pd.DataFrame({'user_message': messages, 'message_date': dates})

# Convert message_date type
df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M%p')
df.rename(columns={'message_date': 'date'}, inplace=True)
df.head(4)

#separate Users and Message
users = []
messages = []
for message in df['user_message']:
    entry = re.split('([\w\W]+?):\s', message)
    if entry[1:]:  # user name
        users.append(entry[1])
        messages.append(" ".join(entry[2:]))
    else:
        users.append('group_notification')
        messages.append(entry[0])

df['user'] = users
df['message'] = messages
df.drop(columns=['user_message'], inplace=True)

#Extract multiple columns from the Date Column
df['only_date'] = df['date'].dt.date
df['year'] = df['date'].dt.year
df['month_num'] = df['date'].dt.month
df['month'] = df['date'].dt.month_name()
df['day'] = df['date'].dt.day
df['day_name'] = df['date'].dt.day_name()
df['hour'] = df['date'].dt.hour
df['minute'] = df['date'].dt.minute

#add period column that shows data capture between which 24 hour format
period = []
for hour in df[['day_name', 'hour']]['hour']:
    if hour == 23:
        period.append(str(hour) + "-" + str('00'))
    elif hour == 0:
        period.append(str('00') + "-" + str(hour + 1))
    else:
        period.append(str(hour) + "-" + str(hour + 1))

df['period'] = period
df.head()

#Total Messages
df.shape[0]



"""#Total numbers of words writen by all"""

#Total Number of words
words = []
for message in df['message']:
  words.extend(message.split())

print(len(words))

"""#How many media files are shared"""

#Number of Media Files shared
df[df['message'] == '<Media omitted>\n'].shape[0]

"""#How many links are shared"""

#Number of Links Shared
from urlextract import URLExtract
extract = URLExtract()

links = []
for message in df['message']:
    links.extend(extract.find_urls(message))

print(len(links))

"""#Heighest Numbers of Massages Done by"""

import matplotlib.pyplot as plt

x = df['user'].value_counts().head()
user_names = x.index
msg_count = x.values

plt.bar(user_names, msg_count)
plt.xticks(rotation='vertical')
plt.show()

"""#Getting the data of users in the form of table

"""

new_df = round(((df['user'].value_counts() / df.shape[0]) * 100), 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})

new_df.head()

!pip install wordcloud

import string

def remove_stop_words(message):
  f = open('WhatsApp Chat with DSGRG Pitchers Startup.txt', 'r')
  stop_words = f.read()
  y = []
  for word in message.lower().split():
      if word not in stop_words:
          y.append(word)
  return " ".join(y)

def remove_punctuation(message):
  x = re.sub('[%s]'% re.escape(string.punctuation), '', message)
  return x

#Data Cleaning
temp = df[df['user'] != 'group_notification'] #remove group notification
temp = temp[temp['message'] != '<Media omitted>\n'] #remove media message
temp['message'] = temp['message'].apply(remove_stop_words) #remove stopwords
temp['message'] = temp['message'].apply(remove_punctuation) #remove punctuations

#Draw the wordCloud
from wordcloud import WordCloud
plt.figure(figsize=(20, 10))
wc = WordCloud(width=1000,height=750,min_font_size=10,background_color='white')
cloud = wc.generate(temp['message'].str.cat(sep=" "))
plt.imshow(cloud)

#Most common words
temp = df[df['user'] != 'group_notification'] #remove group notification
temp = temp[temp['message'] != '<Media omitted>\n']  #remove media msg
temp['message'] = temp['message'].apply(remove_stop_words) #remove stop words
temp['message'] = temp['message'].apply(remove_punctuation) #remove punctuations

words = []
for message in temp['message']:
  words.extend(message.split())

#apply counter
from collections import Counter
most_common_df = pd.DataFrame(Counter(words).most_common(20))
most_common_df

!pip install emoji

#Emoji counter
import emoji

emojis = []
for message in df['message']:
  emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

#Mothaly chat timeline
timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
month_timeline = []

for i in range(timeline.shape[0]):
  month_timeline.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

timeline['time'] = month_timeline

#draw plot
plt.figure(figsize=(12,6))
plt.plot(timeline['time'], timeline['message'])
plt.xticks(rotation='vertical')
plt.show()

#daily timeline
daily_timeline = df.groupby('only_date').count()['message'].reset_index()

plt.figure(figsize=(12,6))
plt.plot(daily_timeline['only_date'], daily_timeline['message'])
plt.show

#activity map on day based
busy_day = df['day_name'].value_counts()
plt.figure(figsize=(12, 6))
plt.bar(busy_day.index, busy_day.values, color='purple')
plt.title("Busy Day")
plt.xticks(rotation='vertical')
plt.show()

#monthaly activity map

busy_month = df['month'].value_counts()
plt.figure(figsize=(12, 6))
plt.bar(busy_month.index, busy_month.values, color='orange')
plt.title("Busy Month")
plt.xticks(rotation='vertical')
plt.show()

#Which time we are active most
import seaborn as sns
plt.figure(figsize=(18, 9))
sns.heatmap(df.pivot_table(index='day_name', columns='period', values='message',
            aggfunc='count').fillna(0))
plt.yticks(rotation='vertical')
plt.show()

# Import the necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Create the datasets
heights = np.array([65, 68, 72, 70, 67])
weights = np.array([140, 150, 160, 155, 145])

# Calculate the Pearson correlation coefficient
r = np.corrcoef(heights, weights)[0, 1]

# Print the Pearson correlation coefficient
print(r)