# sasRec

original code from [kang205/SASRec](https://github.com/kang205/SASRec)
original [paper](https://arxiv.org/abs/1808.09781)

## Model Training 
To train  model on `diginetica` (with default hyper-parameters): 

```
python main.py --dataset=diginetica --train_dir=default 
```

or :

```
python main.py --dataset=diginetica --train_dir=default --maxlen=200 --dropout_rate=0.2 
``` 

## Prerequisite

```bash
pip install -r requirement.txt
```

## Preprocess

* including download dataset into `data` folder
* do some trick here to filter the data
* finallly, maybe execute a python script to dump the processed data into `exp` folder

## sasRec

* using the processed data previously in `exp` folder
* using its model to train
* eval the result
