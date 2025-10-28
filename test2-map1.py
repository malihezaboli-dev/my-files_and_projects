mylist=[2,5,8,9,1,13,20]
print(list(map(lambda x:x*2,mylist)))

def function2(x):
    newlist=[]
    for i in x:
        newlist.append(i*2)
    print(newlist)

function2(mylist)

