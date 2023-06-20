import tkinter as tk
from tkinter import messagebox, ttk
import json

# Global variables
data_file = "data.json"
participants = []
teams = []
events = ["Volleyball", "Football", "Chess", "Ping-Pong", "Cooking competition"]
event_points = {
    "Volleyball": 20,
    "Football": 20,
}
details_combobox = None
individual_entry = None
team_name_entry = None

def load_data():
    try:
        with open(data_file, "r") as file:
            data = json.load(file)
            participants.extend(data.get("participants", []))
            teams.extend(data.get("teams", []))
            events.extend(data.get("events", []))
            event_points.update(data.get("event_points", {}))
    except FileNotFoundError:
        pass
    update_individual_dropdown()


def save_data():
    data = {
        "participants": participants,
        "teams": teams,
        "events": events,
        "event_points": event_points,
    }
    with open(data_file, "w") as file:
        json.dump(data, file)


def register_individual():
    global individual_entry
    if len(participants) < 20:
        participant_name = individual_entry.get().strip()
        if participant_name:
            participants.append({"Name": participant_name, "Scores": {}})
            messagebox.showinfo(
                "Success", f"Individual participant '{participant_name}' has been registered."
            )
            save_data()
            update_individual_dropdown()
        else:
            messagebox.showinfo("Error", "Please enter a valid participant name.")
    else:
        messagebox.showinfo("Error", "No more spaces available for individual competitors.")



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


def enter_event_results(event_choice):
    event_name = event_choice.get()

    if event_name not in event_points:
        messagebox.showinfo("Error", "Points for this event have not been set.")
        return

    if event_name in participants[0]["Scores"]:
        participant_name = individual_choice.get()
        score = individual_score_entry.get().strip()
        if participant_name and score.isdigit():
            for participant in participants:
                if participant["Name"] == participant_name:
                    participant["Scores"][event_name] = int(score)
                    messagebox.showinfo("Success", f"Score of {score} for {event_name} has been added to {participant_name}.")
                    save_data()
                    break
        else:
            messagebox.showinfo("Error", "Please enter a valid participant name and score.")

    elif event_name in teams[0]["Scores"]:
        team_name = team_choice.get()
        score = team_score_entry.get().strip()
        if team_name and score.isdigit():
            for team in teams:
                if team["Team Name"] == team_name:
                    team["Scores"][event_name] = int(score)
                    messagebox.showinfo("Success", f"Score of {score} for {event_name} has been added to {team_name}.")
                    save_data()
                    break
        else:
            messagebox.showinfo("Error", "Please enter a valid team name and score.")


def display_details():
    name = details_combobox.get()
    found = False

    for team in teams:
        if team["Team Name"].lower() == name.lower():
            messagebox.showinfo(
                "Team Details",
                f"Team Name: {team['Team Name']}\nMembers: {', '.join(team['Members'])}",
            )
            total_points = calculate_total_points(team["Team Name"])
            messagebox.showinfo("Team Details", f"Total Points: {total_points}")
            found = True
            break

    if not found:
        for participant in participants:
            if participant["Name"].lower() == name.lower():
                messagebox.showinfo(
                    "Participant Details",
                    f"Participant Name: {participant['Name']}\nScores: {participant['Scores']}",
                )
                found = True
                break

    if not found:
        messagebox.showinfo("Error", "Participant or team not found.")


def calculate_total_points(name):
    total_points = 0
    for event in events:
        if event in event_points and event in participants[0]["Scores"]:
            for participant in participants:
                if (
                    event in participant["Scores"]
                    and participant["Name"].lower() == name.lower()
                ):
                    score = participant["Scores"][event]
                    total_points += score * event_points[event]
    return total_points


def update_individual_dropdown():
    global details_combobox
    
    if details_combobox is not None:
        details_combobox["values"] = [
            participant["Name"] for participant in participants
        ] + [team["Team Name"] for team in teams]


