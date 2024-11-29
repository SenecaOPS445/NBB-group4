import subprocess # Import the subprocess module for the execution of system commands.

def list_users():
    """Function to list all users on the system."""
    try:
        # Execute the 'getent passwd' command to get user information from the system.
        # The 'getent passwd' command retrieves user account details archived in the system's passwd database.
        resultUsers = subprocess.run(
            ["getent", "passwd"], # Command to retrieve all users
            check=True, # Ensures an exception is raised if the command fails
            stdout=subprocess.PIPE, # Captures the command's output (stdout)
            stderr=subprocess.PIPE, # Captures the command's error output (stderr)
            text=True
        )
        
        # The following command decodes the captured output from bytes to string
        # Remove any leading/trailing whitespace and split the result into lines (one user per line)
        users = resultUsers.stdout.strip().split("\n")

        # Check if the users list is empty, if it's empty that means no users found
        if not users:
            print("No users found.") # Inform the user that no users exist on the system
            return

        # Print the header for the user list
        print("List of Users:")
        for user in users:
            # Each line of output corresponds to a user entry, formatted as colon-separated fields
            # Extract the username, which is the first field before the first colon (:)
            username = user.split(":")[0]
            print(username) # Print the extracted username to the console
    
    except subprocess.CalledProcessError as e:
        # This block handles errors that occur when the 'getent' command fails
        # The return code and error message from the command are displayed
        print(f"Error: Failed to list users. Command exited with code {e.returncode}. {e.stderr.decode().strip()}")
    except Exception as e:
        # This block catches any unexpected errors and prints the exception message
        print(f"Unexpected error: {e}")


def display_user_info():
    """Function to display detailed information about a specific user."""
    # Prompt the user to input a username for which they want to fetch details
    username = input("Enter the username to display details: ").strip()

    # Validate the input to ensure the username is not empty
    if not username:
        print("Error: Username cannot be empty.") # Inform the user about invalid input
        return # Exit the function if the input is invalid
    
    try:
        # Run the 'getent passwd <username>' command to fetch details for the specified user
        # This command retrieves the line from the passwd database corresponding to the username
        resultUserInfo = subprocess.run(
["getent", "passwd", username], # Command to get user details
 check=True, # Ensures an exception is raised if the command fails
 stdout=subprocess.PIPE, # Captures the command's output (stdout)
 stderr=subprocess.PIPE, # Captures the command's error output (stderr)
 text=True
)
        
        # Decode the captured output from bytes to string and remove any leading/trailing whitespace
        user_info = resultUserInfo.stdout.strip()
        
        # Check if the command returned an empty result, indicating the user was not found
        if not user_info:
            print(f"Error: User '{username}' not found.") # Inform the user that the username does not exist
            return
        
        # The user information is a single line with colon-separated fields:
        # 'username:password:UID:GID:comment:home_directory:login_shell'
        # Split the user information into individual fields
        user_details = user_info.split(":")
        
         # Display the detailed user information with descriptive labels
        print("\nUser Details:")
        print(f"Username: {user_details[0]}") # The username (e.g., 'root' or 'john') 
        print(f"User ID (UID): {user_details[2]}") # The user ID (numeric identifier)
        print(f"Group ID (GID): {user_details[3]}") # The group ID (numeric identifier for the primary group)
        print(f"Comment: {user_details[4]}") # The comment or description field (optional information)
        print(f"Home Directory: {user_details[5]}") # The path to the user's home directory
        print(f"Login Shell: {user_details[6]}") # The default shell assigned to the user (e.g., '/bin/bash')
    
    except subprocess.CalledProcessError as e:
        # Handle errors that occur when the 'getent' command fails for the specific username
        # Display the return code and error message for troubleshooting
        print(f"Error: Failed to retrieve details for user '{username}'. {e.stderr.strip()}")
    except Exception as e:
        # Catch any other unexpected errors and print the exception message
        print(f"Unexpected error: {e}")

# Uncomment the following lines to test the functions interactively:
# list_users()           # Call this function to list all users on the system
# display_user_info()    # Call this function to display information for a specific user
