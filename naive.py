from scipy.io.arff import loadarff
import scipy as sp
from io import StringIO
import numpy as np
import random
import math
totaldata=[]
dataset=loadarff(open('ThyroidData.arff','r'))
satr=[]
for i in range(0,1034):
    satr.append(i)
satr=random.sample(satr,len(satr))
train=satr[0:827]# satr data train
test=satr[828:] #satr data test
indnom=[1,2,3,4,5,6,7,8,9,10,11,12,13]
indnum=[0,15,16,17,18]
def nominal(feature,value,classi,row):
    m=0
    n=0
    for i in row:
        if dataset[0][i][feature]==value and dataset[0][i][19]==classi:
            n = n +1
        if dataset[0][i][19]==classi:
            m = m + 1        
    n = n + float(0.5)
    m = m+1
    p = n / m
    return p

def avg(feature,classi,row):
    summ = 0 #jam for average
    c =0 #
    for i in row:
        if dataset[0][i][19]==classi:
            summ = summ +float(dataset[0][i][feature])
            c = c+1
    m = summ/c
    return m

def var(feature,classi,row):
     jam=0
     n=0
     m=avg(feature,classi,row)
     for i in row:
         if dataset[0][i][19]==classi:
             n=n+1
             jam=jam+((float(dataset[0][i][feature])-m)*(float(dataset[0][i][feature])-m))  
     y = 1/(n-1)
     v = y*jam
     return v
def psb_class(classi,row):
    c=0
    for i in row:
        if dataset[0][i][19]==classi:
            c=c+1
    p=c/(len(row)) 
    return p       
L1=[]
L2=[]
L3=[]
mahsa=[b'1',b'2',b'3']
for j in mahsa:
    for i in range(0,19): #yasi ro bokon train
        if i in indnom:
            p0=nominal(i,b'0',j,train)
            p1=nominal(i,b'1',j,train)
            if j==b'1':
                 L1.append((p0,p1))
            elif j==b'2':
                L2.append((p0,p1))
            elif j==b'3':
                L3.append((p0,p1))
        if i in indnum:
            avrg=avg(i,j,train)
            vari=var(i,j,train)
            if j==b'1':
                L1.append((avrg,vari))
            elif j==b'2':
                L2.append((avrg,vari))
            elif j==b'3':
                L3.append((avrg,vari))
#vijegi 15 khuneye 14 e Li hast
L1.append(psb_class(b'1',train))
L2.append(psb_class(b'2',train))  
L3.append(psb_class(b'3',train))
L=[]
L.append(L1)
L.append(L2)
L.append(L3)
def f_x(instance,feature,avrg,vari):
    a =( 2)*(math.pi)*(vari)
    b = math.sqrt(a)
    c = 1/(b) ##
    d = -(((float(dataset[0][instance][feature]))-avrg)* ((float(dataset[0][instance][feature]))-avrg))
    e = 2 *(vari)
    f = d / e
    g = math.e
    h = math.pow(g , f) ##
    i =  c * h
    return i            
  
def possibility(instance,classi):
    p=1
    for i in indnom:
        if dataset[0][instance][i]==b'0':
            if classi==b'1':
                p=p*(L[0][i][0])
            elif classi==b'2':
                p=p*(L[1][i][0])
            elif classi==b'3':
                p=p*(L[2][i][0] )
                
        elif dataset[0][instance][i]==b'1':
             if classi==b'1':
                p=p*(L[0][i][1])
             elif classi==b'2':
                p=p*(L[1][i][1])
             elif classi==b'3':
                p=p*(L[2][i][1])
    for i in indnum:
        if i==0:
            if classi==b'1':
                p=p*(f_x(instance,i,L[0][i][0],L[0][i][1]))
            elif classi==b'2':
                p=p*(f_x(instance,i,L[1][i][0],L[1][i][1]))
            elif classi==b'3':
                p=p*(f_x(instance,i,L[2][i][0],L[2][i][1]))
        else:
            if classi==b'1':
                p=p*(f_x(instance,i,L[0][i-1][0],L[0][i-1][1]))
            elif classi==b'2':
                p=p*(f_x(instance,i,L[1][i-1][0],L[1][i-1][1]))
            elif classi==b'3':
                p=p*(f_x(instance,i,L[2][i-1][0],L[2][i-1][1]))
    if classi==b'1':
        p=p*(psb_class(classi,train))
    elif classi==b'2':
        p=p*(psb_class(classi,train))
    elif classi==b'3':
        p=p*(psb_class(classi,train))
    return p

def maxp(instance):
    pc1 = possibility(instance,b'1')
    pc2 = possibility(instance,b'2')
    pc3=possibility(instance,b'3')
    maxx=max(pc1,pc2,pc3)
    if maxx == pc3:
        return b'3'
    elif maxx==pc2:
        return b'2'
    elif maxx==pc1:
        return b'1'
        
def error_test(test):
    e_test = 0
    for i in test:
        if dataset[0][i][19] != maxp(i):
            e_test = e_test + 1 
    return e_test
def error_train(train):
    e_train = 0
    for i in train:
        if dataset[0][i][19] != maxp(i):
            e_train = e_train + 1
    return e_train
a1=0
a2=0
test = satr[0:207]
train=satr[207:]
print(error_train(train)/len(train))
print(error_test(test)/len(test))
a1=a1+error_train(train)/len(train)
a2=a2+error_test(test)/len(test)                 
test = satr[207:414]
train=satr[0:207]+satr[414:]
print(error_train(train)/len(train))
print(error_test(test)/len(test))
a1=a1+error_train(train)/len(train)
a2=a2+error_test(test)/len(test) 
test = satr[414:622]
train=satr[0:414]+satr[622:]   
print(error_train(train)/len(train))
print(error_test(test)/len(test))
a1=a1+error_train(train)/len(train)
a2=a2+error_test(test)/len(test) 
test=satr[622:830]
train=satr[0:622]+satr[830:]
print(error_train(train)/len(train))
print(error_test(test)/len(test))
a1=a1+error_train(train)/len(train)
a2=a2+error_test(test)/len(test) 
test=satr[830:]
train=satr[0:830]
print(error_train(train)/len(train))
print(error_test(test)/len(test))
a1=a1+error_train(train)/len(train)
a2=a2+error_test(test)/len(test) 
print("##########")
print(a1/5 ,"avg error of train")
print(a2/5 ,"avg error of test")

      

         
            
    
    
    
    
    
    
   
    
    
    
    
    
        
            
