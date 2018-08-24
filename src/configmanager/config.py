import yaml
import os

defaults = {

}

import roam.utils


class Config:
    """
    Config object to handle setting the settings for the application.
    """
    def __init__(self, settings, location):
        self.settings = settings
        self.location = location
        self.logger = roam.utils.logger

    @classmethod
    def from_file(cls, file):
        _settings = defaults
        if os.path.exists(file):
            with open(file) as f:
                _settings = yaml.load(f)
        return Config(_settings, file)

    def get(self, key, default=None):
        self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getitem__(self, item):
        return self.get(item)

    def save(self):
        with open(self.location, 'w') as f:
            yaml.safe_dump(data=self.settings, stream=f, default_flow_style=False)
            self.logger.debug(self.settings)