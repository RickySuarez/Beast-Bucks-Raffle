import streamlit as st
import pandas as pd
import random
import time

st.title("Beast Bucks Raffle")

# Upload CSV
uploaded_file = st.file_uploader("Upload grade CSV", type="csv")

if uploaded_file:
    grades = pd.read_csv(uploaded_file, index_col="Name").dropna(axis="columns")
    students = grades.index.tolist()

    num_bucks = st.number_input(
        "How many Beast Bucks?", min_value=1, max_value=len(students), step=1
    )

    # Initialize session state
    if "winner_queue" not in st.session_state:
        st.session_state.winner_queue = []
        st.session_state.current_index = 0

    # Draw winners once
    if st.button("Draw Winners", key="draw_winners"):
        # Weighted raffle
        low = 1
        intervals = []
        for student in students:
            grade = int(grades.loc[student, grades.columns[-1]])
            high = low + grade - 1
            intervals.append((low, high, student))
            low = high + 1
        total = intervals[-1][1]

        winners = set()
        while len(winners) < num_bucks:
            winning_num = random.randint(1, total)
            winner = next(s for (l, h, s) in intervals if l <= winning_num <= h)
            winners.add(winner)

        st.session_state.winner_queue = list(winners)
        st.session_state.current_index = 0

    slot_display = st.empty()

    # Show next winner when button is clicked
    if st.session_state.winner_queue:
        if st.button("Next Winner", key="next_winner"):
            idx = st.session_state.current_index
            if idx < len(st.session_state.winner_queue):
                next_winner = st.session_state.winner_queue[idx]
                # Animate slot machine
                st.markdown("""<audio autoplay style="display:none;">  <source src="media\\slotmachine.mp3" type="audio/mp3"></audio>""", unsafe_allow_html=True)
                for _ in range(75):
                    slot_display.markdown(f"<h1 style='font-size:70px;'> {random.choice(students)} </h1>", unsafe_allow_html=True)
                    time.sleep(0.05)
                slot_display.markdown(f"<h1 style='font-size:70px; color:green;'>🏆 {next_winner} 🏆</h1>", unsafe_allow_html=True)

                st.session_state.current_index += 1
            else:
                st.success("All winners have been drawn!")