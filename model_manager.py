"""
Contains:
Renew model funtionality - button
Keep track of last model update - display next to button

Initialize tensorflow cpu or gpu - keep model loaded
Get predictions from model - array

??
multiple models
live prediction log

"""
import requests
import numpy as np
import pandas as pd
import sys, os, time



MODEL_URL = 'https://github.com/Fall-Prevention-Team/Current_model_stats/raw/main/stats/best_model.hdf5'
MODEL_PATH = './model/model.hdf5'
LOG_PATH_TIME_LAST_RENEW = './logs/last_renew.txt'

# util
def _array_to_prediction_obj(float_arr):
    npaar = np.array([float_arr])
    if len(npaar.shape) == 2:  # if univariate
        # add a dimension to make it multivariate with one dimension
        npaar = npaar.reshape((npaar.shape[0], npaar.shape[1], 1))
    return npaar





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


# stores model in global to keep it loaded.
model = None
def retrieve_new_model(model_download_link=MODEL_URL):
    global model
    try:
        res = requests.get(model_download_link)
        print('status code:', res.status_code)
        
        if res.status_code != 200:
            return f'Error getting model: res_code({res.status_code})'
        
        with open(MODEL_PATH, 'wb') as fr:
            fr.write(res.content)
        
        with open(LOG_PATH_TIME_LAST_RENEW, 'w') as tlog:
            tlog.write(str(time.time()))
        
        model = res.content

        return 'Model updated successfully'
    except Exception as e:
        return f'Something went wrong: {e}'


def tf_init(use='cpu'):
    global model
    if use == 'gpu':
        import tensorflow as tf
        import keras
        os.environ['CUDA_VISIBLE_DEVICES'] = "0"
        physical_devices = tf.config.experimental.list_physical_devices('GPU')
        assert len(physical_devices) > 0, "Not enough GPU hardware devices available"
        config = tf.config.experimental.set_memory_growth(physical_devices[0], True)
        print('GPU config return:', config)
        print('Physical Devices:', physical_devices)   
        model = keras.models.load_model(MODEL_PATH)
    elif use == 'cpu':
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
        import tensorflow as tf
        import keras
        model = keras.models.load_model(MODEL_PATH)
    else:
        print('### tf_init user var:', use)
        assert use == 'gpu' or use == 'cpu', 'plz specify gpu or cpu'


def predict_from_array(input_arr):
    if 'keras' not in sys.modules:
        import keras

    global model
    assert model != None, 'No model initialization'

    item = _array_to_prediction_obj(input_arr)
    return model.predict(item)