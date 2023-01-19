# Student First Name: Linmei
# Student Last Name: Mills
# Student ID: 001530700

from utils import Utils

# Initialize a utils object where stores the program logics and flow
my_utils = Utils()

print('------------------------ WGUPS Routing Program ------------------------')

# User Interface
ans = True
while ans:
    print("""
    1. View Package Status And Info By Time
    2. Search For A Package by Package ID and Time
    3. Total Mileage Traveled By All Trucks
    4. Exit/Quit
    """)

    ans = int(input("Please select a number: "))
    if ans == 1:
        user_input = input("Please enter by time (Example hour formate: 09:00:00 / 13:15:00):")
        my_utils.display_packages_by_time(user_input)
    elif ans == 2:
        pkg_id = int(input("Please enter a package ID number: "))
        time = input("Please enter a time (Example hour formate: 09:00:00 / 13:15:00):")
        my_utils.display_packages_by_time_and_id(pkg_id, time)
    elif ans == 3:
        my_utils.display_all_trucks_traveled_by_time()
    elif ans == 4:
        print("\n Goodbye!")
        exit()
    else:
        print("\n Not Valid Choice. Try again")
