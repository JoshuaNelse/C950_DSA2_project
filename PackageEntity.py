

#######
# Class acts as an interface for package entities / objects in memory
class PackageEntity:

    def __init__(self, package_id, delivery_address, delivery_city, delivery_state,
                 delivery_zip, delivery_deadline, package_weight, special_instruction):
        self.id = package_id
        self.address = delivery_address
        self.city = delivery_city
        self.state = delivery_state
        self.zip = delivery_zip
        self.deadline = delivery_deadline
        self.weight = package_weight
        self.special_instruction = special_instruction
        self.status = PackageStatuses.AT_THE_HUB
        self.time_of_delivery = None

    #######
    # O(1) - constant
    # converts a csv cell into package entity object
    @classmethod
    def of(cls, package_data):
        pd = package_data
        return PackageEntity(pd[0], pd[1], pd[2], pd[3], pd[4], pd[5], pd[6], pd[7])

    #######
    # O(1) - constant
    # to_string formatter for printing package entity object types
    def __str__(self):
        return 'PackageEntity(id: {}, address: {}, city: {}, state: {}, zip: {}, deadline: {}, weight: {}, ' \
               'status: {}, delivery_time: {} special instructions: {})' \
            .format(self.id, self.address, self.city, self.state, self.zip, self.deadline, self.weight, self.status,
                    self.time_of_delivery, self.special_instruction)


#######
# enum to store valid statuses for packages
class PackageStatuses:
    AT_THE_HUB = 'At the hub'
    EN_ROUTE = 'En route'
    DELIVERED = 'Delivered'
