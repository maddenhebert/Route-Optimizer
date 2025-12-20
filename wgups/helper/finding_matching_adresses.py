# This algorithm is not part of the main program but was used to find matching addresses for packages
import csv
import objects.package as p

# list to hold all package objects 
packages = []

with open("wgups/csv/packages.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        package = p.package(
            package_id = int(row[0]),
            address = row[1],
            city = row[2],
            state = row[3],
            zip_code = row[4],
            deadline = row[5],
            weight = int(row[6]),
            special_notes = row[7]
        )

        packages.append(package)

# group package IDs by address in dictionary 
address_matches = {}

# loop through packages to populate dictionary 
for package in packages:
    # if address isnt in dict yet, creates empyt list
    if package.address not in address_matches:
        address_matches[package.address] = []
    address_matches[package.address].append(package.package_id)

# print results, using items to split address and package ids 
for address, id in address_matches.items():
    print(address, id)
