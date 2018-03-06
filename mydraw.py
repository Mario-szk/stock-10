# -- coding: utf-8 --
#数据可视化
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math


def divide_draw(quote,index,dirpath):
    if len(quote.dayinfo)==0:
        print(quote.name+"不存在数据")
        return

    fig=plt.figure(num=index, figsize=(10, 7),dpi=100,facecolor='w')  # 开启一个窗口，同时设置大小

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

#==================================macd图======================================
    sub2=fig.add_subplot(3,1,3,facecolor='w')  #第2个窗口中的第2个子图
    sub2.grid(b=True, which='major', axis='both', alpha=0.5, color='skyblue', linestyle='--', linewidth=0.5)

    draw_macd(sub2, quote)
    draw_dif(sub2, quote)
    draw_dea(sub2, quote)

    # plt.xlabel('time')
    sub2.set_ylabel('macd')
    sub2.set_xlim(0, len(quote.dayinfo))
    sub2.legend()

    #设置横坐标
    macd_xtick = np.arange(0, len(quote.dayinfo), math.floor(len(quote.dayinfo) / 4))  #向下取整， 生成等差数列
    macd_xtime = []
    for i in macd_xtick:
        macd_xtime.append(quote.dayinfo[i]['time'])
    plt.xticks(macd_xtick, tuple(macd_xtime))            # 这里只显示起始到结尾时间中间的四个位置




#=======================================================日K图===========================================
    sub1 = fig.add_subplot(3, 1, 1, facecolor='w')  # 第2个窗口中的第1个子图，背景色
    sub1.grid(b=True, which='major', axis='both', alpha=0.5, color='skyblue', linestyle='--', linewidth=0.5)
    draw_ma5(sub1,quote)
    draw_ma10(sub1,quote)
    draw_ma20(sub1,quote)
    draw_ma30(sub1,quote)
    draw_k(sub1, quote)

    value_min,minindex = quote.par_min('low')
    value_max,maxindex = quote.par_max('high')

    value_more = (value_max-value_min)*0.1  #设置一部分刻度冗余，不要在纵轴上占满
    plt.ylim(value_min-value_more, value_max+value_more)  # 设置纵轴范围，会覆盖上面的纵坐标
    plt.xlim(0,len(quote.dayinfo))

    # y_tick = np.arange(value_min-value_more, value_max+value_more, round(value_max-value_min+value_more*2/10))  #设置显示更多的刻度
    # sub1.set_yticks(y_tick)  #设置纵轴显示
    sub1.set_xticks([])    #去除坐标轴刻度

    sub1.set_title(quote.symbol+"        "+quote.name)

# =======================================================kdj曲线(第十二天才开始有数据)===========================================
    sub3 = fig.add_subplot(3, 1, 2, facecolor='w')  # 第2个窗口中的第1个子图，背景色
    sub3.grid(b=True, which='major', axis='both', alpha=0.5, color='skyblue', linestyle='--', linewidth=0.5)

    draw_kdj_k(sub3, quote)
    draw_kdj_d(sub3, quote)
    draw_kdj_j(sub3, quote)
    sub3.set_xticks([])  # 去除坐标轴刻度
    sub3.set_ylabel('kdj')
    sub3.set_xlim(0, len(quote.dayinfo))
    filepath= dirpath+'/'+quote.symbol+'.png'
    fig.savefig(filepath)
    # plt.show()
    plt.close(index)


#在macdsubplot子图中绘制macd柱形图
def draw_macd(macdsubplot,quote):
    index_up=[]  #红色macd索引
    macd_up = []
    index_dowm = []  #绿色macd索引
    macd_dowm = []
    for i in range(len(quote.dayinfo)):
        if quote.dayinfo[i]['macd']>0:
            index_up.append(i)
            macd_up.append(quote.dayinfo[i]['macd'])
        if quote.dayinfo[i]['macd']<=0:
            index_dowm.append(i)
            macd_dowm.append(quote.dayinfo[i]['macd'])

    index_up = tuple(index_up)  #np.arange(len(quote.dayinfo))   线上柱形图
    index_down = tuple(index_dowm)   #线下柱形图


    #先画线上
    rects1 = macdsubplot.bar(index_up, macd_up, width=0.5, color='r')
    rects2 = macdsubplot.bar(index_down, macd_dowm, width=0.5, color='g')



from scipy.interpolate import spline   #数据差值，进行曲线的线性平滑

#在macdsubplot子图中绘制dif曲线
def draw_dif(difsubplot,quote):
    x = []
    y = []
    for i in range(len(quote.dayinfo)):
        x.append(i)
        y.append(quote.dayinfo[i]['dif'])

    # xnew = np.linspace(min(x), max(x), 300)  # 在最小值和最大值之间建立300个插值点
    # ynew = spline(x, y, xnew)
    plot1=difsubplot.plot(x,y,'-',c='b',label='dif',linewidth=0.5)  #使用蓝色表示dif线


