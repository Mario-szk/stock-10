# -- coding: utf-8 --
#获取一支股票的全部数据，
import pandas as pd
import time,os, requests
import datetime
import json
from io import StringIO
import stockinfo,mydraw
from urllib.request import urlretrieve  #from urllib.request import urlretrieve

#获取指定股票的日K线图、macd
def day_img_macd(stock,dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    urlretrieve("http://image.sinajs.cn/newchart/daily/macd/"+stock.symbol+".gif", dirpath+'/'+stock.symbol+".gif")
    print('成功下载macd图片'+stock.name)


#获取指定股票的日K线图、kdj
def day_img_kdj(stock,dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    urlretrieve("http://image.sinajs.cn/newchart/daily/kdj/"+stock.symbol+".gif", dirpath+'/'+stock.symbol+".gif")
    print('成功下载kdj图片'+stock.name)

#获取指定股票的日K线图、rsi
def day_img_rsi(stock,dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    urlretrieve("http://image.sinajs.cn/newchart/daily/rsi/"+stock.symbol+".gif", dirpath+'/'+stock.symbol+".gif")
    print('成功下载kdj图片'+stock.name)

#获取指定股票的日K线图、boll
def day_img_boll(stock,dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    urlretrieve("http://image.sinajs.cn/newchart/daily/boll/"+stock.symbol+".gif", dirpath+'/'+stock.symbol+".gif")
    print('成功下载kdj图片'+stock.name)

#获取指定股票的日K线图、wr
def day_img_wr(stock,dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    urlretrieve("http://image.sinajs.cn/newchart/daily/wr/"+stock.symbol+".gif", dirpath+'/'+stock.symbol+".gif")
    print('成功下载kdj图片'+stock.name)

#获取指定股票的日K线图、DMI
def day_img_dmi(stock,dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    urlretrieve("http://image.sinajs.cn/newchart/daily/dmi/"+stock.symbol+".gif", dirpath+'/'+stock.symbol+".gif")
    print('成功下载kdj图片'+stock.name)



#获取指定股票日K线的所有数据
def day_data(stock, start_date, end_date, fuquan):  #参数：股票编码，开始时间，结束时间，是否复权
    # 将时间字符串转换为时间戳字符串
    def time_transfer_timeStamp(time_str):  #参数：时间字符串2017-05-20 00:00:00格式的
        timeArray = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")  #时间字符串转化为时间
        timeStamp = int(time.mktime(timeArray))  #时间转化为时间戳
        return str(timeStamp)  #时间戳转化为字符串

    def time_transfer_string(time_str):  #截取部分时间格式
        data = time.mktime(time.strptime(time_str, "%a %b %d %H:%M:%S +0800 %Y"))
        return str(datetime.fromtimestamp(data))[0:10]

    #从雪球获取股票json数据：
    def get_xueqiu(stock, start_date, end_date, fuquan):  #参数：股票编号，开始时间字符串、结束时间字符串、是否复权
        header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                  'Accept-Encoding': 'gzip, deflate, sdch',
                  'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,ja;q=0.2',
                  'Cache-Control': 'max-age=0',
                  'Connection': 'keep-alive',
                  'DNT': '1',
                  'Host': 'xueqiu.com',
                  'Referer': 'https://www.baidu.com/link?url=CQu5rGbzI_vt0fSj3b12LTyZgWvzjrK9f3L_GLIBqum&wd=&eqid=88e8a3ca0001535b00000005572edf29',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
                  }
        proxies = {"http": "http://10.10.1.10:3128", "https": "http://10.10.1.10:1080", }   #代理 http://www.xicidaili.com/

        start_time_tmp = start_date[0:4] + '-' + start_date[4:6] + '-' + start_date[6:] + ' 00:00:00'  #将开始时间字符串转化为规定的格式  20170520转化为2017-05-20 00:00:00
        end_time_tmp = end_date[0:4] + '-' + end_date[4:6] + '-' + end_date[6:] + ' 15:30:00'  #将结束时间字符串转化为规定的格式  20170520转化为2017-05-20 15:30:00

        if stock.address == 'sh':
            daima_new = 'SH' + stock.code  #对股票编码进行处理
        else:
            daima_new = 'SZ' + stock.code   #对股票编码进行处理
        s = requests.session()
        t = s.get('https://xueqiu.com/', headers=header)  #要先访问一遍

        start_time = time_transfer_timeStamp(start_time_tmp)  + '000' #将开始时间字符串转化为时间戳字符串，+'000'因为雪球网的时间戳以ms为单位，
        end_time = time_transfer_timeStamp(end_time_tmp) + '000'  #  #将结束时间字符串转化为时间戳字符串，+'000'因为雪球网的时间戳以ms为单位，
        #雪球网需要的参数：
        requrl = 'https://xueqiu.com/stock/forchartk/stocklist.json?symbol=' + daima_new + '&period=1day&type=' + fuquan +'&begin=' + start_time + '&end=' + end_time + '&_=' + end_time
        # print(requrl)
        r = s.get(requrl,headers=header)   #,proxies=proxies

        result = json.loads(r.content)  #返回的是json字符串，转化为对象
        dayinfo=[]
        if(result['success']=='true'):
            dayinfo = result['chartlist']
            volume_init=1   #初始成交量
            for oneday in dayinfo:  #从头到尾一次迭代
                timeArray = time.localtime(oneday['timestamp']/1000)  #先将时间戳转化为时间
                oneday['time'] = time.strftime("%Y%m%d", timeArray)  #再将时间转化为字符串
                oneday['vol_change'] = (oneday['volume']-volume_init)/volume_init  #计算成交量变化率
                volume_init = oneday['volume']  #将当前成交量赋值给临时数据
        return dayinfo

    #从网易获取股票csv数据：日期	股票代码	名称	收盘价	最高价	最低价	开盘价	前收盘	涨跌额	涨跌幅	换手率	成交量	成交金额	总市值	流通市值
    def get_wangyi(stock, start_date, end_date):
        #股票编码预处理
        if stock.address == 'sh':
            code_new = '0' + stock.code  #上海股票，编码前加0
        else:
            code_new = '1' + stock.code   #深圳股票，编码前加1

        url = 'http://quotes.money.163.com/service/chddata.html?code=' + code_new + '&start=' + start_date + '&end=' + end_date + '&fields=TCLOSE;HIGH;LOW;TOPEN;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
        # print(url)
        condition = True
        while condition:
            try:
                r = requests.get(url, timeout=10)  #秩序请求，直到请求成功
                condition = False
            except Exception as e:
                print(e)
                pass
        #请求下来的直接就是csv文件，所以直接读取csv文件，返回的每列：时间、编码、名称+请求的每列
        backstr = r.content.decode("gbk")  # 先将字节数组，转化为字符串
        a1 = pd.read_csv(StringIO(backstr), skiprows=[0],  #参数必须为unicode字符串
                         names = ['shijian', 'daima', 'name', 'close', 'high', 'low', 'open', 'percent', 'turnrate', 'volume','amount', 'zongshizhi', 'liutongshizhi'])
        if a1.empty:
            return None
        else:
            a2 = a1[a1['volume'] != 0].sort_index(axis=0, ascending=False)  #第一列增长排序，因为默认是降序的
            dayinfo=[]
            for i in range(0,len(a2)):
                oneday={}
                oneday['time'] = a2.ix[i,0].replace('-','')  #时间,2017-02-15转化为20170215
                oneday['close'] = a2.ix[i,3]   #收盘价
                oneday['high'] = a2.ix[i,4]   #最高价
                oneday['low'] = a2.ix[i,5]   #最低价
                oneday['open'] = a2.ix[i,6]   #开盘价
                oneday['percent'] = a2.ix[i,7]  # 涨跌比例
                oneday['turnrate'] = a2.ix[i,8]  # 换手率
                oneday['volume'] = a2.ix[i,9]   #成交量
                oneday['amount'] = a2.ix[i,10]  #成交金额
                oneday['zongshizhi'] = a2.ix[i,11]  #总市值
                oneday['liutongshizhi'] = a2.ix[i,12]  #流通市值

                dayinfo.append(oneday)

            return dayinfo
    #从腾讯接收获取数据，现在还不能指定起止时间只能获取100天的数据
    def get_tengxun(stock):
        dayinfo = []
        # 直接从腾讯的js接口中读取
        if (stock is not None and stock.code is not None):
            try:
                url = 'http://data.gtimg.cn/flashdata/hushen/latest/daily/' + stock.address+stock.code+ '.js'  # 腾讯的日k线数据
                r = requests.get(url)  # 向指定网址请求，下载股票数据
                alldaytemp = r.text.split("\\n\\")[2:]  # 根据返回的字符串进行处理提取出股票数据的数组形式

                for day in alldaytemp:
                    if (len(day) < 10):  # 去掉一些不对的数据，这里去除方法比较笼统.
                        continue
                    oneday = day.strip().split(' ')  # 获取日K线的数据。strip为了去除首部的\n，' '来分割数组，分割出来的数据分别是日期、开盘、收盘、最高、最低、成交量
                    onedayquote = {}
                    onedayquote['time'] = "20" + oneday[0]  # 腾讯股票数据中时间没有20170513中的20，所以这里加上，方便后面比较
                    onedayquote['open'] = oneday[1]  # 开盘
                    onedayquote['close'] = oneday[2]  # 收盘
                    onedayquote['high'] = oneday[3]  # 最高
                    onedayquote['low'] = oneday[4]  # 最低
                    onedayquote['volume'] = oneday[5]  # 成交量
                    dayinfo.append(onedayquote)
            except:
                print("Error: 加载指定股票的数据失败... " +  stock.address+stock.code + "/" +  stock.name+ "\n")

            print("下载指定股票 " + stock.address+stock.code + "/" + stock.name + " 完成..." + "\n")
        return dayinfo


    #组合股票数据
    def zuhe():
        df_xueqiu = get_xueqiu(stock, start_date, end_date,fuquan)
        # df_wangyi = get_wangyi(stock, start_date, end_date)
        # df_tengxun = get_tengxun(stock)
        return df_xueqiu

    try:
        stock.dayinfo = zuhe()  # 修改股票数据
    except:
        try:
            time.sleep(5)  # 速度太快，服务器会拒绝回应，所以休息重试
            stock.dayinfo = zuhe()  # 修改股票数据
        except Exception as e:
            print(e)
            pass
    print(stock.name)
    time.sleep(1)  #速度太快，服务器会拒绝回应

# stock = stockinfo.Stock('600756','sh','浪潮软件')
# day_data(stock,'20170612','20171110','before')
#
# mydraw.divide_draw(stock,1)



