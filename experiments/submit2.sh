#!/bin/bash
LR=0.0001
echo '028'
CUDA_VISIBLE_DEVICES=0 fairseq-train     bin/028     --arch transformer --share-decoder-input-output-embed     --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0     --lr $LR --lr-scheduler inverse_sqrt --warmup-updates 4000     --dropout 0.3 --weight-decay 0.0001     --criterion label_smoothed_cross_entropy --label-smoothing 0.1     --max-tokens 4096     --eval-bleu     --max-epoch 80     --eval-bleu-args '{"beam": 5, "max_len_a": 1.2, "max_len_b": 10}'     --eval-bleu-detok moses     --eval-bleu-remove-bpe     --eval-bleu-print-samples     --best-checkpoint-metric bleu --maximize-best-checkpoint-metric     --save-dir checkpoints/028     --tensorboard-logdir tensorboard/028
    