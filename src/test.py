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

# train_dataset = MultiSessionsGraph("/diginetica", phrase='train')

# data = pickle.load(open('/Users/wangyikai/Desktop/SR-GNN_PyTorch-Geometric/datasets/diginetica/raw/test.txt', 'rb'))
# for sequences, y in zip(data[0], data[1]):
#     print(sequences, y)

# data = pickle.load(open("./diginetica_test/train.txt", 'rb'))
# data_list = []
# k=0
# for sequences, y in zip(data[0], data[1]):
#     if k<10:
#         print("sequences : ",sequences)
#         print("y : ",y)
#         k+=1
#     i = 0
#     nodes = {}    # dict{15: 0, 16: 1, 18: 2, ...}
#     senders = []
#     x = []
#     for node in sequences:
#         if node not in nodes:
#             nodes[node] = i
#             x.append([node])
#             i += 1
#         senders.append(nodes[node])
#     receivers = senders[:]
#     del senders[-1]    # the last item is a receiver
#     del receivers[0]    # the first item is a sender
#     edge_index = torch.tensor([senders, receivers], dtype=torch.long)
#     x = torch.tensor(x, dtype=torch.long)
#     y = torch.tensor([y], dtype=torch.long)
#     print()
    # data_list.append(Data(x=x, edge_index=edge_index, y=y))
    
# data, slices = self.collate(data_list)
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