# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 12:31:05 2020

@author: liusy
"""

import matplotlib.pyplot as plt    #引入绘图库
import numpy as np                 #引入数据处理库

#提示信息
A = "该脚本只针对SERPENT2后处理文件"
B = A.center(50,"=")
C = "Created Time:  2020-09-24"
D = C.center(60,"=")
print(B)
print(D)

#print('请输入文件路径,例如：D:/serpent/CEMSR/CEMSR_20200924/')
#FileLocation = input("请输入文件路径:")

#输入项目名称
FileName = input("请输入结果文件主体命名：")

#整理Keff数据，并绘制Keff曲线
def PlotKeffByDays (Filename):
    file = Filename + '_res.m'          #选择res输出文件
    FigName = Filename + '_keff'
    OpenFileName = open(file, "r")      #打开res输出文件
    
    KEFF = open(Filename + "_KEFF.txt", 'w')    #创建该项目的keff文件
    DAYS = open(Filename + "_DAYS.txt", "w")    #创建该项目的days文件

    keff = []   #创造keff空列表
    days = []   #创造days空列表
    
    for line in OpenFileName:                   #对res文件进行遍历
        if 'COL_KEFF' in line:                  #定位COL_KEFF数据地址
            KEFF.write(line[47:59])             #将keff结果输出至keff文件中
            keff.append(float(line[47:59]))     #将keff结果输出至keff列表中
        elif 'BURN_DAYS' in line:               #定位BURN_DAYS数据地址
            DAYS.write(line[47:59])             #将days数据输出至days文件中
            days.append(float(line[47:59]))     #将days数据输出至days列表中
    
    #关闭文件，节约内存
    OpenFileName.close()
    KEFF.close()
    DAYS.close()
    
    #调用绘图函数
    PlotFunction(days, keff, FigName, '', 'Burnup days', 'Keff')

#整理ZAI数据，并绘制ZAI曲线
def PlotZAIByDays(Filename):
    file = Filename + '_dep.m'                      #选择dep文件
    OpenFileName = open(file, 'r')                  #打开dep文件
    
    #创建文件储存结果数据
    MASSFile = open(Filename + '_Mass.txt', 'w')
    DAYSFile = open(Filename + '_Days.txt', 'w')
    ZAIFile  = open(Filename + '_ZAI.txt',  'w')
    #BUFile   = open('BU.txt',   'w')
    
    #遍历文件位字符串
    StrFile = ''
    for line in OpenFileName:           #遍历dep文件输出到空字符串中
        StrFile = StrFile + line
    
    #截取ZAI数据
    ZAIBegin = StrFile.find('ZAI') + 7
    ZAIClap  = StrFile[ZAIBegin:-1]
    ZAIEnd   = ZAIClap.find(']')
    ZAITxt   = ZAIClap[0:ZAIEnd]
    
    #截取ZAI对应的MAS数据
    MASSBegin = StrFile.find('TOT_MASS') +13
    MASSClap  = StrFile[MASSBegin:-1]
    MASSEnd   = MASSClap.find('% total') + 7
    MASSTxt   = MASSClap[0:MASSEnd]

    #截取DAYS数据    
    DAYSBegin = StrFile.find('DAYS') + 9
    DAYSClap  = StrFile[DAYSBegin:-1]
    DAYSEnd   = DAYSClap.find(']') -1 
    DAYSTxt = DAYSClap[0:DAYSEnd]
    
    OpenFileName.close()
    
    #将MASS与DAY数据输出到对应的文件中保存
    for line in DAYSTxt:
        DAYSFile.write(line)
    for line in MASSTxt:
        MASSFile.write(line)
    for line in ZAITxt:
        ZAIFile.write(line)
    
    #关闭MASS与DAYS文件
    MASSFile.close()
    DAYSFile.close()
    ZAIFile.close()
    
    #再次打开上方两文件，作为轴标签
    YTable = open(Filename + '_Mass.txt','r')
    XTable = open(Filename + '_days.txt','r')
    
    #遍历数据文件，将数据以列表形式储存
    for line in XTable:
        XValue = list(map(float,line.split()))      #将DAYS以列表储存

    for line in YTable:
        YValue = line.split('%')[0]                 #提取该行数值数据
        YValue = list(map(float, YValue.split()))   #将提取数据转换为列表

        FigureTitle = line.split('%')[1]            #提取该行标题数据
        FigureTitle = FigureTitle.strip('\n')       #去掉该标题后的换行符
        
        #调用绘图函数
        PlotFunction(XValue, YValue, FigureTitle, FigureTitle, 'Burnup days', 'Mass(g)')

#绘图函数
def PlotFunction(X, Y, FigName, FigureTitle, XTitle, YTitle):
    #画布设定
    plt.figure(figsize=(5,3),facecolor='white')
    #字体预设
    font1 = {'family':'Times New Roam','weight':'normal','size':10}
    
    plt.title(FigureTitle)      #总标题
    plt.xlabel(XTitle, font1)   #X标题
    plt.ylabel(YTitle, font1)   #X标题
    
    Xmax = np.max(X)            #求得最小值
    Xmin = np.min(X)            #求得最小值
    Ymax = np.max(Y)            #求得最小值
    Ymin = np.min(Y)            #求得最小值
    
    Ymax = (Ymax - Ymin)*1.1 + Ymin     #放大最大值，修正绘图
    
    #Xmax = float('%.2f'%Xmax)   #保留两位小数
    #Xmin = float('%.2f'%Xmin)   #保留两位小数
    #Ymax = float('%.2f'%Ymax)   #保留两位小数
    #Ymin = float('%.2f'%Ymin)   #保留两位小数
    
    #XValue = np.arange(Xmin,Xmax,250)
    #YValue = np.arange(Ymin,Ymax,0.01)
    XValue = np.linspace(Xmin,Xmax,11)  #X轴区间与个数
    YValue = np.linspace(Ymin,Ymax,8)   #Y轴区间与个数
    
    plt.xlim(Xmin,Xmax)     #X值域
    plt.ylim(Ymin,Ymax)     #Y值域
    plt.xticks(XValue)     #X轴标签
    plt.yticks(YValue)     #Y轴标签
    plt.tick_params(labelsize=8)    #轴标签大小
    
    #绘制图形
    plt.plot(X, Y,linewidth=2, color='black', linestyle="-")

    plt.grid(True)                          #添加网格线
    plt.grid(color='gray', linestyle='-')   #网格线设置
    
    #保存图形
    plt.savefig(FigName + ".jpg", dpi=500, bbox_inches='tight')
    plt.show()

#main 这才是主题
print('1 : 输出keff基于燃耗天数的曲线图' '\n'
      '2 : 输出ZAI基于燃耗天数的曲线图')
Chiose = input('请选择输出图表：')

#选择输出图类型
if Chiose is '1':
    PlotKeffByDays(FileName)
elif Chiose is '2':
    PlotZAIByDays(FileName)
else :
    print("嘻嘻嘻")