#!/bin/bash

fairseq-generate bin/005 --path hyperparameters/checkpoints/005/1/checkpoint_best.pt  --batch-size 128 --beam 5 --remove-bpe --source-lang en --target-lang de > temp.txt
