from TimeHelper import Clock


class Truck:
    mph = 18
    miles_per_minute = float(mph / 60)
    package_capacity = 16

    #######
    # O(1) - constant
    # construct a 'truck' object with a specified id
    def __init__(self, truck_id):
        self.id = truck_id
        self.packages = list()
        self.location = 'HUB'
        self.miles_traveled = 0
        self.clock = Clock('8:00', 'AM')
        self.stop_clock = None
        self.clock_is_stopped = False

    #######
    # O(1) - constant
    # adds package to the truck's package list if the capacity has not been reached
    def load_package(self, package):
        if len(self.packages) < self.package_capacity:
            self.packages.append(package)
            return True
        return False

    #######
    # O(1) - constant
    # updates package to delivered and calculates the distance/time spent delivering it
    def deliver_package(self, package, distance_table):
        delivery_distance = distance_table.get_distance(self.location, package.address)

        # get time spent on delivery
        minutes_spent = float(delivery_distance) / self.miles_per_minute

        if self.stop_clock is not None:
            check_clock = Clock(self.clock.time_string()[0:self.clock.time_string().index(' ')], self.clock.period)
            check_clock.add_minutes(minutes_spent)
            if check_clock.greater_than(self.stop_clock):
                self.clock_is_stopped = True

        if not self.clock_is_stopped:
            # add time spent (round up to nearest minute)
            self.clock.add_minutes(minutes_spent)
            # assign delivery time
            package.time_of_delivery = self.clock.time_string()

            self.miles_traveled += float(delivery_distance)
            self.location = package.address
            package.status = 'Delivered'

    #######
    # O(N) - linear
    # checks if all packages are delivered
    def is_route_finished(self):
        for package in self.packages:
            if package.status.upper() != 'DELIVERED':
                return False
        return True

    #######
    # O(1) - constant
    # used for checking at specified times throughout the day. returns if the clock is stopped currently
    def clock_stopped(self):
        if self.stop_clock is not None:
            return self.clock_is_stopped
        return False

    #######
    # O(N) - linear
    # returns first packages with status of 'en route'
    def get_first_undelivered_package(self):
        for package in self.packages:
            if package.status.upper() == 'EN ROUTE' or package.status.upper() == 'AT THE HUB':
                return package

    #######
    # O(1) - constant
    # calculates miles and time for truck to drive back to the hub
    def drive_back_to_hub(self, distance_table):
        if not self.clock_stopped():
            distance_back_to_hub = distance_table.get_distance(self.location, 'HUB')
            self.location = 'HUB'
            self.miles_traveled += float(distance_back_to_hub)
            minutes_spent = float(distance_back_to_hub) / self.miles_per_minute
            self.clock.add_minutes(minutes_spent)

    #######
    # O(N) - linear
    # finds first package with a deadline approaching if one exists
    def approaching_deadline(self):
        for package in self.packages:
            if package.deadline == 'EOD' or package.status.upper() == 'DELIVERED':
                continue
            if self.clock.is_approaching_deadline(package.deadline):
                return package
        return None

    #######
    # O(N) - linear
    # Used for finding additional packages for the same address if one exists
    def package_for_current_address(self):
        for package in self.packages:
            if package.status.upper() == 'DELIVERED':
                continue
            if package.address == self.location:
                return package
        return None

    #######
    # O(N) - linear
    # start clock for truck and set packages en route if applicable
    def start_clock(self, start_clock):
        self.clock = start_clock
        if self.stop_clock is None or self.stop_clock.greater_than(self.clock):
            for package in self.packages:
                package.status = 'En route'
