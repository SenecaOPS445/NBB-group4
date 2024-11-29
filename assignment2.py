#!/usr/bin/env python3

from Prashant import create_user
from a2 import delete_user
from Tanishq import list_users, display_user_info

# a main function to handle the menus and calling the relevant functions.  
def main():
    """Main menu-driven function to manage users."""
    while True:
        # Display the menu options
        print("\nUser Management System")
        print("1. Create a new user")
        print("2. Delete a user")
        print("3. List all users")
        print("4. Display user details")
        print("5. Exit")
        
        # Ask the user to choose an option
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == "1":
            create_user()  # Call function to create a user
        elif choice == "2":
            delete_user()  # Call function to delete a user
        elif choice == "3":
            list_users()  # Call function to list all users
        elif choice == "4":
            display_user_info()  # Call function to display user info
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break  # Exit the loop and end the program
        else:
            print("Invalid choice. Please select a valid option (1-5).")

if __name__ == "__main__":
    main()
