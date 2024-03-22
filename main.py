import discord
from discord.ext import commands
import boto3
from pydub import AudioSegment
from openai import OpenAI
from pydub import AudioSegment
from elevenlabs.client import ElevenLabs, VoiceSettings
from elevenlabs.client import Voice as ElevenVoice
import elevenlabs
import settings


if settings.use_eleven_labs:
    VoiceClient = ElevenLabs(api_key=settings.eleven_labs_api_key)

    
    
    
    
polly = boto3.client(
    'polly',
    aws_access_key_id=settings.aws_access_key_id, aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.region_name
)
        
    
key = settings.openai_api_key
ChatClient = OpenAI(api_key=key)


STARTPROMPT = {"role": "system", "content": f"""{settings.prompt}"""}

messages = []



def JoinSounds(path1, path2):
    sound1 = AudioSegment.from_mp3(path1)
    sound2 = AudioSegment.from_mp3(path2)
    silence = AudioSegment.from_wav("2SecondsOfSilence.wav")
    
    #2 secs of silence at start because start of message is often muffled on discord
    start = silence.append(sound1)
    sound3 = start.append(silence)
    sound4 = sound3.append(sound2)
    sound4.export("response.mp3",format="mp3")
    






intents = discord.Intents.all()
intents.voice_states = True
client = commands.Bot(command_prefix='!', intents=intents, help_command=None)

PollyVoices = [
    "Lotte", "Maxim", "Ayanda", "Salli", "Ola", "Arthur", "Ida", "Tomoko",
    "Remi", "Geraint", "Miguel", "Elin", "Lisa", "Giorgio", "Marlene",
    "Ines", "Kajal", "Zhiyu", "Zeina", "Suvi", "Karl", "Gwyneth", "Joanna",
    "Lucia", "Cristiano", "Astrid", "Andres", "Vicki", "Mia", "Vitoria", "Bianca",
    "Chantal", "Raveena", "Daniel", "Amy", "Liam", "Ruth", "Kevin", "Brian",
    "Russell", "Aria", "Matthew", "Aditi", "Zayd", "Dora", "Enrique", "Hans",
    "Danielle", "Hiujin", "Carmen", "Sofie", "Gregory", "Ivy", "Ewa", "Maja",
    "Gabrielle", "Nicole", "Filiz", "Camila", "Jacek", "Thiago", "Justin",
    "Celine", "Kazuha", "Kendra", "Arlet", "Ricardo", "Mads", "Hannah",
    "Mathieu", "Lea", "Sergio", "Hala", "Tatyana", "Penelope", "Naja", "Olivia",
    "Ruben", "Laura", "Takumi", "Mizuki", "Carla", "Conchita", "Jan",
    "Kimberly", "Liv", "Adriano", "Lupe", "Joey", "Pedro", "Seoyeon",
    "Emma", "Niamh", "Stephen"
]


PollyEnglish = [
    "Nicole", "Russell", "Emma", "Amy",
    "Brian", "Raveena", "Aditi", "Salli",
    "Kimberly", "Kendra", "Joanna", "Ivy",
    "Mathew", "Justin", "Joey", "Geraint"
]





CurrentTTS = "tts.mp3"



@client.command()
async def stop(ctx):
    if ctx.guild.voice_client:
        await ctx.guild.voice_client.disconnect()



@client.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        
@client.command()
async def join(ctx):
    if not ctx.guild.voice_client:
        vc = await ctx.author.voice.channel.connect()

@client.command()
async def tts(ctx, *args):
    if args[0] == "help" and len(args) == 1:
        ttsEmbed = discord.Embed(title="Text to Speech", description="voice will default to Russell, to use another starts message with ![voicename] after !tts", color = settings.color)
        ttsEmbed.add_field(name="English Voices:", value="", inline=False)
        ttsEmbed.add_field(name= "Australian", value="Nicole, Russell", inline=False)
        ttsEmbed.add_field(name="British", value="Emma, Amy, Brian", inline=False)
        ttsEmbed.add_field(name="Indian", value="Raveena, Aditi", inline=False)
        ttsEmbed.add_field(name="Amercian", value="Salli, Kimberly, Joanna, Ivy, Matthew, Justin, Joey", inline=False)
        ttsEmbed.add_field(name="Welsh", value="Geraint", inline=False)
        ttsEmbed.set_footer(text="!tts all for a list of all voices of all languages")
        await ctx.send(embed=ttsEmbed)
        return
    elif args[0] == "all" and len(args) == 1:
        messageString = ""
        for voice in PollyVoices:
            messageString += voice + " "
        await ctx.send(messageString)
        await ctx.send("there are too many voices to format neatly, look through yourself")
        return
    
    if not ctx.guild.voice_client:
        vc = await ctx.author.voice.channel.connect()
    else:
        vc = ctx.guild.voice_client
    
    


    message = ' '.join(str(x) for x in args)
    
    if not ctx.guild.voice_client:
        vc = await ctx.author.voice.channel.connect()
    else:
        vc = ctx.guild.voice_client

    if not vc.is_playing():
        if message[0] == "!":
            words = message.split()
            if words:
                voicetype = words[0]
                voicetype = voicetype[1:]
                # Check if there is at least one word
                if voicetype in PollyVoices:
                    input_voice = voicetype
                    inputString = " ".join(words[1:])
                else:
                    input_voice = "Russell"
                    inputString = message
            else:
                input_voice = "Russell"
                inputString = message
        else:
            input_voice = "Russell"
            inputString = message

        # Specify the output format (e.g., 'mp3')
        if len(inputString) <= 1000:
            output_format = 'mp3'
            
            # Synthesize speech
            response = polly.synthesize_speech(
            Text=inputString,
            OutputFormat=output_format,
            VoiceId=input_voice
        )

            # Save the synthesized speech to a file
            with open("tts.mp3", "wb") as file:
                file.write(response['AudioStream'].read())
            vc.play(discord.FFmpegPCMAudio(CurrentTTS))
        else:
            ctx.send("Message must be under 1000 characters")




