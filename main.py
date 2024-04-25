import requests


def getData():
    res = requests.get('http://127.0.0.1:5000/meteorite/get_data')
    if res.status_code == 200:
        return res.json()
    else:
        print('Error')
        return None


print(getData())
