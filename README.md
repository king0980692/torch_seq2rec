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
