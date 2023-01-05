import service

service.Services()
print('========WGUPS Routing Program=======')
ans = True
while ans:
    print("""
    1. Lookup A Package By Package ID
    2. List All Packages By Time
    3. Total Mileage Traveled By All Trucks
    4. Exit/Quit
    """)

    ans = int(input("What Would You Like To Do? "))
    if ans == 1:
        print("do something")  # fix me
    elif ans == 2:
        print("do something")  # fix me
    elif ans == 3:
        print("do something")  # fix me
    elif ans == 4:
        print("\n Goodbye!")
        ans = None
    else:
        print("\n Not Valid Choice. Try again")

