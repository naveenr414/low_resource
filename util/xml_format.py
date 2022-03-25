import sys

file_loc = sys.argv[1]
output_dir = sys.argv[2]
language = sys.argv[3]

f = open(file_loc,encoding='utf-8')
g = open(output_dir,'w',encoding='utf-8')

line = f.readline()

while line!='':
    if 'lang="{}"'.format(language) in line:
        text = line.split('"{}">'.format(language))[1].split("</")[0]
        if text.strip() != '':
            g.write(text)
            g.write("\n")   
    elif '<seg' in line:
        text = line.split('">')[1].split("</")[0]
        if text.strip() != '':
            g.write(text)
            g.write("\n")
    line = f.readline()
g.close()
