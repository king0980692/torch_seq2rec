#!/usr/bin/env python36
# -*- coding: utf-8 -*-
# 1. remove item (unpopular <=4)
# 2. cut train test (7days) (see max_date)
# 3. remove session_len=1 in train&test

"""
tmeframe (time since the first query in a session, in milliseconds)
duration (page dwell time, in milliseconds)
eventdate (calendar date)
"""

import argparse
import time
import csv
import pickle
import operator
import datetime
import os
import numpy as np 
# import polars as pl   
# from datetime import datetime
parser = argparse.ArgumentParser()
parser.add_argument('--dataset', default='diginetica', help='dataset name: diginetica/yoochoose/sample')
opt = parser.parse_args()
print(opt)
dataset=''
if opt.dataset == 'diginetica':
    dataset ='./data/'+ opt.dataset+'/train-item-views.csv'

elif opt.dataset =='yoochoose':
    dataset ='./data/'+ opt.dataset+'-data/yoochoose-clicks.dat'
print(dataset)
print("-- Starting @ %ss" % datetime.datetime.now())
with open(dataset, "r") as f:
    if opt.dataset == 'yoochoose':
        reader = csv.DictReader(f, delimiter=',') # dat file per session
    elif opt.dataset =='diginetica':
        # f=f[:20]
        reader = csv.DictReader(f, delimiter=',') # csv  per session
    
    sess_clicks = {} # {id: tuple of (item_id,timeframe)}
    sess_date = {}# {id:date}
    ctr = 0
    curid = -1 # current session id
    curdate = None
    i=0

    for data in reader:    
        if opt.dataset=='diginetica':
            data['session_id']=data['sessionId']
            data['item_id']=data['itemId']
            data['user_id']=data['userId']
            del data['sessionId'],data['userId'],data['itemId']
        elif opt.dataset=='yoochoose':
            del data['category']
        sessid = data['session_id']
      
        # deal with time in a fixed session
        # if current date exist in a fixed session
        # to get last time
        if curdate and not curid == sessid:
            date = ''
            if opt.dataset == 'yoochoose':
                date = time.mktime(time.strptime(curdate[:19], '%Y-%m-%dT%H:%M:%S'))
            else:
                date = time.mktime(time.strptime(curdate, '%Y-%m-%d'))
            sess_date[curid] = date
        curid = sessid

        #deal with item id
        if opt.dataset == 'yoochoose':
            item = data['item_id']
        else:
            item = data['item_id'], int(data['timeframe'])
        
        curdate = ' '
        if opt.dataset == 'yoochoose':
            curdate = data['timestamp']
        else:
            curdate = data['eventdate']
      
        if sessid in sess_clicks:
            sess_clicks[sessid] += [item]
        else:
            sess_clicks[sessid] = [item]
        
        ctr += 1
    print("original length : ", len(sess_clicks))
    date = ''

    # translate date 
    if opt.dataset == 'yoochoose':
        date = time.mktime(time.strptime(curdate[:19], '%Y-%m-%dT%H:%M:%S'))
    else:
        date = time.mktime(time.strptime(curdate, '%Y-%m-%d'))
        # sort item in session
        #   [('81766', 526309), ('31331', 1031018), ('32118', 243569), ('9654', 75848)]
        #['9654', '32118', '81766', '31331']
        for i in list(sess_clicks):
            sorted_clicks = sorted(sess_clicks[i], key=operator.itemgetter(1)) #sort by timeframe small to large
            sess_clicks[i] = [c[0] for c in sorted_clicks]

    sess_date[curid] = date # put last id date
    # print(sess_clicks['1']) # {session: item list}
    # print(sess_date)    # {session: timestamp}

print("original length : ", len(sess_clicks))

print("unique user  : ", len(set(sess_clicks.keys())))
# #making   sess_clicks  ,sess_date




# Filter out length 1 sessions
#sess_clicks {session:[item list]}

