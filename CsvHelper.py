from HashMap import HashMap
from PackageEntity import PackageEntity
import csv


#######
# O(1) - constant
# returns the address portion of a csv cell containing location information or HUB if the location is the HUB
def get_address_from_cell(cell):
    cell = str(cell)
    if "Western Governors University" in cell:
        return "HUB"
    else:
        return cell[cell.index('\n'):].strip()


#######
# O(N^2) - quadratic
# takes csv location distance data and creates a 2d hash map (matrix) for quick distance searching
def distance_table_to_hash_map(csv_to_map):
    read_csv = csv.reader(csv_to_map, delimiter=',')
    location_destinations = HashMap()
    locations = None

    # create an entry for each location
    for row in read_csv:
        if row[0] == 'DISTANCE BETWEEN HUBS IN MILES':
            locations = row
            continue

        location_address = get_address_from_cell(row[0])
        distance_list = HashMap()

        # create a list of all other destinations and their distance from this location
        for cell_index in range(2, len(row)):
            other_location_address = get_address_from_cell(locations[cell_index])
            distance = row[cell_index].replace('\n', " ")
            distance_list.add(other_location_address, distance)

        location_destinations.add(location_address, distance_list)
    return location_destinations


#######
# O(N) - linear
# takes packages csv data and create a hash map of packageEntities to store in memory
def package_table_to_hash_map(csv_to_map):
    read_csv = csv.reader(csv_to_map, delimiter=',')
    packages = HashMap()
    for row in read_csv:
        pe = PackageEntity.of(row)
        packages.add(pe.id, pe)
    return packages
