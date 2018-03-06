#coding:utf-8

#爬虫参数配置
import datetime


#获取偏移指定天数的时间表达式
def get_date_str(offset):
    if(offset is None):
        offset = 0
    date_str = (datetime.datetime.today() + datetime.timedelta(days=offset)).strftime("%Y%m%d")
    return date_str



reload_data = 'Y'                      # --reload {Y,N}              是否重新抓取股票数据，默认值：Y
load_img = 'N'                         # --load_img {Y,N}           是否下载日K线曲线图，默认值：N
gen_portfolio = 'N'                    # --portfolio {Y,N}           是否生成选股测试结果，默认值：N
output_type = 'json'                   # --output {json,csv,all}     输出文件格式，默认值：json
charset = 'utf-8'                      # --charset {utf-8,gbk}       输出文件编码，默认值：utf-8
start_date = get_date_str(-180)          # --startdate yyyy-MM-dd      抓取数据的开始日期，默认值：当前系统日期-90天
end_date = get_date_str(None)          # --enddate yyyy-MM-dd        抓取数据的结束日期，默认值：当前系统日期
buy_date = get_date_str(None)       # --targetdate yyyy-MM-dd        买入初始日期，默认值：当前系统日期
buy_date_range = 60                    # --testrange NUM             买入日期范围天数，默认值：50
sell_date_range = 60                    # --testrange NUM             卖出日期范围天数，默认值：50
store_path = 'stockholm_export'      # --storepath PATH            输出文件路径，默认值：stockholm_export
file_name='allstock'
thread = 10                            # --thread NUM                线程数，默认值：10

