# torch seq2rec

## Data & Preprocess

#### diginetica

Data Download
* download the `dataset-train-diginetica.zip` from [link](https://drive.google.com/drive/folders/0B7XZSACQf0KdXzZFS21DblRxQ3c?resourcekey=0-3k4O5YlwnZf0cNeTZ5Y_Uw)
* unzip the file and check if `click-item-views.csv` is under `data/diginetica` folder

Preprocess
* remove items with item_counts<=4
* remove ssessions with session_length=1

#### yoochoose

Data Download
```bash
cd data/yoochoose
wget https://s3-eu-west-1.amazonaws.com/yc-rdata/yoochoose-data.7z
7z x yoochoose-data.7z -o./yoochoose-data
```

Preprocess
* remove items with item_counts<=4
* remove ssessions with session_length=1


## GRU4REC

```bash
pip install -r model/gru4rec/requirements.txt
cd scripts
./run_gru4rec.sh
```

This script will do
* preprocess the original data in `data` folder
* save `train.csv` and `test.csv` in `exp` folder
* train gru4rec model
* evaluate the model with Recall & MRR & NDCG
