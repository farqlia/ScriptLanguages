import requests

url = "https://www.wroclaw.pl/open-data/api/action/datastore_search"
resource_id = "9d5b2336-6f9a-4fa0-8cbe-d6b4776194c3"
limit = 5
response = requests.get(url, params={'resource_id': resource_id, 'limit': limit})
print(response)

print(response.status_code)
print(response.url)
print(response.json()['result']['records'][1])