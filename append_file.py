

f = open('sample_log2.txt', "r")
lines = f.readlines()

f.close()

f = open('sample_log2.txt', 'a')

i = 0

while i < 100000:
    i+=1
    f.writelines(lines)

f.close
