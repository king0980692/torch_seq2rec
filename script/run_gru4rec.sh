python3 ../model/gru4rec/main.py --model_name gru4rec_top1-max --data_folder ../exp/diginetica/ --result_dir ../result/diginetica/ --n_epochs 40 --loss_type TOP1-max
python3 ../model/gru4rec/main.py --model_name gru4rec_bpr-max --data_folder ../exp/diginetica/ --result_dir ../result/diginetica/ --n_epochs 40 --loss_type BPR-max
python3 ../model/gru4rec/main.py --model_name gru4rec_contrastive --data_folder ../exp/diginetica/ --result_dir ../result/diginetica/ --n_epochs 40 --loss_type CL
python3 ../model/gru4rec/main.py --model_name gru4rec_top1-max --data_folder ../exp/yoochoose/ --result_dir ../result/yoochoose/ --n_epochs 8 --loss_type TOP1-max
python3 ../model/gru4rec/main.py --model_name gru4rec_bpr-max --data_folder ../exp/yoochoose/ --result_dir ../result/yoochoose/ --n_epochs 8 --loss_type BPR-max
python3 ../model/gru4rec/main.py --model_name gru4rec_contrastive --data_folder ../exp/yoochoose/ --result_dir ../result/yoochoose/ --n_epochs 8 --loss_type CL
