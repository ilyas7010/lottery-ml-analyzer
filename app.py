import streamlit as st
import pandas as pd
from collections import Counter
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="Lottery ML Analyzer", page_icon="🎲", layout="wide")

st.title("🎲 Lottery ML Analyzer")
st.markdown(
    """
This app analyzes historical lottery draw data and generates ranked number estimates
based on historical frequency and recent draw activity.

**Note:** This is a data analysis and ranking tool, not a guaranteed prediction system.
"""
)

# -------------------------
# Sidebar settings
# -------------------------
st.sidebar.header("Settings")
recent_draws = st.sidebar.slider("Number of recent draws to analyze", 5, 50, 20)
recent_weight = st.sidebar.slider("Recent draw weight", 1, 5, 2)
top_pool = st.sidebar.slider("Top ranked numbers pool for suggestion", 6, 30, 20)

# -------------------------
# File path
# -------------------------
file_path = "data/lottery_data.csv"

try:
    # -------------------------
    # Load dataset
    # -------------------------
    df = pd.read_csv(file_path)

    # -------------------------
    # Clean dataset
    # -------------------------
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df["drawdate"] = pd.to_datetime(df["drawdate"], dayfirst=True)
    df = df.sort_values("drawdate")

    # -------------------------
    # Dataset overview
    # -------------------------
    st.subheader("Dataset Overview")
    col1, col2 = st.columns(2)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    with st.expander("Preview dataset"):
        st.dataframe(df.head(10), use_container_width=True, hide_index=True)

    # -------------------------
    # Main ball columns
    # -------------------------
    ball_columns = [
        "ball_1",
        "ball_2",
        "ball_3",
        "ball_4",
        "ball_5",
        "ball_6",
    ]

    # -------------------------
    # Historical frequency
    # -------------------------
    all_numbers = []
    for col in ball_columns:
        all_numbers.extend(df[col])

    counts = Counter(all_numbers)
    top_10_freq = counts.most_common(10)

    # -------------------------
    # Recent draw analysis
    # -------------------------
    recent_df = df.tail(recent_draws)

    recent_numbers = []
    for col in ball_columns:
        recent_numbers.extend(recent_df[col])

    recent_counts = Counter(recent_numbers)
    hot_numbers = recent_counts.most_common(10)

    # -------------------------
    # Ranking system
    # -------------------------
    scores = {}

    for number in range(1, 60):
        historical_score = counts.get(number, 0)
        recent_score = recent_counts.get(number, 0)

        score = historical_score + (recent_score * recent_weight)
        scores[number] = score

    ranked_numbers = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # -------------------------
    # Probability ranking
    # -------------------------
    total_score = sum(scores.values())
    probability_data = []

    for number, score in ranked_numbers[:10]:
        probability = (score / total_score) * 100
        probability_data.append((number, round(probability, 2)))

    # -------------------------
    # Cold numbers
    # -------------------------
    cold_numbers = [number for number in range(1, 60) if number not in recent_counts]

    # -------------------------
    # Analysis results
    # -------------------------
    st.subheader("Analysis Results")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Top 10 Most Frequent Numbers")
        freq_df = pd.DataFrame(top_10_freq, columns=["Number", "Times Appeared"])
        st.dataframe(freq_df, use_container_width=True, hide_index=True)

        st.markdown(f"### Hot Numbers (Last {recent_draws} Draws)")
        hot_df = pd.DataFrame(hot_numbers, columns=["Number", "Times Appeared"])
        st.dataframe(hot_df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("### Estimated Strongest Numbers")
        ranked_df = pd.DataFrame(ranked_numbers[:10], columns=["Number", "Score"])
        st.dataframe(ranked_df, use_container_width=True, hide_index=True)

        st.markdown("### Estimated Probability Ranking")
        prob_df = pd.DataFrame(probability_data, columns=["Number", "Estimated %"])
        st.dataframe(prob_df, use_container_width=True, hide_index=True)

    # -------------------------
    # Cold numbers section
    # -------------------------
    st.markdown("### Cold Numbers")
    if cold_numbers:
        cold_df = pd.DataFrame({"Cold Numbers": cold_numbers})
        st.dataframe(cold_df, use_container_width=False, hide_index=True)
    else:
        st.write("No cold numbers in this window.")

    # -------------------------
    # Suggested combinations
    # -------------------------
    st.markdown("### Suggested Combinations")

    top_candidates = [num for num, score in ranked_numbers[:top_pool]]

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("Generate 1 Combination"):
            suggested_numbers = sorted(random.sample(top_candidates, 6))
            st.success(f"Suggested combination: {suggested_numbers}")

    with col_b:
        if st.button("Generate 5 Combinations"):
            combinations = []
            seen = set()

            attempts = 0
            while len(combinations) < 5 and attempts < 100:
                combo = tuple(sorted(random.sample(top_candidates, 6)))
                if combo not in seen:
                    seen.add(combo)
                    combinations.append(combo)
                attempts += 1

            combo_df = pd.DataFrame(
                {"Combination": [", ".join(map(str, combo)) for combo in combinations]}
            )
            st.dataframe(combo_df, use_container_width=True, hide_index=True)

    # -------------------------
    # Explain scoring
    # -------------------------
    with st.expander("How the score is calculated"):
        st.write(
            """
Each number gets a score using:

**score = historical frequency + (recent frequency × recent weight)**

- Historical frequency = how often the number appeared in all draws
- Recent frequency = how often the number appeared in the recent draw window
- Recent weight = the slider value in the sidebar

This means numbers that are strong historically and active recently rank higher.
"""
        )

    # -------------------------
    # Frequency chart
    # -------------------------
    st.markdown("### Frequency Distribution Chart")

    numbers = list(counts.keys())
    frequencies = list(counts.values())

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(numbers, frequencies)
    ax.set_title("Lottery Number Frequency Distribution")
    ax.set_xlabel("Number")
    ax.set_ylabel("Times Appeared")
    ax.set_xticks(range(1, 60, 2))

    st.pyplot(fig)

except FileNotFoundError:
    st.error("Dataset file not found. Make sure 'data/lottery_data.csv' exists.")
except Exception as e:
    st.error(f"Something went wrong: {e}")
    st.exception(e)