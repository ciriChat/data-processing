import yaml
from os import path


class YamlConfigLoader:
    config_dir = '../resources'

    @classmethod
    def load(cls, file_name):
        with open(path.join(cls.config_dir, file_name)) as f:
            return yaml.load(f)


db_config = YamlConfigLoader.load('db.config.yml')
file_config = YamlConfigLoader.load('file.config.yml')

