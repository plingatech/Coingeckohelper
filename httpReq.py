import requests
import time

def send_get_request(url):
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()  # بررسی کد وضعیت HTTP
            return response.text
        except requests.exceptions.RequestException as e:
            if '429' in str(e):
                print('Too Many Requests. Waiting for 5 seconds...')
                time.sleep(5)
            else:
                print('Error:', e)