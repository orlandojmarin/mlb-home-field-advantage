# MLB Home Field Advantage Analysis

## Contributors

- Tatiana Eng  
- Orlando Marin

## Tech Stack

- Python  
- Streamlit  
- Pandas  
- NumPy  
- Plotly  
- Matplotlib  
- Folium  
- Streamlit-Folium

## Overview

This Streamlit project explores the impact of home field advantage in Major League Baseball (MLB) using data from the 2022 season. Through a series of interactive visualizations, the dashboard investigates whether MLB teams perform better at home, what factors contribute to any advantage, and how variables such as stadium conditions, travel, and crowd size might influence game outcomes.

## Project Motivation

- **Home Field Advantage is Often Assumed**: Fans and analysts often assume that playing at home gives teams an edge, but the data may tell a different story.  
- **MLB’s Unique Stadium Factors**: Unlike other sports, MLB stadiums vary in size, elevation, weather conditions, and crowd attendance, making the home field advantage more complex and worth exploring.  
- **Ideal for Visualization**: Comparing home and away performance across teams lends itself well to storytelling through data visualizations and interactive dashboards.

## Key Questions

1. Do MLB teams perform better at home than away, and why?  
2. Which teams have the strongest and weakest home field advantage?  
3. How do batting and pitching statistics differ at home vs away?  
4. How does travel impact teams’ performance?  
5. Do environmental or park factors impact home field advantage?

## Data Sources

All data is from the 2022 MLB season:

1. [MLB Ballpark Info (Kaggle)](https://www.kaggle.com/datasets/paulrjohnson/mlb-ballparks)  
2. [Stadium Locations (Kaggle)](https://www.kaggle.com/datasets/logandonaldson/sports-stadium-locations)  
3. [Game Statistics (ESPN)](https://www.espn.com/mlb/standings/_/season/2022/group/overall)  
4. [Attendance (ESPN)](https://www.espn.com/mlb/attendance/_/year/2022)  
5. [Seating Capacity (BetMGM)](https://sports.betmgm.com/en/blog/mlb/biggest-mlb-stadiums-ranking-by-capacity-bm15/)  
6. [Travel Distances (Baseball Savant)](https://baseballsavant.mlb.com/visuals/map?team=&year=2022)  

## Data Preparation

- Merged data from six sources into a single, comprehensive dataset.  
- Added latitude and longitude coordinates for interactive maps.  
- Calculated a **Home Field Advantage score** = Home Win % − Away Win %.  
- Computed total miles traveled for each team.  
- Calculated additional variables such as attendance rate and pitching performance metrics for home vs. away games.

## Visualizations

This Streamlit dashboard includes the following visualizations:

1. **Scatter Plot: Home vs. Away Win Percentage**  
2. **Double Bar Graphs: Batting & Pitching Comparison**  
3. **Box Plots: Distribution of Key Stats**  
4. **Scatter Plot: Miles Traveled vs Home Field Advantage**  
5. **Geospatial Maps (2 Tabs)**:  
   - Environmental Factors Map  
   - Park Factors Map  

## Key Findings

- **Most Teams Perform Better at Home**: 73% of MLB teams had a higher win percentage at home.  
- **Best vs. Worst Home Advantage Teams**:  
  - Best: Rays (0.198), Yankees (0.185), Twins/Rockies (0.173)  
  - Worst: Athletics (-0.016), Nationals (-0.037), White Sox (-0.086)  
- **Pitching Improves at Home**:  
  - 8.63% more strikeouts and 2.8% fewer walks at home.  
- **Travel Affects Performance**:  
  - Teams traveling <35,000 miles had a 223% higher home field advantage score than those traveling more.  
- **Environment and Park Factors Vary**:  
  - Higher elevation, large wall dimensions, and high attendance correlated with stronger home performance in some cases, but no single factor explained the league-wide trend.

## Limitations

- **Single-Season Scope**: Only 2022 data was analyzed. Multi-year trends may differ.  
- **Team-Level Aggregation**: Game-level and player-level variations were not captured.  
- **Excluded Qualitative Factors**: Psychological and emotional factors (e.g., morale) were not part of this analysis.

## Future Improvements

- Expand to multiple MLB seasons for trend analysis  
- Add player-level or game-level statistics  
- Explore sentiment analysis using player interviews or social media  
- Incorporate weather data and game-time temperatures  
- Improve dashboard responsiveness for mobile users

## Try the Live App

You can explore the fully deployed interactive dashboard here:  
[https://mlb-home-field-advantage.streamlit.app/](https://mlb-home-field-advantage.streamlit.app/)

## How to Run

1. Clone this repository:  
   ```bash
   git clone https://github.com/orlandojmarin/mlb-home-field-advantage.git
   cd mlb-home-field-advantage
   ```

2. Create and activate a virtual environment:  
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install required packages:  
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the Streamlit app:  
   ```bash
   streamlit run mlb.py
   ```

The dashboard will be available at [http://localhost:8501](http://localhost:8501)

## License

This project is for educational purposes only and is not intended for production use.
