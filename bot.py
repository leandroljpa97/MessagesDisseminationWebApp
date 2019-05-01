import requests, json
from pprint import pprint

print("Bot ID:")
bot_id = input("> ")
print("Password:")
password = input("> ")
print("Message:")
message = input("> ")
print("Number:")
number = input("> ")
print("Periodicity:")
periodicity = input("> ")

payload = {"bot_id" : bot_id, "password" : password, "message" : message, "number" : number, "periodicity" : periodicity}

r = requests.post("https://asint-227820.appspot.com/bots/", data = payload)

print('Status: ' + str(r.status_code) + '\n')

if r.status_code == 401:
	print('Error: Invalid Login\n')

elif r.status_code != 200:
	print(r.text + '\n')

print(r.text + '\n')