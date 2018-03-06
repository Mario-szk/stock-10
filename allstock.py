# -- coding: utf-8 --
#获取所有股票的相关信息
import pandas as pd
import time,os,requests
import io
import datetime
import timeit
import json
import re
from io import StringIO
from multiprocessing.dummy import Pool as ThreadPool
from functools import partial
import stockinfo,day,option,kdj,mydraw
from urllib.request import urlretrieve  #from urllib.request import urlretrieve



# 下载所有的股票编号，返回字典数组，每个元素都是股票编号字典
def load_all_quote_symbol():
    print("开始下载所有的股票符号..." + "\n")

    #如果本地有所有股票的编号信息，就先不要采集，这个采集需要消耗6秒钟左右，浪费时间
    if(os.path.exists('all_quote_symbol.json')):
        f = io.open('all_quote_symbol.json', 'r', encoding='gbk')
        json_str = f.readline()
        all_quotes_data = json.loads(json_str)
        all_quotes = []
        for quote in all_quotes_data:
            stock = stockinfo.Stock(quote['code'], quote['address'], quote['name'])  # 将字典转化为对象
            all_quotes.append(stock)
        return all_quotes

    start = timeit.default_timer()

    all_quotes = []

    all_quotes.append(stockinfo.sh000001)  #将大盘添加到最前面
    all_quotes.append(stockinfo.sz399001)  #将大盘添加到最前面
    all_quotes.append(stockinfo.sh000300)  #将大盘添加到最前面
    ## all_quotes.append(stockinfo.sz399005) #将大盘添加到最前面
    ## all_quotes.append(stockinfo.sz399006) #将大盘添加到最前面

    try:
        count = 1
        while (count < 100):   #这里测试一部分股票
            para_val = '[["hq","hs_a","",0,' + str(count) + ',500]]'
            r_params = {'__s': para_val}
            all_quotes_url = 'http://money.finance.sina.com.cn/d/api/openapi_proxy.php'
            r = requests.get(all_quotes_url, params=r_params)  #根据网址下载所有的股票编号，这里使用的是新浪网址，有很多网址可以下载股票编号

            if(len(r.json()[0]['items']) == 0):  #响应返回的是一个数组，自己打开网址一看便懂
                break
            for item in r.json()[0]['items']:
                # item[0]  #股票编号：sh000001  item[1]  #股票码：000001   item[2]  #股票名称：上证指数
                all_quotes.append(stockinfo.Stock(item[1],item[0][0:2],item[2]))
            count += 1
    except Exception as e:
        print("Error: 下载股票编号失败..." + "\n")
        print(e)

    print("下载所有的股票编号完成... time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")
    #将所有股票符号写入文件，以便下次读取
    f = io.open('all_quote_symbol.json', 'w', encoding='gbk')  # 使用指定的字符编码写入文件
    all_quotes_temp = []
    for quote in all_quotes:
        all_quotes_temp.append(quote.to_dict())  # 如果是类，就要先转化为字典
    json.dump(all_quotes_temp, f, ensure_ascii=False)

    return all_quotes





# 根据股票编号，下载所有的股票图片
def load_all_quote_img(all_quotes,dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)
    index=1
    for quote in all_quotes:
        try:
            print('下载'+quote.name+"图片")
            mydraw.divide_draw(quote,index,dirpath)
            index=index+1
            # day.day_img_macd(quote,dirpath)
        except:
            print('下载图片出错了')




#根据股票编号，下载所有的股票数据
def load_all_quote_data(all_quotes, start_date, end_date):
    print("开始下载所有股票数据..." + "\n")

    start = timeit.default_timer()

    mapfunc = partial(day.day_data, start_date=start_date, end_date=end_date,fuquan='before')  #创建映射函数
    pool = ThreadPool(option.thread)  # 开辟包含指定数目线程的线程池
    pool.map(mapfunc, all_quotes)   # 多线程执行下载工作
    pool.close()
    pool.join()

    print("下载所有的股票数据完成... time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")
    return all_quotes


#股票数据处理：获取股票类型和KDJ指数
def data_process(all_quotes):
    print("开始处理所有的股票..." + "\n")

    kdjobject = kdj.KDJ()
    start = timeit.default_timer()


    ## 计算KDJ指数
    for quote in all_quotes:
        if(len(quote.dayinfo)!=0):
            try:
                kdjobject.getKDJ(quote.dayinfo)  #计算股票的KDJ指数
            except KeyError as e:
                print("Key Error")
                print(e)
                print(quote)

    print("所有的股票处理结束... time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")




#根据选股策略，选择股票
def quote_pick(all_quotes, buy_date_temp):
    print(buy_date_temp+"选股启动..." + "\n")
    start = timeit.default_timer()
    results = []
    for quote in all_quotes:
        if(quote.value_check(buy_date_temp)):
            results.append(quote)

    print("选股"+str(len(results))+"完成... time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")
    # print(str(data_issue_count) + " 个股票目标时间没有数据...\n")

    return results

#校验日期，检测date时间是否是有效的买入时间。非工作时间不能买入
def check_date(all_quotes, buy_date):
    is_date_valid = False
    for quote in all_quotes:
        if(quote.symbol == stockinfo.sh000001.symbol):  #选取大盘数据，是因为大盘数据绝对会有数据，这就要求你爬虫时一定要把大盘数据获取下来
            for quote_data in quote.dayinfo:  #获取大盘指数每一天的数据行情
                if(quote_data['time'] == buy_date):   #爬虫的股票数据中的时间和将要测试的时间要相同
                    is_date_valid = True
                    return is_date_valid
    if not is_date_valid:
        print(buy_date + " 日期不存在数据...\n")
    return is_date_valid

