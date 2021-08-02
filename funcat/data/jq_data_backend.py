# -*- coding: utf-8 -*-
#

from cached_property import cached_property

from .backend import DataBackend
from ..utils import lru_cache, get_str_date_from_int, get_int_date

import datetime

if True:
    from jqdatasdk import *
    from jqdatasdk.technical_analysis import *

    import jqdatasdk as jq
    jq.auth('', '')
else:
    from jqboson.api.data import *
    from jqdata import *
    from jqlib.technical_analysis import *
    from jqlib import *
    import jqboson.api.data as jq


class JQDataBackend(DataBackend):

    @cached_property
    def jq(self):
        try:
            return jq
        except ImportError:
            print("-" * 50)
            print(">>> Missing tushare. Please run `pip install jqdatasdk`")
            print("-" * 50)
            raise

    @cached_property
    def stock_basics(self):
        return get_all_securities(types=['stock'])

    @staticmethod
    def convert_date_to_int(dt):
        t = dt.year * 10000 + dt.month * 100 + dt.day
        t *= 1000000
        return t

    @staticmethod
    def convert_dt_to_int(dt):
        t = JQDataBackend.convert_date_to_int(dt)

        if type(dt) != datetime.date:
            t += dt.hour * 10000 + dt.minute * 100 + dt.second

        return t

    @lru_cache(maxsize=4096)
    def get_price(self, order_book_id, start=None, end=None, count=None, freq='1d'):
        """
        :param order_book_id: e.g. 000002.XSHE
        :param start: 20160101
        :param end: 20160201
        :returns:
        :rtype: numpy.rec.array
        """

        # str(date) o c h l v int(datetime)

        df = get_bars(security=order_book_id,
                      fields=['date', 'open', 'close', 'high', 'low', 'volume'],
                      count=count,
                      unit=freq,
                      include_now=True,
                      end_dt=end,
                      fq_ref_date=None)

        df["datetime"] = df["date"].apply(JQDataBackend.convert_dt_to_int)
        df['volume'] = df['volume'] / 100
        df['date'] = df['date'].apply(lambda v: v.strftime('%Y%m%d'))

        arr = df.to_records()

        return arr

    @lru_cache()
    def get_order_book_id_list(self):
        """获取所有的股票代码列表
        """
        return list(self.stock_basics.index)

    @lru_cache()
    def get_trading_dates(self, start, end):
        """获取所有的交易日

        :param start: 20160101
        :param end: 20160201
        """
        if type(start) is int:
            start = str(start)
        if type(end) is int:
            end = str(end)

        trading_dates = get_trade_days(start_date=start, end_date=end)
        return [get_int_date(date) for date in trading_dates.tolist()]

    @lru_cache(maxsize=4096)
    def symbol(self, order_book_id):
        """获取order_book_id对应的名字
        :param order_book_id str: 股票代码
        :returns: 名字
        :rtype: str
        """

        return order_book_id + '[' + jq.stock_basics[jq.stock_basics.index == order_book_id]['display_name'][0] + ']'
