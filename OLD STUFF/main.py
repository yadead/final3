from DATABASE.database import signup, signin
from DATABASE.database_diary import diary_entry, sdevname, sprojname, allentries, sCHOICEID, get_user_entries, delete_entry
from datetime import datetime
import math

#prompt user for username and password to sign up with
def sign_up():
    username = input("Username: ")
    password = input("Password: ")
    signup(username, password)
    print(f"User '{username}' has been signed up")

#prompt user for username and password to sign in with
def sign_in():
    global devname
    devname = input("Username: ")
    username = devname
    password = input("Password: ")
    if signin(username, password):
        print(f"{username} has been logged in")
        menu2()
    else:
        print("Invalid username or password. Please try again.")


# query user for information about diary entry
def Create_entry():
    Developer = devname
    print(f"Developer: {Developer}")
    Project = input("Project Name: ")
    time_format = "%H:%M %d/%m/%Y"
    Start_Time = input("Start Time (hh:mm dd/mm/yyyy): ")
    End_Time = input("End Time (hh:mm dd/mm/yyyy): ")
    start_dt = datetime.strptime(Start_Time, time_format)
    end_dt = datetime.strptime(End_Time, time_format)
    Time_Worked = end_dt - start_dt
    total_minutes = Time_Worked.total_seconds() / 60
    rounded_minutes = math.ceil(total_minutes / 15) * 15
    rounded_hours = rounded_minutes / 60
    Time_Worked = rounded_hours
    print(f"Time Worked: {Time_Worked} hours")
    now = datetime.now()
    Diary_Entry = now.strftime("%H:%M %d/%B/%Y")
    print(f"Diary_Entry: {Diary_Entry}")
    Repo = input("Repository Link: ")
    Developer_Notes = input("Developer Notes: ")
    new_id = diary_entry(Developer, Project, Start_Time, End_Time, Diary_Entry, Time_Worked, Repo, Developer_Notes)
    print(f"Diary entry added with ID: {new_id}")

#information to be printed after a specific id is looked up
def searchID():
    choiceid = input("Enter ID: ")
    resultid = sCHOICEID(choiceid)
    if resultid:
        developer, project, start_time, end_time, time_worked, diary_entry, repo, dev_notes = resultid
        print(f"Developer: {developer}")
        print(f"Project Name: {project}")
        print(f"Start Time (hh:mm dd/mm/yyyy): {start_time}")
        print(f"End Time (hh:mm dd/mm/yyyy): {end_time}")
        print(f"Time Worked: {time_worked} hours")
        print(f"Diary_Entry: {diary_entry}")
        print(f"Repository Link: {repo}")
        print(f"Developer Notes: {dev_notes}")

    else:
        print("Invalid ID")

#Information to be printed when searching for a specific developer name
def sdeveloper_name():
    global sdev_name_choice
    sdev_name_choice = input("Developer name: ")  

    dev_name_results = sdevname(sdev_name_choice,)

    if dev_name_results:  
        for dev in dev_name_results:  
            print(" || ".join(map(str, dev)))
    else:
        print("No results found. Please try again.")

#Information to be printed when searching for a specific project name
def sproject_name():
    global sproj_name_choice
    sproj_name_choice = input("Project name: ")  
    proj_name_results = sprojname(sproj_name_choice,)
    if proj_name_results:  
        for proj in proj_name_results:  
            print(" || ".join(map(str, proj)))
    else:
        print("No results found. Please try again.")

#prints all entries found
def all_entries():
    allentries_results = allentries()
    for ent in allentries_results:
        print(" || ".join(map(str, ent)))




#gives users choices to search entries by
def search_entry():
    while True: 
        choicese = input("search by:\n1. Developer Name\n2. Project Name\n3. All entries\n4. Go Back\n")
        if choicese == "1":
            sdeveloper_name()
            searchID()
        elif choicese == "2":
            sproject_name()
            searchID()
        elif choicese == "3":
            all_entries()
            searchID()
        elif choicese == "4":
            menu2()
        else:
            print("Invalid choice. Please enter 1, 2, 3 or 4")

#gives user their entries they are able to delete, asks which specific one to delete and then deletes it
def deleteentry():
    entries = get_user_entries(devname)
    if not entries:
        print("No entries found for you.")
        return
    print("\nYour Entries:")
    for entry in entries:
        print(" || ".join(map(str, entry)))
        entry_id = int(input("\nEnter the ID of the entry you want to delete: "))
        delete_entry(entry_id, devname)
    except ValueError:
        print("Invalid input. Please enter a valid numeric ID.")

#gives users options to sign in or sign up
def menu():
    while True:
        choicem = input("Choose an option:\n1. Sign In\n2. Sign Up\n3. Exit\n")
        if choicem == "1":
            sign_in()
        elif choicem == "2":
            sign_up()
        elif choicem == "3":
            exit()
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

#gives users options to create an entry or lookup an entry
def menu2():
    while True:
        choicem2 = input("Choose an option:\n1. Create Entry\n2. Lookup Entry\n3. Delete Entry\n4. Sign Out\n")
        if choicem2 == "1":
            Create_entry()
        elif choicem2 == "2":
            search_entry()
        elif choicem2 == "3":
            deleteentry()
        elif choicem2 == "4":
            menu()
            sign_in(devname) == None
        else:
            print("Invalid choice. Please enter 1, 2, or 3 or 4")

menu()