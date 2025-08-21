import streamlit as st, pandas as pd
from my_module.draw import draw, slot_machine
from my_module.csv_generator import generate_example

st.title("Beast Bucks Raffle")

# Generate randomized example CSV file for download.
generate_example()

# File uploader for user input.
uploaded_file = st.file_uploader("Upload grade CSV", type="csv")

# When the user uploads the file, this runs.
if uploaded_file:

    # Initialize current state or reset it whenever a new file is uploaded.
    if "current_file" not in st.session_state or st.session_state.current_file != uploaded_file.name:
        st.session_state.current_file = uploaded_file.name
        st.session_state.grades = pd.read_csv(uploaded_file, index_col="Name").dropna(axis="columns")
        st.session_state.students = st.session_state.grades.index.tolist()
        st.session_state.count = 0
        st.session_state.roulette_finished = False

    # User input for the amount of winners.
    num_winners = st.number_input(
        "How many Beast Bucks?", min_value=1, max_value=len(st.session_state.students), step=1
    )
    
    # User input determines the lowest grade possible for consideration.
    threshold = st.number_input(
        "What is the grade threshold?", min_value=1, max_value=100, step=1, value=70
    )

    # Reserve a spot for the button
    button_placeholder = st.empty()
    
    # Label the button and generate a new key every time a new button is made.
    click = button_placeholder.button("Let's Draw!", key ="draw_" + str(st.session_state.count))

    # If the button is pressed, replace the Let's Draw button with a new "Restart" button,
    # draw the winners, and display the slot machine. Increment the count to continue generating new keys.
    if click:
        button_placeholder.empty()
        click = button_placeholder.button("Restart", key ="restart_" + str(st.session_state.count))
        draw(st.session_state, num_winners, threshold)
        slot_machine(st.session_state)
        st.session_state.count += 1