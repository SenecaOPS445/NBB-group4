# Fall 2024 Assignment 2

--> Project Name:
User Management System

Project Description:
The User Management System is a Python-based script designed to simplify and automate the management of system users. It provides an intuitive menu-driven interface for creating, deleting, listing all the user, displaying their information  and managing user accounts, home directories, and permissions. This tool ensures efficient user management while minimizing manual efforts for system administrators.

--> Team Members and Contributions:

1) Prashant Ghimire:

Developed the create_user() function, enabling the creation of new users with custom attributes.
Built the main() function to serve as the interactive menu for user operations and handled its integration.

2) Tanishq Satish Kedare:

Created the list_users() function to list all existing system users.
Developed the display_user_info() function to fetch and display detailed information about a specific user.

3) Simranpreet Kaur:

Designed the delete_user() function to safely delete user accounts and optionally their home directories.

--> Key Features:

1) User Creation: Allows adding new system users with options for custom usernames, UIDs, primary groups, expiry dates, and home directories.
2) User Deletion: Safely removes user accounts and provides an option to delete their associated home directories.
3) List Users: Displays all existing users in the system.
4) User Information: Fetches and displays details like username, UID, GID, home directory, and more.
5) Directory Management: Handles both default and custom home directories, including ownership and permissions.
6) Sudoers File Modification: Configured the sudoers file to allow specific commands (mkdir, useradd, userdel, and chown) without requiring a password for efficient script execution.

--> Steps to Run the Script:

Clone the repository to your local system:
git clone <repository-url>

Navigate to the project directory and execute the Python script:

python3 <script-name>.py
Now, You’ll be presented with a menu to manage users effortlessly.

--> Special Notes (Configuration):

The sudoers file has been edited to remove password requirements for specific commands to ensure smooth execution of this script:

prashant ALL=(ALL) NOPASSWD: /bin/mkdir, /usr/sbin/useradd, /usr/sbin/userdel, /bin/chown

--> Conclusion:
This system is built with simplicity and ease of use in mind, making it ideal for basic user management tasks.

