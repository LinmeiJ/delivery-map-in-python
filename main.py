from utils import Utils

my_utils = Utils()

print('======== WGUPS Routing Program =======')


ans = True
while ans:
    print("""
    1. View Package Status And Info By Time (Example formate: 12:00 PM / 09:00 AM)
    2. Search For A Package by Package ID
    3. Total Mileage Traveled By All Trucks
    4. Exit/Quit
    """)

    ans = int(input("Please select a number: "))
    if ans == 1:
        my_utils.display_packages_by_time(ans)
    elif ans == 2:
        id_num = int(input("Please enter a package ID number: "))
        my_utils.display_package_by_pkg_id(id_num)
    elif ans == 3:
        my_utils.display_all_trucks_traveled_by_time()
    elif ans == 4:
        print("\n Goodbye!")
        exit()
    else:
        print("\n Not Valid Choice. Try again")
