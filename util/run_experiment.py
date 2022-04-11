import os
import sys
import random

def run_experiment(name,src,target,train_data,valid_data,test_data,num_train, num_valid, num_hyperparameter, num_test, settings):
    w = open("experiments/details/{}.txt".format(name),"w")
    w.write("src {}, target {}\n".format(src,target))
    w.write("train_data {}\n".format(", ".join(train_data)))
    w.write("valid_data {}\n".format(", ".join(valid_data)))
    w.write("test_data {}\n".format(", ".join(test_data)))
    w.write("settings: {}\n".format(str(settings)))
    w.close()
    
    # Prepare data
    os.system("mkdir experiments/data/{}".format(name))
    os.system("mkdir experiments/checkpoints/{}".format(name))
    os.system("mkdir experiments/bin/{}".format(name))
    os.system("mkdir experiments/tensorboard/{}".format(name))
    os.system("mkdir experiments/hyperparameters/checkpoints/{}".format(name))
    os.system("mkdir experiments/hyperparameters/data/{}".format(name))

    for data_type,data_list,data_num in zip(["train","valid","test", "hyperparameter"],[train_data,valid_data,test_data,valid_data],[num_train,num_valid,num_test,num_hyperparameter]):
        num_lines = 0
        
        for file in data_list:
            num_lines+=sum(1 for line in open(file+".{}".format(src)))
        
        percent_taken = min(1,data_num/num_lines)
        
        w = open("experiments/data/{}/{}.{}".format(name,data_type,src),"w")
        x = open("experiments/data/{}/{}.{}".format(name,data_type,target),"w")            
            
        for file in data_list:
            f = open(file+".{}".format(src))
            g = open(file+".{}".format(target))
            
            line_1 = f.readline()
            line_2 = g.readline()
            
            while line_1 != '' and line_2 != '':
                if random.random()<percent_taken:
                    w.write(line_1)
                    x.write(line_2)
                line_1 = f.readline()
                line_2 = g.readline()
            
        w.close()
        x.close()


    os.system("cd experiments/data; bash preprocess.sh {} {} {}".format(src,target,name))
    
    # Run preprocessing
    # Preprocess for the hyperparameter tuning 
    preprocess_command = """TEXT=data/{}
fairseq-preprocess --source-lang {} --target-lang {} \
    --trainpref $TEXT/train --validpref $TEXT/hyperparameter --testpref $TEXT/hyperparameter \
    --destdir hyperparameters/data/{} \
    --workers 20""".format(name,src,target,name)
    w = open("experiments/preprocess.sh","w")
    w.write(preprocess_command)
    w.close()
    os.system("cd experiments; bash preprocess.sh")
    
    # Preprocess for the main training loop 
    preprocess_command = """TEXT=data/{}
fairseq-preprocess --source-lang {} --target-lang {} \
    --trainpref $TEXT/train --validpref $TEXT/valid --testpref $TEXT/test \
    --destdir bin/{} \
    --workers 20""".format(name,src,target,name)
    
    w = open("experiments/preprocess.sh","w")
    w.write(preprocess_command)
    w.close()
    
    os.system("cd experiments; bash preprocess.sh")

    # Run some learning rate tuning 
    training_command = """echo '{}'
CUDA_VISIBLE_DEVICES=0 fairseq-train \
    {} \
    --arch transformer --share-decoder-input-output-embed \
    --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0 \
    --lr {} --lr-scheduler inverse_sqrt --warmup-updates 4000 \
    --dropout 0.3 --weight-decay 0.0001 \
    --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
    --max-tokens 4096 \
    --eval-bleu \
    --max-epoch {} \
    --eval-bleu-args '{{"beam": 5, "max_len_a": 1.2, "max_len_b": 10}}' \
    --eval-bleu-detok moses \
    --eval-bleu-remove-bpe \
    --eval-bleu-print-samples \
    --best-checkpoint-metric bleu --maximize-best-checkpoint-metric \
    --save-dir {} \
    --tensorboard-logdir tensorboard/{}
    """
    
    evaluation_command = """fairseq-generate {} \
    --path {}  \
    --batch-size 128 --beam 5 --remove-bpe --source-lang {} --target-lang {}"""
    

    lr_list = [0.1,0.01,0.001,0.0001,0.00001]
    # Setup training + cleanup
    for i, lr in enumerate(lr_list):
        os.system("mkdir experiments/hyperparameters/checkpoints/{}/{}".format(name,i))
        w = open("experiments/submit2.sh","w")
        hyperparameter_epochs = 5
        training_lr_command = training_command.format('{}_{}'.format(name,lr), 'hyperparameters/data/{}'.format(name), lr, hyperparameter_epochs, 'hyperparameters/checkpoints/{}/{}'.format(name,i),name)
        evaluation_lr_command = evaluation_command.format('hyperparameters/data/{}'.format(name),"hyperparameters/checkpoints/{}/{}/checkpoint_best.pt".format(name,i),src,target)        
        
        w = open("experiments/submit2.sh","w")
        w.write("#!/bin/bash")
        w.write("\n")
        w.write(training_lr_command)
        w.write(evaluation_lr_command + "> hyperparameters/checkpoints/{}/{}/output.txt".format(name,i))
        w.close()
        
        os.system("cd experiments; bash submit_small.sh {}".format("{}_{}".format(name,lr)))
        
    max_epochs = 20
    if 'max_epochs' in settings:
        max_epochs = settings['max_epochs']     

    training_main = training_command.format(name,'bin/{}'.format(name),"$LR",max_epochs,'checkpoints/'+name,name)
    
    w = open("experiments/submit2.sh","w")
    w.write("#!/bin/bash")
    w.write("\n")
    w.write("LR=$(python get_best_bleu.py {} \"{}\")".format(name,lr_list))
    w.write("\n")
    w.write(training_main)
    w.close()
    
    # Run sbatch
    os.system("echo 'cd experiments; bash submit.sh {}' | at now + 5 hours".format(name))
    
run_experiment("001","en","de",['data/en-de/processed_data/iwslt/train'],['data/en-de/processed_data/iwslt/valid'],['data/test/flores/devtest/devtest'],10**5, 10**5, 100000000, 100, {'max_epochs': 40})

