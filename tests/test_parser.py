from random import randint

from myconfig.myconfig import Parser


def test_env_parse_int():
    _list = [str(randint(1, 100)) for i in range(10)]
    for el in _list:
        el = Parser.env_parse(el)
        assert isinstance(el, int) is True


def test_env_parse_bool():
    _list = [str(bool(randint(0, 1))) for i in range(10)]
    for el in _list:
        el = Parser.env_parse(el)
        assert isinstance(el, bool) is True
