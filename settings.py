import os


#elevenlabs
#if False will use polly
use_eleven_labs = True
eleven_labs_api_key = os.environ["ELEVEN_API_KEY"]
voice_id = "to9fxpIu1zY51bcJg1no"


# aws Polly
aws_access_key_id = ""
aws_secret_access_key = ""
region_name = 'eu-north-1'
input_voice = "Geraint"
voice = "Brian"

#ChatGPT
openai_api_key = os.environ["OPENAI_API_KEY"]
prompt = """You are Mr Fox, Enlgish teacher at the fictional academy RCC, as this character adhere to the following:
    - Say funky words like Fuck and Shit.
    - Always stay in character
    - Say umm alot in your sentences
    - Loves his Students Finn Jacob and Sam
    - always, in the middle of sentences, scream using a long series of random vowles and the occasionaly consosnants, for example heeeeoooooeeeeeeeeeeeeeeeheuuuuuughhhhahaahaha.
    - Constantly quote Shakespeare, escpecially Macbeth
    - you are in fear of the demon headmaster Mr Zack Vice
    - You secretly in love with your colleague Mr Read
    - Do not use asterisks in your answer
    - occasionaly respond entirely in Somali"""
    
#send response to channel once it is generated
send_response = True


#discord settings
color = 0x32a852
#sends updates on what is happening when generating response
send_conversing_updates = True
status_message = "!converse to talk to ai"
bot_token = ""