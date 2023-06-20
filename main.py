import tkinter as tk
import json
from tkinter import messagebox
from tkinter import ttk

# Initialize data structures
participants = []
teams = []
events = ["Volleyball", "Football", "Chess", "Ping-Pong", "Cooking competition"]

def load_data():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            participants.extend(data.get("participants", []))
            teams.extend(data.get("teams", []))
            events.extend(data.get("events", []))
    except FileNotFoundError:
        # Create a new data dictionary with empty fields
        data = {"participants": [], "teams": [], "events": events}
        with open("data.json", "w") as file:
            json.dump(data, file)
    return(data)

# Save data to JSON file
def save_data():
    data = {"participants": participants, "teams": teams, "events": events}
    with open("data.json", "w") as file:
        json.dump(data, file)

# Register individual participant
def register_individual():
    if len(participants) < 20:
        participant_name = individual_entry.get().strip()
        if participant_name:
            participants.append({"Name": participant_name, "Score": 0})
            messagebox.showinfo("Success", f"Individual participant '{participant_name}' has been registered.")
            save_data()
            update_individual_dropdown()
        else:
            messagebox.showinfo("Error", "Please enter a valid participant name.")
    else:
        messagebox.showinfo("Error", "No more spaces available for individual competitors.")

# Register team
def register_team():
    if len(teams) < 4:
        team_name = team_name_entry.get().strip()
        member1 = member1_entry.get().strip()
        member2 = member2_entry.get().strip()

        if team_name and member1 and member2:
            teams.append({"Team Name": team_name, "Members": [member1, member2], "Score": 0})
            messagebox.showinfo("Success", f"Team '{team_name}' has been registered.")
            save_data()
        else:
            messagebox.showinfo("Error", "Please enter valid team details.")
    else:
        messagebox.showinfo("Error", "No more spaces available for teams.")

# Enter event results
def enter_event_results():
    participant_team = participant_choice.get()
    score = int(score_entry.get())  # Convert the entered score to an integer

    if participant_team.startswith("Participant"):
        participant_name = participant_team.replace("Participant: ", "")
        for participant in participants:
            if participant["Name"].lower() == participant_name.lower():
                participant["Score"] += score
                break
    elif participant_team.startswith("Team"):
        team_name = participant_team.replace("Team: ", "")
        for team in teams:
            if team["Team Name"].lower() == team_name.lower():
                team["Score"] += score
                break

    messagebox.showinfo("Success", f"Score {score} added to {participant_team}.")
    save_data()


def display_details():
    name = display_choice.get()
    if name.startswith("Participant"):
        participant_name = name.replace("Participant: ", "")
        for participant in participants:
            if participant["Name"].lower() == participant_name.lower():
                score = participant["Score"]
                messagebox.showinfo("Success", f"Score {score} assigned to {participant_name}.")
                return
    elif name.startswith("Team"):
        team_name = name.replace("Team: ", "")
        for team in teams:
            if team["Team Name"].lower() == team_name.lower():
                score = team["Score"]
                messagebox.showinfo("Success", f"Score {score} assigned to {team_name}.")
                return
    messagebox.showinfo("Error", "Invalid selection.")



def update_individual_dropdown():
    details_combobox['values'] = [participant["Name"] for participant in participants]

# Load data from the JSON file
load_data()

# Create the main Tkinter window
window = tk.Tk()
window.title("Tournament Management System")

# Create a notebook (tabbed interface)
notebook = ttk.Notebook(window)

# Create tabs for "Add" and "Display"
add_tab = ttk.Frame(notebook)
display_tab = ttk.Frame(notebook)

notebook.add(add_tab, text="Add")
notebook.add(display_tab, text="Display")
notebook.pack()

# Add Individual Participant section
individual_label = ttk.Label(add_tab, text="Add Individual Participant")
individual_label.pack()

individual_entry = ttk.Entry(add_tab)
individual_entry.pack()

individual_button = ttk.Button(add_tab, text="Add Participant", command=register_individual)
individual_button.pack()

# Add Team section
team_label = ttk.Label(add_tab, text="Add Team")
team_label.pack()

team_name_label = ttk.Label(add_tab, text="Team Name:")
team_name_label.pack()

team_name_entry = ttk.Entry(add_tab)
team_name_entry.pack()

member1_label = ttk.Label(add_tab, text="Member 1:")
member1_label.pack()

member1_entry = ttk.Entry(add_tab)
member1_entry.pack()

member2_label = ttk.Label(add_tab, text="Member 2:")
member2_label.pack()

member2_entry = ttk.Entry(add_tab)
member2_entry.pack()

team_button = ttk.Button(add_tab, text="Add Team", command=register_team)
team_button.pack()

# Enter Event Results section
event_label = ttk.Label(add_tab, text="Enter Event Results")
event_label.pack()

event_choice_label = ttk.Label(add_tab, text="Select Event:")
event_choice_label.pack()

event_choice = ttk.Combobox(add_tab, values=events, state="readonly")
event_choice.current(0)  # Default event choice
event_choice.pack()

score_label = ttk.Label(add_tab, text="Enter Score:")
score_label.pack()

participant_label = ttk.Label(add_tab, text="Select Participant/Team:")
participant_label.pack()

participant_choice = ttk.Combobox(add_tab, values=[f"Participant: {participant['Name']}" for participant in participants] +
                                                 [f"Team: {team['Team Name']}" for team in teams],
                                  state="readonly")
participant_choice.current(0)  # Default participant/team choice
participant_choice.pack()

score_entry = ttk.Entry(add_tab)
score_entry.pack()

results_button = ttk.Button(add_tab, text="Enter Results", command=enter_event_results)
results_button.pack()

# Display Details section
display_choice = ttk.Combobox(display_tab, values=[f"Participant: {participant['Name']}" for participant in participants] +
                                                 [f"Team: {team['Team Name']}" for team in teams],
                                  state="readonly")
display_choice.current(0)  # Default participant/team choice
display_choice.pack()

details_button = ttk.Button(display_tab, text="Display", command=display_details)
details_button.pack()

# Start the Tkinter event loop
window.mainloop()
