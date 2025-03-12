import streamlit as st 
import Simulation


st.title("Draft Simulation")

selection = st.pills("", ["Quickdraft", "Premierdraft"], selection_mode="single")
if selection == "Quickdraft":
    DraftObject = Simulation.Quickdraft()
else:
    DraftObject = Simulation.Premierdraft()

winrate = st.number_input("Winrate", value=0.55, min_value=0.0, max_value=1.0)
number_of_drafts = st.number_input("Number of Drafts", value=1, min_value=1, max_value=9000)
starting_diamonds = st.number_input("Starting Diamonds", value=10000, min_value=0, max_value=1000000)
Simulation.Diamonds = starting_diamonds

#------------------- Simulion start --------------------


buttonval = st.button("Start Simulation")
diamondlist = [Simulation.Diamonds]
if buttonval:
    for x in range(number_of_drafts):
        Simulation.start_simulation(DraftObject, winrate)
        diamondlist.append(Simulation.Diamonds)
        if Simulation.Diamonds <= 0:
            break

st.line_chart(diamondlist)
st.write("Diamonds: ", Simulation.Diamonds)

