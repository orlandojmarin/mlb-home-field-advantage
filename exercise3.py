import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set up the Streamlit app title
st.title('Diabetes Insulin Level Distribution')
st.subheader("Orlando Marin")

# Read the dataset
data_url = "https://storage.googleapis.com/scsu-data-science/diabetes_nan.csv"
diabetes = pd.read_csv(data_url)

# Fill NaN "Insulin" values with the average insulin level
diabetes['Insulin'].fillna(diabetes['Insulin'].mean(), inplace=True)

# Filter dataset to include only relevant columns
diabetes_filtered = diabetes[["Insulin", "Outcome"]]

# Option to show the raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw Data')
    st.write(diabetes)

# Add a separator
st.markdown('---')

# Add a subheader for selecting the group (Diabetic or Non-Diabetic)
st.subheader('Select the group for insulin level distribution')

# Radio button for selecting "Diabetic" or "Non-Diabetic"
outcome_selection = st.radio("Select the group:", ["Non-Diabetic", "Diabetic"])

# Map the radio button selection to the corresponding "Outcome" values
if outcome_selection == "Diabetic":
    filtered_data = diabetes_filtered[diabetes_filtered["Outcome"] == 1]
    group_label = "Diabetic"
else:
    filtered_data = diabetes_filtered[diabetes_filtered["Outcome"] == 0]
    group_label = "Non-Diabetic"

# Create insulin level bins for categorizing
bins = list(range(0, 400, 25))  # Bins every 25 units
labels = [f"{bins[i]}-{bins[i + 1]}" for i in range(len(bins) - 1)]

# Categorize insulin levels into the defined bins
filtered_data["Insulin Range"] = pd.cut(filtered_data["Insulin"], bins=bins, labels=labels)

# Count the number of people in each insulin level range
insulin_counts = filtered_data["Insulin Range"].value_counts().sort_index()

# Create a bar plot for insulin level distribution
fig, ax = plt.subplots(figsize=(12, 6))
insulin_counts.plot(kind='bar', color='skyblue', ax=ax)

# Set the plot's title and axis labels
ax.set_title(f"Insulin Level Distribution for {group_label} Patients")
ax.set_xlabel("Insulin Range")
ax.set_ylabel("Number of People")

# Rotate the x-axis labels for better readability
ax.set_xticklabels(insulin_counts.index, rotation=45)

# Set fixed y-axis range from 0 to 250
ax.set_ylim(0, 250)

# Set fixed x-axis range based on the number of insulin range bins
ax.set_xlim(-0.5, len(insulin_counts) - 0.5)

# Display the bar chart in Streamlit
st.pyplot(fig)





