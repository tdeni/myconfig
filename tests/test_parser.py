import json
import os
from atexit import register

import toml
import yaml
from myconfig.main import env_parse, parser


def test_json_parser():
    data = {'var1': 'val1', 'var2': 'val2'}
    path = 'tests/data.json'
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    assert parser([path]) == data


def test_toml_parser():
    data = {'var1': 'val1', 'var2': 'val2'}
    path = 'tests/data.toml'
    with open(path, 'w', encoding='utf-8') as f:
        toml.dump(data, f)
    assert parser([path]) == data


def test_yaml_parser():
    data = {'var1': 'val1', 'var2': 'val2'}
    path = 'tests/data.yaml'
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f)
    assert parser([path]) == data


def test_env_parser():
    data = {
        'string': 'val',
        'integer': 123,
        'bool1': True,
        'bool2': False}
    path = 'tests/env'
    with open(path, 'w', encoding='utf-8') as f:
        f.write("string='val'\ninteger=123\nbool1=True\nbool2=False")
    assert env_parse('tests/env') == data


def delete_data():
    path = [
        'tests/data.json',
        'tests/data.toml',
        'tests/data.yaml',
        'tests/env']
    for file in path:
        os.remove(file)


register(delete_data)
