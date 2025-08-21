import streamlit as st
import random, time, base64

# Autoplay music when called. file_path is the relative location of the audio file as a string.
def autoplay_audio(file_name):
    with open("media/" + file_name + ".mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
    audio_html = f"""
    <audio controls autoplay="true" hidden="hidden">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)



def draw(session_state, num_winners, threshold):
    # Weighted raffle is based on how much of the most recent homework is complete.
    low = 1
    intervals = []
    total = 0

    # Pick the winners.
    for student in session_state.students:
        grade = int(session_state.grades.loc[student, session_state.grades.columns[-1]])

        # If the grade is greater than the threshold, the grade gets added.
        if grade >= threshold:
            high = low + grade - 1
            intervals.append((low, high, student))
            low = high + 1
            total += grade
    
    # If there are not enough students that reach the threshold, readjust.
    if len(intervals) == 0:
        st.write("No students have reached the threshold.")
    elif len(intervals) < num_winners:
        num_winners = len(intervals)
        st.write("Not enough students reached the threshold.")
        st.write(f"Picking {num_winners} winner{'s' if num_winners != 1 else ''} instead.")
        

    # Choose winners and place them into a set to avoid repeats.
    winners = set()
    while len(winners) < num_winners and total > 0:
        winning_num = random.randint(1, total)
        winner = next(s for (l, h, s) in intervals if l <= winning_num <= h)
        winners.add(winner)
    session_state.winners = list(winners)

# Run the slot machines.
def slot_machine(session_state):

    # There is one slot machine for each winner.
    slots = [st.empty() for i in range(len(session_state.winners))]

    # Total seconds you want the animation.
    duration = 3.0          
    delay = 0.05            
    frames = int(duration / delay) 
    
    # Play audio.
    autoplay_audio("ItemBox")

    # Animate for exactly duration seconds.
    for i in range(frames):
        for slot_display in slots:
            slot_display.markdown(
                f"<h1 style='font-size:60px;'> {random.choice(session_state.students)} </h1>",
                unsafe_allow_html=True,
            )
        time.sleep(delay)

    # Display winners.
    for i, slot_display in enumerate(slots):
        slot_display.markdown(
            f"<h1 style='font-size:60px; color:green;'>🏆 {session_state.winners[i]} 🏆</h1>",
            unsafe_allow_html=True,
        )