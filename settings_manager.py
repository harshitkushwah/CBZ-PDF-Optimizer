import json
from pathlib import Path


class SettingsManager:

    DEFAULT_SETTINGS = {
        "max_width": 1200,
        "quality": 85,
        "pages_per_strip": 10
    }

    def __init__(self, filename="settings.json"):

        self.file = Path(filename)

        if not self.file.exists():
            self.save(self.DEFAULT_SETTINGS)

    # -----------------------------------------

    def load(self):

        try:
            with open(self.file, "r") as f:
                data = json.load(f)

            for key, value in self.DEFAULT_SETTINGS.items():
                data.setdefault(key, value)

            return data

        except Exception:
            return self.DEFAULT_SETTINGS.copy()

    # -----------------------------------------

    def save(self, settings):

        with open(self.file, "w") as f:
            json.dump(
                settings,
                f,
                indent=4
            )