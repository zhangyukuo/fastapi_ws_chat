import pytoml as toml
import os


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        conf = toml.load(f)
    return conf


config_toml = "dev_config.toml"

real_path = os.path.dirname(os.path.realpath(__file__))
join_path = os.path.join(real_path, config_toml)

config = load_config(join_path)


if __name__ == "__main__":
    print(config)