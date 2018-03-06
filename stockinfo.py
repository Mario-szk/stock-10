#coding:utf-8

#定义股票信息类
import math


# 流动市值：当时可交易股票数*股价
#总市值：所有股票数*股价


#股票自定义类
class Stock():

    # code=''  #股票编码000001
    # address = ''  #股票上市地址  sh上海股票   sz深圳股票
    # symbol = '' #address+code
    # name = ""  #股票名称，上证指数
    # type=''  #股票类型:创业板、主板
    # dayinfo=[]  #日k数据
    # method=''  #选股策略名称
    #基本构造函数
    def __init__(self,code,address,name,type='',dayinfo=[],method=''):
        self.code = code
        self.address = address
        self.symbol = address+code
        self.name = name
        self.type = type
        self.dayinfo = dayinfo
        self.method = method
        # 划分股票类别
        if (code.startswith('300')):
            self.type = '创业板'
        elif (code.startswith('002')):
            self.type = '中小板'
        else:
            self.type = '主板'

    #将类转化为字典
    def to_dict(self):
        StockDict={}
        StockDict['code'] = self.code
        StockDict['address'] = self.address
        StockDict['name'] = self.name
        StockDict['type'] = self.type
        StockDict['method'] = self.method
        StockDict['dayinfo'] = self.dayinfo
        return StockDict


    #获取股票某一数据的最大值，和最大值处的索引
    def par_max(self,data_par):
        maxvalue=float("-inf")
        maxindex = -1  # 最大值所在是索引处
        for index, oneday in enumerate(self.dayinfo):
            if oneday[data_par]>maxvalue:
                maxvalue=oneday[data_par]
                maxindex = index
        return maxvalue,maxindex

    # 获取股票某一数据的最小值，和最小值处的索引
    def par_min(self, data_par):
        minvalue = float("inf")   #最小值
        minindex = -1    #最小值所在是索引处
        for index,oneday in enumerate(self.dayinfo):
            if oneday[data_par] < minvalue:
                minvalue = oneday[data_par]
                minindex = index
        return minvalue,minindex


    #是否选择该股票
    def value_check(self,buy_date):  #计算指定日期是否应该买入
        if(len(self.dayinfo)==0):  #如果数据为空则返回不买
            return False
        if (self.symbol in index_array):  # 如果是大盘数据，自动选中或不选中
            return False

        #获取指定时间再日K中的索引，为了选股策略使用，同时校验指定时间是否有股票数据，若没有，则当天不买入
        buy_date_idx = None  # 目标时间再日K线数组中的索引
        for idx, quote_data in enumerate(self.dayinfo):  #迭代遍历股票的数据
            if(quote_data['time'] == buy_date):  #首先判断股票是否包含目标时间的数据
                buy_date_idx = idx
        if(buy_date_idx is None):  #如果股票不包含目标时间数据，就错过该股票
            return False

        #选股策略1，macd两三个月的中长线炒股
        try:
            # mindif =self.par_min('dif')  #获取dif的最小值，要使一次检查发生在1/3-1/2的位置，二次金叉发生在0-1/5
            # if self.dayinfo[buy_date_idx]['dea']<=self.dayinfo[buy_date_idx]['dif']<=0:
            #     if self.dayinfo[buy_date_idx - 10]['dif']<self.dayinfo[buy_date_idx - 10]['dea']<self.dayinfo[buy_date_idx]['dea']*2:
            #         return True

            #上扬的线下金叉
            # if self.dayinfo[buy_date_idx-4]['dif']<=self.dayinfo[buy_date_idx-4]['dea']<self.dayinfo[buy_date_idx]['dea']<=self.dayinfo[buy_date_idx]['dif']<0:
            #     return True

            #0轴下15天内有大于10天在上扬的买入
            deanum=0
            difnum=0
            daynum=25
            upzero=0
            downzero=0
            totolnum = len(self.dayinfo)

            #macd慢线连续上涨,且即将线上金叉
            for i in range(daynum):
                if self.dayinfo[totolnum-2-i]['dea']<self.dayinfo[totolnum-1-i]['dea']:
                    deanum+=1
                if self.dayinfo[totolnum-1-i]['dea']>0:
                    upzero+=1
            if deanum>15 and 0<upzero<5 and self.dayinfo[totolnum-1]['dif']<self.dayinfo[totolnum-1]['dea']:
                return True


            #0上金叉
            # for i in range(3):
            #     if self.dayinfo[totolnum-2-i]['macd']<self.dayinfo[totolnum-1-i]['macd']:   #macd连续上涨
            #         deanum+=1
            #     if self.dayinfo[totolnum-1-i]['dea']>0 and self.dayinfo[totolnum-1-i]['dea']>self.dayinfo[totolnum-1-i]['dif']:
            #         upzero+=1
            # if deanum==3 and upzero==3:
            #     return True




            #金针探顶，只要近15天出现了最低值就选中
            # mincloase,minindex = self.par_min('close')
            # if len(self.dayinfo)-3>minindex>len(self.dayinfo)-7:
            #     return True


            # #夹角增大，连续跳空
            # for i in range(3):
            #     if (self.dayinfo[totolnum-1-i]['dif']-self.dayinfo[totolnum-2-i]['dif'])> (self.dayinfo[totolnum-1-i]['dea']-self.dayinfo[totolnum-2-i]['dea']): #夹角增大
            #         if self.dayinfo[totolnum-1-i]['dif']>=self.dayinfo[totolnum-1-i]['dea']:    #金叉后夹角
            #             if self.dayinfo[totolnum-1-i]['open']>=self.dayinfo[totolnum-2-i]['close']:  #跳空
            #                 # if self.dayinfo[totolnum - 1 - i]['close'] >= self.dayinfo[totolnum - 1 - i]['open']:  # 连续上涨
            #                     deanum+=1
            #     if deanum==3:
            #         return True

            # dea刚抬头，绿柱收缩块
            # for i in range(5):
            #     if self.dayinfo[totolnum-1-i]['dea']>=self.dayinfo[totolnum-2-i]['dea']:
            #         deanum += 1
            #     if 0>=self.dayinfo[totolnum-1-i]['macd']>self.dayinfo[totolnum-2-i]['macd']:
            #         downzero+=1
            #
            #     if 3>=deanum>1 and 5>=downzero>=3:
            #         return True


        except:
            pass

        # 选股策略2，根据kdj，一周内短期炒股
        # try:
        #     if(self.dayinfo[buy_date_idx-2]['KDJ_J']<20):
        #         if self.dayinfo[buy_date_idx-1]['KDJ_J']<20:
        #             if self.dayinfo[buy_date_idx - 0]['KDJ_J']-self.dayinfo[buy_date_idx-1]['KDJ_J']>40:
        #                 return True
        # except:
        #     pass

        return False



#大盘指数
sh000001 =Stock('000001','sh','上证指数')
sz399001 =Stock('399001','sz','深证成指')
sh000300 =Stock('000300','sh','沪深300')
sz399005 =Stock('399005','sz','中小板指')
sz399006 =Stock('399006','sz','创业板指')
index_array=['sh000001','sz399001','sh000300','sz399005','sz399006']

