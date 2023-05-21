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
```python3 main.py  --dataset=yoochoose
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
