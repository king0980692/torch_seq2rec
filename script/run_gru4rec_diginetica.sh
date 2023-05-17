mkdir ../exp/diginetica
python3 ../model/gru4rec/main.py --model_name gru4rec_top1-max --data_folder ../exp/diginetica/ --result_dir ../result/diginetica/ --n_epochs 40 --loss_type TOP1-max