for s in list(sess_clicks):
    if len(sess_clicks[s]) == 1:
        del sess_clicks[s]
        del sess_date[s]

# Count number of times each item appears
iid_counts = {} #{"item id":"items"}
for s in sess_clicks:
    seq = sess_clicks[s] # items of session
    for iid in seq:
        if iid in iid_counts:
            iid_counts[iid] += 1
        else:
            iid_counts[iid] = 1
# print(iid_counts)
# # (item,counts)
# sorted_counts = sorted(iid_counts.items(), key=operator.itemgetter(1)) 

length = len(sess_clicks)

for s in list(sess_clicks):
    curseq = sess_clicks[s]
    filseq = list(filter(lambda i: iid_counts[i] >= 5, curseq)) # rule out item count >5 
    # print(filseq)
    if s=='1':
        print("curseq   ",curseq)
        print("filseq   ",filseq)
    if len(filseq) < 2:
        del sess_clicks[s]
        del sess_date[s]
    else:
        sess_clicks[s] = filseq


# Split out test set based on dates
dates = list(sess_date.items())
# print("dates",dates[:5])
maxdate = dates[0][1]
#find max date
for _, date in dates:
    if maxdate < date:
        maxdate = date

# 7 days for test
splitdate = 0
if opt.dataset == 'yoochoose':
    splitdate = maxdate - 86400 * 1  # the number of seconds for a day：86400
else:
    splitdate = maxdate - 86400 * 7

print('Splitting date', splitdate , datetime.datetime.fromtimestamp(splitdate) )      # Yoochoose: ('Split date', 1411930799.0)
print('maxdate date', maxdate , datetime.datetime.fromtimestamp(maxdate) )

train_sess = filter(lambda x: x[1] < splitdate, dates)
test_sess = filter(lambda x: x[1] > splitdate, dates)

# Sort sessions by date
train_sess = sorted(train_sess, key=operator.itemgetter(1))     # [(session_id, timestamp), (), ]
test_sess = sorted(test_sess, key=operator.itemgetter(1))     # [(session_id, timestamp), (), ]
print("-- Splitting train set and test set @ %ss" % datetime.datetime.now())
print("xxxxxxxxxxxx")
print(len(list(train_sess)),len(list(test_sess)))
# Choosing item count >=5 gives approximately the same number of items as reported in paper
item_dict = {}

# Convert training sessions to sequences and renumber items to start from 1
def obtian_train():
    train_ids = []  #session id
    train_seqs = [] # ITEM SEQ
    train_dates = []
    item_order_counter = 1
    k=0
    # in a session, sequence of item ,outseq  
    for s, date in train_sess: # s:sesion_id, date: timestamp
        seq = sess_clicks[s]  # extract item list by session id
        outseq = [] # order for item in sessions ex:session 4737  item =['166617', '59333'] outseq= [1,2]
                                                #session 4741  item =['1389', '35734', '35311'] outseq= [3,4,5]
        for i in seq: #i for item 
            if i in item_dict: 
                outseq += [item_dict[i]]  
            else:
                outseq += [item_order_counter]
                item_dict[i] = item_order_counter
                item_order_counter += 1
               
        if len(outseq) < 2:  # Doesn't occur
            continue
      
        train_ids += [s]
        train_dates += [date]
        train_seqs += [outseq]
        # if k<10:
        #     print("train_seqs",train_seqs)
        #     k+=1
        # 43098, 37484
    return train_ids, train_dates, train_seqs


# Convert test sessions to sequences, ignoring items that do not appear in training set
def obtian_tes():
    test_ids = []
    test_seqs = []
    test_dates = []
    for s, date in test_sess:
        seq = sess_clicks[s]
        outseq = []
        for i in seq:
            if i in item_dict:
                outseq += [item_dict[i]]
        if len(outseq) < 2:
            continue
        test_ids += [s]
        test_dates += [date]
        test_seqs += [outseq]
    return test_ids, test_dates, test_seqs


