import argparse
import json
from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Any, List

import toml
import yaml

formats = ["json", "yaml", "yml", "toml"]
gitignore = Path(".gitignore")
config_ignore = "\n\n# myconfig\n{}"

python_code = """from myconfig import MyConfig

config = MyConfig(['{}', '{}'])
"""

python_env_only = """from myconfig import MyConfig

config = MyConfig()
"""


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class PathDescriptor:
    def __init__(self, name):
        self.name = name

    def __set__(self, obj, value):
        value = [Path(path) for path in value]
        for path in value:
            fformat = str(path).split(".")[-1].lower()
            if fformat not in formats:
                raise Exception("Format error: {}".format(fformat))
            if not path.exists():
                raise OSError("There is no such file: {}".format(str(path.absolute())))
        obj.__dict__[self.name] = value


class MyConfig(metaclass=Singleton):
    __filenames = PathDescriptor("_MyConfig__filenames")
    ENV = Path(".env")

    def __init__(self, filenames: List[str] = None) -> None:
        if filenames:
            self.__filenames = filenames
            self.parser()
        if self.ENV.exists():
            self.env_parse()

    def __getattr__(self, key: str) -> Any:
        return self.__dict__.get(key, None)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_MyConfig__filenames":
            return super().__setattr__(name, value)
        return self.__dict__.update({name: value})

    def parser(self):
        for file in self.__filenames:
            file_data = dict()
            with open(file, encoding="utf-8") as f:
                format = str(file).split(".")[-1]
                if format == "json":
                    try:
                        file_data = json.load(f)
                    except JSONDecodeError:
                        pass
                elif format == "toml":
                    file_data = toml.load(f)
                elif format in ["yaml", "yml"]:
                    file_data = yaml.safe_load(f)
            for key in file_data.keys():
                self.__setattr__(key.replace("-", "_"), file_data[key])

    def env_parse(self):
        with open(self.ENV, encoding="utf-8") as file:
            for line in file:
                key, value = [x.strip() for x in line.strip("\n").split("=", 1)]
                if value.isdigit():
                    self.__setattr__(key, int(value))
                elif value.lower() in ["true", "false"]:
                    if value.lower() == "true":
                        self.__setattr__(key, True)
                        continue
                    self.__setattr__(key, False)
                elif value.startswith("[") and value.endswith("]"):
                    value = [x.strip() for x in value[1:-1].split(",")]
                    for i, el in enumerate(value):
                        if el.isdigit():
                            value[i] = int(el)
                        elif el.lower() in ["true", "false"]:
                            if el.lower() == "true":
                                value[i] = True
                                continue
                            value[i] = False
                        else:
                            value[i] = el
                    self.__setattr__(key, value)
                elif value == "":
                    self.__setattr__(key, None)
                else:
                    self.__setattr__(key, value)

    def init(fformat: str) -> None:
        if fformat:
            settings = "settings"
            secrets = ".secrets"

            if fformat not in formats:
                raise Exception("Unknown format.")

            for file in [settings, secrets]:
                f = open(Path("{}.{}".format(file, fformat)), "a", encoding="utf-8")
                f.close()
                print("Created: {}.{}".format(file, fformat))
            with open(Path("settings.py"), "w", encoding="utf-8") as f:
                f.write(
                    python_code.format(
                        "{}.{}".format(settings, fformat),
                        "{}.{}".format(secrets, fformat),
                    )
                )
            if gitignore.exists():
                file = gitignore.read_text(encoding="utf-8")
                file += config_ignore.format(secrets + ".*")
                with open(gitignore, "r+", encoding="utf-8") as file:
                    text = file.read() + config_ignore.format(secrets + ".*")
                    file.seek(0)
                    file.write(text)
        else:
            with open(Path("settings.py"), "w", encoding="utf-8") as file:
                file.write(python_env_only)
        print("Created: settings.py")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--init", default=None, type=str, nargs="?")
    args = parser.parse_args()
    return MyConfig.init(args.init)


if __name__ == "__main__":
    main()
