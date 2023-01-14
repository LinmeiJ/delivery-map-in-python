# from truck import Truck
# from utils import Utils
#
# utils = Utils()
#
# truck = Truck(pkgs.package_urgent_list, pkgs.package_urgent_delayed_list,
#               pkgs.package_not_urgent_delayed_list, pkgs.package_with_wrong_address, pkgs.package_with_truck2_only,
#               pkgs.package_must_on_same_truck,
#               pkgs.package_remaining_packages)
# truck.load_cargo()
#
# # despite package id 15 requires delivery at 9:00AM, based on the current route, it will deliver on time
# truck1_total_time, truck1_total_mile, route1 = Service.plan_and_deliver_packages(truck.truck1, "truck1",
#                                                                                  '08:00 AM')  # driver1
# # let truck2 wait until 9:05 to leave the hub for loading the delayed packages
# truck.load_delayed_packages()
# truck2_total_time, truck2_total_mile, route2 = Service.plan_and_deliver_packages(truck.truck2, "truck2",
#                                                                                  '09:05 AM')  # driver2
# start_delivery_time = route1[-1].get('delivery_time')
# truck3_total_time, truck3_total_mile, route3 = Service.plan_and_deliver_packages(truck.truck3, "truck3",
#                                                                                  start_delivery_time)  # diver1

# print(f'{truck1_total_time}, {truck1_total_mile}')
# print(f'{truck2_total_time}, {truck2_total_mile}')
# print(f'{truck3_total_time}, {truck3_total_mile}')
from utils import Utils

my_utils = Utils()

print(my_utils.route1)
print(my_utils.route2)
print(0)


print('======== WGUPS Routing Program =======')
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
        print("View Package Status And Info By Time")
    elif ans == 2:
        print("Search For Package by Package ID")  # fix me
    elif ans == 3:
        print("do something")  # fix me
    elif ans == 4:
        print("\n Goodbye!")
        ans = None
    else:
        print("\n Not Valid Choice. Try again")
#
# truck = Truck(pkgs.package_urgent_list, pkgs.package_urgent_delayed_list,
#               pkgs.package_not_urgent_delayed_list, pkgs.package_with_wrong_address, pkgs.package_with_truck2_only,
#               pkgs.package_must_on_same_truck,
#               pkgs.package_remaining_packages)
# truck.load_cargo()
#
# # despite package id 15 requires delivery at 9:00AM, based on the current route, it will deliver on time
# truck1_total_time, truck1_total_mile, route1 = Service.plan_and_deliver_packages(truck.truck1, "truck1",
#                                                                                  '08:00 AM')  # driver1
# # let truck2 wait until 9:05 to leave the hub for loading the delayed packages
# truck.load_delayed_packages()
# truck2_total_time, truck2_total_mile, route2 = Service.plan_and_deliver_packages(truck.truck2, "truck2",
#                                                                                  '09:05 AM')  # driver2
# start_delivery_time = route1[-1].get('delivery_time')
# truck3_total_time, truck3_total_mile, route3 = Service.plan_and_deliver_packages(truck.truck3, "truck3",
#                                                                                  start_delivery_time)  # diver1