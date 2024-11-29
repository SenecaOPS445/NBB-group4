import subprocess
#This function deletes a user from the system
def delete_user():
    """Function to delete a system user."""
#This line of code will ask user to enter a username which they want to remove. strip() will remove any whitespace from the input provided by user.
    username = input("Enter the username to delete: ").strip()

# This if statement will check if the username is empty. If it is than an error message will be returned with says "Username cannot be empty". The return statement at end will immediately exits the function.
    if not username:
        print("Error: Username cannot be empty.")
        return

#The try block first run the subprocess.run to fetch the user information from the passwd database. the stdout will capture the output of command for further processing. This block will etract users home directory which is 6th field [5].
    try:
        user_info = subprocess.run(
            ["getent", "passwd", username], 
            check=True, 
            stdout=subprocess.PIPE, 
            text=True
        )
        home_dir = user_info.stdout.split(":")[5]
#The except block here raise an exception if getent command fails if the username does not exsist in the databasr then an error message will be displayed. At last, the return exits the function as there is not information to proceed for username deletion.
    except subprocess.CalledProcessError:
        print(f"Error: User '{username}' does not exist.")
        return

#This block of code will ask user for confirmation if  they really want to delete the given user. If the user does not enter yes or eneterd nothing that the process of user deletion will get cancelled and after it will exit the delete_user function    
    confirm = input(f"Are you sure you want to delete user '{username}'? (yes/no): ").strip().lower()
    if confirm != "yes" and confirm != "":
        print("User deletion cancelled.")
        return

#This line of code will prompt user if they want to delete the users home directory along with the user account.
    remove_home = input("Do you want to remove the user's home directory? (yes/no): ").strip().lower()

#This if-else statement says that if user enters yes or entered nothing will delete the home directory. -r flag is added to the remove_flag list. else if the user entered a no it will leave the remove_flag list empty and the home directory will not be removed
    if remove_home == "yes" or remove_home == "":
        remove_flag = ["-r"]
    else:
        remove_flag = []

#This line of code explaines the delete command used to delete the user.
    command = ["sudo", "userdel"] + remove_flag + [username]

#This try block execute the constructed command and handle the errors that may occur while deleting the user. At last, the success message will be printed on screen if the user and home directory is deleted.
    try:
       
        subprocess.run(command, check=True, stderr=subprocess.PIPE)
        print(f"User '{username}' deleted successfully!")
        print(f"Home directory '{home_dir}' removed successfully.")
#This except block will handle any error occured by subprocess.run if the userdel command is failed and will print the error message from stderr from the failed command            
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to delete user '{username}'. {e.stderr.decode().strip()}")
#This except block will capture the unexpected errors that can occur. 
    except Exception as e:
        print(f"Unexpected error: {e}")

