import requests, json
from pprint import pprint

def login():
	while True:
		print("Username:")
		username = input("> ")
		print("Password:")
		password = input("> ")

		payload = {"username" : username, "password" : password}
		r = requests.post("https://asint-227820.appspot.com/admin/login/", data = payload)

		print('Status: ' + str(r.status_code) + '\n')

		if r.status_code == 401:
			print('Error: Invalid Login\n')
			main()
			return
		elif r.status_code != 200:
			print('Error Accessing\n')
			return
		else:
			print('Login Successful\n')
			break

		print(r.text + '\n')

	secret = r.json()
	print('Secret: ' + str(secret['secret']) + '\n')

	return secret

def defineBuildings(secret):
	#pprint(secret)

	json_data = open('buildings-alameda.json')
	buildings_dict = json.load(json_data) #deserialises data
	buildings_dict = buildings_dict['containedSpaces']

	for aux in buildings_dict:
		payload = {"secret" : secret['secret'], "id" : aux['id'], "name": aux['name'], "lat" : aux['lat'], "longit" : aux['longit']}
		pprint(payload)
		r = requests.post("https://asint-227820.appspot.com/admin/buildings/", data=payload)

		print('Status: ' + str(r.status_code) + '\n')
		print('Message: ' + r.text + '\n')

		if r.status_code == 401:
			print('Error: Invalid Login\n')
			main()
			return
		elif r.status_code != 200:
			print('Error Accessing\n')
			return

def allUsers(secret):
	i = 0
	#pprint(secret)

	r = requests.post("https://asint-227820.appspot.com/admin/users/", data = secret)

	print('Status: ' + str(r.status_code) + '\n')

	if r.status_code == 401:
		print('Error: Invalid Login\n')
		main()
		return
	elif r.status_code != 200:
		print('Error Accessing\n')
		return

	data = r.json()

	for aux in data:
		print("USER " + str(i))
		print('IST ID: ' + aux['pk'])
		print('Name: ' + aux['fields']['name'])
		print('Building ID: ' + aux['fields']['build_id'] + '\n')
		i = i + 1

def buildingUsers(secret):
	i = 0
	#pprint(secret)

	print("Building ID:")
	build_id = input("> ")

	payload = {"secret" : secret['secret'], "build_id" : build_id}

	r = requests.post("https://asint-227820.appspot.com/admin/building/users/", data = payload)

	print('Status: ' + str(r.status_code) + '\n')

	if r.status_code == 401:
		print('Error: Invalid Login\n')
		main()
		return
	elif r.status_code != 200:
		print('Error Accessing\n')
		return

	data = r.json()

	for aux in data:
		print("USER " + str(i))
		print('IST ID: ' + aux['pk'])
		print('Name: ' + aux['fields']['name'])
		print('Building ID: ' + aux['fields']['build_id'] + '\n')
		i = i + 1

def registerBot(secret):
	#pprint(secret)

	print("Building ID:")
	build_id = input("> ")

	payload = {"secret" : secret['secret'], "build_id" : build_id}

	r = requests.post("https://asint-227820.appspot.com/admin/bots/", data = payload)

	print('Status: ' + str(r.status_code) + '\n')

	if r.status_code == 401:
		print('Error: Invalid Login\n')
		main()
		return
	elif r.status_code != 200:
		print(r.text + '\n')
		return

	data = r.json()

	print('Bot ID: ' + str(data['bot_id']))
	print('Building ID: ' + str(data['build_id']))
	print('Password: ' + str(data['password']) + '\n')

def sendMessagesBot(secret):
	#pprint(secret)

	print("Building ID:")
	build_id = input("> ")
	print("Message:")
	message = input("> ")
	print("Number:")
	number = input("> ")
	print("Periodicity:")
	periodicity = input("> ")

	payload = {"secret" : secret['secret'], "build_id" : build_id, "message" : message, "number" : number, "periodicity" : periodicity}

	r = requests.post("https://asint-227820.appspot.com/admin/bots/messages/", data = payload)

	print('Status: ' + str(r.status_code) + '\n')

	if r.status_code == 401:
		print('Error: Invalid Login\n')
		main()
		return
	elif r.status_code != 200:
		print(r.text + '\n')
		return

	print(r.text + '\n')

def logMovementsUser(secret):
	i = 0
	#pprint(secret)

	print("IST ID:")
	ist_id = input("> ")

	payload = {"secret" : secret['secret'], "ist_id" : ist_id}

	r = requests.post("https://asint-227820.appspot.com/admin/logs/movements/user", data = payload)

	print('Status: ' + str(r.status_code) + '\n')

	if r.status_code == 401:
		print('Error: Invalid Login\n')
		main()
		return
	elif r.status_code != 200:
		print(r.text + '\n')
		return

	data = r.json()

	#pprint(data)

	for aux in data:
		print("MOVEMENT " + str(i))
		print('IST ID: ' + aux['fields']['ist_id'])
		print('Building ID: ' + aux['fields']['build_id'])
		print('Exit Date: ' + str(aux['fields']['end']) + '\n')
		i = i + 1

