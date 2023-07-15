import requests

def dive(url):
    found = requests.get(url)
    return str(found.url)

def hasKeyword(string, keyword):
    return keyword.lower() in string.lower()