import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import folium
from streamlit_folium import st_folium
 
# Load data
url = "https://raw.githubusercontent.com/orlandojmarin/mlb-home-field-advantage/refs/heads/main/mlb_data.csv"
df = pd.read_csv(url)
 
# Set up Streamlit app
st.title("MLB Home Field Advantage Analysis ⚾")
 
st.markdown("---")

# FIGURE 1: DOUBLE BAR GRAPHS
### add a subheader to title the first figure
### move the sentence that's currently above figure 1 below it so it serves as the "caption"
### move legend to top left corner for the PITCHING view
 
st.subheader("MLB Teams Bat and Pitch Better at Home")
 
# Dropdown to select Batting or Pitching
option = st.selectbox(
    "Use the dropdown below to switch between batting and pitching metrics:",
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

    # Plot the bars with custom colors
    fig, ax = plt.subplots(figsize=(10, 8))
    bars_home = ax.bar(x_home, home_totals, width, label="Home", color="#002D72", edgecolor="black")
    bars_away = ax.bar(x_away, away_totals, width, label="Away", color="#d9d9d9", edgecolor="black")

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

    # Set up categories and totals (strikeouts first)
    categories = ["Strikeouts", "Walks"]
    home_totals = [total_strikeouts_home, total_walks_home]
    away_totals = [total_strikeouts_away, total_walks_away]

    # Set x positions for each category
    x = range(len(categories))  # [0, 1]
    width = 0.35  # width of each bar

    # Calculate x positions for the Home and Away bars
    x_home = [pos - width/2 for pos in x]  # Home bars shifted left
    x_away = [pos + width/2 for pos in x]  # Away bars shifted right

    # Plot the bars with custom colors
    fig, ax = plt.subplots(figsize=(10, 8))
    bars_home = ax.bar(x_home, home_totals, width, label="Home", color="#002D72", edgecolor="black")
    bars_away = ax.bar(x_away, away_totals, width, label="Away", color="#d9d9d9", edgecolor="black")

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

st.markdown("""
This visualization compares league-wide batting and pitching performance at home vs. away.  

Teams scored 1.46% more runs at home and hit 1.04% more home runs at home, suggesting a modest offensive boost at home ballparks.  

On the pitching side, teams recorded 8.63% more strikeouts at home, indicating stronger pitching effectiveness on home turf. However, teams also issued 2.83% fewer walks at home, which is desirable, as fewer walks allowed reduces opponent scoring chances.  

Overall, these differences reflect a consistent home field advantage across both batting and pitching metrics.
""")
 
st.markdown("---")
 
###############################################

# FIGURE 2: BOX PLOTS

st.subheader("Distribution of Runs, Home Runs, Strikeouts, or Walks (Home vs Away)")

# Dropdown for metric selection
metric = st.selectbox(
    "Use the dropdown below to switch between runs, home runs, strikeouts, and walks:",
    ("Runs", "Home Runs", "Strikeouts", "Walks")
)

# Map user-friendly labels to actual column names in the dataset
metric_columns = {
    "Runs": ("runs_scored_home", "runs_scored_away"),
    "Home Runs": ("home_runs_home", "home_runs_away"),
    "Strikeouts": ("strikeouts_home", "strikeouts_away"),
    "Walks": ("walks_home", "walks_away")
}

home_col, away_col = metric_columns[metric]

# Prepare the data in long format for box plot
data = pd.DataFrame({
    "Performance": df[home_col].tolist() + df[away_col].tolist(),
    "Location": ["Home"] * len(df) + ["Away"] * len(df)
})

# Create box plot with custom colors
fig = px.box(
    data,
    x="Location",
    y="Performance",
    color="Location",
    color_discrete_map={
        "Home": "#002D72",    # Navy
        "Away": "#d9d9d9"     # Light gray
    }
)

# Make the Away box plot fully opaque and darken its outline
for trace in fig.data:
    if trace.name == "Away":
        trace.fillcolor = "rgba(217,217,217,1)"  # solid light gray
        trace.line.color = "#4D4D4D"             # dark gray border

# Update layout with proper centering, padding, and visual spacing
fig.update_layout(
    title=dict(
        text=f"{metric} Distribution: Home vs Away",
        x=0.5,
        xanchor="center",  # ✅ truly centers the title
        font=dict(size=20, color='black')
    ),
    plot_bgcolor='white',
    paper_bgcolor='#f5f5f5',  # light gray around plot to give border effect
    margin=dict(l=40, r=40, t=60, b=60),  # ✅ clean spacing on all sides
    font=dict(color='black', size=14),
    showlegend=False,
    xaxis_title="Location",
    yaxis_title=metric,
    xaxis=dict(
        title_font=dict(color='black', size=16),
        tickfont=dict(color='black', size=14)
    ),
    yaxis=dict(
        title_font=dict(color='black', size=16),
        tickfont=dict(color='black', size=14)
    )
)

# Show the plot
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")





###############################################
    
# FIGURE 3: SCATTER PLOTS
 
st.subheader("Correlation between Elevation or Attendance on Home Field Advantage")
 
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
 
# Caption to explain color
st.caption("Green = positive home field advantage, Red = neutral or negative")
 
st.caption("""
This visualization explores whether **elevation** or **attendance** affects a team's **home field advantage**.
Hover over a point to see the team name and values.
""")
 
st.markdown("---")
 
###############################################


#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# BUBBLE CHART

# Calculate home run difference
df["hr_diff"] = df["home_runs_home"] - df["home_runs_away"]

# Create interactive bubble chart
fig = px.scatter(
    df,
    x="max_wall_height_ft",
    y="hr_diff",
    size="avg_attendance_home",
    hover_name="team_name",
    color="hr_diff",
    color_continuous_scale="RdYlGn",
    labels={
        "max_wall_height_ft": "Max Wall Height (ft)",
        "hr_diff": "Home Run Difference (Home - Away)",
        "avg_attendance_home": "Avg Home Attendance"
    },
    title="🏟️ Max Wall Height vs Home Run Difference"
)

# Customize hover template
fig.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>" +
                  "Max Wall Height: %{x} ft<br>" +
                  "HR Difference: %{y}<br>" +
                  "Avg Attendance: %{marker.size:,}<extra></extra>"
)

