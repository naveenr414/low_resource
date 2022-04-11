import sys
import glob
import re

experiment_name = sys.argv[1]
lr_list = eval(sys.argv[2])
lr_scores = {}

for i in range(len(lr_list)):
	score = open("hyperparameters/checkpoints/{}/{}/output.txt".format(experiment_name,i))
	score = score.read().strip().split("\n")[-1]
	m = re.search('BLEU4 = ((\d|\.)+)',score)
	lr_scores[lr_list[i]] = float(m.group(1))
print(max(lr_scores,key=lr_scores.get))
