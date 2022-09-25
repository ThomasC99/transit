import json
import random
import os

file = open("save.json", "r")
save_data = file.read()
file.close()
save_data = json.loads(save_data)

def save ():
    file = open("save.json", "w")
    file.write(json.dumps(save_data, indent=4))
    file.close()

os.system("ls levels > level-list.txt")
file = open("level-list.txt")
level_list = file.read()
file.close()
os.system("rm level-list.txt")
level_list = level_list.replace(".json", "")
level_list = level_list.split("\n")
level_list.remove("")

level = None
for i in range (0, len(level_list)):
    print(str(i + 1) + ". " + level_list[i], end="")
    if (level_list[i] not in save_data["levels"]):
        print(" (Locked)", end="")
    print()
choice = 0
while choice < 1 or choice > len(level_list):
    choice = int(input(""))
    print("\n\n")
    if level_list[choice - 1] not in save_data["levels"]:
        file = open("levels/" + level_list[choice - 1] + ".json", "r")
        cost = len(json.loads(file.read())["stations"])
        print("Unlock " + level_list[choice - 1] + " for " + str(cost) + "? you have " + str(save_data["funds"]))
        answer = input("y / n : ")
        if answer == "y" and save_data["funds"] >= cost:
            save_data["funds"] -= cost
            save_data["levels"].append(level_list[choice - 1])
            print("You now have " + str(save_data["funds"]) + " funds")
            print("\n\n")
            save()
            level = level_list[choice - 1]
    else:
        level = level_list[choice - 1]

file = open("levels/" + level + ".json", "r")
data = file.read()
file.close()

data = json.loads(data)
stations = data["stations"]
lines = data["lines"]

map = {}

def get_random_station (station):
    station_list = list(stations.keys())
    if station in station_list:
        station_list.remove(station)
    return station_list[random.randint(0, len(station_list) - 1)]

def get_random_line (station):
    station_lines = stations[station]
    if len(station_lines) > 1:
        return station_lines[random.randint(0, len(station_lines) - 1)]
    else:
        return station_lines[0]

def get_random_service (station):
    line = get_random_line(station)
    services = lines[line]
    avail_services = {}
    for service in services:
        if services[service][-1] != station:
            avail_services[service] = services[service]
    services = list(avail_services.keys())
    if len(services) == 1:
        return {line : services[0]}
    else:
        return {line : services[random.randint(0, len(services) - 1)]}

current_station = get_random_station("")

while True:
    target_station = None
    while target_station == None or target_station == current_station:
        target_station = get_random_station(current_station)
    print("Current station : " + current_station)
    print("Taget station : " + target_station)
    service = None
    while True:
        print("\n\n")
        service = get_random_service(current_station)
        line = list(service.keys())[0]
        service = service[line]
        print("1. Take service : " + line + " (" + str(lines[line][service][len(lines[line][service]) - 1]) + ")")
        print("2. Wait")
        choice = 0
        while choice != 1 and choice != 2:
            choice = int(input(""))
        print("\n\n")
        if (choice == 1):
            route_stations = lines[line][service]
            while current_station != route_stations[-1]:
                current_station_index = route_stations.index(current_station) + 1
                current_station = route_stations[current_station_index]
                if current_station_index + 1 == route_stations[-1]:
                    print("Getting of at " + route_stations[current_station_index])
                    current_station = route_stations[current_station_index]
                else:
                    print("1. Get off at " + route_stations[current_station_index])
                    print("2. Continue on " + line + " (" + str(lines[line][service][len(lines[line][service]) - 1]) + ")")
                    choice = 0
                    while choice != 1 and choice != 2:
                        choice = int(input(""))
                        print("\n\n")
                    if choice == 1:
                        print ("Current atation : " + current_station)
                        print ("Target station : " + target_station)
                        print("\n\n")
                        break
        if current_station == target_station:
            print("Target station reached!")
            print("+ 10 funds")
            save_data["funds"] += 10
            print(str(save_data["funds"]) + " total funds")
            save()
            print("\n\n")
            break

# 40