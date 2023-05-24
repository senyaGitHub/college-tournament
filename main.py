import tkinter as tk
import json
from tkinter import messagebox
from tkinter import ttk

# Initialize data structures
participants = []
teams = []
events = ["Volleyball", "Football", "Chess", "Ping-Pong", "Cooking competition"]
event_points = {
    "Volleyball": 20,
    "Football": 20,
}

# Load data from JSON file
def load_data():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            participants.extend(data.get("participants", []))
            teams.extend(data.get("teams", []))
            events.extend(data.get("events", []))
            event_points.update(data.get("event_points", {}))
    except FileNotFoundError:
        pass

# Save data to JSON file
def save_data():
    data = {"participants": participants, "teams": teams, "events": events, "event_points": event_points}
    with open("data.json", "w") as file:
        json.dump(data, file)

# Register individual participant
def register_individual():
    if len(participants) < 20:
        participant_name = individual_entry.get().strip()
        if participant_name:
            participants.append({"Name": participant_name, "Scores": {}})
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
            teams.append({"Team Name": team_name, "Members": [member1, member2], "Scores": {}})
            messagebox.showinfo("Success", f"Team '{team_name}' has been registered.")
            save_data()
        else:
            messagebox.showinfo("Error", "Please enter valid team details.")
    else:
        messagebox.showinfo("Error", "No more spaces available for teams.")

# Enter event results
def enter_event_results():
    event_name = event_choice.get()
    event_type = "Individual" if event_name in participants[0]["Scores"] else "Team"

    if event_name not in event_points:
        messagebox.showinfo("Error", "Points for this event have not been set.")
        return

    if event_type == "Individual":
        for i, participant in enumerate(participants):
            score = individual_scores[i].get()
            participant["Scores"][event_name] = score

    elif event_type == "Team":
        for i, team in enumerate(teams):
            score = team_scores[i].get()
            team["Scores"][event_name] = score

    messagebox.showinfo("Success", f"Results for {event_name} ({event_type}) have been entered.")
    save_data()

def display_details():
    name = details_combobox.get()
    found = False

    # Search for team details
    for team in teams:
        if team["Team Name"].lower() == name.lower():
            messagebox.showinfo("Team Details", f"Team Name: {team['Team Name']}\nMembers: {', '.join(team['Members'])}")
            # Calculate and display total points for the team
            total_points = calculate_total_points(team["Team Name"])
            messagebox.showinfo("Team Details", f"Total Points: {total_points}")
            found = True
            break

    # Search for individual participant details
    if not found:
        for participant in participants:
            if participant["Name"].lower() == name.lower():
                messagebox.showinfo("Participant Details", f"Participant Name: {participant['Name']}")
                found = True
                break

    if not found:
        messagebox.showinfo("Error", "Participant or team not found.")

def calculate_total_points(name):
    total_points = 0
    for event in events:
        if event in event_points and event in participants[0]["Scores"]:
            for participant in participants:
                if event in participant["Scores"] and participant["Name"].lower() == name.lower():
                    score = participant["Scores"][event]
                    total_points += score * event_points[event]
    return total_points

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

individual_scores = []
team_scores = []

results_button = ttk.Button(add_tab, text="Enter Results", command=enter_event_results)
results_button.pack()

# Display Details section
details_label = ttk.Label(display_tab, text="Display Details")
details_label.pack()

details_combobox = ttk.Combobox(display_tab, values=[participant["Name"] for participant in participants], state="readonly")
details_combobox.current(0)  # Default participant choice
details_combobox.pack()

details_button = ttk.Button(display_tab, text="Display", command=display_details)
details_button.pack()

# Start the Tkinter event loop
window.mainloop()
