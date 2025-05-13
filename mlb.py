import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
 
# Load data
url = "https://raw.githubusercontent.com/orlandojmarin/mlb-home-field-advantage/refs/heads/main/mlb-data.csv"
df = pd.read_csv(url)
 
# Set up Streamlit app
st.title("MLB Home Field Advantage Analysis ⚾")
 
st.markdown("---")

###############################################

# FIGURE 1: HOME VS AWAY WIN PERCENTAGE SCATTER PLOT

st.subheader("Win Rates Show That Home Field Matters in Major League Baseball")

with st.expander("How to read this scatter plot"):
    st.markdown("""
    This scatter plot shows each MLB team's home win percentage versus away win percentage.  
    Each point represents a team, labeled by its abbreviation.

    - **Above the diagonal line** = better performance at home  
    - **Below the line** = better performance on the road  
    - **Color intensity** reflects the size of the team's home field advantage score  
    - **Hover** over a point to view the team's full name, win percentages, and advantage score
    """)

# Calculate win percentages
df["home_win_pct"] = df["home_wins"] / (df["home_wins"] + df["home_losses"])
df["away_win_pct"] = df["away_wins"] / (df["away_wins"] + df["away_losses"])
df["home_field_advantage"] = df["home_win_pct"] - df["away_win_pct"]

# Create the scatter plot
fig = go.Figure()

# Add team points
fig.add_trace(go.Scatter(
    x=df["away_win_pct"],
    y=df["home_win_pct"],
    mode="markers+text",
    text=df["team_abv"],  # Still shows abbreviations on the plot
    hovertext=df["team_name"],  # Full name on hover
    textposition="bottom center",
    textfont=dict(size=14, color="black"),
    cliponaxis=False,
    marker=dict(
        size=10,
        color=df["home_field_advantage"],
        colorscale="Blues",
        colorbar=dict(title="Home<br>Advantage"),
        line=dict(width=1, color="black")
    ),
    hovertemplate=(
    "<b>%{hovertext}</b><br>" +
    "Home Win %: %{y:.3f}<br>" +
    "Away Win %: %{x:.3f}<br>" +
    "Home Field Advantage %: %{marker.color:.3f}<extra></extra>"
    )
))

# Add diagonal reference line (y = x)
fig.add_trace(go.Scatter(
    x=[0, 1],
    y=[0, 1],
    mode="lines",
    line=dict(dash="dash", color="gray"),
    showlegend=False
))

