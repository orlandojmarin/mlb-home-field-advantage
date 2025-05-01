import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
 
# Load your data
url = "https://raw.githubusercontent.com/orlandojmarin/mlb-home-field-advantage/refs/heads/main/mlb_data.csv"
df = pd.read_csv(url)
 
# Set up Streamlit app
st.title("MLB Home Field Advantage Analysis ⚾")
 
st.markdown("---")
 
st.markdown("This visualization compares **MLB league-wide home vs. away performance**. Use the dropdown above to switch between batting and pitching metrics.")
 
# Dropdown to select Batting or Pitching
option = st.selectbox(
    "Select Performance Type:",
    ("Batting", "Pitching")
)
 
# Calculate league-wide totals and create figure
if option == "Batting":
    total_runs_home = df["runs_scored_home"].sum()
    total_runs_away = df["runs_scored_away"].sum()
    total_hr_home = df["home_runs_home"].sum()
    total_hr_away = df["home_runs_away"].sum()
 
    # Set up categories and totals
    categories = ["Runs Scored", "Home Runs"]
    home_totals = [total_runs_home, total_hr_home]
    away_totals = [total_runs_away, total_hr_away]
 
    # Set x positions for each category
    x = range(len(categories))  # [0, 1]
    width = 0.35  # width of each bar
 
    # Calculate x positions for the Home and Away bars
    x_home = [pos - width/2 for pos in x]  # Home bars shifted left
    x_away = [pos + width/2 for pos in x]  # Away bars shifted right
 
    # Plot the bars
    fig, ax = plt.subplots(figsize=(10, 8))
    bars_home = ax.bar(x_home, home_totals, width, label="Home")
    bars_away = ax.bar(x_away, away_totals, width, label="Away")
 
    # Add value labels above each bar
    for bar in bars_home + bars_away:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 5),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)
 
    # Customize the plot
    ax.set_ylabel("Total")
    ax.set_title("MLB League-Wide Batting Performance (Home vs Away)")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
 
    st.pyplot(fig)
 
elif option == "Pitching":
    # Calculate league-wide totals for pitching
    total_walks_home = df["walks_home"].sum()
    total_walks_away = df["walks_away"].sum()
    total_strikeouts_home = df["strikeouts_home"].sum()
    total_strikeouts_away = df["strikeouts_away"].sum()
 
    # Set up categories and totals
    categories = ["Walks Allowed", "Strikeouts"]
    home_totals = [total_walks_home, total_strikeouts_home]
    away_totals = [total_walks_away, total_strikeouts_away]
 
    # Set x positions for each category
    x = range(len(categories))  # [0, 1]
    width = 0.35  # width of each bar
 
    # Calculate x positions for the Home and Away bars
    x_home = [pos - width/2 for pos in x]  # Home bars shifted left
    x_away = [pos + width/2 for pos in x]  # Away bars shifted right
 
    # Plot the bars
    fig, ax = plt.subplots(figsize=(10, 8))  # Adjusted height
    bars_home = ax.bar(x_home, home_totals, width, label="Home")
    bars_away = ax.bar(x_away, away_totals, width, label="Away")
 
    # Add value labels above each bar
    for bar in bars_home + bars_away:
        height = bar.get_height()
        ax.annotate(f'{int(height)}',
                    xy=(bar.get_x() + bar.get_width()/2, height),
                    xytext=(0, 5),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)
 
    # Customize the plot
    ax.set_ylabel("Total")
    ax.set_title("MLB League-Wide Pitching Performance (Home vs Away)")
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
 
    st.pyplot(fig)

# Load data
url = "https://raw.githubusercontent.com/orlandojmarin/mlb-home-field-advantage/refs/heads/main/mlb_data.csv"
df = pd.read_csv(url)
 
# Calculate home and away win percentages
df["home_win_pct"] = df["home_wins"] / (df["home_wins"] + df["home_losses"])
df["away_win_pct"] = df["away_wins"] / (df["away_wins"] + df["away_losses"])
df["home_advantage_score"] = df["home_win_pct"] - df["away_win_pct"]
 
# Create color column based on home_advantage_score (no lambda)
colors = []
for score in df["home_advantage_score"]:
    if score > 0:
        colors.append("green")
    else:
        colors.append("red")
df["advantage_color"] = colors
 
# App title and description
st.title("MLB Home Field Advantage Analysis ⚾")
 
st.markdown("""
This visualization explores whether **elevation** or **attendance** affects a team's **home field advantage**.
Hover over a point to see the team name and values.
""")
 
# Dropdown: Elevation or Attendance
factor = st.selectbox("Select a Factor:", ("Elevation", "Attendance"))
 
# Choose x-axis column and label
if factor == "Elevation":
    x_col = "elevation_ft"
    x_label = "Ballpark Elevation (ft)"
else:
    x_col = "avg_attendance_home"
    x_label = "Average Home Game Attendance"
 
y_col = "home_advantage_score"
y_label = "Home Advantage Score"
 
fig = px.scatter(
    df,
    x=x_col,
    y=y_col,
    color="advantage_color",
    hover_name="team_name",  # ✅ shows team name on hover
    custom_data=[x_col, y_col],
    labels={x_col: x_label, y_col: y_label},
    title=f"{factor} vs Home Field Advantage",
    color_discrete_map={"green": "green", "red": "red"}
)
 
fig.update_traces(
    marker=dict(size=10),
    hovertemplate=
        "<b>%{hovertext}</b><br>" +  # ✅ now using hovertext
        f"{x_label}: %{{customdata[0]:,.0f}}<br>" +
        f"{y_label}: %{{customdata[1]:.4f}}" +
        "<extra></extra>"
)
 
# Clean up layout
fig.update_layout(
    xaxis_title=x_label,
    yaxis_title=y_label,
    title_x=0.5,
    height=600,
    showlegend=False  # hide green/red legend
)
 
# Show the plot
st.plotly_chart(fig, use_container_width=True)
 
# Optional caption to explain color
st.caption("Green = positive home field advantage, Red = neutral or negative")

