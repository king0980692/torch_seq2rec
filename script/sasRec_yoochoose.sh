mkdir ../exp/diginetica
python3 ../model/sasRec/Dataprocessing.py --dataset='yoochoose'
python3 ../model/sasRec/main.py --dataset='../data/sasRec/yoochoose'
