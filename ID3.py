# -*- coding: utf-8 -*-
from math import log
import math
##创建数据集
import math
label = ['年龄','收入','学生','信誉']
train = [ ['青','高','否','良',64,'不买'],['青','高','否','优',64,'不买'],['中','高','否','良',128,'买'],
          ['老','中','否','良',60,'买'],['老','低','是','良',64,'买'],['老','低','是','优',64,'不买'],
          ['中','低','是','优',64,'买'],['青','中','否','良',128,'不买'],
          ['青','低','是','良',64,'买'],['老','中','是','良',132,'买'],
          ['青','中','是','优',64,'买'],['中','中','否','优',32,'买'],
          ['中','高','是','良',32,'买'],['老','中','否','优',63,'不买'],['老','中','否','优',1,'买']]
def getN(train):#获取样本总数量
    num = 0
    for i in train:
        num = num + i[4]
    return num
def chocieEnt(train):#计算决策属性的熵
    m = {}
    for i in train:
        if(m.__contains__(i[5])):
            m[i[5]] += i[4]
        else:
            m[i[5]] = i[4]
    N = len(m.keys())
    allsize = 0
    for i in m.keys():
        #print(m[i])
        allsize = allsize + m[i]
    #print(allsize)
    num = []
    for i in m.keys():
        p = round(m[i]/allsize,4)
        #print(p)
        num.append(p)
    ent = 0.0
    for i in num:
        ent = ent + i*math.log(i,2)
    ent = round(-ent,4)
    #print(ent)
    return ent

def getAllChoice(attr,train,label):#获取某一属性的所有取值比如年龄[青，中，老]
    index = label.index(attr)
    all = []
    for i in train:
        all.append(i[index])
    all = list(set(all))
    return all

def attrEnt(attr,train,index):#计算条件属性的熵单一属性,如青年
    m = {}
    for i in train:
        if(i.__contains__(attr)):
            if(i[index] == attr):
                if (m.__contains__(i[5])):
                    m[i[5]] += i[4]
                else:
                    m[i[5]] = i[4]
    N = len(m.keys())
    allsize = 0
    for i in m.keys():
        #print(m[i])
        allsize = allsize + m[i]
    #print(allsize)
    num = []
    for i in m.keys():
        p = round(m[i]/allsize,4)
        #print(p)
        num.append(p)
    ent = 0.0
    for i in num:
        ent = ent + i*math.log(i,2)
    ent = round(-ent,4)
    return abs(ent)

def getNum(attr,train,index):#计算某个属性对应所有人数
    m = {}
    for i in train:
        if(i.__contains__(attr)):
            if(i[index] == attr):
                if (m.__contains__(i[5])):
                    m[i[5]] += i[4]
                else:
                    m[i[5]] = i[4]
    allsize = 0
    for i in m.keys():
        # print(m[i])
        allsize = allsize + m[i]
    return allsize


def entIncrease(allchoice,train,index):#计算某个集体属性如年龄的信息熵增
    ent = {}
    num = {}
    N = getN(train)
    for i in allchoice:
       ent[i] = attrEnt(i, train,index)
       #print(ent[i])
       num[i] = getNum(i,train,index)
    #for i in num:
    #   print(i,num[i])
    E = 0.0
    for i in ent.keys():
        E = E + ent[i] * num[i] / N
    #print(round(E,4))
    G = round(chocieEnt(train) - E,4)
    print(G)
    return G
def getBuyOrNoBuy(attr,train,index):
    m = {}
    for i in train:
        if (i.__contains__(attr)):
            if (i[index] == attr):
                if (m.__contains__(i[5])):
                    m[i[5]] += i[4]
                else:
                    m[i[5]] = i[4]
    return m

def getSonTrain(V,train,index):
    son = []
    for i in train:
        if(i[index] == V):
            son.append(i)
    return son
#print(chocieEnt(train))
#print('青年的信息熵为',attrEnt('青',train,0))
for i in label:
    a = getAllChoice(i,train,label)
    print(i + '的信息增益为',)
    entIncrease(a,train,label.index(i))
def createDataSet():
    ans = []
    for i in train:
        for k in range(i[4]):
            t = []
            for j in range(len(i)):
                if (j == 0):
                    t.append(i[j] + '年')
                elif (not j == 4):
                    t.append(i[j])
            ans.append(t)
    print(ans)
    label = ['年龄', '收入', '学生', '信誉']
    # 返回数据集和每个维度的名称
    return ans, label

