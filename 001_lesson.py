import json
from pprint import pprint
import requests
username = input("Введите имя пользователя на GitHub:")
request = requests.get('https://api.github.com/users/'+username+'/repos')
json_data = request.json()
pprint(json_data)

with open(f"{username } user_repos.json", "w") as file:
    json.dump(json_data, file)
    print('Данные записаны успешно')