# Centered and styled layout
fig.update_layout(
    title=dict(
        text="Home vs. Away Win Percentage by Team",
        x=0.5,
        xanchor="center",
        font=dict(size=22, color="black")
    ),
    height=650,
    plot_bgcolor="white",
    paper_bgcolor="#f5f5f5",
    font=dict(color="black", size=14),
    margin=dict(l=50, r=50, t=70, b=70),
    showlegend=False,
    xaxis=dict(
        title="Away Win %",
        range=[0.3, 0.7],
        title_font=dict(size=18, color="black"),
        tickfont=dict(size=14, color="black")
    ),
    yaxis=dict(
        title="Home Win %",
        range=[0.3, 0.7],
        title_font=dict(size=18, color="black"),
        tickfont=dict(size=14, color="black")
    )
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Caption
with st.expander("Show caption and interpretation"):
    st.markdown("""
    This visualization compares each MLB team's home and away win percentages using a scatter plot.

    Out of 30 teams, 22 (73%) performed better at home (above the diagonal line), 3 (10%) performed the same at home and on the road (on the line), and only 5 (17%) performed better on the road (below the line).

    These results provide strong evidence of a league-wide home field advantage, with nearly three-quarters of MLB teams winning more frequently at home than on the road.
    """)


st.markdown("---")

###############################################

# FIGURE 2: DOUBLE BAR GRAPHS
### add a subheader to title the first figure
### move the sentence that's currently above figure 1 below it so it serves as the "caption"
### move legend to top left corner for the PITCHING view
 
st.subheader("MLB Totals Reveal Stronger Pitching and Slight Offensive Boost at Home")
 
# Dropdown to select Batting or Pitching
option = st.selectbox(
    "Use the dropdown below to switch between pitching and batting metrics:",
    ("Pitching", "Batting")
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

with st.expander("Show caption and interpretation"):
    st.markdown("""
    This bar graph visualization compares league-wide batting and pitching performance at home vs. away.

    On the pitching side, teams recorded 8.63% more strikeouts at home, indicating stronger pitching effectiveness at home. Teams also issued 2.83% fewer walks at home, which is desirable, as fewer walks allowed reduces opponent scoring chances.  

    Teams scored 1.46% more total runs at home and hit 1.04% more home runs at home, suggesting a modest offensive boost at home ballparks.  

    Overall, these differences reflect a consistent home field advantage across both pitching and batting metrics.
    """)
 
st.markdown("---")
 
###############################################

# FIGURE 3: BOX PLOTS

st.subheader("Pitching Fuels MLB Home Field Advantage More Than Hitting")

# Dropdown for metric selection
metric = st.selectbox(
    "Use the dropdown below to switch between strikeouts, walks, runs, and home runs:",
    ("Strikeouts", "Walks", "Runs", "Home Runs")
)

# Map user-friendly labels to column names in the dataset
metric_columns = {
    "Strikeouts": ("strikeouts_home", "strikeouts_away"),
    "Walks": ("walks_home", "walks_away"),
    "Runs": ("runs_scored_home", "runs_scored_away"),
    "Home Runs": ("home_runs_home", "home_runs_away")
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
        xanchor="center",  # truly centers the title
        font=dict(size=20, color='black')
    ),
    plot_bgcolor='white',
    paper_bgcolor='#f5f5f5',  # light gray around plot to give border effect
    margin=dict(l=40, r=40, t=60, b=60),  # clean spacing on all sides
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

with st.expander("Show caption and interpretation"):
    st.markdown("""
    This box plot visualization shows the distribution of team-level performance metrics at home vs. away.

    Median values show that teams hit a nearly identical number of runs at home (343) and away (352), and hit a nearly identical number of home runs at home (86) and away (87.5). These offensive numbers may be partially explained by the fact that home teams do not bat in the 9th inning if they are already winning.

    On the pitching side, teams recorded more strikeouts at home (719) than away (658.5), and issued slightly fewer walks at home (241.5) than away (255). This is especially notable since home teams may pitch more total innings, yet still have fewer walks at home than on the road.

    These patterns suggest that home field advantage in baseball is most evident on the pitching side, where home teams demonstrate more effective control and dominance on the mound.
    """)

st.markdown("---")

###############################################

# FIGURE 4: MILES TRAVELED SCATTER PLOT VISUALIZATION

st.subheader("More Travel, More Trouble? Road Fatigue and Home Field Advantage")

with st.expander("How to read this scatter plot"):
    st.markdown("""
    This scatter plot shows the relationship between the **total miles traveled** by each MLB team and their **home field advantage score** in 2022.

    - **Higher up = stronger home field advantage**  
    - **Farther right = more miles traveled**  
    - Each point represents a team (abbreviation shown)  
    - Hover over a point to view full team name, travel miles, and advantage score  
    - A **trendline** has been added to show the overall direction of the relationship
    """)

import numpy as np

# Prepare data
x = df["miles_traveled"]
y = df["home_field_advantage"]

# Fit a linear regression model
slope, intercept = np.polyfit(x, y, 1)
line_x = np.linspace(x.min(), x.max(), 100)
line_y = slope * line_x + intercept

# Create the scatter plot
fig = go.Figure()

# Team data points
fig.add_trace(go.Scatter(
    x=x,
    y=y,
    mode="markers+text",
    text=df["team_abv"],
    hovertext=df["team_name"],
    textposition="bottom center",
    textfont=dict(size=14, color="black"),
    cliponaxis=False,
    marker=dict(
        size=10,
        color=y,
        colorscale="Blues",
        colorbar=dict(title="Home<br>Advantage"),
        line=dict(width=1, color="black")
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>" +
        "Miles Traveled: %{x:,.0f}<br>" +
        "Home Field Advantage: %{y:.3f}<extra></extra>"
    )
))

# Add trendline
fig.add_trace(go.Scatter(
    x=line_x,
    y=line_y,
    mode="lines",
    line=dict(color="gray", dash="dash"),
    name="Trendline",
    hoverinfo="skip"
))

# Layout styling
fig.update_layout(
    title=dict(
        text="Miles Traveled vs Home Field Advantage by Team",
        x=0.5,
        xanchor="center",
        font=dict(size=22, color="black")
    ),
    height=650,
    plot_bgcolor="white",
    paper_bgcolor="#f5f5f5",
    font=dict(color="black", size=14),
    margin=dict(l=50, r=50, t=70, b=70),
    showlegend=False,
    xaxis=dict(
        title="Total Miles Traveled in 2022",
        title_font=dict(size=18, color="black"),
        tickfont=dict(size=14, color="black")
    ),
    yaxis=dict(
        title="Home Field Advantage Score",
        title_font=dict(size=18, color="black"),
        tickfont=dict(size=14, color="black")
    )
)

st.plotly_chart(fig, use_container_width=True)

with st.expander("Show caption and interpretation"):
    st.markdown("""
    This scatter plot visualization explores whether travel demands contribute to home field advantage in Major League Baseball.

    - Teams that traveled more than 35,000 miles during the 2022 season averaged a home field advantage score of 0.026, compared to 0.084 for those under 35k — a 223% difference.
    - The dashed trendline shows a slight negative relationship between miles traveled and home field advantage — supporting the idea that excessive travel may negatively impact performance.

    While not the sole cause, travel appears to be one contributing factor to MLB’s home field advantage pattern.
    """)

st.markdown("---")

###############################################
# FIGURE 5: MAP VISUALIZATION WITH ENVIRONMENT AND PARK TABS

# Ensure required calculations exist
df["home_win_pct"] = df["home_wins"] / (df["home_wins"] + df["home_losses"])
df["away_win_pct"] = df["away_wins"] / (df["away_wins"] + df["away_losses"])
df["home_field_advantage_score"] = df["home_win_pct"] - df["away_win_pct"]
df["attendance_rate"] = df["avg_attendance_home"] / df["seat_capacity"]

# Normalize miles_traveled for marker sizing (shared across both tabs)
max_miles = df["miles_traveled"].max()
min_miles = df["miles_traveled"].min()

# Create tabs for two different map views
tab1, tab2 = st.tabs(["🌦️ Environmental Factors", "🏟️ Park Factors"])

# ---------- TAB 1: ENVIRONMENTAL FACTORS ----------
with tab1:
    st.subheader("🌦️ Stadium Environment and Home Field Advantage")

    st.markdown("**Marker color = Home Advantage Score (green = positive, red = neutral or negative)**  \n"
                "**Marker size = Total Miles Traveled in 2022**")

    with st.expander("Show caption and interpretation"):
        st.markdown("""
        This map highlights each stadium's environmental conditions and their home field advantage in 2022.

        - **Green markers** = stronger home performance  
        - **Red markers** = equal or worse performance at home  
        - **Larger markers** = more miles traveled by the team in 2022  
        - Hover to explore temperature, elevation, roof usage, day games, and travel distance  
        """)

    m_env = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles="OpenStreetMap")

    for _, row in df.iterrows():
        lat = row["ballpark_lat"]
        lon = row["ballpark_long"]
        team = row["team_name"]
        stadium = row["ballpark"]
        hfa = row["home_field_advantage_score"]
        temp = row["avg_temp_f"]
        elev = row["elevation_ft"]
        roof = row["roof_pct"]
        day = row["daytime_pct"]
        miles = row["miles_traveled"]

        color = "green" if hfa > 0 else "red"
        radius = 5 + 10 * ((miles - min_miles) / (max_miles - min_miles))  # scale 5–15

        tooltip = folium.Tooltip(
            f"<b>{team}</b><br>"
            f"Stadium: {stadium}<br>"
            f"Home Field Advantage: {hfa:.3f}<br>"
            f"Avg Temp: {temp:.1f}°F<br>"
            f"Elevation: {elev} ft<br>"
            f"Roof Usage: {roof:.0%}<br>"
            f"Day Games: {day:.0%}<br>"
            f"Miles Traveled: {miles:,.0f}",
            sticky=True
        )

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color="black",
            weight=1,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            tooltip=tooltip
        ).add_to(m_env)

    st_folium(m_env, width=700, height=400)

