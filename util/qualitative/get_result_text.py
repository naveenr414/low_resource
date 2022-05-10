import os

def write_list_of_lines(file_name,lines):
    w = open(file_name,"w")
    w.write("\n".join(lines))
    w.close()

experiment_1 = "016"
experiment_2 = "018"

file_location = "../../experiments/results/{}.txt"
experiment_1_data = open(file_location.format(experiment_1)).read().strip().split("\n")
experiment_2_data = open(file_location.format(experiment_2)).read().strip().split("\n")

experiment_1_source = set([i.strip().split("\t")[1] for i in experiment_1_data if i[0] == "S"])
experiment_2_source = set([i.strip().split("\t")[1] for i in experiment_2_data if i[0] == "S"])

intersecting_source = experiment_1_source.intersection(experiment_2_source)
intersecting_source = sorted(list(intersecting_source))

print("Length of intersecting source: {}".format(len(intersecting_source)))

indexes = {}
for i,text in enumerate(intersecting_source):
	indexes[text] = i

experiment_1_predictions = ["" for i in range(len(intersecting_source))]
experiment_2_predictions = ["" for i in range(len(intersecting_source))]
references = ["" for i in range(len(intersecting_source))]

for dataset,predictions in ([experiment_1_data,experiment_1_predictions],[experiment_2_data,experiment_2_predictions]):
    for i in range(len(dataset)):
        if "\t" in dataset[i]:
            text = dataset[i].split("\t")[1].strip()

            if dataset[i][0] == "S" and text in indexes:
                index = indexes[text]
                target = dataset[i+1].split("\t")[1].strip()
                prediction = dataset[i+2].split("\t")[2].strip()
                
                references[indexes[text]] = target
                predictions[indexes[text]] = prediction    
                
                
assert len([i for i in experiment_1_predictions if len(i) == 0]) == 0
assert len([i for i in experiment_2_predictions if len(i) == 0]) == 0

write_list_of_lines("references.txt",references)
write_list_of_lines("sys1.txt",experiment_1_predictions)
write_list_of_lines("sys2.txt",experiment_2_predictions)

os.system("compare-mt --output_directory output/ references.txt sys1.txt sys2.txt --sys_names 100_data 150_data")
os.system("python -m http.server 8000 --bind materialgpu02.umiacs.umd.edu")
