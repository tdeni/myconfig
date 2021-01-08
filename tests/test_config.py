import json
import os

from myconfig import MyConfig


def test_config():
    data = {"var1": "val1", "var2": "val2"}
    path = "tests/data.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)

    config = MyConfig([path])
    assert config.var1 == data.get("var1")
    assert config.var2 == data.get("var2")
    os.remove(path)
