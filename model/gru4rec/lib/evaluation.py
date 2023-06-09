import lib
import numpy as np
import torch
from tqdm import tqdm

class Evaluation(object):
    def __init__(self, model, loss_func, use_cuda, k=20):
        self.model = model
        self.loss_func = loss_func
        self.topk = k
        self.device = torch.device('cuda' if use_cuda else 'cpu')

    def eval(self, eval_data, batch_size):
        self.model.eval()
        losses = []
        recalls = []
        mrrs = []
        ndcgs = []
        dataloader = lib.DataLoader(eval_data, batch_size)
        with torch.no_grad():
            hidden = self.model.init_hidden()
            for ii, (input, target, mask) in tqdm(enumerate(dataloader), total=len(dataloader.dataset.df) // dataloader.batch_size, miniters = 1000):
            #for input, target, mask in dataloader:
                input = input.to(self.device)
                target = target.to(self.device)
                logit, hidden = self.model(input, hidden)
                logit_sampled = logit[:, target.view(-1)]
                loss = self.loss_func(logit_sampled)
                recall, mrr, ndcg = lib.evaluate(logit, target, k=self.topk)

                # torch.Tensor.item() to get a Python number from a tensor containing a single value
                losses.append(loss.item())
                recalls.append(recall)
                mrrs.append(mrr)
                ndcgs.append(ndcg)
        mean_losses = np.mean(losses)
        mean_recall = np.mean(recalls)
        # mean_recall = torch.mean(torch.stack(recalls)).cpu().numpy()
        mean_mrr = torch.mean(torch.stack(mrrs)).cpu().numpy()
        mean_ndcg = torch.mean(torch.stack(ndcgs)).cpu().numpy()
        # print("ndcgs: ", ndcgs)
        # print("middle: ", torch.stack(ndcgs))
        # print("mean_ndcg: ", mean_ndcg)

        return mean_losses, mean_recall, mean_mrr, mean_ndcg
