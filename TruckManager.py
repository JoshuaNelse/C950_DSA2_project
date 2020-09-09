from Truck import Truck
from TimeHelper import Clock
from PackageEntity import PackageStatuses


# Singleton  object
class TruckManager:
    truck_1 = Truck(truck_id='truck_1')
    truck_2 = Truck(truck_id='truck_2')
    truck_3 = Truck(truck_id='truck_3')

    #######
    # O(1) - constant
    # creates new truck objects (used for completing deliveries multiple times over)
    @classmethod
    def reset_trucks(cls):
        cls.truck_1 = Truck(truck_id='truck_1')
        cls.truck_2 = Truck(truck_id='truck_2')
        cls.truck_3 = Truck(truck_id='truck_3')

    #######
    # O(1) - constant
    # to_string formatter for the TruckManager object
    @classmethod
    def __str__(cls):
        return '''TruckManager: ( 
                    truck_1: {},
                    truck_2: {},
                    truck_3: {}
              ) 
        '''.format(cls.truck_1.packages, cls.truck_2.packages, cls.truck_3.packages)

    #######
    # O(N^2) - quadratic (calls 'send_out_truck' which is a quadratic function)
    # sends out trucks based on driver availability
    @classmethod
    def run_fleet(cls, distance_table):
        cls.send_out_truck(cls.truck_1, distance_table, Clock('8:00', 'AM'))
        cls.send_out_truck(cls.truck_2, distance_table, Clock('11:30', 'AM'))
        cls.send_out_truck(cls.truck_3, distance_table, Clock('9:10', 'AM'), ignore_deadline=True)

    #######
    # O(N^2) - quadratic time.
    # Delivers all packages that were loaded onto a specific truck
    @classmethod
    def send_out_truck(cls, truck, distance_table, start_clock, ignore_deadline=False):
        truck.start_clock(start_clock)

        # Loops until all packages in truck are delivered
        # 1. First checks if more than one package go to the same address
        # 2. Second checks if any deadlines are approaching that need to be prioritized
        # 3. Lastly, uses a greedy algorithm to find nearest location to deliver next package
        while not truck.is_route_finished() and not truck.clock_stopped():
            package_with_deadline = truck.approaching_deadline() if not ignore_deadline else None
            package_for_same_address = truck.package_for_current_address()
            if package_for_same_address is not None:
                next_delivery = package_for_same_address
            elif package_with_deadline is not None:
                next_delivery = package_with_deadline
            else:
                next_delivery = cls.get_closest_package(truck, distance_table)
            truck.deliver_package(next_delivery, distance_table)
        # After all packages are delivered drive back to HUB
        truck.drive_back_to_hub(distance_table)

    #######
    # O(N) - linear
    # greedy algorithm (find closest destination from current location)
    @classmethod
    def get_closest_package(cls, truck, distance_table):
        closest_package = truck.get_first_undelivered_package()
        closest_distance = distance_table.get_distance(truck.location, closest_package.address)

        for package in truck.packages:
            if package.status == PackageStatuses.DELIVERED:
                continue

            other_distance = distance_table.get_distance(truck.location, package.address)
            if other_distance < closest_distance:
                closest_package = package
                closest_distance = other_distance

        return closest_package

    #######
    # O(N) - linear
    # loads each package onto a given truck
    @classmethod
    def load_truck(cls, truck, package_list, package_table):
        for package_id in package_list:
            package = package_table.get(str(package_id))
            truck.load_package(package)

    #######
    # O(1) - constant
    # sets stop time on trucks. used for reporting status at a specific time of the day
    @classmethod
    def set_stop_time(cls, stop_time):
        time = stop_time[0: stop_time.index(' ')]
        period = stop_time[stop_time.index(' ') + 1:]

        cls.truck_1.stop_clock = Clock(time, period)
        cls.truck_2.stop_clock = Clock(time, period)
        cls.truck_3.stop_clock = Clock(time, period)

    #######
    # O(1) - constant
    # simply adds all miles traveled by all trucks
    @classmethod
    def get_miles_traveled_by_all_trucks(cls):
        return cls.truck_1.miles_traveled \
               + cls.truck_2.miles_traveled \
               + cls.truck_3.miles_traveled

    #######
    # O(N) - linear
    # report for the package information by delivery truck
    @classmethod
    def print_report(cls):
        PACKAGE_TABLE_HEADER = '|\tID\t|\tDELIVERY ADDRESS\t\t|\tCITY\t\t\t|\tSTATE\t|\tZIP\t\t|\tDEADLINE\t|\tWEIGHT\t' \
                               '|\tSTATUS\t\t|\tDELIVERY TIME\t|\tINSTRUCTIONS'
        hr = '--------------------------------------------------------------------------------------------------------' \
             '--------------------------------------------------------'
        print('////////////////////////////////////////////////////////')
        print('PACKAGE REPORT (BY TRUCK)\n')
        print('Truck 1: location {}, time arrived: {}, miles traveled {}'
              .format(cls.truck_1.location, cls.truck_1.clock.time_string(), cls.truck_1.miles_traveled))

        print(hr + '\n' + PACKAGE_TABLE_HEADER + '\n' + hr)
        for package in cls.truck_1.packages:
            print(cell_row_of(package))

        print('\n\nTruck 2: location {}, time arrived: {}, miles traveled {}'
              .format(cls.truck_2.location, cls.truck_2.clock.time_string(), cls.truck_2.miles_traveled))
        print(hr + '\n' + PACKAGE_TABLE_HEADER + '\n' + hr)
        for package in cls.truck_2.packages:
            print(cell_row_of(package))

        print('\n\nTruck 3: location {}, time arrived: {}, miles traveled {}'
              .format(cls.truck_3.location, cls.truck_3.clock.time_string(), cls.truck_3.miles_traveled))
        print(hr + '\n' + PACKAGE_TABLE_HEADER + '\n' + hr)
        for package in cls.truck_3.packages:
            print(cell_row_of(package))

        print('\n\nTotal miles traveled: {}'.format(cls.get_miles_traveled_by_all_trucks()))
        print('////////////////////////////////////////////////////////')


########
# O(1) -  constant
# format package entity for printing to screen
def cell_row_of(package_entity):
    pad = lambda string, size: \
        (string + ' ' * (size - len(string)) if size - len(string) > 0 else string[0:size - 5] + ' ... ') \
            if string is not None else ' - ' + ' ' * (size - len(' - '))
    pe = package_entity
    return '|\t{id}|\t{address}|\t{city}|\t{state}|\t{zip}|\t{deadline}|\t{weight}|\t{status}' \
           '|\t{delivery_time}|\t{instructions}'.format(id=pad(pe.id, 4),
                                                        address=pad(pe.address, 24),
                                                        city=pad(pe.city, 16),
                                                        state=pad(pe.state, 8),
                                                        zip=pad(pe.zip, 8),
                                                        deadline=pad(pe.deadline, 12),
                                                        weight=pad(pe.weight, 8),
                                                        status=pad(pe.status, 12),
                                                        delivery_time=pad(pe.time_of_delivery, 16),
                                                        instructions=pe.special_instruction)
