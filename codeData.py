#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 默认以2020-07-10的MA1000为基准价、MA120为目标价
# codeData格式：{code: (basePrice, sellPrice, secuType, baseMoney, totalUpPct1, totalUpPct2)}
codeData = {
    'sz399997': (8769.046, 11843.521, 'index', -1, 66, 96),  # 中证白酒。2020-08-28的MA250为基准价、MA20为目标价
    'sz399396': (19740.864, 27401.309, 'index', -1, 65, 95),  # 国证食品。2020-08-28的MA250为基准价、MA20为目标价
    'sh000932': (17600.745, 23697.68, 'index', -1, 58, 88),  # 中证消费。2020-08-28的MA250为基准价、MA20为目标价
    # 'sz159928': (3.126, 3.804, 'ETF', 20000),  # 中证消费ETF。2020-07-17的MA250为基准价、MA30为目标价
    'sh000913': (12126.877, 16581.43, 'index', -1, 50, 80),  # 300医药。2020-08-28的MA250为基准价、2020-08-18 MA20为目标价
    # 'sh000933': (11434.951, 15593.366, 'index', -1),  # 中证医药。2020-08-28的MA250为基准价、2020-08-18 MA20为目标价
    'sz399324': (9879.326, 11525.961, 'index', -1, 36, 54),  # 深证F60。2020-08-28的MA250为基准价、MA20为目标价
    'sz399701': (8095.715, 9209.119, 'index', -1, 32, 47),  # 深证F60。2020-08-28的MA250为基准价、MA20为目标价
    # 'sz159916': (3.823, 4.445, 'ETF', 20000),  # 深F60 ETF。2020-07-10的MA500为基准价、2020-03-13 A60为目标价
    # 'sz399702': (6491.832, 7418.204, 'index', -1),  # 深证F120。2020-07-10的MA500为基准价、2020-03-13 A60为目标价
    # 'sz159910': (1.733, 1.994, 'ETF', 20000),  # 深证F120 ETF。2020-07-10的MA500为基准价、2020-03-13 A60为目标价
    # 'sz399550': (6602.926, 7449.134, 'index', -1),  # 央视50。2020-07-10的MA500为基准价、2018-03-22 MA60为目标价
    # 'sz159965': (1.083, 1.193, 'ETF', 20000),  # 央视50 ETF。2020-07-10的MA250为基准价、MA30为目标价
    # 'sh000170': (5133.008, 5677.468, 'index', -1),  # 50AH优选。2020-07-10的MA500为基准价、2020-01-23 MA30为目标价
    # 'sh501050': (1.23, 1.362, 'ETF', 20000),  # 50AH LOF。2020-07-10的MA500为基准价、2020-01-23 MA30为目标价
    # 'sh000016': (2635.838, 2965.167, 'index', -1),  # 上证50。2020-03-06 MA120为目标价
    # 'sh000919': (4510.335, 5141.756, 'index', -1),  # 300价值。2018-04-13 MA120为目标价
    'sh000925': (4019.155, 4524.765, 'index', -1, -1, -1),  # 基本面50。2018-04-13 MA120为目标价
    'sh000922': (4293.802, 4819.761, 'index', -1, -1, -1),  # 中证红利。2018-03-22 MA120为目标价
    'sh000001': (3028.058, 3373.018, 'index', -1, -1, -1),  # 上证指数。2018-02-08 MA120为目标价
    'hkHSI': (26592.763, 29604.089, 'index', -1, -1, -1)  # 恒生指数。2018-08-31 MA250为目标价
}
