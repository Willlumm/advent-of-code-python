import requests



url = "https://adventofcode.com/2024/day/7/input"
header = ""

headers = {"Cookie": header}

response = requests.get(url, headers=headers)
print(response.text)