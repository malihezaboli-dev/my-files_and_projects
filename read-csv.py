import csv
f=open("read-csv.txt")
data=csv.reader(f)
#header=next(data)
#header=next(data)
#header=next(data)
mylist=[]
for i in data:
    mylist.append(i)
#print(mylist[0][3])
print(mylist)
f.close()