# train_ids : SESSION id
# train_dates : item date
# train_seqs : item sequence per session [[1, 2], [3, 4, 5], [6, 7], [8, 9], [10, 11, 12, 12, 13, 14, 15]]
train_ids, train_dates, train_seqs = obtian_train()

print("unique id ",len(set(train_ids)))
print("train_seqs",len(train_seqs))
# k=0

test_ids, test_dates, test_seqs = obtian_tes()
print("unique test id ",len(set(test_ids)))
print("test_seqs",len(test_seqs))
print("process_seqs\n")
def process_seqs(item_seq, item_dates):
    out_seqs = [] # neighbors 
    out_dates = []
    labs = [] # nodes last buy 
    ids = []
    k=1
    for id, seq, date in zip(range(len(item_seq)), item_seq, item_dates):
        for i in range(1, len(seq)):
            tar = seq[-i]
            labs += [tar]
            out_seqs += [seq[:-i]]
            out_dates += [date]
            ids += [id]
    return out_seqs, out_dates, labs, ids


train_seqs, train_dates, train_labs, train_ids = process_seqs(train_seqs, train_dates)
print("temp1 ",len(train_labs)) 
test_seqs, test_dates, test_labs, test_ids = process_seqs(test_seqs, test_dates)

tra = (train_seqs, train_labs)
tes = (test_seqs, test_labs)

print("train  ",len(train_seqs))
print("train labs    " , train_labs[:20])
# print("test  ",test_seqs[:3], test_dates[:3], test_labs[:3])
all = 0


for seq in train_seqs:
    all += len(seq)
for seq in test_seqs:
    all += len(seq)
print('avg length: ', all/(len(train_seqs) + len(test_seqs) * 1.0))
if opt.dataset == 'diginetica':
    if not os.path.exists('diginetica'):
        os.makedirs('diginetica')
    pickle.dump(tra, open('../exp/diginetica/raw/train.txt', 'wb'))
    pickle.dump(tes, open('../exp/diginetica/raw/test.txt', 'wb'))
    pickle.dump(train_seqs, open('../exp/diginetica/raw/all_train_seq.txt', 'wb'))

elif opt.dataset == 'yoochoose':
    if not os.path.exists('yoochoose1_4'):
        os.makedirs('yoochoose1_4')
    if not os.path.exists('yoochoose1_64'):
        os.makedirs('yoochoose1_64')
    pickle.dump(tes, open('../exp/yoochoose1_4/raw/test.txt', 'wb'))
    pickle.dump(tes, open('../exp/yoochoose1_64/raw/test.txt', 'wb'))

    split4, split64 = int(len(train_seqs) / 4), int(len(train_seqs) / 64)
    print(len(train_seqs[-split4:]))
    print(len(train_seqs[-split64:]))

    tra4, tra64 = (train_seqs[-split4:], train_labs[-split4:]), (train_seqs[-split64:], train_labs[-split64:])
    seq4, seq64 = train_seqs[train_ids[-split4]:], train_seqs[train_ids[-split64]:]

    pickle.dump(tra4, open('../exp/yoochoose1_4/raw/train.txt', 'wb'))
    pickle.dump(seq4, open('../exp/yoochoose1_4/raw/all_train_seq.txt', 'wb'))

    pickle.dump(tra64, open('../exp/yoochoose1_64/raw/train.txt', 'wb'))
    pickle.dump(seq64, open('../exp/yoochoose1_64/raw/all_train_seq.txt', 'wb'))

else:
    if not os.path.exists('sample'):
        os.makedirs('sample')
    pickle.dump(tra, open('../exp/sample/train.txt', 'wb'))
    pickle.dump(tes, open('../exp/sample/test.txt', 'wb'))
    pickle.dump(train_seqs, open('../exp/sample/all_train_seq.txt', 'wb'))
print("final len train ",len(tra[0]))


print('Done.')