##分割数据集
def splitDataSet(dataSet,axis,value):
    # 循环遍历dataSet中的每一行数据
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reduceFeatVec = featVec[:axis] # 删除这一维特征
            reduceFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reduceFeatVec)
    return retDataSet

##计算信息熵
# 计算的始终是类别标签的不确定度
def calcShannonEnt(dataSet):
    numEntries = len(dataSet) # 实例的个数
    labelCounts = {}
    for featVec in dataSet: # 遍历每个实例，统计标签的频次
        currentLabel = featVec[-1] # 表示最后一列
        # 当前标签不在labelCounts map中，就让labelCounts加入该标签
        if currentLabel not in labelCounts.keys(): 
            labelCounts[currentLabel] =0
        labelCounts[currentLabel] +=1

    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEntries
        shannonEnt -= prob * math.log(prob,2) # log base 2
    return shannonEnt

## 计算条件熵
def calcConditionalEntropy(dataSet,i,featList,uniqueVals):
    ce = 0.0
    for value in uniqueVals:
        subDataSet = splitDataSet(dataSet,i,value)
        prob = len(subDataSet) / float(len(dataSet)) # 极大似然估计概率
        ce += prob * calcShannonEnt(subDataSet) #∑pH(Y|X=xi) 条件熵的计算 
    return ce

##计算信息增益
def calcInformationGain(dataSet,baseEntropy,i):
    featList = [example[i] for example in dataSet] # 第i维特征列表
    uniqueVals = set(featList) # 换成集合 - 集合中的每个元素不重复
    newEntropy = calcConditionalEntropy(dataSet,i,featList,uniqueVals)#计算条件熵，
    infoGain = baseEntropy - newEntropy # 信息增益 = 信息熵 - 条件熵
    return infoGain

def chooseBestFeatureToSplitByID3(dataSet):
    numFeatures = len(dataSet[0]) -1 # 最后一列是分类
    baseEntropy = calcShannonEnt(dataSet) #返回整个数据集的信息熵
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures): # 遍历所有维度特征
        infoGain = calcInformationGain(dataSet,baseEntropy,i) #返回具体特征的信息增益
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature # 返回最佳特征对应的维度

def majorityCnt(l):
    pass
def createTree(dataSet,featureName,chooseBestFeatureToSplitFunc = chooseBestFeatureToSplitByID3):
    classList = [example[-1] for example in dataSet] # 类别列表
    if classList.count(classList[0]) == len(classList): # 统计属于列别classList[0]的个数
        return classList[0] # 当类别完全相同则停止继续划分
    if len(dataSet[0]) ==1: # 当只有一个特征的时候，遍历所有实例返回出现次数最多的类别
        return majorityCnt(classList) # 返回类别标签
    bestFeat = chooseBestFeatureToSplitFunc(dataSet)#最佳特征对应的索引
    bestFeatLabel = featureName[bestFeat] #最佳特征
    myTree ={bestFeatLabel:{}}  # map 结构，且key为featureLabel
    del (featureName[bestFeat])
    # 找到需要分类的特征子集
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = featureName[:] # 复制操作
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

# 测试决策树的构建
dataSet,featureName = createDataSet()
myTree = createTree(dataSet,featureName)
print(myTree)
import matplotlib.pyplot as plt

# 定义文本框和箭头格式
decisionNode = dict(boxstyle="round4", color='#3366FF')  #定义判断结点形态
leafNode = dict(boxstyle="circle", color='#FF6633')  #定义叶结点形态
arrow_args = dict(arrowstyle="<-", color='g')  #定义箭头

#绘制带箭头的注释
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
                            xytext=centerPt, textcoords='axes fraction',
                            va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)


#计算叶结点数
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs


#计算树的层数
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth


#在父子结点间填充文本信息
def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0]) / 2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1]) / 2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)


def plotTree(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)  #在父子结点间填充文本信息
    plotNode(firstStr, cntrPt, parentPt, decisionNode)  #绘制带箭头的注释
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTree(secondDict[key], cntrPt, str(key))
        else:
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD


def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalW;
    plotTree.yOff = 1.0;
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()
# -*- coding: utf-8 -*-
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题

# 测试决策树的构建
myDat, labels = createDataSet()
myTree = createTree(myDat, labels)
# 绘制决策树

createPlot(myTree)