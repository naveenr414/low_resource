import os
import sys

def run_experiment(name,src,target,train_data,valid_data,test_data,settings):
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

    for data_type,data_list in zip(["train","valid","test"],[train_data,valid_data,test_data]):
        for direction in [src,target]:
            w = open("experiments/data/{}/{}.{}".format(name,data_type,direction),"w")
            
            for file in data_list:
                f = open(file+".{}".format(direction))
                for line in f:
                    w.write(line)
            w.close()
    
    # Run preprocessing
    command = """TEXT=experiments/data/{}
fairseq-preprocess --source-lang {} --target-lang {} \
    --trainpref $TEXT/train --validpref $TEXT/valid --testpref $TEXT/test \
    --destdir experiments/bin/{} \
    --workers 20""".format(name,src,target,name)
    os.system(command)
    
    # Setup training + cleanup
    command = """ echo '{}'
    CUDA_VISIBLE_DEVICES=0 fairseq-train \
    bin/{} \
    --arch transformer_iwslt_de_en --share-decoder-input-output-embed \
    --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0 \
    --lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
    --dropout 0.3 --weight-decay 0.0001 \
    --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
    --max-tokens 4096 \
    --eval-bleu \
    --eval-bleu-args '{"beam": 5, "max_len_a": 1.2, "max_len_b": 10}' \
    --eval-bleu-detok moses \
    --eval-bleu-remove-bpe \
    --eval-bleu-print-samples \
    --best-checkpoint-metric bleu --maximize-best-checkpoint-metric
    """.format(name,name)
    
    cleanup = """rm -rf bin/{}
    rm -f data/{}""".format(name,name)
    
    w = open("submit2.sh","w")
    w.write("#!/bin/bash")
    w.write("\n")
    w.write(command)
    w.write(cleanup)
    w.close()
    
    # Run sbatch
    os.system("bash submit.sh {}".format(name))
    
run_experiment("001","en","de",['data/en-de/processed_data/wikititles'],['data/test/flores/dev/dev'],['data/test/flores/devtest/devtest'],{'max_epochs': 20})