import json
import os

def get_level_list ():
	file = open("levels/levels.json", "r")
	data = file.read()
	data = json.loads(data)
	file.close()
	return data

def load_level (level):
	file = open("levels/" + level, "r")
	data = file.read()
	file.close()
	data = json.loads(data)
	return data

def verify_stations (level_json):
	stations = level_json["stations"]
	lines = level_json["lines"]
	for station in stations:
		station_lines = stations[station]
		for station_line in station_lines:
			if station_line in lines:
				flag = True
				services = lines[station_line]
				for service in services:
					if station in services[service]:
						flag = False
				if flag:
					print("   ERROR : station '" + station + "' not found in any services for '" + station_line + "'")
			else:
				print("   ERROR : line '" + station_line + "' does not exist")
	
def verify_services (level_json):
	stations = level_json["stations"]
	lines = level_json["lines"]
	for line in lines:
		services = lines[line]
		for service in services:
			service_stations = services[service]
			for station in service_stations:
				if station not in stations:
					print("   ERROR : station '" + station + "' on '" + line + "' service '" + service + "' does not exist")
				if station in stations:
					if line not in stations[station]:
						print("   ERROR : line '" + line + "' not listed as serving '" + station + "' but appears in services")

levels = get_level_list()
for level in levels:
	print()
	print(level)
	level_content = load_level(levels[level])
	verify_stations(level_content)
	verify_services(level_content)
print()
