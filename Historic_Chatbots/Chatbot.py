#!/usr/bin/env python

"""\
This class allows to create a chatbot with a given type and optional filepath.
- type can be "Rive" or "AIML"
- filepath is the path to the chatbot's files. all files in the directory will be loaded.

Chatbot.py is the parent class for Chatbot_AIML.py and Chatbot_Rive.py.
"""

import rivescript as rv
import aiml

from Chatbot_AIML import Chatbot_AIML
from Chatbot_Rive import Chatbot_Rive

class Chatbot:

    def __init__(self, type, filepath=None):
        self.type = type
        self.filepath = filepath
        self.bot = None

        if type == "Rive":
            self.bot = Chatbot_Rive(filepath)
        elif type == "AIML":
            self.bot = Chatbot_AIML(filepath)
        else:
            print("Error: Chatbot type", type, "not supported!")
            print("Supported types are: Rive, AIML")
            return

    # make the bot learn additional files
    def load(self, path):
        self.bot.load(path)

    # get a response from the bot
    def respond(self, message) -> str:
        return self.bot.respond(message)
    