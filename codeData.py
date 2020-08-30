#!/usr/bin/python3
# -*- coding: utf-8 -*-

# # 以2019-09-10的收盘价为基准
# codeData = {'sh000001': 3021.2, 'sh000919': 4902.99, 'sh000922': 4381.25, 'sh000925': 4366.95,
#             'sh000170': 5474.77, 'hkHSI': 26683.68}
# 默认以2020-03-16的MA500为基准价
# codeData格式：{code: (basePrice, sellPrice, secuType, baseMoney)}
# codeData = {
#     'sz399702': (6450.389, 7736.84, 'index', -1),  # 深证F120，19.94%
#     'sz159910': (1.712, 2.127, 'ETF', 2000),  # 深证F120 ETF，24.24%
#     'sz399550': (6604.355, 7827.59, 'index', -1),  # 央视50，18.52%
#     'sz159965': (1.047, 1.339, 'ETF', 2000),  # 央视50 ETF，22.5%。以2020-05-06的MA250为基准
#     'sh000170': (5097.254, 6000, 'index', -1),  # 50AH优选，17.71%
#     'sh501050': (1.213, 1.505, 'ETF', 2000),  # 50AH LOF，24.07%
#     'sh000016': (2728.95, 3215.91, 'index', -1),  # 上证50，17.84%
#     'sh000919': (4725.945, 5393.44, 'index', -1),  # 300价值，14.12%
#     'sh000922': (4298.479, 5083.33, 'index', -1),  # 中证红利，18.26%
#     'sh000925': (4202.138, 4669.81, 'index', -1),  # 基本面50，11.13%
#     'sh000001': (2904.667, 3548.52, 'index', -1),  # 上证指数，22.17%
#     'hkHSI': (26309.026, 31287.88, 'index', -1)  # 恒生指数，18.92%。以2020-03-16的MA1000为基准
# }
# 默认以2020-07-10的MA1000为基准价、MA120为目标价
# codeData格式：{code: (basePrice, sellPrice, secuType, baseMoney)}
codeData = {
    'sh000933': (10661.06, 13585.506, 'index', -1),  # 中证医药。2020-07-17的MA250为基准价、MA30为目标价
    'sh000932': (16645.559, 20070.27, 'index', -1),  # 中证消费。2020-07-17的MA250为基准价、MA30为目标价
    'sz159928': (3.126, 3.804, 'ETF', 20000),  # 中证消费ETF。2020-07-17的MA250为基准价、MA30为目标价
    'sz399701': (7181.274, 8317.387, 'index', -1),  # 深证F60。2020-07-10的MA500为基准价、2020-03-13 A60为目标价
    # 'sz159916': (3.823, 4.445, 'ETF', 20000),  # 深F60 ETF。2020-07-10的MA500为基准价、2020-03-13 A60为目标价
    'sz399702': (6491.832, 7418.204, 'index', -1),  # 深证F120。2020-07-10的MA500为基准价、2020-03-13 A60为目标价
    'sz159910': (1.733, 1.994, 'ETF', 20000),  # 深证F120 ETF。2020-07-10的MA500为基准价、2020-03-13 A60为目标价
    'sz399550': (6602.926, 7449.134, 'index', -1),  # 央视50。2020-07-10的MA500为基准价、2018-03-22 MA60为目标价
    'sz159965': (1.083, 1.193, 'ETF', 20000),  # 央视50 ETF。2020-07-10的MA250为基准价、MA30为目标价
    # 'sh000170': (5133.008, 5677.468, 'index', -1),  # 50AH优选。2020-07-10的MA500为基准价、2020-01-23 MA30为目标价
    # 'sh501050': (1.23, 1.362, 'ETF', 20000),  # 50AH LOF。2020-07-10的MA500为基准价、2020-01-23 MA30为目标价
    # 'sh000016': (2635.838, 2965.167, 'index', -1),  # 上证50。2020-03-06 MA120为目标价
    'sh000919': (4510.335, 5141.756, 'index', -1),  # 300价值。2018-04-13 MA120为目标价
    'sh000925': (4019.155, 4524.765, 'index', -1),  # 基本面50。2018-04-13 MA120为目标价
    'sh000922': (4293.802, 4819.761, 'index', -1),  # 中证红利。2018-03-22 MA120为目标价
    'sh000001': (3028.058, 3373.018, 'index', -1),  # 上证指数。2018-02-08 MA120为目标价
    'hkHSI': (26592.763, 29604.089, 'index', -1)  # 恒生指数。2018-08-31 MA250为目标价
}
