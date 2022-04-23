import requests
import os
import time


headers = {
    'Content-Type': 'application/json',
}
for filename in os.listdir('json_test_send'):
    with open (os.path.join('json_test_send', filename), 'r') as f:
        data = f.read()

        response = requests.post('http://127.0.0.1:5000/detected_protocol', headers=headers, data=data)
        print(response.text)
        # time.sleep(3)