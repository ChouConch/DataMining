C = [["豆奶","莴苣"],
     ["莴苣","尿布","葡萄酒","甜菜"],
     ["豆奶","尿布","葡萄酒","橙汁"],
     ["莴苣","豆奶","尿布","葡萄酒"],
     ["莴苣","豆奶","尿布","橙汁"]]
C = [['l1', 'l2', 'l5'], ['l2', 'l4'], ['l2', 'l3'],
     ['l1', 'l2', 'l4'], ['l1', 'l3'], ['l2', 'l3'],
     ['l1', 'l3'], ['l1', 'l2', 'l3', 'l5'], ['l1', 'l2', 'l3']]
C =[["啤酒","尿布","婴儿爽身粉","面包","雨伞"],["尿布","婴儿爽身粉"] ,["啤酒","牛奶","尿布"],
     ["尿布","啤酒","洗衣粉"] ,["啤酒","牛奶","可乐饮料"]]
sup = 0.4
conf = 0.5
def checkin(a,b): #检测是否在原数据中出现过
    l = a.split(",")
    for i in b:
        if(set(i) >= set(l)):
            return True
    return False

def getN(C):#获得最大的长度
    maxn = 0
    for i in C:
        if(len(i)>maxn):
            maxn = len(i)
    return maxn

N = getN(C)

def scan(m):#扫描剔除不符合支持度的项,返回频繁项集
    for key in list(m.keys()):#直接用字典删除会出现异常
        if(m.get(key)<sup):
            m.pop(key)
    new = []
    for i in m:
        new.append(i)
    return new

def getC(C,n,L): #生成候选n象集合
    if(n==1):
        c = []
        for i in C:
            for j in i:
                c.append(j)
        a = list(set(c))
        return a
    else:#n>=2的时候利用频繁项集L生成候选象集C
        if(L == []):
            return []
        c = ""
        final = []#最后返回的集合
        p = [] #去重需要的集合
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                u = L[j].split(",")
                for t in u:
                    if(t not in L[i]):
                        c = c + t + "," + L[i]
                        if(checkin(c,C)):
                            check = "".join((lambda x: (x.sort(), x)[1])(list(c)))#检测是否重复了
                            if (check not in p):
                                final.append(c)
                                p.append(check)
                        c = ""
        return final

def getDit(l,C):#生成一个字典，各个项与其支持度相对应
    global N
    m = {}
    for i in l:
        num = 0
        p = i.split(",")
        for j in C:
            if(set(j)>=set(p)):#如果项出现了
                num = num + 1
        m[i] = round(num*1.0/N,3)
    return m

def getSup():
    L = []
    for i in range(N):
        p = getC(C, i, L)
        print("候选" + str(i) + '项集:')
        print(p)
        m = getDit(p, C)
        print("候选" + str(i) + '项集以及对应的支持度')
        for j in m:
            if (m[j] < sup):
                print(j, m[j], "小于最低支持度")
            else:
                print(j, m[j])
        L = scan(m)
        if (L == [] and i > 1):
            break
        print("频繁" + str(i) + '项集:')
        print(L)
        print("频繁" + str(i) + '项集以及对应的支持度')
        for j in L:
            print(j, m[j])


def getAllDit():#将所有支持度放到一个字典里面
    m = {}
    L = []
    for i in range(N):
        p = getC(C, i, L)
        md = getDit(p, C)
        L = scan(md)
        m.update(md)
    return m

def getUnorderDit():
    m = getAllDit()
    newm = {}
    for key in list(m.keys()):
        newKey = "".join((lambda x: (x.sort(), x)[1])(list(key)))
        newKey = newKey.replace(",","")
        newm[newKey] = m.get(key)
    return newm

def getSonSet():
    C1 = getC(C, 1, [])
    m1 = getDit(C1, C)
    L1 = scan(m1)  # 频繁1项集
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
def getRule(m,l):
    rule = {}
    for i in range(len(l)):
        for j in range(i+1,len(l)):
            if(list(set(l[i]) & set(l[j])) == []):
                x = "".join(l[i]) #实际左边
                y = "".join(l[j]) #实际右边
                xx = ",".join(l[i])  # 实际左边
                yy = ",".join(l[j])  # 实际右边
                xy = x + y
                x1 = "".join((lambda x: (x.sort(), x)[1])(list(x)))
                y1 = "".join((lambda x: (x.sort(), x)[1])(list(y)))
                xy1 = "".join((lambda x: (x.sort(), x)[1])(list(xy)))
                key1 = xx + "->" + yy
                key2 = yy + "->" + xx
                if(m.__contains__(x1) and m.__contains__(y1) and m.__contains__(xy1)):
                    value1 = round(m[xy1] / m[x1],3)
                    value2 = round(m[xy1] / m[y1],3)
                    #if(value1>1):
                    #   print(xy1,m[xy1],x1,m[x1],key1)
                    #if(value2>1):
                    #   print(xy1, m[xy1], y1, m[y1],key2)
                    rule[key1] = value1
                    rule[key2] = value2
    return rule
if __name__ == "__main__":
    getSup()
    m = getUnorderDit()
    l = getSonSet()
    print(l)
    rule = getRule(m,l)
    print("关联规则如下:")
    for i in rule:
       print(i,"置信度为：",rule[i])
