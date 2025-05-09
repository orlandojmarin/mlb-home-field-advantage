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

    Out of 30 teams, 22 (73%) performed better at home (above the diagonal line), 3 (10%) performed the same (on the line), and only 5 (17%) performed better on the road (below the line).

    These results provide strong evidence of a league-wide home field advantage, with nearly three-quarters of MLB teams winning more frequently on their home turf than on the road.
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
    "Use the dropdown below to switch between batting and pitching metrics:",
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
    This visualization compares league-wide batting and pitching performance at home vs. away.  

    Teams scored 1.46% more runs at home and hit 1.04% more home runs at home, suggesting a modest offensive boost at home ballparks.  

    On the pitching side, teams recorded 8.63% more strikeouts at home, indicating stronger pitching effectiveness on home turf. However, teams also issued 2.83% fewer walks at home, which is desirable, as fewer walks allowed reduces opponent scoring chances.  

    Overall, these differences reflect a consistent home field advantage across both batting and pitching metrics.
    """)
 
st.markdown("---")
 
###############################################

# FIGURE 3: BOX PLOTS

st.subheader("Pitching Fuels MLB Home Field Advantage More Than Hitting")

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
    This visualization shows the distribution of team-level performance metrics at home vs. away using box plots.

    Median values show that teams scored slightly fewer runs at home (343) than away (352), and hit a nearly identical number of home runs at home (86) and away (87.5). This slight dip in home offense may be partially explained by the fact that home teams often do not bat in the 9th inning if they are already winning.

    On the pitching side, teams recorded more strikeouts at home (719) than away (658.5), and issued slightly fewer walks at home (241.5) than away (255). This is especially notable since home teams may pitch fewer total innings, yet still outperform away teams in key pitching metrics.

    These patterns suggest that home field advantage in baseball is most evident on the pitching side, where home teams demonstrate more effective control and dominance on the mound, even with fewer opportunities.
    """)

st.markdown("---")

###############################################
    
# FIGURE 4: SCATTER PLOTS
 
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

# FIGURE 5: BUBBLE CHART

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

# FIGURE 6: MAP VISUALIZATION WITH TABS (Captions Below Legend)

# Ensure required calculations exist
df["home_win_pct"] = df["home_wins"] / (df["home_wins"] + df["home_losses"])
df["away_win_pct"] = df["away_wins"] / (df["away_wins"] + df["away_losses"])
df["home_field_advantage_score"] = df["home_win_pct"] - df["away_win_pct"]
df["attendance_rate"] = df["avg_attendance_home"] / df["seat_capacity"]

# Create tabs for two different map views
tab1, tab2 = st.tabs(["🌦️ Environmental Factors", "🏟️ Park Factors"])

# ---------- TAB 1: ENVIRONMENTAL FACTORS ----------
with tab1:
    st.subheader("🌦️ Stadium Environment and Home Field Advantage")

    st.markdown("**Marker color = Home Advantage Score (green = positive, red = neutral or negative)**")

    with st.expander("Show caption and interpretation"):
        st.markdown("""
        This map highlights each stadium's environmental conditions and their home field advantage in 2022.

        - Green markers = stronger home performance  
        - Red markers = equal or worse performance at home  
        - Hover to explore average temperature, elevation, roof usage, and daytime game rates  
        """)

    # Create the map
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

        color = "green" if hfa > 0 else "red"

        tooltip = folium.Tooltip(
            f"<b>{team}</b><br>"
            f"Stadium: {stadium}<br>"
            f"Home Field Advantage: {hfa:.3f}<br>"
            f"Avg Temp: {temp:.1f}°F<br>"
            f"Elevation: {elev} ft<br>"
            f"Roof Usage: {roof:.0%}<br>"
            f"Day Games: {day:.0%}",
            sticky=True
        )

        folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(color=color, icon="info-sign"),
            tooltip=tooltip
        ).add_to(m_env)

    st_folium(m_env, width=700, height=400)

# ---------- TAB 2: PARK FACTORS ----------
with tab2:
    st.subheader("🏟️ Park Features and Home Field Advantage")

    st.markdown("**Marker color = Home Advantage Score (green = positive, red = neutral or negative)**")

    with st.expander("Show caption and interpretation"):
        st.markdown("""
        This map focuses on physical ballpark features and crowd attendance.

        - Hover to view stadium wall dimensions, average attendance, and fill rate  
        - Teams with greener markers tended to win more at home in 2022  
        - This map helps assess how park design and fan turnout may impact home field performance
        """)

    # Create the map
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

        color = "green" if hfa > 0 else "red"

        tooltip = folium.Tooltip(
            f"<b>{team}</b><br>"
            f"Stadium: {stadium}<br>"
            f"Home Field Advantage: {hfa:.3f}<br>"
            f"Max Wall Height: {wall_max} ft<br>"
            f"Min Wall Height: {wall_min} ft<br>"
            f"Avg Attendance: {att:,.0f}<br>"
            f"Attendance Rate: {att_rate:.0%}",
            sticky=True
        )

        folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(color=color, icon="info-sign"),
            tooltip=tooltip
        ).add_to(m_park)

    st_folium(m_park, width=700, height=400)

