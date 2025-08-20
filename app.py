import streamlit as st
import pandas as pd
import numpy as np
import random, time, base64

st.title("Beast Bucks Raffle")

# Generate example CSV with random grades.
students = ["Alice", "Bob", "Charlie", "David", "Eva"]
columns = [str(i) for i in range(1, 16)]

example_df = pd.DataFrame(
    np.random.randint(60, 101, size=(len(students), len(columns))),  # random grades 60–100
    columns=columns
)
example_df.insert(0, "Name", students)

# Convert to CSV.
csv = example_df.to_csv(index=False)

# Create download button for the CSV.
st.download_button(
    label="📥 Download Example CSV",
    data=csv,
    file_name="example_grades.csv",
    mime="text/csv"
)

# File uploader for user input.
uploaded_file = st.file_uploader("Upload grade CSV", type="csv")

# Autoplay music when called. file_path is the relative location of the audio file as a string.
def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    audio_html = f"""
    <audio controls autoplay="true" hidden="hidden">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# Run the slot machines.
def slot_machine():

    # There is one slot machine for each winner.
    slots = [st.empty() for i in range(len(st.session_state.winners))]

    # Play the audio used for the slot machine.
    autoplay_audio("media/ItemBox.mp3")

    # Total seconds you want the animation.
    duration = 3.0          
    delay = 0.05            
    frames = int(duration / delay) 

    # Animate for exactly duration seconds.
    for i in range(frames):
        for slot_display in slots:
            slot_display.markdown(
                f"<h1 style='font-size:60px;'> {random.choice(students)} </h1>",
                unsafe_allow_html=True,
            )
        time.sleep(delay)

    # Display winners.
    for i, slot_display in enumerate(slots):
        slot_display.markdown(
            f"<h1 style='font-size:60px; color:green;'>🏆 {st.session_state.winners[i]} 🏆</h1>",
            unsafe_allow_html=True,
        )


# When the user uploads the file, this runs.
if uploaded_file:
    grades = pd.read_csv(uploaded_file, index_col="Name").dropna(axis="columns")
    students = grades.index.tolist()
    num_bucks = st.number_input(
        "How many Beast Bucks?", min_value=1, max_value=len(students), step=1
    )

    if st.button("Let's Draw!", key="draw"):
            
        # Weighted raffle is based on how much of the most recent homework is complete.
        low = 1
        intervals = []
        for student in students:
            grade = int(grades.loc[student, grades.columns[-1]])
            high = low + grade - 1
            intervals.append((low, high, student))
            low = high + 1
        total = intervals[-1][1]

        # Choose winners and place them into a set to avoid repeats.
        winners = set()
        while len(winners) < num_bucks:
            winning_num = random.randint(1, total)
            winner = next(s for (l, h, s) in intervals if l <= winning_num <= h)
            winners.add(winner)
        st.session_state.winners = list(winners)

        # Run the slot machine.
        slot_machine()

        # Button to restart the slots.
        st.button("Restart", key="restart")