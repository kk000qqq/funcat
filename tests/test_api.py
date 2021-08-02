#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import sys
sys.path.append('../funcat')
sys.path.append('../funcat/data')

from funcat import *
import numpy as np

def test_000001():
    from funcat.data.jq_data_backend import JQDataBackend
    # set_data_backend(TushareDataBackend())

    # T("20200814")
    # S("000001.XSHG")

    # print(CLOSE.value)
    # print(O, H, L)

    # assert np.equal(round(CLOSE.value, 2), 3122.98)
    # assert np.equal(round(OPEN[2].value, 2), 3149.38)
    # assert np.equal(round((CLOSE - OPEN).value, 2), 11.47)
    # assert np.equal(round((CLOSE - OPEN)[2].value, 2), -8.85)
    # assert np.equal(round(((CLOSE / CLOSE[1] - 1) * 100).value, 2), 0.17)
    # assert np.equal(round(MA(CLOSE, 60)[2].value, 2), 3131.08)
    # assert np.equal(round(MACD().value, 2), -37.18)
    # assert np.equal(round(HHV(HIGH, 5).value, 2), 3245.09)
    # assert np.equal(round(LLV(LOW, 5).value, 2), 3100.91)
    # assert COUNT(CLOSE > OPEN, 5) == 2

    # ts = TushareDataBackend()
    # print(ts.get_price('000001.XSHE', '20200101', '20200108', freq='1d'))
    # index str(date) o c h l v int(datetime)

    # jq = JQDataBackend()
    # print(jq.get_price(order_book_id='000001.XSHE', end='2020-01-10 14:20:00', count=10, freq='1d'))

    # print(jq.stock_basics[jq.stock_basics.index[['000001.XSHG']]]['display_name'])
    # print(jq.stock_basics[jq.stock_basics.index == '000001.XSHE']['display_name'][0])
    # print(jq.get_order_book_id_list())

    # print(jq.stock_basics.index)

    # print(jq.get_trading_dates('20200101', '20200130'))

    set_data_backend(JQDataBackend())
    set_current_date('2020-08-14 16:56:00')
    set_count(90)
    set_current_freq('1d')

    S('000001.XSHE')

    LC = REF(CLOSE, 1)
    RSI5 = ((SMA(MAX((CLOSE - LC), 0), 5, 1) / SMA(ABS((CLOSE - LC)), 5, 1)) * 100)
    TR1 = SUM(MAX(MAX((HIGH - LOW), ABS((HIGH - REF(CLOSE, 1)))), ABS((LOW - REF(CLOSE, 1)))), 10)
    HD = (HIGH - REF(HIGH, 1))
    LD = (REF(LOW, 1) - LOW)
    DMP = SUM(IF(((HD > 0) & (HD > LD)), HD, 0), 10)
    DMM = SUM(IF(((LD > 0) & (LD > HD)), LD, 0), 10)
    PDI = ((DMP * 100) / TR1)
    MDI = ((DMM * 100) / TR1)
    TT1 = (ABS((MDI - PDI)) / (MDI + PDI)) * 100
    ADX = MA(TT1, 5)
    AV = (RSI5 + ADX)
    DXR = (((ADX + REF(ADX, 5)) / 2) + RSI5)
    WR10 = ((100 * (HHV(HIGH, 10) - CLOSE)) / (HHV(HIGH, 10) - LLV(LOW, 10)))
    NEWVOL = (RSI5 - WR10)
    阶段底部 = (AV + NEWVOL)
    # STICKLINE((阶段底部 < 0),0,-10,0.8,1),LINETHICK6,coloryellow;
    趋势线 = LLV(阶段底部, 1)
    # STICKLINE(CROSS(阶段底部,0),0,-10,0.8,1),LINETHICK6,colorred;
    # STICKLINE((趋势线 >230 ),100,90,0.3,1),LINETHICK6,colorgreen;
    LOWV = LLV(LOW, 9)
    HIGHV = HHV(HIGH, 9)
    N, M1, M2 = 9, 3, 3
    RSV1 = (CLOSE - LLV(LOW, N)) / (HHV(HIGH, N) - LLV(LOW, N)) * 100
    RSV = EMA(RSV1, 3)
    K = EMA(RSV, 3)
    D = MA(K, 3)
    # STICKLINE(K>D , K,D ,2.5,0),colorred,LINETHICK2;
    # STICKLINE(D>K,K,D,2.5,0),colorgreen,LINETHICK2;
    逃顶线 = 90
    中轴线 = 50
    抄底线 = 10
    警戒 = 阶段底部 < 0
    出击 = CROSS(阶段底部, 0)
    VAR1 = (HHV(HIGH, 13) - LLV(LOW, 13))
    VAR2 = (HHV(HIGH, 13) - CLOSE)
    VAR3 = (CLOSE - LLV(LOW, 13))
    VAR4 = (((VAR2 / VAR1) * 100) - 70)
    VAR5 = ((CLOSE - LLV(LOW, 60)) / (HHV(HIGH, 60) - LLV(LOW, 60))) * 100
    VAR6 = ((((2 * CLOSE) + HIGH) + LOW) / 4)
    VAR7 = SMA(((VAR3 / VAR1) * 100), 3, 1)
    VAR8 = LLV(LOW, 34)
    VAR9 = (SMA(VAR7, 3, 1) - SMA(VAR4, 9, 1))
    VAR10 = IF((VAR9 > 100), (VAR9 - 100), 0)
    VAR11 = HHV(HIGH, 34)
    VAR12 = EMA((((VAR6 - VAR8) / (VAR11 - VAR8)) * 100), 13)
    VAR13 = EMA(((0.667 * REF(VAR12, 1)) + (0.333 * VAR12)), 2)
    # STICKLINE(((VAR12 - VAR13) > 0), VAR12, VAR13, 12, 0), colorred
    # STICKLINE(((VAR12 - VAR13) < 0), VAR12, VAR13, 8, 0), colorcyan
    低位绿变红看多 = EMA(VAR13, 5)
    高位红变绿减仓 = 99


    print(ADX, VAR13)


test_000001()
