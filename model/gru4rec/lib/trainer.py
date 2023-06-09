import os
import lib
import time
import torch
import numpy as np
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Trainer(object):
    def __init__(self, model, train_data, eval_data, optim, use_cuda, loss_func, batch_size, args):
        self.model = model
        self.train_data = train_data
        self.eval_data = eval_data
        self.optim = optim
        self.loss_func = loss_func
        self.evaluation = lib.Evaluation(self.model, self.loss_func, use_cuda, k = args.k_eval)
        self.device = torch.device('cuda' if use_cuda else 'cpu')
        self.batch_size = batch_size
        self.args = args

    def train(self, start_epoch, end_epoch, start_time=None):
        if start_time is None:
            self.start_time = time.time()
        else:
            self.start_time = start_time

        train_losses = []
        valid_losses = []
        recalls = []
        mrrs = []
        ndcgs = []
        for epoch in range(start_epoch, end_epoch + 1):
            st = time.time()
            print('Start Epoch #', epoch)
            train_loss = self.train_epoch(epoch)
            loss, recall, mrr, ndcg = self.evaluation.eval(self.eval_data, self.batch_size)
            train_losses.append(train_loss)
            valid_losses.append(loss)
            recalls.append(recall)
            mrrs.append(mrr)
            ndcgs.append(ndcg)

            print("Epoch: {}, train loss: {:.4f}, loss: {:.4f}, recall: {:.4f}, mrr: {:.4f}, ndcg: {:.4f}, time: {}".format(epoch, train_loss, loss, recall, mrr, ndcg, time.time() - st))
            checkpoint = {
                'model': self.model,
                'args': self.args,
                'epoch': epoch,
                'optim': self.optim,
                'loss': loss,
                'recall': recall,
                'mrr': mrr,
                'ndcg': ndcg
            }
            model_name = os.path.join(self.args.checkpoint_dir, "model_{0:05d}.pt".format(epoch))
            torch.save(checkpoint, model_name)
            print("Save model as %s" % model_name)

        # best_recall = round(max(recalls),5)
        best_recall = np.round(max(recalls),5)
        best_mrr = np.round(max(mrrs),5)
        best_ndcg = np.round(max(ndcgs),5)
        print('best recall@20: ', best_recall, 'best mrr@20: ', best_mrr, 'best ndcg@20: ', best_ndcg)
        res_df = pd.DataFrame({
            "model_name": [self.args.model_name],
            "recall@20": [best_recall],
            "mrr@20": [best_mrr],
            "ndcg@20": [best_ndcg]
        })
        res_df.to_csv(os.path.join(self.args.result_dir, self.args.model_name + ".csv"), index = False)

        fig, axes = plt.subplots(2, 1)
        x_plot = np.arange(end_epoch + 1) + 1
        sns.lineplot(x=x_plot, y=np.array(train_losses), ax=axes[0])
        sns.lineplot(x=x_plot, y=np.array(valid_losses), ax=axes[0])
        sns.lineplot(x=x_plot, y=np.array(recalls), ax=axes[1])
        sns.lineplot(x=x_plot, y=np.array(mrrs), ax=axes[1])
        sns.lineplot(x=x_plot, y=np.array(ndcgs), ax=axes[1])
        plt.savefig(os.path.join(self.args.checkpoint_dir,'train_plot.jpg'))


    def train_epoch(self, epoch):
        self.model.train()
        losses = []

        def reset_hidden(hidden, mask):
            """Helper function that resets hidden state when some sessions terminate"""
            if len(mask) != 0:
                hidden[:, mask, :] = 0
            return hidden

        hidden = self.model.init_hidden()
        dataloader = lib.DataLoader(self.train_data, self.batch_size)
        #for ii,(data,label) in tqdm(enumerate(train_dataloader),total=len(train_data)):
        for ii, (input, target, mask) in tqdm(enumerate(dataloader), total=len(dataloader.dataset.df) // dataloader.batch_size, miniters = 1000):
            input = input.to(self.device)
            target = target.to(self.device)
            self.optim.zero_grad()
            hidden = reset_hidden(hidden, mask).detach()
            logit, hidden = self.model(input, hidden)
            # output sampling
            logit_sampled = logit[:, target.view(-1)]
            loss = self.loss_func(logit_sampled)
            losses.append(loss.item())
            loss.backward()
            self.optim.step()

        mean_losses = np.mean(losses)
        return mean_losses
