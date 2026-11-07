from datetime import datetime


class Logger:

    def __init__(self, callback=None):
        self.callback = callback

    def set_callback(self, callback):
        self.callback = callback

    def log(self, message):

        timestamp = datetime.now().strftime("%H:%M:%S")

        text = f"[{timestamp}] {message}"

        print(text)

        if self.callback:
            self.callback(text)