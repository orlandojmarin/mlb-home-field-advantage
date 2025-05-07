import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
 
url = "https://raw.githubusercontent.com/iantonios/dsc205/refs/heads/main/bike_sharing.csv"
 
df = pd.read_csv(url)
 
# add a title to the streamlit app
st.title("Team Members: Jessica Morrill, Orlando Marin, Tatiana Eng")
 
# insert a horizontal line
st.markdown("---")
 
# add a title above the dataframe
st.subheader("Bicycle Ridership Data: January 2011 - December 2012")
 
# display df in streamlit app
st.dataframe(df, width=800, height=400)
 
# insert a horizontal line
st.markdown("---")
 
########################################
 
# convert date column to datetime
df['dteday'] = pd.to_datetime(df['dteday'])
 
# set date as index for easier time-based operations
df.set_index('dteday', inplace=True)
 
# resample using 'MS' so dates are aligned to the start of the month
monthly_data = df['cnt'].resample('MS').sum()
 
# generate list of monthly tick marks from Jan 2011 to Dec 2012
tick_dates = pd.date_range(start='2011-01-01', end='2012-12-01', freq='MS')
 
# add a subheader before the figure
st.subheader("Total Ridership Over Time")
 
# create line plot
fig, ax = plt.subplots(figsize=(12,5))
ax.plot(monthly_data.index, monthly_data.values, marker='o')
ax.set_xlabel("Date")
ax.set_ylabel("Total Riders")
ax.set_title("Monthly Total Ridership")
 
# set custom ticks for each month and format
ax.set_xticks(tick_dates)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # format month to be like "Jan 2011"
plt.setp(ax.get_xticklabels(), rotation=60, ha='right')
 
st.pyplot(fig)
 
########################################
 
# insert a horizontal line
st.markdown("---")
 
# add a subheader before the figure
st.subheader("Total Ridership Each Season")
 
# create bar plot of total ridership by season
season_map = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
df['season_name'] = df['season'].map(season_map)
season_totals = (
    df.groupby('season_name')['cnt']
    .sum()
    .reindex(["Winter", "Spring", "Summer", "Fall"])
)
 
fig2, ax2 = plt.subplots(figsize=(8, 5))
season_totals.plot(kind='bar', ax=ax2, color='skyblue', edgecolor='black')
 
ax2.set_xlabel("Season")
ax2.set_ylabel("Total Riders")
ax2.set_title("Total Ridership by Season")
 
# prevent labels from overlapping or rotating
ax2.set_xticklabels(season_totals.index, rotation=0)
 
# "zoom out" by setting a higher y-limit
ax2.set_ylim(0, season_totals.max() * 1.1)
 
# show full number format instead of scientific notation
ax2.ticklabel_format(style='plain', axis='y')
 
# add value labels
for i, v in enumerate(season_totals):
    ax2.text(i, v + season_totals.max() * 0.02, f'{v:,.0f}', ha='center', va='bottom')
 
st.pyplot(fig2)
 
########################################
 
# insert a horizontal line
st.markdown("---")
 
# add subheader
st.subheader("Rolling Average Ridership")
 
# create a radio button
rolling_option = st.radio("Select one of the following:", ("7-day average", "14-day average", "Total ridership by week"))
 
# create plot
fig3, ax3 = plt.subplots(figsize=(12, 5))
 
if rolling_option == "7-day average":
    df['rolling'] = df['cnt'].rolling(window=7).mean()
    ax3.plot(df.index, df['rolling'], label="7-day Average", color='green')
    title = "Rolling Average Over a 7-day Period"
 
elif rolling_option == "14-day average":
    df['rolling'] = df['cnt'].rolling(window=14).mean()
    ax3.plot(df.index, df['rolling'], label="14-day Average", color='blue')
    title = "Rolling Average Over a 14-day Period"
 
else:
    weekly_totals = df['cnt'].resample('W').sum()
    ax3.plot(weekly_totals.index, weekly_totals.values, label="Weekly Total", color='orange')
    title = "Total Ridership Each Week"
 
ax3.set_xlabel("Date")
ax3.set_ylabel("Riders")
ax3.set_title(title)
ax3.legend()
 
# format x-axis tick marks
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')
 
st.pyplot(fig3)