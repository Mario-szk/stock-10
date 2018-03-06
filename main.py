#coding:utf-8

# 一个股票数据（沪深）爬虫和选股策略测试框架，数据基于雅虎YQL和新浪财经。
# 根据选定的日期范围抓取所有沪深两市股票的行情数据。
# 根据指定的选股策略和指定的日期进行选股测试。
# 计算选股测试实际结果（包括与沪深300指数比较）。
# 保存数据到JSON文件、CSV文件。
# 支持使用表达式定义选股策略。
# 支持多线程处理。

import os,datetime,shutil
import allstock,day,myfile,option,kdj,stockinfo



def checkFoldPermission(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            txt = open(path + os.sep + "test.txt","w")
            txt.write("test")
            txt.close()
            os.remove(path + os.sep + "test.txt")

    except Exception as e:
        print(e)
        return False
    return True

#下载数据
def data_load(start_date, end_date, output_types):
    all_quotes = allstock.load_all_quote_symbol()  #下载所有的股票符号
    print("共 " + str(len(all_quotes)) + " 股票符号下载完成..." + "\n")
    allstock.load_all_quote_data(all_quotes, start_date, end_date)  #下载所有的股票数据
    allstock.data_process(all_quotes)  #数据处理，获取kdj指数
    myfile.data_export(all_quotes, output_types, option.store_path,option.file_name,option.charset)  #数据导出



#量化交易。根据选股策略，在买入时间范围内，选择股票，在买入后的卖出时间范围内，计算每日利率
def data_test(buy_date, buy_date_range, output_types):

    all_quotes = myfile.file_data_load(option.store_path,option.file_name,option.charset)   #从文件中加载股票数据

    target_date_time = datetime.datetime.strptime(buy_date, "%Y%m%d") #将初始化买入时间字符串转化为时间对象
    for i in range(buy_date_range):
        buy_date_temp = (target_date_time - datetime.timedelta(days=i)).strftime("%Y%m%d")  #将过去时间字符串转换为指定时间格式
        is_date_valid = allstock.check_date(all_quotes, buy_date_temp)  #校验买入时间是否有效，非工作日不能买入
        if is_date_valid:
            selected_quotes = allstock.quote_pick(all_quotes, buy_date_temp)  #根据选策略选取股票
            res = allstock.profit_test(selected_quotes, buy_date_temp,option.sell_date_range)  #计算股票利率
            myfile.data_export(res, output_types, option.store_path,'result_' + buy_date_temp,option.charset)  #测试结果导出


#挑选近期可买入股票
def choose_stock(buy_date, buy_date_range, output_types):

    all_quotes = myfile.file_data_load(option.store_path,option.file_name,option.charset)   #从文件中加载股票数据
    if os.path.exists('choose_stock'):
        shutil.rmtree('choose_stock')  #删除非空文件夹
    buy_date_time = datetime.datetime.strptime(buy_date, "%Y%m%d") #将初始化买入时间字符串转化为时间对象
    allchoose_stock=[]
    for i in range(buy_date_range):
        buy_date_temp = (buy_date_time - datetime.timedelta(days=i)).strftime("%Y%m%d")  #将过去时间字符串转换为指定时间格式
        is_date_valid = allstock.check_date(all_quotes, buy_date_temp)  #校验买入时间是否有效，非工作日不能买入
        if is_date_valid:
            selected_quotes = allstock.quote_pick(all_quotes, buy_date_temp)  #根据选策略选取股票
            for stock in selected_quotes:
                if stock not in allchoose_stock:
                    allchoose_stock.append(stock)

    # allstock.addchoose(allchoose_stock)  # 将选中的股票加入同花顺自选股
    allstock.load_all_quote_img(allchoose_stock,'choose_stock')  #下载图片查看是否正确



def main():
    if not checkFoldPermission(option.store_path):  #检测是否具有读写存储文件的权限
        print('\n没有文件读写权限: %s' % option.store_path)
    else:
        print('股票数据爬虫和预测启动...\n')
        ## 输出数据类型
        output_types = []
        if (option.output_type == "json"):
            output_types.append("json")
        elif (option.output_type == "csv"):
            output_types.append("csv")
        elif (option.output_type == "all"):
            output_types = ["json", "csv"]

        ## 根据选定的日期范围抓取所有沪深两市股票的行情数据。
        if (option.reload_data == 'Y'):
            print("开始下载股票数据...\n")
            data_load(option.start_date, option.end_date, output_types)

        # 选择股票，计算利率
        if (option.gen_portfolio == 'Y'):
            print("开始选股测试...\n")
            data_test(option.buy_date, option.buy_date_range, output_types)

        if (option.load_img == 'Y'):
            print("开始下载图片...\n")
            all_quotes = myfile.file_data_load(option.store_path, option.file_name, option.charset)  # 从文件中加载股票数据
            allstock.load_all_quote_img(all_quotes, 'allstock')  # 下载所有的股票图片

        #挑选近期可购进股票，并下载图片
        choose_stock(option.buy_date, 5, output_types)

        print('股票数据爬虫和预测完成...\n')



if __name__ == '__main__':
    main()