def main():
    # Load data from the JSON file
    load_data()
    

    # Create the main Tkinter window
    window = tk.Tk()
    window.title("Tournament Management System")
    global individual_entry
    global team_name_entry
    # Create a notebook (tabbed interface)
    notebook = ttk.Notebook(window)
    notebook.pack()

    # Add Individual Participant section
    add_tab = ttk.Frame(notebook)
    notebook.add(add_tab, text="Add")

    individual_label = ttk.Label(add_tab, text="Add Individual Participant")
    individual_label.pack()

    individual_entry = ttk.Entry(add_tab)
    individual_entry.pack()

    individual_button = ttk.Button(
        add_tab, text="Add Participant", command=register_individual
    )
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

    global member1_entry
    global member2_entry
    global member3_entry
    global member4_entry
    global member5_entry
    
    member1_entry = ttk.Entry(add_tab)
    member1_entry.pack()

    member2_label = ttk.Label(add_tab, text="Member 2:")
    member2_label.pack()

    member2_entry = ttk.Entry(add_tab)
    member2_entry.pack()

    member3_label = ttk.Label(add_tab, text="Member 3:")
    member3_label.pack()

    member3_entry = ttk.Entry(add_tab)
    member3_entry.pack()

    member4_label = ttk.Label(add_tab, text="Member 4:")
    member4_label.pack()

    member4_entry = ttk.Entry(add_tab)
    member4_entry.pack()

    member5_label = ttk.Label(add_tab, text="Member 5:")
    member5_label.pack()

    member5_entry = ttk.Entry(add_tab)
    member5_entry.pack()

    
    team_button = ttk.Button(add_tab, text="Add Team", command=register_team)
    team_button.pack()

    # Enter Event Results section
    event_tab = ttk.Frame(notebook)
    notebook.add(event_tab, text="Enter Results")

    event_label = ttk.Label(event_tab, text="Enter Event Results")
    event_label.pack()

    event_choice_label = ttk.Label(event_tab, text="Select Event:")
    event_choice_label.pack()

    event_choice = ttk.Combobox(event_tab, values=events, state="readonly")
    event_choice.current(0)
    event_choice.pack()

    individual_scores_label = ttk.Label(event_tab, text="Individual Scores:")
    individual_scores_label.pack()

    individual_choice_label = ttk.Label(event_tab, text="Select Individual:")
    individual_choice_label.pack()

    individual_choice = ttk.Combobox(
        event_tab, values=[participant["Name"] for participant in participants], state="readonly"
    )
    individual_choice.current(0)
    individual_choice.pack()

    individual_score_label = ttk.Label(event_tab, text="Enter Score:")
    individual_score_label.pack()

    individual_score_entry = ttk.Entry(event_tab)
    individual_score_entry.pack()

    team_scores_label = ttk.Label(event_tab, text="Team Scores:")
    team_scores_label.pack()

    team_choice_label = ttk.Label(event_tab, text="Select Team:")
    team_choice_label.pack()

    team_choice = ttk.Combobox(
        event_tab, values=[team["Team Name"] for team in teams], state="readonly"
    )
    team_choice.current(0)
    team_choice.pack()

    team_score_label = ttk.Label(event_tab, text="Enter Score:")
    team_score_label.pack()

    team_score_entry = ttk.Entry(event_tab)
    team_score_entry.pack()

    results_button = ttk.Button(event_tab, text="Enter Results", command=lambda: enter_event_results(event_choice))
    results_button.pack()

    # Display Details section
    display_tab = ttk.Frame(notebook)
    notebook.add(display_tab, text="Display")

    details_label = ttk.Label(display_tab, text="Display Details")
    details_label.pack()

    details_combobox = ttk.Combobox(
        display_tab,
        values=[participant["Name"] for participant in participants]
        + [team["Team Name"] for team in teams],
        state="readonly",
    )
    details_combobox.current(0)
    details_combobox.pack()

    details_button = ttk.Button(display_tab, text="Display", command=display_details)
    details_button.pack()
    
    # Start the Tkinter event loop
    window.mainloop()


if __name__ == "__main__":
    main()
