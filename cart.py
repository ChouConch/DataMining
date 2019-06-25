# -*- coding: utf-8 -*-
import numpy as np
from sklearn.feature_extraction import DictVectorizer
import csv
from sklearn import tree
from sklearn import preprocessing
from sklearn import *
import pydotplus
from IPython.display import Image
import graphviz
import pandas as pd
label = ['年龄','收入','学生','信誉']
train = [ ['青','高','否','良',64,'不买'],['青','高','否','优',64,'不买'],['中','高','否','良',128,'买'],
          ['老','中','否','良',60,'买'],['老','低','是','良',64,'买'],['老','低','是','优',64,'不买'],
          ['中','低','是','优',64,'买'],['青','中','否','良',128,'不买'],
          ['青','低','是','良',64,'买'],['老','中','是','良',132,'买'],
          ['青','中','是','优',64,'买'],['中','中','否','优',32,'买'],
          ['中','高','是','良',32,'买'],['老','中','否','优',63,'不买'],['老','中','否','优',1,'买']]
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
label2 = ['年龄','收入','学生','信誉','是否购买']
test = pd.DataFrame(columns=label2, data=ans)  #
test.to_csv('testcsv.csv', encoding='gbk')

allElectornicsData = open('testcsv.csv', 'r')
reader = csv.reader(allElectornicsData)
headers = next(reader)

print(headers)

featureList = []
labelList = []

for row in reader:
    labelList.append(row[len(row) - 1])
    rowDict = {}
    for i in range(1, len(row) - 1):
        rowDict[headers[i]] = row[i]
    featureList.append(rowDict)

print(featureList)
print(labelList)

vec = DictVectorizer()
dummyX = vec.fit_transform(featureList).toarray()

#print("dummyX: " + str(dummyX))
#print(vec.get_feature_names())
#print("labelList: " + str(labelList))

lb = preprocessing.LabelBinarizer()
dummyY = lb.fit_transform(labelList)
#print("dummyY: ", str(dummyY))

#clf = tree.DecisionTreeClassifier()
clf = tree.DecisionTreeClassifier(criterion='gini')
clf = clf.fit(dummyX, dummyY)
#print("clf: ", str(clf))

with open("decisiontree.dot", 'w') as f:
	f = tree.export_graphviz(clf, feature_names = vec.get_feature_names(), out_file = f)
#打开dot文件
with open("decisiontree.dot") as f:
    dot_graph = f.read()
    dot=graphviz.Source(dot_graph)
    dot.view()



