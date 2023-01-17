from utils import Utils

my_utils = Utils()

print('------------------------ WGUPS Routing Program ------------------------')

ans = True
while ans:
    print("""
    1. View Package Status And Info By Time
    2. Search For A Package by Package ID
    3. Total Mileage Traveled By All Trucks
    4. Exit/Quit
    """)

    ans = int(input("Please select a number: "))
    if ans == 1:
        user_input = input("Please enter by time (Example hour formate: 09:00:00 / 13:15:00):")
        my_utils.display_packages_by_time(user_input)
    elif ans == 2:
        user_input = int(input("Please enter a package ID number: "))
        my_utils.display_package_by_pkg_id(user_input)
    elif ans == 3:
        my_utils.display_all_trucks_traveled_by_time()
    elif ans == 4:
        print("\n Goodbye!")
        exit()
    else:
        print("\n Not Valid Choice. Try again")
