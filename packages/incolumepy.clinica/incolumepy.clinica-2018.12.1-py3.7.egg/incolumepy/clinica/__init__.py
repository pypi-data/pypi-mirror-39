#!/usr/bin/env python
# --*-- encoding: utf-8 --*--

import datetime
import gspread
from os.path import exists, abspath, join, dirname
from oauth2client.service_account import ServiceAccountCredentials

# See http://peak.telecommunity.com/DevCenter/setuptools
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)


def version():
    return datetime.datetime.now().strftime('%Y.%-m.%-d')


def package():
    return "package: {}, Version: {}".format(__package__, __version__)


def singleton(cls):
    ''' Decorator for classes '''
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
def get_client_google():
    __escopo = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    __file_credenciais = abspath(join(dirname(__file__), 'credenciais', 'incolumepy-clinica-95c7132c5028.json'))

    assert exists(__file_credenciais), "Arquivo {} indisponível!".format(__file_credenciais)
    __credenciais = ServiceAccountCredentials.from_json_keyfile_name(__file_credenciais, __escopo)

    client_google = gspread.authorize(__credenciais)
    return client_google


__package__ = 'incolumepy.clinica'
__version__ = version()

# sheet = get_client_google().open('incolumepy.clinica').sheet1


if __name__ == '__main__':
    print(package())
