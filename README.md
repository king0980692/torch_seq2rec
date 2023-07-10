# SRGNN

Original code from [here](https://github.com/userbehavioranalysis/SR-GNN_PyTorch-Geometric). 
Original [paper](https://arxiv.org/abs/1811.00855).

## diginetica
```
 ./script/run_SRGNN_diginetica.sh
```
## yoochoose
```
./script/run_SRGNN_yoochoose1_4.sh 
./script/run_SRGNN_yoochoose1_64.sh
```
### python 
```python=
python ./model/main.py
```
* ```--dataset ``` : dataset  name , default= 'diginetica'
* ```--batch_size``` : input batch size , default=100
* ```--hidden_size ``` :  hidden state size , default =100
* ```--epoch ``` : the number of epochs to train for , default=10
* ```--lr``` : learning rate , default= 0.001 
* ```--lr_dc ``` : learning rate decay rate , default= 0.1
* ```--lr_dc_step ```  : the number of steps after which the learning rate decay , default= 3
* ```--l2 ``` : l2 penalty , default =  0.00001
* ```--top_k``` : top K indicator for evaluation , default = 20
## Prerequisite

```bash
pip install -r requirement.txt
```

