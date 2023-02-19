#!/usr/bin/env python

"""\
This is a class for a RiveScript chatbot.
Accepts the optional parameter filepath, if given will load all files in the directory.

Files can be loaded/learned with the load() function.
The bot can be asked for a response with the respond() function.
"""

import rivescript as rv
import os

class Chatbot_Rive():

    # constructor with filepath to chatbot files
    def __init__(self, filepath):
        self.filepath = filepath
        self.bot = rv.RiveScript()

        # load the chatbots files
        if filepath is not None:
            self.load(filepath)

    # loads the files of a custom path
    def load(self, path):
        # get list of files in filepath directory
        files = os.listdir(path)
        
        # learn all files in filepath
        for file in files:
            self.bot.load_file(path + "/" + file)

        # we have loaded the files, the last step is to sort replies
        self.bot.sort_replies()

    # get a response from the bot
    def respond(self, message) -> str:
        return self.bot.reply("Bob", message)