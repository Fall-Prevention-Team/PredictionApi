import pandas as pd
import time, json, os
from dhooks import Webhook
from dotenv import load_dotenv


class Brrr_alert:
    def __init__(self) -> None:
        load_dotenv()
        disc_hook = os.getenv('WEBHOOK_TOKEN')
        self.captain_hook = Webhook(disc_hook)

    def gobrrr(self, custom_msg:str='', pid:str='', power:int=18):
        if not custom_msg:
            person_info = {'name': 'Someone'}
            if pid:
                if os.path.exists(self.ppath):
                    with open(self.ppath + "personal_logs.json", 'r') as fptl:
                        people = json.load(fptl)
                person_info = people[pid]
            self.captain_hook.send(str(person_info['name'])+' went br'+'r'*power)
            return
        self.captain_hook.send(custom_msg)
        return


class TheCollector:
    def __init__(self):
        self.logs_root_path = './logs/tsvs/'
        self.people_root_path = './logs/people/'
        self.log_path = './logs/log.txt'
        self.personal_logs = self.get_personal_logs()
        self.alerter = Brrr_alert()


    def death_and_taxes(self, data_dict):
        """
        get data -> store data/json/csv? -> keep track of each persons data 
        """
        
        datapoint = pd.DataFrame([[time.time()] + [data_dict['class']] + data_dict['content']])
        
        person_data_df = self.get_tsv(data_dict['id'])
        if person_data_df is None:
            person_data_df = pd.DataFrame(datapoint) # new dataframe/person
        else:
            person_data_df = pd.concat([person_data_df, datapoint])
        
        self.put_tsv(data_dict['id'], person_data_df)

        self.new_personal_logs(data_dict['id'])        


    def get_tsv(self, person_id):
        try:
            return pd.read_csv(self.logs_root_path + str(person_id) + '.tsv', sep='\t', header=None)
        except FileNotFoundError as e:
            print(e, '\nNo tsv found, creating new.')
            return None


    def put_tsv(self, person_id, df):
        df.to_csv(self.logs_root_path + str(person_id) + '.tsv', sep='\t', header=False, index=False)


    def get_personal_logs(self):
        try:
            with open(self.people_root_path + "personal_logs.json", "r") as f:
                return json.load(f)
        except Exception as e:
            print(e, '\nNew dict created.')
            return dict()


    def put_personal_logs(self):
        with open(self.people_root_path + "personal_logs.json", "w") as f:
            json.dump(self.personal_logs,f,indent=4,sort_keys=True)


    def new_personal_logs(self, logid):
        if not str(logid) in self.personal_logs:
            new_person_dict = {
                'pid': str(logid),
                'name': 'No name connected',
                'notifier': 'none'
            }
            self.personal_logs[str(logid)] = self.personal_logs.get(str(logid), new_person_dict)
            self.put_personal_logs()
        return self.personal_logs[str(logid)]


    def logs_add_or_update_info(self, logid, new_name=None , new_notifier=None):
        p_log = self.personal_logs[str(logid)]
        if new_name:
            p_log['name'] = str(new_name)
        if new_notifier:
            p_log['notifier'] = str(new_notifier)
        self.personal_logs[str(logid)] = p_log
        self.put_personal_logs()
    
    def simple_log(self, logtxt):
        log = []
        if os.path.exists(self.log_path):
            with open(self.log_path, 'r') as fp:
                log = [line.rstrip() for line in fp]
                log = log or []
        if logtxt:
            log.insert(0,logtxt)
            log = log[:100]
            with open(self.log_path, 'w') as fp:
                for li in log:
                    fp.write(li + '\n')
        return log


if __name__ == '__main__':
    col = TheCollector()
    dadict = {
        'id':123,
        'content':[1,1,1,1,1,1],
        'class': 1 # ?
    }
    col.death_and_taxes(dadict)


