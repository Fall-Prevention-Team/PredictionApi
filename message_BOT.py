import time
import os
import discord
import pandas as pd
from dotenv import load_dotenv



load_dotenv()
Token = os.getenv('DISCORD_TOKEN')
Server = os.getenv('SERVER_NAME')
bot_connection = discord.Client()
print(Token)

@bot_connection.event
async def on_ready():
    print("CONNECTED...  " + str(bot_connection.user))
    for server in bot_connection.guilds:
        if server.name == Server:
            print(server.name)
            continue



@bot_connection.event
async def on_message(message):
    if message.author == bot_connection.user:
        return
    
    root = os.path.join(os.path.dirname(__file__), os.path.join('logs', "tsvs"))
    if str(message.author) == "Kenneth Køpke#8877":
        print("det er bueno der skriver...")
        #await message.channel.send("```Hej Bueno... im a bot```")

    print(message.author)
    logs = os.listdir(root)
    print(logs)
    print(str(message.content) + ".tsv")
    if str(message.content) + ".tsv" in logs:
        print("HERE")

    #dataframe = pd.read_csv(root + str(message) + ".tsv")
    #print("``` " + dataframe + "```")



    
    
    
bot_connection.run(Token)