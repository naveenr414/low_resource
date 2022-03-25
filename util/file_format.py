import sys

original_file = sys.argv[1]
new_file = sys.argv[2]
column_number = int(sys.argv[3])
ignore_first_lines = int(sys.argv[4])

f = open(original_file,encoding='utf-8') 
w = open(new_file,'w',encoding='utf-8')

for line in range(ignore_first_lines):
    f.readline()
    
line = f.readline()
while line != '':
    line = line.strip('\n')
    split_line = line.split("\t")
    if len(split_line) > column_number:
        w.write(split_line[column_number])
        w.write("\n")
    else:
        print(split_line)
        print("Exiting")
        break
    line = f.readline()

w.close()

