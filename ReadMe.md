# Discord Character Bot
Discord bot that allows the user to ask GPT-4 questions and have them respond as a certain character, works with both elevenlabs and amazon Polly for text to speech.
## installation
1) Program is written using python 3.12, which can be obtained [here](https://www.python.org/downloads/release/python-3122/)
2) install the requirments with ```pip install -r requirements.txt```
3) you must set up accounts and API keys with the services: Open AI, AWS, an ElevenLabs account is needed if you want to use those voices.
4) run the program with ```python main.py```
## usage
- change simple settings in [settings.py](settings.py)
- More detailed explanations within the help messages, for example ```!help```
- use ```!tts [message]```  for text to speach
- use ```!converse [message]``` to talk to an AI