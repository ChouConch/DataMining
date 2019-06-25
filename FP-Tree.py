C = [['A','B','C','E','F','O'],['A','C','G'],['E','I'],['A','C','D','E','G'],
     ['A','C','E','G','L'],['E','J'],['A','B','C','E','F','P'],
     ['A','C','D'],['A','C','E','G','M'],['A','C','E','G','N']]
C = [['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'],
     ['a', 'f', 'g'],
     ['b', 'd', 'e', 'f', 'j'],
     ['a', 'b', 'd', 'i', 'k'],
     ['a', 'b', 'e', 'g']
     ]
sup = 3
C1 = C.copy()#复制一份C
N = len(C)

class fptree(object):
    def __init__(self, name,count,next,pri,nextname,m):
        self.name = name
        self.count = count
        self.next = next
        self.pri = pri
        self.nextname = nextname
        self.m = {}
    def update(self,next,nextname):
        self.m[nextname] = next
    def __str__(self):
        return self.name + ":" + str(self.count) +'父节点为' + self.pri.name+ "后继节点有" + self.nextname.__str__()

def getHead(C):
    m = {}
    for i in C:
        for j in i:
            if (m.__contains__(j)):
                m[j] = m[j] + 1
            else:
                m[j] = 1
    return m

def getDit(C):
    N = len(C)
    m = {}
    for i in C:
        for j in i:
            if(m.__contains__(j)):
                m[j] = m[j] + 1
            else:
                m[j] = 1
    for i in list(m.keys()):
        m[i] = round(m[i],3)
    print(m)
    return m

def checkC(C,m):
    for i in C:
        for j in i:
            if(m[j]<sup):
                i.remove(j)
                m.pop(j)
        i.sort(key=lambda x:m[x],reverse=True)
        #print(i)
    return C


def add(T, C):
    head = T
    for i in C:
        if (T.nextname.__contains__(i)):
            T.m[i].count += 1
            T = T.m[i]
        else:
            node = fptree(i,1,[],T,[],{})
            T.nextname.append(i)
            T.next.append(node)
            T.update(node,i)
            T = node
    T = head

def printT(T):
    for i in T.next:
        print(i)
        printT(i)

def getNode(T,name,ans):
    for i in T.nextname:
        if(i == name):
            ans.append(T.m[i])
        elif(T.m[i].next == None):
            return
        else:
            getNode(T.m[i],name,ans)

def init(node,m):
    if (not node.name == ''):
        m[node.name] = 0
        init(node.pri, m)

def getNodeDit(node,m,num):
    if(not node.pri.name == ''):
        m[node.pri.name] = m[node.pri.name] + num
        getNodeDit(node.pri,m,num)

def slove(T,s):#获得s的最大频繁项集
    l = []
    ans = []
    nodeM = {}
    getNode(T, s, ans)
    for i in ans:
        nodeM[i.name] = 0
        #print(i)
    for i in ans:
        init(i, nodeM)
    for i in ans:
        getNodeDit(i, nodeM, i.count)
    for i in ans:
        nodeM[i.name] += i.count
    #for i in nodeM.keys():
    #    print(i,nodeM[i])
    for i in list(nodeM.keys()):
        if (round(nodeM[i] , 3) < sup):
            nodeM.pop(i)
    for i in nodeM.keys():
        l.append(i + ':' + str(nodeM[i]))
        #print(i, nodeM[i])
    return l

def getSonSet(L1):
    aL = []
    N = len(L1)
    for i in range(2 ** N):
        combo = []
        for j in range(N):
            if ((i >> j) % 2 == 1):
                combo.append(L1[j])
        if (not combo == []):
            aL.append(combo)
    return aL


m = getDit(C)
C1 = checkC(C1,m)
T = fptree("",0,[],None,[],{})
for i in C1:
    add(T,i)
printT(T)

for i in list(m.keys()):
    max = slove(T,i)
    l = getSonSet(max)
    t = []
    for j in max:
        if(not j[0] == i):
            t.append(j)
    print(i + '的条件模式基为' ,t)
    print(i + '的最大频繁项集为' ,max)
    print(i + '的所有频繁项集为',l)