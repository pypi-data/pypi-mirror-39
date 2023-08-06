import os
from pathlib import Path
from apigateway.default import *


def gen_file(file_name: str):
    return Path(Path.cwd(), f"{file_name}.py")


def fill_default_content():
    with open(gen_file('settings'), mode='w', encoding='utf8') as f:
        f.write(f"{settings}")
    with open(gen_file('main'), mode='w', encoding='utf8') as f:
        f.write(f"{main}")
    with open(gen_file('urls'), mode='w', encoding='utf8') as f:
        f.write(f"{urlpatterns}")
    with open(gen_file('views'), mode='w', encoding='utf8') as f:
        f.write('')


def set_root_dir():
    """for prepare load settings"""
    os.environ['root'] = os.path.join(os.getcwd(), 'settings.py')


def load_settings():
    """load settings"""
    with open(os.environ.get('root'), encoding='utf8') as f:
        codes = f.read()[11:]
    res = eval(codes)
    return res


def startup():
    """create default file and fill it."""
    fill_default_content()
    set_root_dir()
