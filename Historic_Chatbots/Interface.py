from google.cloud import speech_v1 as speech
import requests as rq
import gradio as gr
import numpy as np
import os
import io

from Chatbot import Chatbot

# chat_history is the array that stores all messages and replies
# current_bot_name is the name of the current bot
# current_bot is the current bot, can be asked to respond using respond(msg)
chat_history = []
chatbots = {}
current_bot_name  = "Eliza"

# ELiza  : RiveScript
# Source : https://github.com/aichaos/rivescript-js/blob/master/eg/brain/eliza.rive
def reset_bot_eliza():
    global bot_eliza, chatbots
    bot_eliza = Chatbot("Rive", "./Chatbots/Eliza")
    chatbots["Eliza"] = bot_eliza

# Alice  : AIML
# Source : https://github.com/paulovn/python-aiml
def reset_bot_alice():
    global bot_alice, chatbots
    bot_alice = Chatbot("AIML", "./Chatbots/Alice")
    chatbots["Alice"] = bot_alice

# Standard  : AIML
# Source    : https://github.com/paulovn/python-aiml
def reset_bot_standard():
    global bot_standard, chatbots
    bot_standard = Chatbot("AIML", "./Chatbots/Standard")
    chatbots["Standard"] = bot_standard

# Professor : AIML
# Source    : https://code.google.com/archive/p/professor-chatbot-aiml-code/
def reset_bot_professor():
    global bot_professor, chatbots
    bot_professor = Chatbot("AIML", "./Chatbots/Professor")
    chatbots["Professor"] = bot_professor


# start all bots
reset_bot_eliza()
reset_bot_alice()
reset_bot_standard()
reset_bot_professor()

# setup google speech-to-text client
# you might have to set the environment variable GOOGLE_APPLICATION_CREDENTIALS to the path of your google key
# see here: https://codelabs.developers.google.com/codelabs/cloud-speech-text-python3/
os.environ['GOOGLE_APPLICATION_CREDENTIALS']= './david_google_key.json'
client = speech.SpeechClient()

# change the current bot to a different one and clear the chat history
def set_bot(bot_name):
    # set current bot to bot_name
    global current_bot_name, chat_history
    current_bot_name = bot_name

    print("Set Bot to " + current_bot_name)

    # clear the chat history
    chat_history = []
    return chat_history

# get reply from current_bot and store message and reply in chat_history
def bot_reply(message):

    # check if the current bot exists
    if current_bot_name not in chatbots:
        response = "ERR: No Bot with name " + current_bot_name + " found"
        chat_history.append((message, response))
        return [chat_history, ""]
    
    # get a response from the current bot
    current_bot = chatbots[current_bot_name]
    response = current_bot.respond(message)

    # did we get a response?
    if response == '':
        response = "ERR: No Pattern matched"
        
    # append message to array
    chat_history.append((message, response))
    
    return [chat_history, ""]


# process the temporary audio recording
def process_audio(audio_path):

    # did we actually recieve audio?
    if audio_path != None:
        print("Audio recording saved at " + audio_path)

        with io.open(audio_path, "rb") as audio_file:

            # read the audio file
            content = audio_file.read()

            # some preprocessing and configuration
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=48000,
                language_code="en-US",
            )

            # here is where the actual magic happens
            # we send the audio to google and get the response
            response = client.recognize(config=config, audio=audio)

            transcripts = []

            for result in response.results:
                # The first alternative is the most likely one for this portion.
                print("Transcript: {}".format(result.alternatives[0].transcript))
                transcripts.append(result.alternatives[0].transcript)

            # get the bots reply for the transcript
            reply = bot_reply(transcripts[0])
            return reply
        
    # we didnt recieve audio
    # return the unedited chat_history
    return [chat_history, ""]


# build UI
with gr.Blocks(title="Historic Chatbots") as demo:

    # i am trying to insert a SEMS logo, but somehow it doesnt scale down
    # sems_logo = "https://www.inf.uni-hamburg.de/33133714/sems-logo-7373293ce1c817dfffded3b34bb7ac0078485299.png"
    # gr.Image(value=sems_logo, shape=(32, None), show_label=False)
    
    with gr.Box():
        
        with gr.Column():

            radio_bot_choice = gr.Radio(choices=["Eliza", "Alice", "Standard", "Professor"], value="Eliza", show_label=False)
            
            chat_window = gr.Chatbot(show_label=False)
            chat_window.color_map = (('lime', 'gray'))

            # radio buttons to change the current bot
            radio_bot_choice.change(
                fn=set_bot,
                inputs=radio_bot_choice,
                outputs=chat_window
            )

            input_field = gr.Textbox(show_label=False)

            input_audio = gr.Audio(
                source="microphone",
                interactive=True,
                show_label=False,
                type="filepath",
                )
            
            input_audio.change(
                fn=process_audio,
                inputs=input_audio,
                outputs=[chat_window, input_field]
            )
            
            button_send = gr.Button(value="Send",variant="primary")

            # submit value via click
            button_send.click(
                fn=bot_reply,
                inputs=input_field,
                outputs=[chat_window, input_field],
            )
            
            # submit value via enter
            input_field.submit(
                fn=bot_reply,
                inputs=input_field,
                outputs=[chat_window, input_field],            
            )

if __name__ == "__main__":
    # launch demo
    demo.launch(inline=False, inbrowser=True, favicon_path="sems-logo.png")