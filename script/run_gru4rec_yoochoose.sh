mkdir ../exp/yoochoose
python3 ../model/gru4rec/main.py --model_name gru4rec_top1-max --data_folder ../exp/yoochoose/ --result_dir ../result/yoochoose/ --n_epochs 8 --loss_type TOP1-max
