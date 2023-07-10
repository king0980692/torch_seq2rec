import gzip
from collections import defaultdict
from datetime import datetime
import csv
import argparse



parser = argparse.ArgumentParser()
parser.add_argument('--dataset', required=True)
args = parser.parse_args()


def parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)


countU = defaultdict(lambda: 0)
countP = defaultdict(lambda: 0)
line = 0

dataset_name = args.dataset
f = open('./data/sasRec/reviews_' + dataset_name + '.txt', 'w')
dataset = f'./data/{dataset_name}.csv'
with open(dataset, "r") as d:
    reader = csv.DictReader(d, delimiter=';')

    for l in reader:
        line += 1
        f.write(" ".join([l['sessionId'], l['itemId'], str(l['timeframe'])]) + ' \n')
        asin = l['itemId']
        rev = l['sessionId']
        time = l['timeframe']
        countU[rev] += 1
        countP[asin] += 1
f.close()
d.close()

usermap = dict()
usernum = 0
itemmap = dict()
itemnum = 0
User = dict()
with open(dataset, "r") as d:
    reader = csv.DictReader(d, delimiter=';')
    for l in reader:
        line += 1
        asin = l['itemId']
        rev = l['sessionId']
        time = l['timeframe']
        if countU[rev] < 5 or countP[asin] < 5:
            continue

        if rev in usermap:
            userid = usermap[rev]
        else:
            usernum += 1
            userid = usernum
            usermap[rev] = userid
            User[userid] = []
        if asin in itemmap:
            itemid = itemmap[asin]
        else:
            itemnum += 1
            itemid = itemnum
            itemmap[asin] = itemid
        User[userid].append([time, itemid])
    # sort reviews in User according to time

    for userid in User.keys():
        User[userid].sort(key=lambda x: x[0])

    print( usernum, itemnum)

    f = open(f'./data/sasRec/{dataset_name}.txt', 'w')
    for user in User.keys():
        for i in User[user]:
            f.write('%d %d\n' % (user, i[1]))
    f.close()
    d.close()