@client.command()
async def help(ctx):
    helptext = discord.Embed(
        title = "Help:",
        description="all commands make the bot join the call, other than !pause and !stop",
        color = settings.color
    )
    helptext.add_field(name="", value="", inline=False)
    helptext.add_field(name="!tts", value= "your message be spoken aloud in your voice chat, !tts help for more info", inline = False)
    helptext.add_field(name= "!converse", value="bot will start a converstion in your DMs his responses will be spoken to the masses in a voice call", inline=False)
    helptext.add_field(name="\n", value="\n", inline=False)
    helptext.add_field(name="", value="", inline=False)
    helptext.add_field(name="!join", value="bot will join call and sit there in awkward silence")
    helptext.add_field(name="!pause", value="bot will stop audio but not leave voice chat")
    helptext.add_field(name= "!stop", value="bot will leave voice chat")
    await ctx.send(embed= helptext)








@client.command()
async def converse(ctx, *args):
    global messages
    updates = settings.send_conversing_updates
    if args[0] == "help" and len(args) == 1:
        ConEmbed = discord.Embed(
            title="How to use Talk2Bot™",
            description="by default you are a stranger however you CANNOT switch to other characters with ![character], which does absalutly nothing!!!",
            color = settings.color
        )
        await ctx.send(embed=ConEmbed)
        return
    
    message = ' '.join(str(x) for x in args)
    
    if not ctx.guild.voice_client:
        vc = await ctx.author.voice.channel.connect()
    else:
        vc = ctx.guild.voice_client

    

        
    if vc.is_playing():
            await ctx.send("Currently speaking")
    content = message
    
    if len(messages) == 0:
        messages.append(STARTPROMPT)


    InputVoice = settings.input_voice
    
    output_format = 'mp3'


    if updates:
        UpdateEmbed = discord.Embed(title="GETTING SPEACH FROM INPUT", color = 0xFFA500)
        await ctx.send(embed=UpdateEmbed)

    InputOutput = polly.synthesize_speech(
            Text=content,
            OutputFormat=output_format,
            VoiceId=InputVoice
    )
    with open("ttsInput.mp3", "wb") as file:
        file.write(InputOutput['AudioStream'].read()) 
    
    if updates:
        UpdateEmbed = discord.Embed(title="GETTING RESPONSE FROM CHATGPT", color = 0xFFFF00)
        await ctx.send(embed=UpdateEmbed)
    
    messages.append({"role": "user", "content": f"{content}"})
    response = ChatClient.chat.completions.create(model="gpt-4", messages=messages)
    responseContent = response.choices[0].message.content
    messages.append({"role": "assistant", "content": responseContent})
    
    if len(responseContent) <= 1000:
        if updates:
            UpdateEmbed = discord.Embed(title="GETTING SPEACH FROM RESPONSE", color = 0xcafc03)
            await ctx.send(embed=UpdateEmbed)
        output_format = 'mp3'
        
        
        if settings.use_eleven_labs:
            response = VoiceClient.generate(
                text=responseContent,
                voice=ElevenVoice(
                    voice_id= settings.voice_id,
                    settings=VoiceSettings(stability=0.5, similarity_boost=0.0, style=0, use_speaker_boost=True)
                    ),
                model="eleven_multilingual_v2"
            ) 
            elevenlabs.save(response, "tts.mp3")
        else:
            InputOutput = polly.synthesize_speech(
                    Text=responseContent,
                    OutputFormat=output_format,
                    VoiceId=settings.voice
            )
            with open("tts.mp3", "wb") as file:
                file.write(InputOutput['AudioStream'].read()) 
        
        if updates:
            UpdateEmbed = discord.Embed(title="JOINING 2 SOUND FILES", color = 0x32CD32)
            await ctx.send(embed=UpdateEmbed)
        
        
        JoinSounds("ttsinput.mp3", "tts.mp3")
        
        if updates:
            UpdateEmbed = discord.Embed(title="all done, playing 😊", color = 0x00FF00)
            await ctx.send(embed=UpdateEmbed)
        
        vc.play(discord.FFmpegPCMAudio("response.mp3"))
        if settings.send_response:
            ctx.send(content=responseContent)
    else:
        UpdateEmbed = discord.Embed(title="Error, response too long", color = 0xFF0000)
        await ctx.send(embed=UpdateEmbed)




@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    await client.change_presence(
        activity= discord.Game(name= settings.status_message)
    )




@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)
        






client.run(settings.bot_token)


