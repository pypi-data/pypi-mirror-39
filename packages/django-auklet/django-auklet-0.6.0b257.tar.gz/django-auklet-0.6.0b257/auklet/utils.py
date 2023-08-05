import os
import sys
import uuid
import hashlib
import requests
import tempfile

from auklet.__about__ import __version__ as auklet_version

__all__ = ['open_auklet_url', 'create_file', 'clear_file', 'build_url',
           'get_mac', 'get_device_ip', 'get_agent_version',
           'post_auklet_url', 'create_dir', 'get_monitor', 'b', 'u']


def open_auklet_url(url, apikey):
    try:
        res = requests.get(url, headers={"Authorization": "JWT {}".format(apikey)})
    except Exception:
        return None
    return res


def post_auklet_url(url, apikey, data):
    try:
        res = requests.post(
            url,
            json=data,
            headers={"Authorization": "JWT {}".format(apikey),
                     "Content-Type": "application/json"})
    except requests.HTTPError:
        return None
    return res.json()


def create_dir(dir_name=".auklet"):
    dirs = [os.getcwd(), os.path.expanduser("~")]
    for directory in dirs:
        full_path = "{}/{}".format(directory, dir_name)
        if os.access(directory, os.W_OK):
            if not os.path.exists(full_path):
                os.mkdir(full_path)
            return full_path
    return tempfile.gettempdir()


def create_file(filename):
    open(filename, "a").close()


def clear_file(filename):
    open(filename, "w").close()


def build_url(base_url, extension):
    return '{}{}'.format(base_url, extension)


def get_mac():
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
    return hashlib.md5(b(mac)).hexdigest()


def get_device_ip():
    try:
        res = requests.get("https://api.ipify.org")
        return u(res.content)
    except (requests.RequestException, Exception):
        # TODO log to kafka if the ip service fails for any reason
        return None


def get_agent_version():
    return auklet_version


def get_monitor():
    from django.conf import settings
    settings.AUKLET_CONFIG.get("monitor", False)


if sys.version_info < (3,):
    # Python 2 and 3 String Compatibility
    def b(x):
        return x

    def u(x):
        return x
else:
    # https://pythonhosted.org/six/#binary-and-text-data
    import codecs

    def b(x):
        # Produces a unicode string to encoded bytes
        return codecs.utf_8_encode(x)[0]

    def u(x):
        # Produces a byte string from a unicode object
        return codecs.utf_8_decode(x)[0]
