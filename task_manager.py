from datetime import datetime

#===== Define Functions =====#
# Define function to create nested dictionary of tasks
def task_dictionary():
    task_dict = {}
    task_num = 0
    with open('tasks.txt', 'r') as f:
        # Remove blank lines to avoid IndexError
        lines = filter(None, (line.rstrip() for line in f))
        for line in lines:
            # Create nested dictionary {dictionary number: {key: string from txt file}}
            # Add tasks to dictionary with a corresponding key number
            temp = line.strip().split(", ")
            task_num += 1
            task_info = {
                "user": temp[0],
                "task": temp[1],
                "description": temp[2],
                "date": temp[3],
                "due": temp[4],
                "complete": temp[5]
            }
            task_dict[task_num] = task_info
    return task_dict

# Define function to create task display
def display(task, name, date_created, date_due, status, descr):
    task_display = (u'\u2500' * 60 + f"\nTask:\t\t\t\t{task}"
                                     f"\nAssigned to:\t\t{name}"
                                     f"\nDate assigned:\t\t{date_created}"
                                     f"\nDue date:\t\t\t{date_due}"
                                     f"\nTask Complete?\t\t{status}"
                                     f"\nTask description:\n {descr}" + "\n" + u'\u2500' * 60)
    return task_display

# Define function to display a specific task
def display_selected(selection):
    for i in task_dict:
        if task_dict[i] == task_dict[selection]:
            print(f'\nTask Number: {i}')
            print(display(task_dict[i]["task"], task_dict[i]["user"], task_dict[i]["date"],
                          task_dict[i]["due"], task_dict[i]["complete"], task_dict[i]["description"]) + "\n")

#--- Defining Menu Option Functions ---#
# Define function to register a new user
def reg_user():
    # Request new username from user
    while True:
        new_username = input("Enter new username: ")
        # Error message if new username is already in list of users
        if new_username in user_list:
            print("Sorry, that username is already taken. Please try again.")
        else:
            break

    # Request new password from user
    new_password = input("Enter new password: ")

    # Confirm new username and password
    print("Confirm username and password:")
    while True:
        check_username = input("Re-enter username: ")
        if check_username == new_username:
            break
        else:
            print("The username did not match. Please try again.")
    while True:
        check_password = input("Re-enter password: ")
        if check_password == new_password:
            break
        else:
            print("The password did not match. Please try again.")

    # Add new username and password to user.txt file when confirmation successful
    with open('user.txt', 'a') as users:
        users.write(f"\n{new_username}, {new_password}")
        print("New user successfully added.")

# Define function to add a new task
def add_task():
    # Ask user for task information
    user = input("Enter username: ")
    task_title = input("Enter the task's title: ")
    description = input("Enter the task description: ")
    due_date = input("Enter the due date: ")
    date = input("Enter today's date: ")
    complete = input("Is the task complete (Yes/No)? ")

    # Format and add task information to tasks.txt file
    with open('tasks.txt', 'a') as tasks:
        tasks.write(f"\n{user}, {task_title}, {description}, {date}, {due_date}, {complete}")

# Define function to view all tasks
def view_all():
    # Print information for every task from task dictionary
    for key in task_dict:
        print(display(task_dict[key]["task"], task_dict[key]["user"], task_dict[key]["date"],
                      task_dict[key]["due"], task_dict[key]["complete"], task_dict[key]["description"]))

# Define function to view a single user's tasks
def view_mine():
    # Only print tasks from dictionary for user that matches logged-in user
    for key in task_dict:
        if task_dict[key]["user"] == username:
            print(f"Task ID: {key}")
            print(display(task_dict[key]["task"], task_dict[key]["user"], task_dict[key]["date"],
                          task_dict[key]["due"], task_dict[key]["complete"], task_dict[key]["description"]))

# Define functions to generate text file reports
# Task overview report
def task_report():
    # Find the total number of tasks generated
    total_tasks = len(task_dict)

    # Find number of completed tasks
    complete_tasks = 0
    for key in task_dict:
        if task_dict[key]["complete"] == "Yes":
            complete_tasks += 1

    # Find number of incomplete tasks
    incomplete_tasks = len(task_dict) - complete_tasks

    # Find number of overdue tasks
    overdue_tasks = 0
    for key in task_dict:
        if task_dict[key]["complete"] == "No":
            # Convert string dates to date objects
            format = "%d %b %Y"
            due_date = datetime.strptime(task_dict[key]["due"], format)
            # Compare due dates to today's date and count number of tasks overdue
            today = datetime.today()
            if due_date < today:
                overdue_tasks += 1

    # Calculate percentage of incomplete tasks
    percentage_incomplete = int((incomplete_tasks/total_tasks)*100)

    # Calculate percentage of overdue tasks
    percentage_overdue = int((overdue_tasks/total_tasks)*100)

    # Create task overview file
    with open("task_overview.txt", "w") as f:
        f.write(f"Total Tasks:      {total_tasks}"
                f"\nCompleted Tasks:  {complete_tasks}"
                f"\nIncomplete Tasks: {incomplete_tasks}"
                f"\nOverdue Tasks:    {overdue_tasks}"
                f"\nPercentage of Tasks Incomplete: {percentage_incomplete}%"
                f"\nPercentage of Tasks Overdue:    {percentage_overdue}%")

