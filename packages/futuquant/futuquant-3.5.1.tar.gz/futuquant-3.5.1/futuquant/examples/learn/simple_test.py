from futuquant import *
import numpy as np
import pandas as pd



if __name__ == "__main__":
    pd.set_option('display.max_columns', 20)

    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    # print(quote_ctx.get_market_snapshot('HK.00700'))
    print(quote_ctx.get_stock_basicinfo(Market.HK, SecurityType.STOCK, 'HK.01707'))
    quote_ctx.close()
