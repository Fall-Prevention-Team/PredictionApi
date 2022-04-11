import imp
import time
import os
import discord
import pandas as pd
from dotenv import load_dotenv
from data_collector import TheCollector
from dhooks import Webhook


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
    
    hook = Webhook("https://discord.com/api/webhooks/960524647487660152/9EfNeUaAukY_HQjSGFPV1VkSs6pwUHcBDrsfsu6ymE1K7-qdtBaVKMswUzYOo78rDZno")
    hook.send("!123.tsv")



@bot_connection.event
async def on_message(message):
    if message.author == bot_connection.user:
        return
    
    root = os.path.join(os.path.dirname(__file__), os.path.join('logs', "tsvs"))
    logs = os.listdir(root)
    content = message.content


    if str(content) == "test":
        print("det er bueno der skriver...")
        await message.channel.send("```test```")
    
    if content.startswith('!'):
        print("HERE")           
        for l in logs:
            name_of_file = l.split('.')[0]
            if name_of_file in content:
                print("H")
                await message.channel.send("FILE FOUND MATCHING YOUR STRING:  " +str(l))

    if content in logs:
        df = pd.read_csv(root + "\\"+ content, sep="\t", header=None)
        print(df.to_string())
        await message.channel.send(df.to_string())
    
    if content == "forrest...":
        await message.channel.send(Run_Forrest_Run())
        




    if "HELP" in content.upper():
        await message.channel.send("``` INFO: \n !some_string = find a matching file on user id \n some_file_name = give data from file ```")


#@bot_connection.event
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import accuracy_score
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