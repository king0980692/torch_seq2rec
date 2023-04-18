import numpy as np
import pandas as pd
import datetime
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--remove_items', default=4, type=int)
args = parser.parse_args()

ori_data_path = './data/diginetica/diginetica.csv'
train_data_path = './exp/preprocessed_data/train.csv'
valid_data_path = './exp/preprocessed_data/valid.csv'
test_data_path = './exp/preprocessed_data/test.csv'

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
ori_data = pd.read_csv(ori_data_path, sep=',')
ori_data['Time'] = ori_data['Time'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').timestamp())

# remove unpopular items
ori_data = removeUnpopularItems(ori_data, args.remove_items)

# split into train, valid, test(?)
time_max = ori_data['Time'].max()
session_time_max = ori_data.groupby('SessionID')['Time'].max()

train_session_idx = session_time_max[session_time_max < (time_max - week_time)].index
valid_session_idx = session_time_max[session_time_max >= (time_max - week_time)].index

train_data = ori_data[np.in1d(ori_data['SessionID'], train_session_idx)]
valid_data = ori_data[np.in1d(ori_data['SessionID'], valid_session_idx)]

# remove short sessions and unpopular items
train_data = removeShortSessions(train_data)
valid_data = removeShortSessions(valid_data)
# print(valid_data.shape)

# Delete records in validation split where items are not in training split
valid_data = valid_data[np.in1d(valid_data['ItemID'], train_data['ItemID'])]
# print(valid_data.shape)

# save to csv
print('shape of train data: ', train_data.shape)
print('unique train sessions: ', train_data['SessionID'].nunique())
print('unique train items: ', train_data['ItemID'].nunique())
train_data.to_csv(train_data_path, sep=',', index=False)

print('shape of valid data: ', valid_data.shape)
print('unique valid sessions: ', valid_data['SessionID'].nunique())
print('unique valid items: ', valid_data['ItemID'].nunique())
valid_data.to_csv(valid_data_path, sep=',', index=False)




