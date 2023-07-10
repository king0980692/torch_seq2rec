import torch
# from torchmetrics import RetrievalRecall
# from torchmetrics import RetrievalMRR
# from torchmetrics import RetrievalNormalizedDCG
# from torchmetrics.functional import retrieval_recall
# from torchmetrics.functional import retrieval_reciprocal_rank
# from torchmetrics.functional import retrieval_normalized_dcg


def get_recall(indices, targets): #recall --> wether next item in session is within top K=20 recommended items or not
    """
    Calculates the recall score for the given predictions and targets
    Args:
        indices (Bxk): torch.LongTensor. top-k indices predicted by the model.
        targets (B): torch.LongTensor. actual target indices.
    Returns:
        recall (float): the recall score
    """
    targets = targets.view(-1, 1).expand_as(indices)
    hits = (targets == indices).nonzero()
    if len(hits) == 0:
        return 0
    n_hits = (targets == indices).nonzero()[:, :-1].size(0)
    recall = float(n_hits) / targets.size(0)
    return recall


def get_mrr(indices, targets): #Mean Receiprocal Rank --> Average of rank of next item in the session.
    """
    Calculates the MRR score for the given predictions and targets
    Args:
        indices (Bxk): torch.LongTensor. top-k indices predicted by the model.
        targets (B): torch.LongTensor. actual target indices.
    Returns:
        mrr (float): the mrr score
    """
    targets = targets.view(-1, 1).expand_as(indices)
    hits = (targets == indices).nonzero()
    ranks = hits[:, -1] + 1
    ranks = ranks.float()
    rranks = torch.reciprocal(ranks)
    mrr = torch.sum(rranks).data / targets.size(0)
    return mrr


def get_ndcg(indices, targets):
    targets = targets.view(-1, 1).expand_as(indices)
    hits = (targets == indices).nonzero()
    ranks = hits[:, -1] + 1
    ranks = ranks.float()
    ndcgs = 1 / torch.log2(ranks+1) / 1
    ndcg = torch.sum(ndcgs).data / targets.size(0)
    return ndcg


def evaluate(indices, targets, k=20):
    """
    Evaluates the model using Recall@K, MRR@K scores.

    Args:
        logits (B,C): torch.LongTensor. The predicted logit for the next items.
        targets (B): torch.LongTensor. actual target indices.

    Returns:
        recall (float): the recall score
        mrr (float): the mrr score
    """
    # print("INDICES: ", indices.shape)
    # print("TARGETS: ", targets.shape)
    logits, indices = torch.topk(indices, k, -1)
    # print("topk_(logits): )", _.shape, _)
    # print("topkINDICES: ", indices.shape, indices)

    recall = get_recall(indices, targets)
    mrr = get_mrr(indices, targets)
    ndcg = get_ndcg(indices, targets)

    # # fast
    # targets = targets.view(-1, 1).expand_as(indices)
    # hits = (targets == indices)
    # indexes = torch.arange(50).repeat_interleave(indices.shape[1])
    #
    # # long
    # recall = RetrievalRecall(k=k)(indices.view(-1), hits.view(-1), indexes)
    # mrr = RetrievalMRR()(indices.view(-1), hits.view(-1), indexes)
    # ndcg = RetrievalNormalizedDCG()(indices.view(-1), hits.view(-1), indexes)
    # print('finish')
    return recall, mrr, ndcg
