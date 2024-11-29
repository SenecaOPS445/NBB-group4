#!/usr/bin/env python3

import subprocess  
from datetime import datetime 
import os  

# This function will create a system user after asking inputs for the user options. The options will be validated with several checks.
def create_user():
    """Function to create a new system user with options."""

    # ask for the username
    username = input("Enter the username to create: ").strip()
    
    # if the username is empty, or blank spaces or is not alphanumeric, then the return statement immediately exits the current function 
    if not username or " " in username or not username.isalnum():
        print("Error: Invalid username. It cannot be empty or contain spaces or special characters.")
        return

    # ask for the optional comment
    comment = input("Enter a comment for the user (optional): ").strip()
    # ask for the optional expiry date of the user
    expiry_date = input("Enter an expiry date (YYYY-MM-DD) (optional): ").strip()

    # validating expiry_date 
    if expiry_date:
        try:
            # here, the datetime.strptime() method is used to check if the input date maches the format "YYYY-MM-DD" and convert the string into a datetime object. if the format doesn't match, it will raise a value error which is handled by except block.
            expiry_date_obj = datetime.strptime(expiry_date, "%Y-%m-%d") 

            # if the input date is in the past, print an error message and exit the function
            if expiry_date_obj < datetime.now():
                print("Error: Expiry date must be in the future.")
                return
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return
    
    # ask for the optional primary group for the user, if not provided, a default primary group will be added with the user's name and the user will be added to that group
    primary_group = input("Enter a primary group for the user (optional): ").strip()

    # validating primary_group
    if primary_group:
        # run the system command getent group primary_group (group name) to see if the primary group exist. if not, throw an error and exit the function.
        resultPRGRP = subprocess.run(["getent", "group", primary_group], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if not resultPRGRP.stdout.strip():
            print(f"Error: The group '{primary_group}' does not exist.")
            return

    # ask for the custom and optional home directory for the user
    home_dir = input("Enter a custom home directory (optional): ").strip()

    # validating home_dir
    if home_dir and not os.path.isdir(home_dir):
        try:
            # create a custom home directory if a input is provided
            subprocess.run(["sudo", "mkdir", "-p", home_dir], check=True)
            print(f"Custom home directory '{home_dir}' created successfully.")
            
        except subprocess.CalledProcessError as e:
            # print an error message if the directory creation fails and exit the function 
            print(f"Failed to create directory '{home_dir}': {e}")
            return

    # ask for the custom and optional uid
    uid = input("Enter a UID for the user (optional, leave empty for automatic assignment): ").strip()
    
    if uid:
        # verify that the UID is numeric
        if not uid.isdigit():
            print("Error: UID must be a numeric value.")
            return
        else:
            # convert the UID to an integer
            uid = int(uid)
            # we run the getend passwd command to get list of all current users with their information, here we are specifically looking for the UID information
            resultUID = subprocess.run(["getent", "passwd"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            # split the output into a list of user records
            users = resultUID.stdout.strip().split("\n")

            # iterate through each user record to check if the UID is already in use
            for user in users:
                user_info = user.split(":")
                if int(user_info[2]) == uid:
                    # print an error message and exit if the UID is already in use
                    print(f"Error: UID {uid} is already in use by another user.")
                    return

    # here, we are creating a list named command and build the command which we will use further
    command = ["sudo", "useradd", "-m", username]

    # if the inputs are provided, we add the options to the command list  
    if comment:
        command.extend(["-c", comment])
    if expiry_date:
        command.extend(["-e", expiry_date])
    if home_dir:
        command.extend(["-d", home_dir])
    if uid:
        command.extend(["-u", uid])
    if primary_group:
        command.extend(["-g", primary_group])
    

    try:
        # here, we run the command using the subprocess module
        subprocess.run(command, check=True, stderr=subprocess.PIPE)
        print(f"User '{username}' created successfully!")
        
        # if a custom home directory, change the ownership of that directory to the new user since the default permission is owned by root
        if home_dir:
            if primary_group:
                user_group = primary_group
            else:
                user_group = username
            
            # change ownership of the home directory to the new user using the chown command
            subprocess.run(["sudo", "chown", f"{username}:{user_group}", home_dir], check=True)
            print(f"Permissions for '{home_dir}' changed to '{username}:{user_group}'.")

    # if useradd command fails, raise a CalledProcessError
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to create user '{username}'. {e.stderr.decode().strip()}")

    # catch any other unexpected errors and print an error message
    except Exception as e:
        print(f"Unexpected error: {e}")

