# -- coding: utf-8 --
#获取一支股票的全部数据，
import pandas as pd
import time,os, requests
import datetime
import json
from io import StringIO
import stockinfo
from urllib.request import urlretrieve  #from urllib.request import urlretrieve


#KDJ指数类
class KDJ():
    def _avg(self, array):
        length = len(array)
        return sum(array)/length

    def _getMA(self, values, window):
        array = []
        x = window
        while x <= len(values):
            curmb = 50
            if(x-window == 0):
                curmb = self._avg(values[x-window:x])
            else:
                curmb = (array[-1]*2+values[x-1])/3
            array.append(round(curmb,3))
            x += 1
        return array
    #先计算每日rsv=(收盘价-近9日最低价)/(近9日最高价-近9日最低价)*100%
    def _getRSV(self, arrays):
        rsv = []
        x = 9
        while x <= len(arrays):
            high = max(map(lambda x: x['high'], arrays[x-9:x]))
            low = min(map(lambda x: x['low'], arrays[x-9:x]))
            close = arrays[x-1]['close']
            rsv.append((close-low)/(high-low)*100)
            t = arrays[x-1]['time']
            x += 1
        return rsv

    #根据股票数据，计算KDJ指数。没有前日数据使用50代替
    #   K=2/3*前日K值+1/3*当日RSV
    #   D=2/3*前日D值+1/3*当日K值
    #   J=3*D一2*K
    def getKDJ(self, quote_data):
        if(len(quote_data) > 12):
            rsv = self._getRSV(quote_data)
            k = self._getMA(rsv,3)
            d = self._getMA(k,3)
            j = list(map(lambda x: round(3*x[0]-2*x[1],3), zip(k[2:], d)))

            for idx, data in enumerate(quote_data[0:12]):
                data['KDJ_K'] = None
                data['KDJ_D'] = None
                data['KDJ_J'] = None
            for idx, data in enumerate(quote_data[12:]):
                data['KDJ_K'] = k[2:][idx]
                data['KDJ_D'] = d[idx]
                if(j[idx] > 100):
                    data['KDJ_J'] = 100
                elif(j[idx] < 0):
                    data['KDJ_J'] = 0
                else:
                    data['KDJ_J'] = j[idx]

        return quote_data