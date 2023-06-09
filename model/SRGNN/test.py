import argparse
import logging
from tqdm import tqdm

import pickle
import torch
from torch_geometric.data import InMemoryDataset, Data
from dataset import MultiSessionsGraph
# import torch 
# import sys
# sys.path.append("/usr/local/lib/python3.9/site-packages")
# print(sys.path)
from torch_geometric.data import DataLoader
# from model import *
# from train import forward
# from tensorboardX import SummaryWriter
from torch import nn 
# from  dataset import MultiSessionsGraph
import pickle
import os

x=torch.tensor([1,2,4])
e=torch.tensor([[1,2,4],[2,3,1]])
y=torch.tensor([2,3,1])

print(x)
print(e)
print(y)
print(Data(x=x,edge_index=e,y=y).items())


# train_dataset = MultiSessionsGraph("/diginetica", phrase='train')

# data = pickle.load(open('/Users/wangyikai/Desktop/SR-GNN_PyTorch-Geometric/datasets/diginetica/raw/train.txt', 'rb'))
# print(len(data[0]))
# data2 = pickle.load(open('/Users/wangyikai/Desktop/SR-GNN_PyTorch-Geometric/datasets/diginetica/raw/test.txt', 'rb'))
# print(len(data2[0]))
sess_clicks={
    1:[1,2,6,4,5],
    2:[1,2,2,4,5],
    3:[1,2,3,4,5],
    4:[1,7,3,4,5],
    5:[1,7,3,4,5],
}
print(sess_clicks)
iid_counts={}
for s in sess_clicks:
    seq = sess_clicks[s] # items of session
    for iid in seq:
        if iid in iid_counts:
            iid_counts[iid] += 1
        else:
            iid_counts[iid] = 1

for s in list(sess_clicks):
    curseq = sess_clicks[s]
    filseq = list(filter(lambda i: iid_counts[i] >= 5, curseq)) # rule out item count >5 
    print(s)
    print(filseq)
    if len(filseq) < 2:
        del sess_clicks[s]
    else:
        sess_clicks[s] = filseq
print(sess_clicks)
exit()
# for sequences, y in zip(data[0], data[1]):
#     print(sequences, y)

data_list = []
k=0
temp={}
for sequences, y in zip(data[0], data[1]):
    print(sequences, y)
    
    # i = 0 
    # nodes = {}    # dict{15: 0, 16: 1, 18: 2, ...}
    # senders = []
    # x = []
   
    # for node in sequences:
    #     if node not in nodes:
    #         nodes[node] = i
    #         x.append([node])
    #         i += 1
    #     senders.append(nodes[node])
    # receivers = senders[:]
    # del senders[-1]    # the last item is a receiver
    # del receivers[0]    # the first item is a sender
    # edge_index = torch.tensor([senders, receivers], dtype=torch.long)
    # x = torch.tensor(x, dtype=torch.long)
    # y = torch.tensor([y], dtype=torch.long)
    # print(nodes)
    # print(x)
    # print(y)
    # print(edge_index)
    # temp=nodes
    # if k<10:
    #     # print("sequences : ",sequences)
    #     # print("y : ",y)
    #     print(nodes)
    #     k+=1
    # data_list.append(Data(x=x, edge_index=edge_index, y=y))
exit()
print(data_list[0])
print(data_list[0].items())
print(data_list[1].items())
print(data_list[2].items())
data, slices = InMemoryDataset.collate(data_list)
print(data)
print(slices)
# torch.save((data, slices), self.processed_paths[0])


# test=[[1,2,3,4,5],[1,2,3,4,5]]
# test2=[1,2,3,4,5]
# a=(test,test2)
# print(a)
# hh=[[1,1],[2,2],[3,3],[4,4],[5,5]]
# print(test[:])
# # for i in test:
# #     print(test[:])
# #     test.append(1)
# test.append(1)    
# print(test[:])
# data = pickle.load(open('./datasets/sample/raw/test.txt', 'rb'))
# data_list = []
# print()
# k=0

# for sequences, y in zip(data[0], data[1]): # (sequences, y)=(train_seqs, train_labs) 
#     # if k<10:
#     #     print("sequences    ",sequences)
#     #     print("y    ", y)
#     #     k+=1
#     i = 0
#     nodes = {}    # dict{15: 0, 16: 1, 18: 2, ...}
#     senders = []
#     x = []
#     for node in sequences:
#         if node not in nodes:
#             nodes[node] = i
#             x.append([node])
#             i += 1
#         senders.append(nodes[node]) # store index 
#     # print("senders     : ",senders)
#     receivers = senders[:]
    
#     del senders[-1]    # the last item is a receiver
#     del receivers[0]    # the first item is a sender
#     # print("senders     : ",senders)
#     # print("receivers    : ",receivers)
#     edge_index = torch.tensor([senders, receivers], dtype=torch.long)
    # if k<10:
    #     print("senders  ",senders)
    #     print("receivers    ",receivers)
    #     print("x ",x)
    #     print("y",y)
    #     print("edge_index" , edge_index)
    #     k+=1
#     x = torch.tensor(x, dtype=torch.long)
#     y = torch.tensor([y], dtype=torch.long)
    
#     data_list.append(Data(x=x, edge_index=edge_index, y=y))
#     # if k<10:
#     #     # print("nodes ",nodes)
#     #     print("\n")
#     #     k+=1
# # print()
# data, slices = InMemoryDataset.collate(data_list)
# # print(data)
# # print(slices)
# for i in data_list:
#     #output : {x :tensor([node i ]... ),edge_index: tensor([sender]),[receiver],y: tensor(node j )}

#     print(i.to_dict())

# # train_dataset = MultiSessionsGraph(cur_dir + '/../SR-GNN_PyTorch-Geometric/datasets/' + opt.dataset, phrase='train')
# train_dataset=(data, slices)
# # print(torch.save((data, slices), self.processed_paths[0]))
# print(type(train_dataset))
# train_loader = DataLoader(data, batch_size=100, shuffle=True)
# print(next(iter(train_loader)))


# nodes  {282: 0}
# nodes  {281: 0, 308: 1}
# nodes  {281: 0}
# nodes  {58: 0, 230: 1, 246: 2}
# nodes  {58: 0, 230: 1, 246: 2}
# nodes  {58: 0, 230: 1}
# nodes  {58: 0, 230: 1}
# nodes  {58: 0, 230: 1}