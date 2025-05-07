
# Import necessary libraries
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
 
# --- Load and Prepare the Dataset ---
# Load the CSV file from the provided URL
df = pd.read_csv("https://raw.githubusercontent.com/iantonios/dsc205/refs/heads/main/CT-towns-income-census-2020.csv")

# Strip any leading or trailing spaces in column names to avoid KeyErrors
df.columns = df.columns.str.strip()

# --- Data Cleaning ---
# Remove dollar signs and commas from income columns and convert them to integers
df['Per capita income'] = df['Per capita income'].str.replace('$', '').str.replace(',', '').astype(int)
df['Median household income'] = df['Median household income'].str.replace('$', '').str.replace(',', '').astype(int)
df['Median family income'] = df['Median family income'].str.replace('$', '').str.replace(',', '').astype(int)

# --- Streamlit App: Titles and Data Display ---
# Display team member names and dataset title
st.header("Jessica Morrill, Orlando Marin")
st.title("CT Census Data (2020)")

# Display the full dataset with a fixed width and height
st.dataframe(df, width=800, height=200)

# --- Question 1: Filter by County ---
# Display subheader for county selection
st.subheader("CT towns in the selected county")

# Create a list of unique counties for the selectbox
county_list = df['County'].drop_duplicates().tolist()

# Selectbox to choose a county
county = st.selectbox("Select County: ", county_list)

# Filter the dataset based on the selected county
df_county = df.loc[df['County'] == county]

# Display the filtered dataset for the selected county
st.dataframe(df_county, width=800, height=200)

# --- Question 2: Filter by Income Range ---
# Add slider to select a range of median household income
values = st.slider(
    "Select Range of Median Household Income", 
    min_value=0, 
    max_value=250000, 
    value=(50000, 100000)
)

# Filter the county dataset by the selected income range
df_range = df_county[
    (df_county['Median household income'] >= values[0]) & 
    (df_county['Median household income'] <= values[1])
]

# Display the filtered towns based on income range
st.subheader(f"Towns with Median Household Income between {values[0]:,} and {values[1]:,} US dollars")
st.dataframe(df_range, width=800, height=200)

# --- Question 3: Bonus - Display Top and Bottom 5 Cities by Income ---
st.subheader("Highest and Lowest Median Household Incomes by City")

# Sort the entire dataset by median household income
df_sorted = df.sort_values("Median household income")

# Select the top 5 and bottom 5 cities
top_5 = df_sorted.tail(5)
bottom_5 = df_sorted.head(5)

# Combine the top and bottom 5 cities into a single dataframe
df_combined = pd.concat([top_5, bottom_5])

# Create a bar chart for the top and bottom 5 cities by income
plt.figure(figsize=(12, 6))  # Set figure size
plt.bar(df_combined["Place"], df_combined["Median household income"], color="skyblue")
plt.xlabel("City")
plt.ylabel("Median Household Income")
plt.xticks(rotation=45)
plt.title("Top and Bottom 5 Cities by Median Household Income (US Dollars)")

# Display the bar chart in the Streamlit app
st.pyplot(plt)
