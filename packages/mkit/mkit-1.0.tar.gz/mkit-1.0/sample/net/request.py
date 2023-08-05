import requests


def request():
    result = requests.get("http://www.baidu.com")
    print(result.text)