# Center and scale layout
fig.update_layout(
    title_x=0.5,
    height=600,
    xaxis=dict(tickformat=".0f"),
    yaxis=dict(title="Home Runs (Home - Away)"),
    coloraxis_colorbar=dict(title="HR Difference"),
    showlegend=False
)

# Display in Streamlit
st.subheader("🏟️ Max Wall Height vs Home Run Difference")
st.markdown("**Each bubble represents a team. Size = Avg Home Attendance. Hover to view details.**")
st.plotly_chart(fig, use_container_width=True)
st.caption("Each bubble represents an MLB team. The x-axis shows the stadium's maximum wall height, while the y-axis shows the difference in home runs hit at home versus away. Bubble size reflects average home attendance. Hover to view team details.")

# add a horizontal line to divide the section
st.markdown("---") 

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# MAP VISUALIZATION

# Calculate win percentages with safer denominator handling
df["home_win_pct"] = df["home_wins"] / df[["home_wins", "home_losses"]].sum(axis=1)
df["away_win_pct"] = df["away_wins"] / df[["away_wins", "away_losses"]].sum(axis=1)
df["home_advantage_score"] = df["home_win_pct"] - df["away_win_pct"]

# Normalize attendance for bubble scaling
min_att = df["avg_attendance_home"].min()
max_att = df["avg_attendance_home"].max()

# Initialize a colorful Folium map (switch from CartoDB to OpenStreetMap)
m = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles="OpenStreetMap")

# Add a circle marker for each stadium
for _, row in df.iterrows():
    lat = row["ballpark_lat"]
    lon = row["ballpark_long"]
    team = row["team_name"]
    stadium = row["ballpark"]
    score = row["home_advantage_score"]
    attendance = row["avg_attendance_home"]

    # Choose color based on home field advantage
    color = "green" if score > 0 else "red"

    # Normalize and cap bubble radius
    normalized = (attendance - min_att) / (max_att - min_att)
    radius = max(5, min(20, 5 + 15 * normalized))  # Clamp between 5 and 20

    # Popup info
    popup = folium.Popup(
        f"<b>{team}</b><br>"
        f"Stadium: {stadium}<br>"
        f"Home Advantage Score: {score:.3f}<br>"
        f"Avg Attendance: {attendance:,.0f}",
        max_width=300
    )

    folium.CircleMarker(
        location=[lat, lon],
        radius=radius,
        color=color,
        fill=True,
        fill_opacity=0.7,
        popup=popup
    ).add_to(m)

# ✅ Use a container to isolate the layout and reduce space issues
with st.container():
    st.subheader("📍 MLB Stadium Map: Home Field Advantage")
    st.markdown("**Bubble color = Home Advantage Score (green = positive), Size = Avg Home Attendance**")
    st.caption("Each bubble represents an MLB stadium. Green bubbles indicate a positive home field advantage, while red bubbles indicate neutral or negative advantage. Bubble size reflects average home game attendance.")
    st_folium(m, width=700, height=400) 

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -







