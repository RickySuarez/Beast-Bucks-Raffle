import streamlit as st
import pandas as pd
import random

st.title("🎡 Beast Bucks Raffle")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a grade CSV", type="csv")

if uploaded_file:
    grades = pd.read_csv(uploaded_file, index_col="Name").dropna(axis="columns")
    students = grades.index.tolist()

    # Select how many Beast Bucks
    num_bucks = st.number_input("How many Beast Bucks?", min_value=1, max_value=len(students))

    if st.button("Draw Winners"):
        # Build weighted intervals
        low = 1
        intervals = []
        for student in students:
            grade = int(grades.loc[student, grades.columns[-1]])
            high = low + grade - 1
            intervals.append((low, high, student))
            low = high + 1
        total = intervals[-1][1]

        # Pick winners
        winners = set()
        while len(winners) < num_bucks:
            winning_num = random.randint(1, total)
            winning_student = next(s for (l, h, s) in intervals if l <= winning_num <= h)
            winners.add(winning_student)

        # Show results
        st.subheader("🎉 Winners 🎉")
        for w in winners:
            st.write(f"- {w}")