#在macdsubplot子图中绘制dea曲线
def draw_dea(deasubplot,quote):
    x = []
    y = []
    for i in range(len(quote.dayinfo)):
        x.append(i)
        y.append(quote.dayinfo[i]['dea'])

    # xnew = np.linspace(min(x), max(x), 300)  # 在最小值和最大值之间建立300个插值点
    # ynew = spline(x, y, xnew)
    plot1=deasubplot.plot(x,y,'-',c='#ed36da',label='dea',linewidth=0.5)  #使用紫色表示des线

#在ksubplot子图中绘制ma5曲线
def draw_ma5(ma5subplot,quote):
    x = []
    y = []
    for i in range(len(quote.dayinfo)):
        x.append(i)
        y.append(quote.dayinfo[i]['ma5'])

    plot1=ma5subplot.plot(x,y,'-',c='black',label='ma5',linewidth=0.5)  #黑色表示ma5线


#在ksubplot子图中绘制ma10曲线
def draw_ma10(ma10subplot,quote):
    x = []
    y = []
    for i in range(len(quote.dayinfo)):
        x.append(i)
        y.append(quote.dayinfo[i]['ma10'])

    plot1=ma10subplot.plot(x,y,'-',c='b',label='ma10',linewidth=0.5)  #蓝色表示ma10线

#在ksubplot子图中绘制ma20曲线
def draw_ma20(ma20subplot,quote):
    x = []
    y = []
    for i in range(len(quote.dayinfo)):
        x.append(i)
        y.append(quote.dayinfo[i]['ma20'])

    plot1=ma20subplot.plot(x,y,'-',c='g',label='ma20',linewidth=0.5)  #绿色表示ma20线


#在ksubplot子图中绘制ma30曲线
def draw_ma30(ma30subplot,quote):
    x = []
    y = []
    for i in range(len(quote.dayinfo)):
        x.append(i)
        y.append(quote.dayinfo[i]['ma30'])

    plot1=ma30subplot.plot(x,y,'-',c='m',label='ma30',linewidth=0.5)  #洋红色表示ma30线

#在kdj子图中绘制k线
def draw_kdj_k(kdjsubplot,quote):
    x = []
    y = []
    for i in range(len(quote.dayinfo)):
        x.append(i)
        y.append(quote.dayinfo[i]['KDJ_K'])

    plot1=kdjsubplot.plot(x,y,'-',c='b',label='KDJ_K',linewidth=0.5)  #使用蓝色表示dif线

#在kdj子图中绘制d线
def draw_kdj_d(kdjsubplot,quote):
    x = []
    y = []
    for i in range(len(quote.dayinfo)):
        x.append(i)
        y.append(quote.dayinfo[i]['KDJ_D'])

    plot1=kdjsubplot.plot(x,y,'-',c='g',label='KDJ_D',linewidth=0.5)  #使用蓝色表示dif线

#在kdj子图中绘制j线
def draw_kdj_j(kdjsubplot,quote):
    x = []
    y = []
    for i in range(len(quote.dayinfo)):
        x.append(i)
        y.append(quote.dayinfo[i]['KDJ_J'])

    plot1=kdjsubplot.plot(x,y,'-',c='r',label='KDJ_J',linewidth=0.5)  #使用蓝色表示dif线


# #=================================K线图================================
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
from matplotlib.finance import candlestick_ohlc
from matplotlib.pylab import date2num
import datetime
from matplotlib.patches import Rectangle
def draw_k(ksubplot,quote):
    ksubplot = plt.gca()
    for i in range(len(quote.dayinfo)):
        oneday = quote.dayinfo[i]
        #如果开盘价更高，绘制绿色，粗柱
        if(oneday['open']>oneday['close']):

            rect = Rectangle((i-0.3,oneday['close']),0.6,oneday['open']-oneday['close'],color='g')
            ksubplot.add_patch(rect)
            rect1 = Rectangle((i-0.05, oneday['low']), 0.1, oneday['high'] - oneday['low'],color='g')
            ksubplot.add_patch(rect1)

        # 如果收盘价更高，绘制红色，粗柱
        if (oneday['open'] <= oneday['close']):  # 如果开盘价更高
            rect = Rectangle((i-0.3, oneday['open']), 0.6, oneday['close'] - oneday['open'],color='r')
            ksubplot.add_patch(rect)
            rect1 = Rectangle((i-0.05, oneday['low']), 0.1,oneday['high'] - oneday['low'], color='r')
            ksubplot.add_patch(rect1)

    ksubplot.figure.canvas.draw()
    pass




