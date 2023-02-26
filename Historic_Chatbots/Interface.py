#!/usr/bin/env python

"""\
This class contains the main functionality of the historic chatbots project.
- setting up the bots
- setting up the gradio UI
- whisper speech-to-text model

"""

import whisper
import gradio as gr
from Chatbot import Chatbot

# chat_history is the array that stores all messages and replies
# chatbots is a dictionary that stores all chatbots
# current_bot_name is the name of the current bot, can be used as a key for chatbots

chat_history = []
chatbots = {}
current_bot_name  = "Eliza"

# ELiza     : Rive, https://github.com/aichaos/rivescript-
# Alice     : AIML, https://github.com/paulovn/python-aiml
# Standard  : AIML, https://github.com/paulovn/python-aiml
# Professor : AIML, https://code.google.com/archive/p/professor-chatbot-aiml-code/

bot_eliza     = Chatbot("Rive", "./Chatbots/Eliza")
bot_alice     = Chatbot("AIML", "./Chatbots/Alice")
bot_standard  = Chatbot("AIML", "./Chatbots/Standard")
bot_professor = Chatbot("AIML", "./Chatbots/Professor")

chatbots["Eliza"]     = bot_eliza
chatbots["Alice"]     = bot_alice
chatbots["Standard"]  = bot_standard
chatbots["Professor"] = bot_professor

# setup whisper speech-to-text model
# see here: https://github.com/openai/whisper
whisper_model = whisper.load_model("base")

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
        print("Audio recording saved at: " + audio_path)

        # transcribe using whisper
        transcript_full = whisper_model.transcribe(audio_path)
        transcript_text = transcript_full['text']

        print("Transcript: " + transcript_text)

        # get the bots reply for the transcript
        reply = bot_reply(transcript_text)

    # update the chat history and clear audio input
    return [chat_history, None]


# build UI
with gr.Blocks(
    title="Historic Chatbots") as demo:
    
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

            with gr.Row(
                variant='compact'):
                
                with gr.Column(scale=4):
                    # input field for text messages
                    input_field = gr.Textbox(
                        show_label=False,
                        placeholder="Type a message here...",
                    )

                with gr.Column(scale=1):
                    # audio input via microphone
                    input_audio = gr.Audio(
                        source="microphone",
                        interactive=True,
                        show_label=False,
                        type="filepath",
                        elem_id="input_audio"
                    )
                
            # process audio
            input_audio.change(
                fn=process_audio,
                inputs=input_audio,
                outputs=[chat_window, input_audio]
            )
            
            # submit button
            button_send = gr.Button(value="Send",variant="primary")

            # submit value via click on button_send
            button_send.click(
                fn=bot_reply,
                inputs=input_field,
                outputs=[chat_window, input_field],
            )
            
            # submit value via enter in input_field
            input_field.submit(
                fn=bot_reply,
                inputs=input_field,
                outputs=[chat_window, input_field],            
            )

if __name__ == "__main__":
    # launch demo
    demo.launch(
        inline=False,
        inbrowser=True,
        favicon_path="sems-logo.png" # tab icon in browser
        )
