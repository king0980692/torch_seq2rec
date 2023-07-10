# -*- coding: utf-8 -*-
"""
Created on 5/4/2019
@author: RuihongQiu
"""


import numpy as np
import logging
from torchmetrics.functional import retrieval_normalized_dcg
import torch
from torchmetrics import RetrievalNormalizedDCG
def forward(model, loader, device, writer, epoch, top_k=20, optimizer=None, train_flag=True):
    if train_flag:
        model.train()
    else:
        model.eval()
        ndcg, hit, mrr = [], [],[]

    mean_loss = 0.0
    updates_per_epoch = len(loader)

    for i, batch in enumerate(loader):
        if train_flag:
            optimizer.zero_grad()
        scores = model(batch.to(device))
        targets = batch.y - 1
        loss = model.loss_function(scores, targets)

        if train_flag:
            loss.backward()
            optimizer.step()
            writer.add_scalar('loss/train_batch_loss', loss.item(), epoch * updates_per_epoch + i)
        else:
            s,t=[],[]
            sub_scores = scores.topk(top_k)[1]    # batch * top_k
            real_scores= scores.topk(top_k)[0]
            for score, target,prob in zip(sub_scores.detach().cpu().numpy(), targets.detach().cpu().numpy(),real_scores.detach().cpu().numpy()):
                hit.append(np.isin(target, score))
                if len(np.where(score == target)[0]) == 0:
                    mrr.append(0)
                else:
                    mrr.append(1 / (np.where(score == target)[0][0] + 1))
            targets = targets.view(-1, 1).expand_as(sub_scores)
            hits = (targets == sub_scores)
            indexes = torch.arange(len(targets)).repeat_interleave(sub_scores.shape[1])
            
            ndcg.append(RetrievalNormalizedDCG()(real_scores.view(-1), hits.view(-1), indexes))
        mean_loss += loss / batch.num_graphs
    if train_flag:
        writer.add_scalar('loss/train_loss', mean_loss.item(), epoch)
    else:
        ndcg=[i.cpu().numpy() for i in ndcg]
        writer.add_scalar('loss/test_loss', mean_loss.item(), epoch)
        hit = np.mean(hit) * 100
        
        mrr = np.mean(mrr) * 100
        ndcg= np.mean(ndcg) * 100
        writer.add_scalar('index/hit', hit, epoch)
        writer.add_scalar('index/mrr', mrr, epoch)
        writer.add_scalar('index/ndcg',ndcg,epoch)
        print("hit " , hit)
        print("mrr" , mrr)
        print("ndcg ",ndcg)
        return {"hit": hit,"mrr":mrr,"ndcg":ndcg}
