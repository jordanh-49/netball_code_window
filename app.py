import streamlit as st
import time
from datetime import timedelta
import pandas as pd

# Initialize session state for keeping track across fragments and reruns
if 'quarter' not in st.session_state:
    st.session_state.quarter = None
if 'team' not in st.session_state:
    st.session_state.team = None
if 'position' not in st.session_state:
    st.session_state.position = None
if 'shot_results' not in st.session_state:
    st.session_state.shot_results = []
if "timer" not in st.session_state:
    st.session_state.timer = 600

@st.experimental_fragment(run_every="1s")
def display_timer(timer_placeholder):
    st.session_state.timer -= 1
    minutes = st.session_state.timer // 60  # Calculate the number of full minutes
    seconds = st.session_state.timer % 60  # Calculate the remaining seconds
    time_to_display = f"{minutes:02}:{seconds:02}"
    timer_placeholder.metric("⏳ Timer", time_to_display)

    if st.session_state.timer == 0:
        reset()


@st.experimental_fragment
def shot_recording_fragment(quarter_selected):
    t1,t2 = st.columns(2)
    # Team selection
    if t1.button("Home Team"):
        st.session_state.team = "Home"
    elif t2.button("Away Team"):
        st.session_state.team = "Away"

    # Position and shot result buttons
    if st.session_state.team:
        t3,t4 = st.columns(2)

        if t3.button("GS"):
            st.session_state.position = "GS"
        elif t4.button("GA"):
            st.session_state.position = "GA"
        
        if st.session_state.position:
            t5,t6 = st.columns(2)
            if t5.button("Make"):
                st.session_state.shot_results.append((st.session_state.team, st.session_state.position, "Make",quarter_selected,f"{(st.session_state.timer // 60):02}:{(st.session_state.timer % 60):02}"))
            elif t6.button("Miss"):
                st.session_state.shot_results.append((st.session_state.team, st.session_state.position, "Miss",quarter_selected,f"{(st.session_state.timer // 60):02}:{(st.session_state.timer % 60):02}"))

    # Display shot results
    st.write("Shot Results:")

    df = pd.DataFrame(st.session_state.shot_results, columns=["Team", "Position", "Result","Quarter","Timestamp"])
    st.dataframe(df)


# Select quarter and reset control
quarter_selected = st.selectbox("Select Quarter", options=[None,1, 2, 3, 4],key='quarter')


def reset():
    if st.session_state.quarter:
        pd.DataFrame(st.session_state.shot_results, columns=["Team", "Position", "Result","Quarter","Timestamp"]).to_csv(f'data/{st.session_state.quarter}_game.csv',index=False)
        st.toast("Data saved for this quarter!")

    st.session_state.timer = 600
    st.session_state.shot_results = []
    st.session_state.quarter = None


    return

if quarter_selected:
    timer_placeholder = st.empty()

    display_timer(timer_placeholder)

    shot_recording_fragment(quarter_selected)

    st.button("Reset for Next Quarter", on_click=reset)
        
