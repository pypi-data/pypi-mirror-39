from finviz import Screener

stock_list = Screener(filters=['cap_mega'])
stock_list.add(filters=['fa_div_high'], table='Performance')
print(stock_list)