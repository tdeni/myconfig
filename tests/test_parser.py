from myconfig import parser


def test_json_parser():
    assert parser(['tests/data/data.json']) == {'var1': 1, 'var2': 2}


def test_toml_parser():
    assert parser(['tests/data/data.toml']) == {'var1': 1, 'var2': 2}


def test_yaml_parser():
    assert parser(['tests/data/data.yaml']) == {'var1': 1, 'var2': 2}
