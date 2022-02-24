"""
renew model - button
keep track of last model update - display next to button

??
multiple models
live prediction log

"""
import requests
import time

MODEL_URL = 'https://github.com/Fall-Prevention-Team/Current_model_stats/raw/main/stats/best_model.hdf5'
MODEL_PATH = './model/model.hdf5'
LOG_PATH_TIME_LAST_RENEW = './logs/last_renew.txt'

def retrieve_new_model(model_download_link=MODEL_URL):
    try:
        res = requests.get(model_download_link)
        print('status code:', res.status_code)
        
        if res.status_code != 200:
            return f'Error getting model: res_code({res.status_code})'
        
        with open(MODEL_PATH, 'wb') as fr:
            fr.write(res.content)
        
        with open(LOG_PATH_TIME_LAST_RENEW, 'w') as tlog:
            tlog.write(str(time.time()))

        return 'Model updated successfully'
    except Exception as e:
        return f'Something went wrong: {e}'


def get_last_model_renew_time():
    try:
        with open(LOG_PATH_TIME_LAST_RENEW, 'r') as t:
            epoch_time_str = t.read()
        timestamp_model = time.ctime(float(epoch_time_str))
        hours_since = float(epoch_time_str) - time.time()
        hours_since = -1 * hours_since / (60 * 60)

        return timestamp_model, round(hours_since, 2)
    except Exception as e:
        return f'Something went wrong!', e

        