#比较两个价格的变化率
def get_profit_rate(price1, price2):
    if(price1 == 0):
        return None
    else:
        return round((price2-price1)/price1, 5)


#把根据选股策略选择的股票，在买入后一定时间范围内进行利率计算
def profit_test(selected_quotes,buy_date,sell_date_range):
    print("启动股票策略测试..." + "\n")

    start = timeit.default_timer()

    results = []
    INDEX = None  #沪深300股票
    INDEX_idx = 0  #股票目标日期的数据在日k线中的索引

    for quote in selected_quotes:   #遍历每只选中的股票，找到沪深300指定日期的股票数据，为在计算利率时要把大盘影响去掉
        if(quote.symbol == stockinfo.sh000300.symbol):  #如果是沪深300
            INDEX = quote
            for idx, quote_data in enumerate(quote.dayinfo):  #迭代股票每一天的数据，为了找到指定日期的数据
                if(quote_data['time'] == buy_date):
                    INDEX_idx = idx
            break

    for quote in selected_quotes:
        buy_date_idx = None

        if(quote in stockinfo.index_array):  #去除大盘股票
            continue

        #获取指定时间在股票数据中的索引，去除不包含指定日期的股票，这么没必要，因为在选取的时候就是按照包含指定日期选取的
        for idx, quote_data in enumerate(quote.dayinfo):  #迭代股票每一天的数据
            if(quote_data['time'] == buy_date):
                buy_date_idx = idx
        if(buy_date_idx is None):
            print(quote.name + " 的股票数据不可处理..." + "\n")
            continue

        test_stock = {}
        test_stock['Name'] = quote.name #股票名称
        test_stock['Symbol'] = quote.symbol  #股票编号
        test_stock['Method'] = quote.method  #选股策略
        test_stock['Type'] = quote.type #股票类型：创业板，中小板，主板
        if('KDJ_K' in quote.dayinfo[buy_date_idx]):
            test_stock['KDJ_K'] = quote.dayinfo[buy_date_idx]['KDJ_K']  #kdj指数
            test_stock['KDJ_D'] = quote.dayinfo[buy_date_idx]['KDJ_D']  #kdj指数
            test_stock['KDJ_J'] = quote.dayinfo[buy_date_idx]['KDJ_J']  #kdj指数
        test_stock['Close'] = quote.dayinfo[buy_date_idx]['close']  #收盘价
        test_stock['Change'] = quote.dayinfo[buy_date_idx]['percent'] #变化率
        test_stock['vol_change'] = quote.dayinfo[buy_date_idx]['vol_change'] #成交量变化率
        test_stock['MA_5'] = quote.dayinfo[buy_date_idx]['ma5'] #5日均值
        test_stock['MA_10'] = quote.dayinfo[buy_date_idx]['ma10'] #10日均值
        test_stock['MA_20'] = quote.dayinfo[buy_date_idx]['ma20'] #20日均值
        test_stock['MA_30'] = quote.dayinfo[buy_date_idx]['ma30'] #30日均值
        test_stock['Data'] = [{}]

        for i in range(1,sell_date_range):
            if(buy_date_idx+i >= len(quote.dayinfo)):  #如果预测日期超出数据范围，则结束
                print(quote.name + " 的数据在 "+buy_date+"后" + str(i) + " 天的测试存在问题..." + "\n")
                break

            day2day_profit = get_profit_rate(quote.dayinfo[buy_date_idx]['close'], quote.dayinfo[buy_date_idx+i]['close'])  #获取多日股价变化率
            test_stock['Data'][0]['Day_' + str(i) + '_Profit'] = day2day_profit  #记录股价变化率数据
            if(INDEX_idx+i < len(INDEX.dayinfo)):
                day2day_INDEX_change = get_profit_rate(INDEX.dayinfo[INDEX_idx]['close'], INDEX.dayinfo[INDEX_idx+i]['close'])
                test_stock['Data'][0]['Day_' + str(i) + '_INDEX_Change'] = day2day_INDEX_change
                test_stock['Data'][0]['Day_' + str(i) + '_Differ'] = day2day_profit-day2day_INDEX_change

        results.append(test_stock)

    print("选股测试完成... time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")
    return results

# 将所有股票加入同花顺自选
def addchoose(allstock):
    s = requests.Session()
    headers = {
        'Host': 'stock.10jqka.com.cn',
        'Referer': 'http://t.10jqka.com.cn/newcircle/user/userPersonal/?from=circle',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'
    }
    s.headers.update(headers)  # 更新header

    cookie = {
        'spversion': '20130314',
        ' Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1': '1512137723,1512189809',
        ' historystock': '300199%7C*%7C002174%7C*%7C1A0001',
        ' user': 'MDo4MjU0ODU2OTc6Ok5vbmU6NTAwOjE0MTEyNjg4Mjo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA6Mjc6OjoxMzExMjY4ODI6MTUxNDE5Nzc1OTo6OjEzMzY2MTU4MDA6NjA0ODAwOjA6MThjODhkYzNhYzI1NWE1YTQxZDllNzQxN2YyMWI0ZWIyOmRlZmF1bHRfMjow',
        ' userid': '131126882',
        ' u_name': '825485697',
        ' escapename': '825485697',
        ' ticket': '133267cc1eac58cd0f0d4812c8551220',
        ' v': 'Ap2qNtsCm3yFiX9QHP0BPcForHKxutQG2_s14F9T3WcjirPuJwrh3Gs-RfHv'
    }

    for stock in allstock:
        url = 'http://stock.10jqka.com.cn/self.php?stockcode=' + stock.code + '&op=add&&jsonp=jQuery111006127251748077938_1514197785114&_=1514197785134'  # 请求地址是变化的
        r = s.get(url=url, cookies=cookie)
        print(r.text)