# User overview report
def user_report():
    # Find the total number of users registered
    total_users = len(user_list)

    # Find the total number of tasks generated and tracked
    total_tasks = len(task_dict)

    # User specific statistics
    # Total tasks assigned to user
    user_tasks = 0
    for task in task_dict:
        if task_dict[task]["user"] == username:
            user_tasks += 1

    # Calculate percentage of tasks assigned to user out of total tasks
    percentage_assigned = int((user_tasks/total_tasks)*100)

    # Calculate the percentage of tasks the user has completed
    complete_tasks = 0
    for task in task_dict:
        if task_dict[task]["user"] == username and task_dict[task]["complete"] == "Yes":
            complete_tasks += 1
    percentage_complete = int((complete_tasks/user_tasks)*100)

    # Calculate the percentage of tasks the user still needs to complete
    percentage_incomplete = 100 - percentage_complete

    # Calculate the percentage of incomplete tasks that are overdue
    overdue_tasks = 0
    for key in task_dict:
        if task_dict[key]["user"] == username and task_dict[key]["complete"] == "No":
            # Convert string dates to date objects
            format = "%d %b %Y"
            due_date = datetime.strptime(task_dict[key]["due"], format)
            # Compare due dates to today's date and count number of tasks overdue
            today = datetime.today()
            if due_date < today:
                overdue_tasks += 1
    percentage_overdue = int((overdue_tasks/user_tasks)*100)

    # Create user overview file
    with open("user_overview.txt", "w") as f:
        f.write(f"Total Users: {total_users}"
                f"\nTotal Tasks: {total_tasks}"
                f"\nPercentage Assigned to You:          {percentage_assigned}%"
                f"\nPercentage of Your Tasks Completed:  {percentage_complete}%"
                f"\nPercentage of Your Tasks Incomplete: {percentage_incomplete}%"
                f"\nPercentage of Your Tasks Overdue:    {percentage_overdue}%")

# Define function to display summary statistics
def summary_stats():
    # Generate reports with statistics
    task_report()
    user_report()

    # Read task overview
    with open("task_overview.txt", "r") as f:
        task_overview = f.read()
    with open("user_overview.txt", "r") as f:
        user_overview = f.read()

    # Print files to console
    print("Task Overview\n" + u'\u2500' * 40)
    print(task_overview)
    print(u'\u2500' * 40 + "\nUser Overview\n" + u'\u2500' * 40)
    print(user_overview + "\n" + u'\u2500' * 40)

# Define function to overwrite tasks text file with user's changes
def tasks_overwrite():
    # Clear file
    with open("tasks.txt", "w") as f:
        f.truncate(0)
    # Write each task to file
    for task in task_dict:
        task_print = f"\n{task_dict[task]['user']}, {task_dict[task]['task']}, {task_dict[task]['description']}, " \
                     f"{task_dict[task]['date']}, {task_dict[task]['due']}, {task_dict[task]['complete']}"
        with open("tasks.txt", "a") as f:
            f.write(task_print)

#=== Read Text Files ===#
# Create a list of valid username and password pairs
with open("user.txt", "r") as f:
    # Remove blank lines to avoid IndexError
    lines = filter(None, (line.rstrip() for line in f))
    valid_logins = []
    for line in lines:
        valid_logins.append(line.strip("\n").split(", "))

# Create a list of usernames
user_pass = []
for x in valid_logins:
    for item in x:
        user_pass.append(item)
        user_list = user_pass[0::2]

# Create a nested dictionary of tasks
task_dict = task_dictionary()

#=== Login Section ===#
# Ask user for login details
login = False

while login == False:
    # Request username from user
    username = input("Enter username: ")
    password = input("Enter password: ")

    # Check if username and password pair is in list of users
    if [username, password] in valid_logins:
        login = True
    # Error messages when username or password incorrect
    else:
        if username in user_list:
            print("Incorrect password. Please try again.")
        else:
            print("User does not exist. Please try again.")

