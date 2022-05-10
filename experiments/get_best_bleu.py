import sys
import glob
import re

experiment_name = sys.argv[1]
lr_list = eval(sys.argv[2])
lr_scores = {}
bleu_1_scores = {}


for i in range(len(lr_list)):
	try:
		score = open("hyperparameters/checkpoints/{}/{}/output.txt".format(experiment_name,i))
		score = score.read().strip().split("\n")[-1]
		m = re.search('BLEU4 = ((\d|\.)+)',score)
		lr_scores[lr_list[i]] = float(m.group(1))
		n = re.search(', ((\d|\.)+)/',score)
		bleu_1_scores[lr_list[i]] = float(n.group(1))
	except:
		lr_scores[lr_list[i]] = 0
		bleu_1_scores[lr_list[i]] = 0


if max(lr_scores.values()) == 0:
	lr_scores = bleu_1_scores

print(max(lr_scores,key=lr_scores.get))
