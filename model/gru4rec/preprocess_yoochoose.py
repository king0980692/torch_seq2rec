import numpy as np
import pandas as pd
import datetime
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--remove_items', default=4, type=int)
args = parser.parse_args()

ori_data_path = './data/yoochoose/yoochoose-clicks.dat'
train_data_path = './exp/yoochoose/train.csv'
# valid_data_path = './exp/yoochoose/valid.csv'
test_data_path = './exp/yoochoose/test.csv'

week_time= 86400*7
day_time = 86400

def removeShortSessions(data):
    # delete sessions of length = 1
    session_len = data.groupby('SessionID').size()
    data = data[np.in1d(data['SessionID'], session_len[session_len > 1].index)]
    return data

def removeUnpopularItems(data, num):
    # delete items appearing < 5 times
    item_len = data.groupby('ItemID').size()
    data = data[np.in1d(data['ItemID'], item_len[item_len > num].index)]
    return data

# read data and convert the timestamp
ori_data = pd.read_csv(ori_data_path, sep=',', header=None, usecols=[0,1,2], dtype={0:np.int32, 1:str, 2:np.int64})
ori_data.columns = ['SessionID', 'Time', 'ItemID']
ori_data['Time']= ori_data.Time.apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ').timestamp())
ori_data = ori_data.sort_values(['SessionID', 'Time'], ascending=True)

# remove short sessions and unpopular items
ori_data = removeShortSessions(ori_data)
ori_data = removeUnpopularItems(ori_data, args.remove_items)

# split into train, valid, test(?)
time_max = ori_data['Time'].max()
print('time_max: ', time_max, datetime.datetime.fromtimestamp(time_max))
session_time_max = ori_data.groupby('SessionID')['Time'].max()

train_session_idx = session_time_max[session_time_max < (time_max - week_time)].index
valid_session_idx = session_time_max[session_time_max >= (time_max - week_time)].index

split1_4 = int(len(train_session_idx)/4)
train_session_idx = train_session_idx[-split1_4:]
train_data = ori_data[np.in1d(ori_data['SessionID'], train_session_idx)]
valid_data = ori_data[np.in1d(ori_data['SessionID'], valid_session_idx)]

# remove short sessions
train_data = removeShortSessions(train_data)
valid_data = removeShortSessions(valid_data)

# Delete records in validation split where items are not in training split
valid_data = valid_data[np.in1d(valid_data['ItemID'], train_data['ItemID'])]

# save to csv
print('shape of train data: ', train_data.shape)
print('unique train sessions: ', train_data['SessionID'].nunique())
print('unique train items: ', train_data['ItemID'].nunique())
train_data.to_csv(train_data_path, sep=',', index=False)

print('shape of test data: ', valid_data.shape)
print('unique test sessions: ', valid_data['SessionID'].nunique())
print('unique test items: ', valid_data['ItemID'].nunique())
valid_data.to_csv(test_data_path, sep=',', index=False)


