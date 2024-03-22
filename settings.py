import os


#elevenlabs
#if False will use polly
use_eleven_labs = True
eleven_labs_api_key = os.environ["ELEVEN_API_KEY"]
voice_id = "21m00Tcm4TlvDq8ikWAM"


# aws Polly
aws_access_key_id = ""
aws_secret_access_key = ""
region_name = 'eu-north-1'
input_voice = "Geraint"
voice = "Brian"

#ChatGPT
openai_api_key = os.environ["OPENAI_API_KEY"]
prompt = ""
    
#send response to channel once it is generated
send_response = True


#discord settings
color = 0x32a852
#sends updates on what is happening when generating response
send_conversing_updates = True
status_message = "!converse to talk to ai"
bot_token = ""