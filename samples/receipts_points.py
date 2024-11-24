import requests
from samples.config import base_url, receipt_id

response = requests.get(f'{base_url}/receipts/{receipt_id}/points')

print(response.text)
print(response.status_code)
