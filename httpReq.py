import requests

def send_get_request(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # بررسی کد وضعیت HTTP

        return response.text
    except requests.exceptions.RequestException as e:
        print('Error:', e)