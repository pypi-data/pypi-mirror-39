from requests.auth import HTTPBasicAuth


def basic_auth(username="", password=""):
    return HTTPBasicAuth(username=username, password=password)

