#!/usr/bin/env python

"""\
This is a class for an AIML chatbot.
Accepts the optional parameter filepath, if given will load all files in the directory.

Files can be loaded/learned with the load() function.
The bot can be asked for a response with the respond() function.
"""

import aiml
import os

class Chatbot_AIML():

    # constructor with filepath to chatbot files
    def __init__(self, filepath=None):
        self.filepath = filepath
        self.bot = aiml.Kernel()

        # load the chatbots files
        if filepath is not None:
            self.load(filepath)

    # loads the files of a custom path
    def load(self, path):
        # get list of files in filepath directory
        files = os.listdir(path)
        
        # learn all files in filepath
        for file in files:
            self.bot.learn(path + "/" + file)

    # get a response from the bot
    def respond(self, message) -> str:
        return self.bot.respond(message)