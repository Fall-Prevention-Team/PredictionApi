import json
import os
import discord
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
from tsvmerge_forester import Tsv_handler

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
    
    root = os.path.join(os.path.dirname(__file__), "logs")
    tsvs = os.listdir(os.path.join(root,"tsvs"))
    people = os.path.join(root, os.path.join(root, "people"))
    personal_logs = Path(people + "\\" + os.listdir(people)[0])
    content = message.content


    if str(content) == "test":
        print("det er bueno der skriver...")
        await message.channel.send("```test```")
        await message.channel.send(personal_logs)

    
    if content.startswith('!'):
        print("HERE")           
        for l in tsvs:
            name_of_file = l.split('.')[0]
            if name_of_file in content:
                print("H")
                await message.channel.send("FILE FOUND MATCHING YOUR STRING:  " +str(l))

    if str(content) == "Pong!":
        await message.channel.send("STOP... it is I who is bot")
    
    if content.startswith("!name"):
        full_string = content.split(' ')
        
        with open(personal_logs) as JsonFile:
            jsonObject = json.load(JsonFile)
            JsonFile.close()
        
        if not len(full_string) == 3:
            await message.channel.send("Format is: !name [some_id] [some_name]", f'```json\n{personal_logs.read_text()}```')
            return
        await message.channel.send("YES")       
        com, watch_id, name = full_string
        if  str(watch_id) in jsonObject:
            jsonObject[str(watch_id)]['name'] = name
            with open(personal_logs, "w") as JsonFile:
                json.dump(jsonObject, JsonFile, indent=2)
        
            await message.channel.send(f'```json\n{personal_logs.read_text()}```')
        else: 
            await message.channel.send("no such is on a watch: " + str(watch_id))
        

    if content == "give me stats":
        await message.channel.send(Tsv_handler.Run_Forrest_Run())
        




    if "HELP" in content.upper():
        await message.channel.send("``` INFO: \n !some_string = find a matching file on user id \n some_tsvfile_name = give data from file \n  update personal_logs.json names = !name wacth_id name```")


bot_connection.run(Token)