import pandas as pd
from zipline import TradingAlgorithm
from zipline.api import order, sid,get_datetime
from zipline.data.loader import load_data
from zipline.api import order_target, record, symbol, history, add_history,symbol,set_commission,order_percent,set_long_only,get_open_orders
from zipline.finance.commission import OrderCost
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

input_data = load_data(
    stockList=['002057'],
    start="2015-11-04",
    end="2016-01-16"
)
def analyze(context=None, results=None):
    import matplotlib.pyplot as plt

    # Plot the portfolio and asset data.
    ax1 = plt.subplot(211)
    results.algorithm_period_return.plot(ax=ax1,color='blue',legend=u'策略收益')
    ax1.set_ylabel(u'收益')
    results.benchmark_period_return.plot(ax=ax1,color='red',legend=u'基准收益')

    # Show the plot.
    plt.gcf().set_size_inches(18, 8)
    plt.show()



def initialize(context):
    context.has_ordered = False
    set_commission(OrderCost(open_tax=0,close_tax=0.001,open_commission=0.0003,close_commission=0.0003,close_today_commission=0,min_commission=5))
    set_long_only()

def handle_data(context, data):

    #输出每天持仓情况

    if not context.has_ordered:
        for stock in data:
            closeprice=history(5,'1d','close')
            #-2:昨天,-3 前天.-4 大前天
            print get_datetime(),closeprice[sid(stock)][0],closeprice[sid(stock)][1],closeprice[sid(stock)][2],closeprice[sid(stock)][3],closeprice[sid(stock)][4]
            if closeprice[sid(stock)][-2]>closeprice[sid(stock)][-3] and closeprice[sid(stock)][-3]>closeprice[sid(stock)][-4]:
                print "buy",get_datetime()
                order(stock, 300)
            elif closeprice[sid(stock)][-2]<closeprice[sid(stock)][-3] and closeprice[sid(stock)][-3]<closeprice[sid(stock)][-4]:
                print "sell",get_datetime()
                order(stock, -300)


algo = TradingAlgorithm(initialize=initialize, handle_data=handle_data,capital_base=10000,benchmark='399004')



results = algo.run(input_data)
print results
analyze(results=results)