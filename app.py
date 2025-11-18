import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

@st.cache_data
def load_data():
    return pd.read_csv('ewf_standings.csv')

df = load_data()

# Debug: show column names to confirm structure
st.write("CSV columns:", df.columns.tolist())

# App title and instructions
st.title("Team Comparison Dashboard")
st.write("Select two teams and what aspect of their performance you want to compare")

# ✅ Check that 'team' column exists
if 'team' not in df.columns:
    st.error("The column 'team' was not found in your CSV. Please check the file.")
    st.stop()

# ✅ Extract team names from 'team' column
teams = sorted(df['team'].dropna().unique())

# Sidebar inputs
team1 = st.sidebar.selectbox("Select Team 1", teams)
team2 = st.sidebar.selectbox("Select Team 2", teams, index=1 if len(teams) > 1 else 0)

# ✅ Stat options — must match your CSV column names
stat_options = ["wins", "losses", "draws"]
missing_stats = [stat for stat in stat_options if stat not in df.columns]

if missing_stats:
    st.error(f"Missing columns in your CSV: {', '.join(missing_stats)}")
    st.stop()

stat = st.sidebar.selectbox("Select Stat to Compare", stat_options)

# ✅ Get stat values directly from the DataFrame using 'team'
try:
    val1 = df.loc[df['team'] == team1, stat].values[0]
    val2 = df.loc[df['team'] == team2, stat].values[0]
except IndexError:
    st.error("One of the selected teams doesn't have data for that stat.")
    st.stop()

# ✅ Plot bar chart
fig, ax = plt.subplots()
ax.bar([team1, team2], [val1, val2], color=["#1f77b4", "#ff7f0e"])
ax.set_ylabel(stat.capitalize())
ax.set_title(f"{stat.capitalize()} Comparison")

st.pyplot(fig)