# ---------- TAB 2: PARK FACTORS ----------
with tab2:
    st.subheader("🏟️ Park Features and Home Field Advantage")

    st.markdown("**Marker color = Home Advantage Score (green = positive, red = neutral or negative)**  \n"
                "**Marker size = Total Miles Traveled in 2022**")

    with st.expander("Show caption and interpretation"):
        st.markdown("""
        This map focuses on physical ballpark features and crowd attendance.

        - **Green markers** = stronger home performance  
        - **Larger markers** = teams that traveled more miles  
        - Hover to view stadium wall dimensions, attendance, fill rate, and miles traveled  
        """)

    m_park = folium.Map(location=[39.8283, -98.5795], zoom_start=4, tiles="OpenStreetMap")

    for _, row in df.iterrows():
        lat = row["ballpark_lat"]
        lon = row["ballpark_long"]
        team = row["team_name"]
        stadium = row["ballpark"]
        hfa = row["home_field_advantage_score"]
        wall_max = row["max_wall_height_ft"]
        wall_min = row["min_wall_height_ft"]
        att = row["avg_attendance_home"]
        att_rate = row["attendance_rate"]
        miles = row["miles_traveled"]

        color = "green" if hfa > 0 else "red"
        radius = 5 + 10 * ((miles - min_miles) / (max_miles - min_miles))  # scale 5–15

        tooltip = folium.Tooltip(
            f"<b>{team}</b><br>"
            f"Stadium: {stadium}<br>"
            f"Home Field Advantage: {hfa:.3f}<br>"
            f"Max Wall Height: {wall_max} ft<br>"
            f"Min Wall Height: {wall_min} ft<br>"
            f"Avg Attendance: {att:,.0f}<br>"
            f"Attendance Rate: {att_rate:.0%}<br>"
            f"Miles Traveled: {miles:,.0f}",
            sticky=True
        )

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color="black",
            weight=1,
            fill=True,
            fill_color=color,
            fill_opacity=0.8,
            tooltip=tooltip
        ).add_to(m_park)

    st_folium(m_park, width=700, height=400)

