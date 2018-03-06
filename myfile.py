# -- coding: utf-8 --
#获取一支股票的全部数据，
import os
import timeit
import io
import json
import csv
from io import StringIO
import stockinfo

#获取csv文件存储时，第一行的列名，参数quote为字典
def get_columns(quote):
    try:
        quote=quote.to_dict()   #如果是类就先转化为字典
    except:
        pass
    columns = []
    if(quote is not None):
        for key in quote.keys():
            if(key == 'dayinfo'):
                for data_key in quote['dayinfo'][-1]:
                    columns.append("dayinfo." + data_key)
            else:
                columns.append(key)
        columns.sort()
    return columns

# 数据导出
def data_export(all_quotes, export_type_array, export_folder,file_name,charset):
    print("开始导出" + str(len(all_quotes)) + "个股票数据")
    start = timeit.default_timer()
    directory = export_folder
    if (file_name is None):
        return
    if not os.path.exists(directory):  # 如果目录不存在
        os.makedirs(directory)  # 创建目录

    if (all_quotes is None or len(all_quotes) == 0):
        print("没有数据要导出...\n")
        return

    if ('json' in export_type_array):  # 如果导出类型中包含json，就导出json文件
        print("开始导出到json文件...\n")
        f = io.open(directory + '/' + file_name + '.json', 'w', encoding=charset)  # 使用指定的字符编码写入文件
        try:
            all_quotes_temp = []
            for quote in all_quotes:
                all_quotes_temp.append(quote.to_dict())  # 如果是类，就要先转化为字典
            json.dump(all_quotes_temp, f, ensure_ascii=False)
        except:
            json.dump(all_quotes, f, ensure_ascii=False)  # 如果本来就是字典，则可以直接使用

    if ('csv' in export_type_array):  # 如果导出类型中包含csv，就导出csv文件
        print("开始导出到csv文件...\n")
        columns = []
        if (all_quotes is not None and len(all_quotes) > 0):
            columns = get_columns(all_quotes[0])  # 获取csv文件第一行的列名
        writer = csv.writer(open(directory + '/' + file_name + '.csv', 'w', encoding=charset))  # 使用指定的字符编码写入文件
        writer.writerow(columns)  # 写入列头作为第一行

        for quote in all_quotes:  # 将数据一次写入每一行
            try:
                quote = quote.to_dict()  # 如果是类，就先转化为字典
            except:
                pass
            if (len(quote['dayinfo']) != 0):
                for oneday in quote['dayinfo']:  # oneday是一日数据的字典表示
                    try:
                        line = []
                        for column in columns:
                            if (column.find('dayinfo.') > -1):
                                if (column[8:] in oneday):  # 如果每日数据包含这个字段
                                    line.append(oneday[column[8:]])  # 将这个字段的取值加入到一行中
                            else:
                                line.append(quote[column])
                        writer.writerow(line)
                    except Exception as e:
                        print(e)
                        print("write csv error: " + quote['name'])

    print("导出数据完成.. time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")


#从json文件中读取数据（股票所有数据）
def file_data_load(export_folder,file_name,charset):
    print("开始从文件中加载数据..." + "\n")

    start = timeit.default_timer()
    directory = export_folder

    f = io.open(directory + '/' + file_name + '.json', 'r', encoding=charset)
    json_str = f.readline()
    all_quotes_data = json.loads(json_str)
    all_quotes = []
    for quote in all_quotes_data:
        stock = stockinfo.Stock(quote['code'], quote['address'], quote['name'], quote['type'], quote['dayinfo'],quote['method'])  # 将字典转化为对象
        all_quotes.append(stock)

    print("文件中数据加载" + str(len(all_quotes)) + "个股票完成... time cost: " + str(round(timeit.default_timer() - start)) + "s" + "\n")
    return all_quotes