def logMovementsBuilding(secret):
	i = 0
	#pprint(secret)

	print("Building ID:")
	build_id = input("> ")

	payload = {"secret" : secret['secret'], "build_id" : build_id}

	r = requests.post("https://asint-227820.appspot.com/admin/logs/movements/building", data = payload)

	print('Status: ' + str(r.status_code) + '\n')

	if r.status_code == 401:
		print('Error: Invalid Login\n')
		main()
		return
	elif r.status_code != 200:
		print(r.text + '\n')
		return

	data = r.json()

	#pprint(data)

	for aux in data:
		print("MOVEMENT " + str(i))
		print('IST ID: ' + aux['fields']['ist_id'])
		print('Building ID: ' + aux['fields']['build_id'])
		print('Entry Date: ' + aux['fields']['start'])
		print('Exit Date: ' + str(aux['fields']['end']) + '\n')
		i = i + 1

def logMovements(secret):
	while True:
		print("Filter:")
		print("(1) - User")
		print("(2) - Building")
		
		command = input('>> ')

		if command == '1':
			logMovementsUser(secret)
			return

		elif command == '2':
			logMovementsBuilding(secret)
			return

		else:
			print('Insert a valid command!\n')

def logMessagesUser(secret):
	i = 0
	#pprint(secret)

	print("IST ID:")
	ist_id = input("> ")

	payload = {"secret" : secret['secret'], "ist_id" : ist_id}

	r = requests.post("https://asint-227820.appspot.com/admin/logs/messages/user", data = payload)

	print('Status: ' + str(r.status_code) + '\n')

	if r.status_code == 401:
		print('Error: Invalid Login\n')
		main()
		return
	elif r.status_code != 200:
		print(r.text + '\n')
		return

	data = r.json()

	#pprint(data)

	for aux in data:
		print("MESSAGE " + str(i))
		print('Content: ' + aux['fields']['content'])
		print('sender ID: '+ aux['fields']['sender'])
		print('receiver ID: '+ aux['fields']['receiver'])
		print('Building ID: ' + aux['fields']['build_id'])
		print('Date: ' + aux['fields']['date'] + '\n')
		i = i + 1

def logMessagesBuilding(secret):
	i = 0
	#pprint(secret)

	print("Building ID:")
	build_id = input("> ")

	payload = {"secret" : secret['secret'], "build_id" : build_id}

	r = requests.post("https://asint-227820.appspot.com/admin/logs/messages/building", data = payload)

	print('Status: ' + str(r.status_code) + '\n')

	if r.status_code == 401:
		print('Error: Invalid Login\n')
		main()
		return
	elif r.status_code != 200:
		print(r.text + '\n')
		return

	data = r.json()

	#pprint(data)

	for aux in data:
		print("MESSAGE " + str(i))
		print('Content: ' + aux['fields']['content'])
		print('sender ID: '+ aux['fields']['sender'])
		print('receiver ID: '+ aux['fields']['receiver'])
		print('Building ID: ' + aux['fields']['build_id'])
		print('Date: ' + aux['fields']['date'] + '\n')
		i = i + 1

def logMessages(secret):
	while True:
		print("Filter:")
		print("(1) - User")
		print("(2) - Building")
		
		command = input('>> ')

		if command == '1':
			logMessagesUser(secret)
			return

		elif command == '2':
			logMessagesBuilding(secret)
			return

		else:
			print('Insert a valid command!\n')

def logout(secret):

	#pprint(secret)
	r = requests.post("https://asint-227820.appspot.com/admin/logout/", data = secret)

	print('Status: ' + str(r.status_code) + '\n')
	print('Message: ' + r.text + '\n')

	if r.status_code != 200:
		main()
		return

def clearBD(secret):
	r = requests.post("https://asint-227820.appspot.com/admin/clear/", data = secret)

def main():
	print("\n---------- ADMINISTRATOR PAGE ----------\n")

	secret = login()

	while True:
		print("Action:")
		print("(1) - Define builds and their locations (latitude, longitude)")
		print("(2) - List all users that are logged-in into the system")
		print("(3) - List all users that are inside a certain buiding")
		print("(4) - List the history of all the user movements")
		print("(5) - List the history of all the exchanged messages")
		print("(6) - Register a new bot")
		print("(7) - Run a bot")
		print("(8) - Erase Data Base")
		print("(10) - Logout")

		command = input('>> ')

		if command == '1':
			defineBuildings(secret)

		elif command == '2':
			allUsers(secret)

		elif command == '3':
			buildingUsers(secret)

		elif command == '4':
			logMovements(secret)

		elif command == '5':
			logMessages(secret)

		elif command == '6':
			registerBot(secret)

		elif command == '7':
			sendMessagesBot(secret)

		elif command == '8':
			clearBD(secret)

		elif command == '10':
			logout(secret)

		else:
			print('Insert a valid command!\n')
	
if __name__ == "__main__":
    main()