# Historic Chatbots Communication Project

This software project allows users to communicate with historic chatbots. These chatbots were some of the earliest examples of natural language processing and were designed to simulate conversation with a human user.

This project is implemented in Python programming language and utilizes the RiveScript and AIML packages as well as Gradio frontend. The chatbots included in this project are:

    ELIZA:     a chatbot created in the 1960s that simulates a Rogerian psychotherapist
    ALICE:     a chatbot created in the late 1990s that simulates a conversational agent
    Standard:  a chatbot that assists the user in their day to day life
    Professor: a chatbot trained on many scientific topics. Only accepts specified input (no fuzziness).

## Usage

To run the project, navigate to the main project directory and run the following command:

```python Interface.py```

This command launches the gradio interface in the command-line. After some loading it should
open a website containing the gradio interface.

## Voice Input

The project also allows speech input via microphone by accessing Googles speech-to-text API. If this doesnt work, there might be a problem with the key .json file. Check if the **GOOGLE\_APPLICATION\_CREDENTIALS** environment variable contains the path to the key .json file. For more information see here: https://codelabs.developers.google.com/codelabs/cloud-speech-text-python3/ 

## Adding new Bots

This project supports RiveScript and AIML bots, and as such only .rive or .aiml files. Follow these steps if you want to add a new bot:

1. Place your bots files in a new folder under **./Chatbots/Your\_Bot\_Name**
2. In **Interface.py** implement a new **reset\_bot\_yourbotname()** function similar to the others. In Chatbot(), specify the bots type ("Rive" or "AIML") and the relative file path to your folder from step 1.
3. Call the reset function with the others (-> under "start all bots")
4. In the gradio interface, add your bots name to the choices in **radio\_bot\_choice**

## License

This project is licensed under the MIT License.