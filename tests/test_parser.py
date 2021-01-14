from pathlib import Path

from myconfig import MyConfig

env = ".env"

with open(env, "w", encoding="utf-8") as file:
    file.write(
        """str = string
int = 111
bool = True
list = [True, admin, 111]"""
    )


def test_env_parser():
    config = MyConfig()
    Path(env).unlink()
    assert config.str == "string"
    assert config.int == 111
    assert config.bool is True
    assert config.list == [True, "admin", 111]
