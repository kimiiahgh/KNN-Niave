from scipy.io.arff import loadarff
import random 
import math
totaldata=[]

dataset=loadarff(open('C:/Users/MAHSA/Desktop/ThyroidData.arff','r'))
hameyesatrha=[i for i in range(0,1034)]
satrjadid=[]
satrjadid=random.sample(hameyesatrha,len(hameyesatrha))
##########################
tdata1=[]
tdata2=[]
tdata3=[]
tdata4=[]
tdata5=[]
testdata1=[]
testdata2=[]
testdata3=[]
testdata4=[]
testdata5=[]
indtdata1=[]
indtdata2=[]
indtdata3=[]
indtdata4=[]
indtdata5=[]
indtestdata1=[]
indtestdata2=[]
indtestdata3=[]
indtestdata4=[]
indtdatadata5=[]
indtestdata1 = satrjadid[0:207]
indtdata1=satrjadid[207:]
indtestdata2 = satrjadid[207:414]
indtdata2=satrjadid[0:207]+satrjadid[414:]
indtestdata3 = satrjadid[414:621]
indtdata3=satrjadid[0:414]+satrjadid[621:]   
indtestdata4=satrjadid[620:827]
indtdata4=satrjadid[0:620]+satrjadid[827:]
indtestdata5=satrjadid[827:]
indtdata5=satrjadid[0:827]

  
#######################
def train(indx):
    tdata=[]
    for i in indx:
        tdata.append(dataset[0][i])
    return tdata
def test(indx):
    testdata=[] #data test
    for i in indx:
        testdata.append(dataset[0][i])
    return testdata
#difnum = fasele nominal
tdata1=train(indtdata1)
tdata2=train(indtdata2)
tdata3=train(indtdata3)
tdata4=train(indtdata4)
tdata5=train(indtdata5)
testdata1=test(indtestdata1)
testdata2=test(indtestdata2)
testdata3=test(indtestdata3)
testdata4=test(indtestdata4)
testdata5=test(indtestdata5)
def minimum(tdata,testdata):
    minimumi=[]
    #nomindx=[1,2,3,4,5,6,7,8,9,10,11,12,13]
    numindx=[0 , 14,15,16,17,18]
    for j in numindx:
        mini = 1.5
        for i in range(0,827):
            if tdata[i][j]<mini:
                mini = tdata[i][j]
        for i in range(0,207):
            if testdata[i][j]<mini:
                mini = testdata[i][j]
        minimumi.append(mini)
    return minimumi
minimum1= minimum(tdata1,testdata1)
minimum2= minimum(tdata2,testdata2)
minimum3= minimum(tdata3,testdata3)
minimum4= minimum(tdata4,testdata4)
minimum5= minimum(tdata5,testdata5)
def maximum(tdata,testdata):
    numindx=[0 , 14,15,16,17,18]
    maximumi=[]
    for j in numindx:
        maxi = -1
        for i in range(0,827):
            if tdata[i][j]>maxi:
                maxi = tdata[i][j]
        for i in range(0,207):
            if testdata[i][j]>maxi:
                maxi = testdata[i][j]
        maximumi.append(maxi)
    return maximumi
maximum1 = maximum(tdata1, testdata1)
maximum2 = maximum(tdata2, testdata2)
maximum3 = maximum(tdata3, testdata3)
maximum4 = maximum(tdata4, testdata4)
maximum5 = maximum(tdata5, testdata5)
def normaltrain(tdata ,mini , maxi):
    normaldata=[]
    for i in range(0 , 827):
        t=[]
        numindx=[0 , 14,15,16,17,18]
        nomindx=[1,2,3,4,5,6,7,8,9,10,11,12,13]
        for j in range(0,19):
            if j in nomindx:
                t.append(tdata[i][j])
            else:
                indxn= numindx.index(j)
                t.append((tdata[i][j] - mini[indxn])/(maxi[indxn] - mini[indxn]))
        t.append(tdata[i][19])
        normaldata.append(t)
        
    return normaldata

def normaltest(testdata , mini , maxi):
    normaldata=[]
    numindx=[0 , 14,15,16,17,18]
    nomindx=[1,2,3,4,5,6,7,8,9,10,11,12,13]
    for i in range(0 , 207):
        t=[]
        for j in range(0,19):
            if j in nomindx:
                t.append(testdata[i][j])
            else:
                indxn= numindx.index(j)
                t.append((testdata[i][j] - mini[indxn])/(maxi[indxn] - mini[indxn]))
        t.append(testdata[i][19])
        normaldata.append(t) 
    return normaldata
