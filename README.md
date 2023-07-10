# torch seq2rec

## Data & Preprocess

#### diginetica

* Data Download
```bash
mkdir data/diginetica
```
  1. download the `dataset-train-diginetica.zip` from [link](https://drive.google.com/drive/folders/0B7XZSACQf0KdXzZFS21DblRxQ3c?resourcekey=0-3k4O5YlwnZf0cNeTZ5Y_Uw)
  2. unzip the file and put `click-item-views.csv` is under `data/diginetica` folder

* Preprocess
  1. remove items with item_counts<=4
  2. remove ssessions with session_length=1
  3. use last week as testing data

#### yoochoose(1/4)

* Data Download
```bash
mkdir data/yoochoose
cd data/yoochoose
wget https://s3-eu-west-1.amazonaws.com/yc-rdata/yoochoose-data.7z
7z x yoochoose-data.7z -o./yoochoose-data
```

* Preprocess
  1. remove items with item_counts<=4
  2. remove ssessions with session_length=1
  3. sort sessions by timestamp and only keep last 1/4 sessions
  4. use last day as testing data

## GRU4REC


### Implementation
```bash
pip install -r model/gru4rec/requirements.txt
cd scripts
./run_gru4rec_[dataset_name].sh
```

This script will do
1. preprocess the original data in `data` folder
2. save `train.csv` and `test.csv` in `exp` folder
3. train gru4rec model
4. evaluate the model with Recall & MRR & NDCG



## SRGNN

Original code from [here](https://github.com/userbehavioranalysis/SR-GNN_PyTorch-Geometric). 
Original [paper](https://arxiv.org/abs/1811.00855).

### preprocessing
```python
python ./model/SRGNN/preprocess.py
```

## Implementation
```bash
pip install -r ./model/SRGNN/requirement.txt 
./script/run_SRGNN_[dataset_name].sh 
```




## sasRec

### Paper 

[Wang-Cheng Kang](http://kwc-oliver.com), [Julian McAuley](http://cseweb.ucsd.edu/~jmcauley/) (2018). [Self-Attentive Sequential Recommendation.](https://cseweb.ucsd.edu/~jmcauley/pdfs/icdm18.pdf) In Proceedings of IEEE International Conference on Data Mining (ICDM'18)


### Implementation

```bash
cd script
./sasRec_yoochoose.sh
```


### Preprocess

- Data Dowmload into data folder 
- You need to run the file  model/sasRec/DataProcess.py first to preprocess the data.
- data preprocess
```python
 python3 ./model/sasRec/DataProcessing.py --dataset=yoochoose
```

### Run model

-you can run the file main.py or  to train the model.
For example: 
```python 
python3 main.py --dataset=sample
```
-You can  change other parameters according to the usage:
if your dataset is from yoochoose
```python
python3 ./model/sasRec/main.py  --dataset=yoochoose
```


