python multiGPU_main_time.py --data_folder ../Data/ctr/ --data_action movielen_1M_time --data_name movielens --embedding_dim 64 --hidden_size 64 --lr 0.002 --test_observed 5 --n_epochs 100 --shared_embedding 1 --batch_size 1200 --optimizer_type Adam --loss_type 'XE' --negative_num 1000 --topk 20 --rank 0 --multiprocessing_distributed --world_size 1