tdata1=normaltrain(tdata1,minimum1,maximum1)
tdata2=normaltrain(tdata2,minimum2,maximum2)
tdata3=normaltrain(tdata3,minimum3,maximum3)
tdata4=normaltrain(tdata4,minimum4,maximum4)
tdata5=normaltrain(tdata5,minimum5,maximum5)
testdata1=normaltest(testdata1,minimum1 , maximum1)
testdata2=normaltest(testdata2,minimum2 , maximum2)
testdata3=normaltest(testdata3,minimum3 , maximum3)
testdata4=normaltest(testdata4,minimum4 , maximum4)
testdata5=normaltest(testdata5,minimum5 , maximum5)

def difnom(a,b):
    if a==b:
        dif = 0
    else:
        dif = 1
    return dif
#difnum = fasele numercha 
def difnum(a , b):
    dif = (a-b)*(a-b)
    return dif
def KNN(k , data , tdata ):
    numindx=[0 , 14,15,16,17,18]
    nomindx=[1,2,3,4,5,6,7,8,9,10,11,12,13]
    sigma=0
    dbox=[]
    #dbox = (list faselehaye oghlidosi, shomare satr)
    #tafazol = 0
    for i in range(0,827):
        for j in range(0,19):
            tafazol = 0
            if j in nomindx:
                tafazol = difnom(tdata[i][j], data[j])
            elif j in numindx:
                tafazol = difnum(data[j] , tdata[i][j])
            sigma = sigma + tafazol
        dbox.append((math.sqrt(sigma),i))
        sigma=0
    dbox.sort()
    n1=0
    n2=0
    n3=0
    for i in range(0,k):
        if tdata[dbox[i][1]][19]==b'1':
            n1 = n1 +1
        elif tdata[dbox[i][1]][19]==b'2' :
            n2 = n2 +1
        elif tdata[dbox[i][1]][19]== b'3':
            n3 = n3+1        
    maxx = max(n1 , n2 , n3)
#    print(n1,n2,n3)
    if n1 == maxx:
        cmax = b'1'
    elif n2 == maxx:
        cmax = b'2'
    elif n3 == maxx:
        cmax = b'3'
    return cmax

def Errortrain(datatrain , k,tdata):
    e =0 #tedade errorha
    for i in range(0 , 827):
        if KNN(k , datatrain[i],tdata)!= datatrain[i][19]:
            e=e+1
    return e
def Errortest(datatest , k,tdata):
    e=0
    for i in range(0 , 207):
        if KNN(k , datatest[i],tdata) != datatest[i][19]:
            e=e+1
    return e
def etest (k, testdata, tdata):
    o = 100*Errortest(testdata , k , tdata)/207
    print("k = " , k , "test error = ", o, "%")
    return o
def etrain(k,tdata):
    o= 100*Errortrain(tdata , k+1, tdata)/827
    print(" k = ", k ,  " train error = ",o , "%")
    return o
    
k = [1,10 , 20 , 50 ,100, 200 , 500 , 800]
avgtest=[]
avgtrain=[]
for z in k:
    sumtrain=0
    sumtest=0
    sumtest += etest(z,testdata1,tdata1)
    sumtest += etest(z,testdata2,tdata2)
    sumtest +=etest(z,testdata3,tdata3)
    sumtest +=etest(z,testdata4,tdata4)
    sumtest +=etest(z,testdata5,tdata5)
    avgtest.append(sumtest/5)
    print("Test average for k = " + str(z) + " is "+ str(sumtest/5)+"%")
    sumtrain += etrain(z,tdata1)
    sumtrain += etrain(z,tdata2)
    sumtrain += etrain(z,tdata3)
    sumtrain += etrain(z,tdata4)
    sumtrain += etrain(z,tdata5)
    avgtrain.append(sumtrain/5)  
    print("Train average for k = " + str(z) + " is "+ str(sumtrain/5)+"%")
from matplotlib import pyplot as plt   
plt.plot(k, avgtrain, label = "train")   
plt.plot(k, avgtest, label = "test") 
plt.xlabel('k') 
plt.ylabel('error')  
plt.title('train and test error in k-nearest neighbor') 
plt.legend()  
plt.show() 

        
        
