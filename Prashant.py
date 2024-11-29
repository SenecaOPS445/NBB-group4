#!/usr/bin/env python3

import subprocess  
from datetime import datetime 
import os  


def create_user():
    """Function to create a new system user with options."""
    username = input("Enter the username to create: ").strip()
    
    if not username or " " in username or not username.isalnum():
        print("Error: Invalid username. It cannot be empty or contain spaces or special characters.")
        return

    comment = input("Enter a comment for the user (optional): ").strip()
    expiry_date = input("Enter an expiry date (YYYY-MM-DD) (optional): ").strip()

    if expiry_date:
        try:
            expiry_date_obj = datetime.strptime(expiry_date, "%Y-%m-%d")
            if expiry_date_obj < datetime.now():
                print("Error: Expiry date must be in the future.")
                return
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return

    primary_group = input("Enter a primary group for the user (optional): ").strip()

    if primary_group:
        resultPRGRP = subprocess.run(["getent", "group", primary_group], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if not resultPRGRP.stdout.strip():
            print(f"Error: The group '{primary_group}' does not exist.")
            return

    home_dir = input("Enter a custom home directory (optional): ").strip()

    if home_dir and not os.path.isdir(home_dir):
        try:
            subprocess.run(["sudo", "mkdir", "-p", home_dir], check=True)
            print(f"Custom home directory '{home_dir}' created successfully.")
            
        except subprocess.CalledProcessError as e:
            print(f"Failed to create directory '{home_dir}': {e}")
            return

    uid = input("Enter a UID for the user (optional, leave empty for automatic assignment): ").strip()
    
    if uid:
        if not uid.isdigit():
            print("Error: UID must be a numeric value.")
            return
        else:
            uid = int(uid)
            resultUID = subprocess.run(["getent", "passwd"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            users = resultUID.stdout.strip().split("\n")
            for user in users:
                user_info = user.split(":")
                if int(user_info[2]) == uid:
                    print(f"Error: UID {uid} is already in use by another user.")
                    return

    command = ["sudo", "useradd", "-m", username]
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
        subprocess.run(command, check=True, stderr=subprocess.PIPE)
        print(f"User '{username}' created successfully!")
        
        if home_dir:
            if primary_group:
                user_group = primary_group
            else:
                user_group = username
            
            subprocess.run(["sudo", "chown", f"{username}:{user_group}", home_dir], check=True)
            print(f"Permissions for '{home_dir}' changed to '{username}:{user_group}'.")

    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to create user '{username}'. {e.stderr.decode().strip()}")
    except Exception as e:
        print(f"Unexpected error: {e}")

