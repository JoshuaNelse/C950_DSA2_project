from CsvHelper import distance_table_to_hash_map, package_table_to_hash_map
from TruckManager import TruckManager as Tm


def process_shipments(stop_time=None):
    Tm.reset_trucks()

    if stop_time is not None:
        Tm.set_stop_time(stop_time)

    #######
    # mapping csv files to hash maps
    with open('resources/WGUPS distance table.csv') as csv_file:
        distance_table = distance_table_to_hash_map(csv_file)
    with open('resources/WGUPS package file.csv') as csv_file:
        package_table = package_table_to_hash_map(csv_file)

    #######
    # indexes used to manually load trucks.
    truck_1_packages = [1, 4, 11, 13, 14, 15, 16, 17, 19, 20, 21, 22, 24, 29, 34, 40]
    truck_2_packages = [2, 3, 5, 7, 8, 9, 10, 18, 23, 27, 33, 35, 36, 38, 39]
    truck_3_packages = [6, 12, 25, 26, 28, 30, 31, 32, 37]

    #######
    # loading trucks using packages indexes - O(N)
    Tm.load_truck(Tm.truck_1, truck_1_packages, package_table)
    Tm.load_truck(Tm.truck_2, truck_2_packages, package_table)
    Tm.load_truck(Tm.truck_3, truck_3_packages, package_table)

    #######
    # updating package id # 9 with correct address - O(1)
    update_package = package_table.get('9')
    update_package.address = '410 S State St'
    update_package.zip = '84111'

    #######
    # delivers all packages loaded into trucks - O(N^2)
    Tm.run_fleet(distance_table)

    #######
    # Print report for shipments
    Tm.print_report()


#######
# User Interface logic
is_running = True
while is_running:
    print("--- Package Shipping Warehouse Interface (Main Menu) ----")
    print('\tOptions:')
    print('\t1. \tComplete entire day of deliveries (See report)')
    print('\t2. \tSee status of deliveries at a specified time (See report)')
    print('\t3. \tQuit program')
    print()
    user_input = input('Input: ')

    if user_input == '1':
        process_shipments()
    elif user_input == '2':
        print('Please enter a time to see statuses. format: \'8:00 AM\'')
        input_time = input('Input: ')
        process_shipments(input_time)
    elif user_input == '3':
        is_running = False
        print('Goodbye!')
