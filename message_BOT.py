import json
import os
import discord
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path


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
        if not len(full_string) ==3:
            await message.channel.send("it is not in the right format ma dude form wanted: '!name [some_id] [some_name]' (without the anglebracket ofcourse stupid boi)")
            return
        await message.channel.send("YES")       
        watch_id =full_string[1]
        name = full_string[2]
        with open(personal_logs) as JsonFile:
            jsonObject = json.load(JsonFile)
            JsonFile.close()
        if  str(watch_id) in jsonObject:
            jsonObject[str(watch_id)]['name'] = name
            with open(personal_logs, "w") as JsonFile:
                json.dump(jsonObject, JsonFile, indent=2)
        
            await message.channel.send(f'```{personal_logs.read_text()}```')
        else: 
            await message.channel.send("no such is on a watch: " + str(watch_id))
        

    if content == "forest...":
        await message.channel.send(Run_Forrest_Run())
        




    if "HELP" in content.upper():
        await message.channel.send("``` INFO: \n !some_string = find a matching file on user id \n some_tsvfile_name = give data from file \n  update personal_logs.json names = !name wacth_id name```")


#@bot_connection.event
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import accuracy_score, consensus_score
from sklearn.feature_selection import SelectFromModel
import pickle, sys  
def Run_Forrest_Run():
    root = os.path.join(os.path.dirname(__file__), os.path.join('logs', "tsvs"))
    test_data = pd.read_csv(root + '/out_TEST.tsv', sep='\t', header=None)
    train_data = pd.read_csv(root + '/out_TRAIN.tsv', sep='\t', header=None)
    y_test = test_data[0]
    x_test = test_data.loc[:, test_data.columns != 0]
    y_train = train_data[0]
    x_train = train_data.loc[:, test_data.columns != 0]
    feat_clf = SelectFromModel(RandomForestClassifier(n_estimators=20))
    clf = RandomForestClassifier(n_estimators=20)
    clf.fit(x_train, y_train)
    feat_clf.fit(x_train, y_train)
    features_selected = x_train.columns[(feat_clf.get_support())]
    print(len(features_selected))
    print(features_selected)
    print(clf.estimators_[0])
    prediction_of_y = clf.predict(x_test)
    acc = accuracy_score(y_true=y_test, y_pred=prediction_of_y)
    return acc


bot_connection.run(Token)