#==== Menu Section ====
# Display menu when username and password in database
while login == True:
    if username == "admin":
        # Display full menu to admin
        # Ask user for selection and convert input to lowercase
        menu = input("Please select one of the following options: \nr\t-\tregister user "
          "\na\t-\tadd task \nva\t-\tview all tasks \nvm\t-\tview my tasks"
            "\ngr\t-\tgenerate reports \nds\t-\tdisplay statistics "
            "\ne\t-\texit\n").lower()

    else:
        # Display limited menu
        # Ask user for selection and convert input to lowercase
        menu = input("Please select one of the following options: "
          "\na\t-\tadd task \nva\t-\tview all tasks \nvm\t-\tview my tasks "
                     "\ngr\t-\tgenerate reports \ne\t-\texit\n").lower()

    ## Add a new user to user.txt file ##
    if menu == "r":
        # Only admin can register new users
        if username == "admin":
            reg_user()
        else:
            print("Sorry, you do not have permission to access this option.")

    ## Add a new task to tasks.txt file ##
    elif menu == "a":
        add_task()
        # Add task to task dictionary
        task_dict = task_dictionary()

    ## View all tasks ##
    elif menu == "va":
        view_all()

    ## View my tasks ##
    elif menu == "vm":
        view_mine()
        vm = True
        while vm == True:

            # Allow user to select task
            selection = int(input("Enter the number of the task you wish to edit "
                                  "or enter -1 to return to the main menu: "))

            # If user chooses to return to main menu exit vm while loop
            if selection == -1:
                vm = False
                break

            else:
                # Display the selected task
                display_selected(selection)

                # User chooses to either mark the task as complete or edit the task
                option = input("Please select one of the following options:"
                                   "\nm\t-\tmark as complete \ne\t-\tedit task\n")

                # Option m - Mark task as complete
                if option == "m":
                    # Change "completed" value in dictionary to "Yes"
                    task_dict[selection]["complete"] = "Yes"
                    print("Task marked as complete")
                    # Alter task in tasks text file
                    tasks_overwrite()

                # Option e - Edit task
                if option == "e":
                    # Only incomplete tasks can be edited
                    if task_dict[selection]["complete"] == "Yes":
                        print("Task must be incomplete to be edited")
                    else:
                        edit = True
                        # User chooses what they want to edit
                        while edit == True:
                            choice = input("Please select one of the following options:"
                                           "\nt\t-\tedit task title \nu\t-\tedit the username that the task is "
                                           "assigned to \nd\t-\tedit due date \ne\t-\texit task\n")

                            while True:
                                # Choice t - edit task title
                                if choice == "t":
                                    new_title = input("Enter new title: ")
                                    # Change "task" value in dictionary to new_title
                                    task_dict[selection]["task"] = new_title

                                    # Display change to user and ask if changes are correct
                                    display_selected(selection)
                                    correct = input("Is this correct? \ny\t-\tyes \nn\t-\tno\n")
                                    # If changes are correct change text file and return to edit menu,
                                    # if not ask user to enter new title again
                                    if correct == "y":
                                        tasks_overwrite()
                                        break
                                    else:
                                        pass

                                # Choice u - edit task username
                                if choice == "u":
                                    edited_user = input("Enter username of the person assigned to this task: ")
                                    # Change "user" value in dictionary to edited_user
                                    task_dict[selection]["user"] = edited_user

                                    # Display change to user and ask if changes are correct
                                    display_selected(selection)
                                    correct = input("Is this correct? \ny\t-\tyes \nn\t-\tno\n")
                                    # If changes are correct change text file and return to edit menu,
                                    # if not ask user to enter new user again
                                    if correct == "y":
                                        tasks_overwrite()
                                        break
                                    else:
                                        pass

                                # Choice d - edit due date
                                if choice == "d":
                                    new_due_date = input("Enter the task's new due date: ")
                                    # Change "due" value in dictionary to new_due_date
                                    task_dict[selection]["due"] = new_due_date

                                    # Display change to user and ask if changes are correct
                                    display_selected(selection)
                                    correct = input("Is this correct? \ny\t-\tyes \nn\t-\tno\n")
                                    # If changes are correct change text file and return to edit menu,
                                    # if not ask user to enter new title again
                                    if correct == "y":
                                        tasks_overwrite()
                                        break
                                    else:
                                        pass

                                # Choice r - Return to main menu
                                if choice == "e":
                                    edit = False
                                    break

    ## Generate Reports ##
    elif menu == "gr":
        task_report()
        user_report()
        print("task_overview.txt and user_overview.txt have been generated")

    ## Display Summary Statistics ##
    elif menu == "ds":
    # Only admin can access summary statistics error message
        if username == "admin":
            summary_stats()
        else:
            print("Sorry, you do not have permission to access this option.")

    ## Exit ##
    elif menu == "e":
        print("Goodbye!!!")
        exit()

    # If user does not correctly pick a menu option
    else:
        print("You have made a wrong choice. Please try again")
