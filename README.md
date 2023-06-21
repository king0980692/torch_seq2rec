
# sasRec

## Paper 

[Wang-Cheng Kang](http://kwc-oliver.com), [Julian McAuley](http://cseweb.ucsd.edu/~jmcauley/) (2018). *[Self-Attentive Sequential Recommendation.](https://cseweb.ucsd.edu/~jmcauley/pdfs/icdm18.pdf)* In Proceedings of IEEE International Conference on Data Mining (ICDM'18)

##Dataset

 After downloaded the datasets, you can put them in the folder `data/`:

- YOOCHOOSE:  <https://www.kaggle.com/chadgostopp/recsys-challenge-2015>

- DIGINETICA: <http://cikm2016.cs.iupui.edu/cikm-cup> or <https://competitions.codalab.org/competitions/11161>


## Usage

You need to run the file  `data/preprocess.py` first to preprocess the data.

For example: `cd data; python preprocess.py --dataset=sample`


Then you can run the file `main.py` or  to train the model.

For example: `cd pytorch_code; python main.py --dataset=sample`

You can add the suffix `--nonhybrid` to use the global preference of a session graph to recommend instead of the hybrid preference.

You can also change other parameters according to the usage:
if your dataset is from `yoochoose`
```
python3 main.py  --dataset=yoochoose
```
```
optional arguments:
	--dataset, default = 'diginetica'
	--train_dir',default = '../exp/'
	--batch_size', default=128
	--lr', default=0.001
	--maxlen', default=20
	--hidden_units', default=50
	--num_blocks', default=2
	--num_epochs', default=50
	--num_heads', default=1
	--dropout_rate', default=0.5
	--l2_emb', default=0.0
	--device', default='cpu'
	--inference_only', default=True
	--state_dict_path', default=None
```

## Requirements

- Python 3
- PyTorch 0.4.0 

## Preprocess

- Data Dowmload into `data` folder 
- do some trick to filter the data 
- data preprocess
```
	python3 data/DataProcessing.py --dataset=yoochoose
```
=======
# torch seq2rec

## Data & Preprocess

#### diginetica

* Data Download
  1. download the `dataset-train-diginetica.zip` from [link](https://drive.google.com/drive/folders/0B7XZSACQf0KdXzZFS21DblRxQ3c?resourcekey=0-3k4O5YlwnZf0cNeTZ5Y_Uw)
  2. unzip the file and check if `click-item-views.csv` is under `data/diginetica` folder

* Preprocess
  1. remove items with item_counts<=4
  2. remove ssessions with session_length=1
  3. use last week as testing data

#### yoochoose(1/4)

* Data Download
```bash
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
./run_gru4rec.sh
```

This script will do
1. preprocess the original data in `data` folder
2. save `train.csv` and `test.csv` in `exp` folder
3. train gru4rec model
4. evaluate the model with Recall & MRR & NDCG
