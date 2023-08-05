from urllib.parse import urlparse
from codegenhelper import debug, log
import requests
import urllib
import demjson
from getpass import getpass
def get_input(name):
    result = input("please input {}:".format(name))
    if not result:
        raise Exception("no {} is supplied".format(name))
    return result

def get_login_url(host_url):
    return (lambda result:"{scheme}://{netloc}/auth/login".format(scheme = debug(result, "result").scheme, netloc = result.netloc))(urlparse(host_url))

def getToken(login_url, name, pwd):
    return (lambda result:\
            result.content.decode(result.encoding))\
            (requests.post(login_url, json={"name": name, "pwd": pwd}))

def get_json(host_url, name, token):
    return log(__name__)("get_json").debug(requests.get(host_url, headers={"name": name, "token": token}).text) if host_url and len(host_url) > 0 else None

def build_download_url(host_url, user_name, project_name):
    return host_url + "/_api/interfacedef_get_service/query/{project}/interface_entries".format(project="$$".join([user_name, project_name]))
def getJson(host_url, project_name, userName=None, password=None):
    return demjson.decode(\
                          (lambda name, pwd:\
            get_json(build_download_url(host_url, name, project_name), name, getToken(get_login_url(host_url), name, pwd))) \
            (userName or get_input("username"), password or getpass("please input password:")) \
    ) if host_url and len(host_url) > 0 else None
