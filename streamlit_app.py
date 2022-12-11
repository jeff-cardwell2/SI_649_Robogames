import altair as alt
import pandas as pd
import streamlit as st

import Robogame as rg
import networkx as nx
import altair as alt
import time, json
import pandas as pd
import numpy as np

game = rg.Robogame("bob")
game.setReady()
game.getGameTime()

while(True):
    gametime = game.getGameTime()
    timetogo = gametime['gamestarttime_secs'] - gametime['servertime_secs']

    if ('Error' in gametime):
        print("Error"+str(gametime))
        break
    if (timetogo <= 0):
        print("Let's go!")
        break

    print("waiting to launch... game will start in " + str(int(timetogo)))
    time.sleep(1)

def make_viz(text):
    game.getHints()
    robots = game.getRobotInfo()
    hints = game.getAllPredictionHints()

    hints_df = pd.DataFrame(hints)

    prod = robots[robots.Productivity >0]
    unprod = robots[robots.Productivity < 0]

    selection = alt.selection_single(fields=['id'], bind=text)

    line = alt.Chart(hints_df).mark_line().encode(
    x=alt.X('time:Q'),
    y=alt.Y('value:Q'),
    color = 'id:N'
    ).properties(
        width=800,
        height=500
    ).transform_filter(selection)

    circles = alt.Chart(hints_df).mark_point().encode(
        x=alt.X('time:Q'),
        y=alt.Y('value:Q'),
        color = 'id:N',
        tooltip = ['id', 'time', 'value']
    ).transform_filter(selection)

    v_line = alt.Chart(robots).mark_rule(color='black').encode(
        x='expires',
        tooltip = ['id', 'expires']
    ).transform_filter(selection)

    lines = alt.layer(line, circles, v_line)
    return lines

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False

text_input = st.text_input(
        "ID for Line graph",
        "0",
        key="linegraphtext",
    )


viz1 = make_viz(text_input)
viz1