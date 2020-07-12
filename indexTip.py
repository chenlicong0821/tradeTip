#!/usr/bin/python3
# -*- coding: utf-8 -*-

import datetime
import json
import logging
import os
import re
import sys
import time
from enum import IntEnum

import requests
import urls


def logInit(logfile):
    logdir = os.path.dirname(logfile)
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s || %(levelname)s || %(name)s || %(filename)s:%(lineno)d || %(message)s',
                        datefmt='%a %Y-%m-%d %H:%M:%S', filename=logfile, filemode='a')


class TCQtIdx(IntEnum):
    MARKET_ID = 0  # 市场标识，1-sh，51-sz
    CHS_NAME = 1  # 证券中文简称
    RAW_SYMBOL = 2  # 证券代码（不含市场标识）
    LAST_PRICE = 3  # 最新价格
    PREV_CLOSE = 4  # 昨收价
    OPEN_PRICE = 5  # 今开价
    TOTAL_VOLUME = 6  # 总成交量：手，实际同VOLUME
    OUT_BUY = 7  # 外盘：手
    IN_SELL = 8  # 内盘：手
    BUY1_PRICE = 9  # 买1价
    BUY1_VOLUME = 10  # 买1量：手
    BUY2_PRICE = 11  # 买2价
    BUY2_VOLUME = 12  # 买2量
    BUY3_PRICE = 13  # 买3价
    BUY3_VOLUME = 14  # 买3量
    BUY4_PRICE = 15  # 买4价
    BUY4_VOLUME = 16  # 买4量
    BUY5_PRICE = 17  # 买5价
    BUY5_VOLUME = 18  # 买5量
    SELL1_PRICE = 19  # 卖1价
    SELL1_VOLUME = 20  # 卖1量：手
    SELL2_PRICE = 21  # 卖2价
    SELL2_VOLUME = 22  # 卖2量
    SELL3_PRICE = 23  # 卖3价
    SELL3_VOLUME = 24  # 卖3量
    SELL4_PRICE = 25  # 卖4价
    SELL4_VOLUME = 26  # 卖4量
    SELL5_PRICE = 27  # 卖5价
    SELL5_VOLUME = 28  # 卖5量
    CURRENT_VOLUME = 29  # 当前成交量
    QUOTE_DATETIME = 30  # 行情日期时间
    NET_CHG = 31  # 涨跌额
    CHG_PCT = 32  # 涨跌幅（%）
    HIGH_PRICE = 33  # 最高价格
    LOW_PRICE = 34  # 最低价格
    LAST_VOLUME_AMOUNT = 35  # 最新价/成交量(手)/成交额(元)
    VOLUME = 36  # 成交量(手)
    AMOUNT = 37  # 成交额(万元)，整数
    TURNOVER_RATE = 38  # 换手率（%）
    PE_TTM = 39  # 市盈率(TTM)
    SECU_STATUS = 40  # 股票状态,允许有多个状态，每种状态一个字符表示: 无或空表示正常, D 退市, S 停牌, U 未上市
    TODAY_HIGH_PRICE = 41  # 当天最高价格
    TODAY_LOW_PRICE = 42  # 当天最低价格
    AMPLITUDE = 43  # 当天振幅（%）
    CIRC_MARKET_VALUE = 44  # 流通市值(亿)
    TOTAL_MARKET_VALUE = 45  # 总市值(亿)
    PB = 46  # 市净率
    HIGH_LIMIT = 47  # 涨停价
    LOW_LIMIT = 48  # 跌停价
    QUANT_RELATIVE = 49  # 量比
    WEI_CHA = 50  # 委差(手)
    AVG_PRICE = 51  # 均价
    PE_DYNAMIC = 52  # 市盈率(动)
    PE_STATIC = 53  # 市盈率(静)
    IDX54 = 54
    IDX55 = 55
    BETA_VALUE = 56  # 贝塔值
    AMOUNT2 = 57  # 成交额(万元)，带小数
    POST_AMOUNT = 58  # 盘后交易额(万元)
    POST_VOLUME = 59  # 盘后交易量(股)
    IDX60 = 60
    SECU_TYPE = 61  # 证券类别，GP-A-KCB表示股票-A股-科创板，ZS表示指数
    IDX62 = 62
    IDX63 = 63
    DPS = 64  # 股息率(%)
    IDX65 = 65
    IDX66 = 66


class dataFromTencent():
    def __init__(self):
        self.STARMarketPattern = re.compile(r'sh68[89]+')
        self.marketIdDict = {'1': 'sh', '51': 'sz', '100': 'hk', '200': 'us'}
        self.baseUrl = urls.tcQtUrl

    def _getVolume(self, code, rawVolume):
        if (self.STARMarketPattern.match(code)):  # 科创板
            return rawVolume
        else:  # 非科创板
            return rawVolume * 100

    def _checkCodeFlag(self, codeFlag, code):
        if codeFlag.startswith('v_') and (codeFlag[2:] == code if code[:2] != 'hk' else codeFlag[2:] == ('r_' + code)):
            return True
        else:
            log.warning(f'codeFlag:{codeFlag} not match code:{code}')
            return False

    def _checkCodeData(self, codeData, code, market):
        rawSymbol = codeData[TCQtIdx.RAW_SYMBOL] if market != 'us' else codeData[TCQtIdx.RAW_SYMBOL].split('.')[0]
        if self.marketIdDict[codeData[TCQtIdx.MARKET_ID]] + rawSymbol == code:
            return True
        else:
            log.warning(f'codeData:{codeData} not match code:{code}')
            return False

    def _getQtDateTimeFmt(self, market):
        if market == 'hk':
            return "%Y/%m/%d %H:%M:%S"
        elif market == 'us':
            return "%Y-%m-%d %H:%M:%S"
        else:
            return "%Y%m%d%H%M%S"

    def _parseData(self, text, codeList):
        res = {}

        log.debug(f'text to be parsed:{text}')
        # 每一条数据都是以';\n'结尾，split之后最后一项就是空字符串、所以忽略之
        qtList = text.split(';\n')[:-1]
        for i, qt in enumerate(qtList):
            codeFlag, codeData = qt.split('=')
            info = codeData.strip('"').split('~')

            # for idx, item in enumerate(info):
            #     print(idx, item, TCQtIdx._value2member_map_[idx])

            code = codeList[i]
            market = code[:2]
            if not (self._checkCodeFlag(codeFlag, code) and self._checkCodeData(info, code, market)):
                continue

            qtDatetime = info[TCQtIdx.QUOTE_DATETIME]
            qtDatetime = datetime.datetime.strptime(qtDatetime, self._getQtDateTimeFmt(market))
            if qtDatetime < datetime.datetime(2020, 1, 1):
                log.warning(f"quoteTime {qtDatetime} incorrect")
                continue
            chsName = info[TCQtIdx.CHS_NAME]
            lastPrice = float(info[TCQtIdx.LAST_PRICE])
            # prevClose = info[TCQtIdx.PREV_CLOSE]
            # openPrice = info[TCQtIdx.OPEN_PRICE]
            # netChg = info[TCQtIdx.NET_CHG]
            chgPct = float(info[TCQtIdx.CHG_PCT])
            # highPrice = info[TCQtIdx.HIGH_PRICE]
            # lowPrice = info[TCQtIdx.LOW_PRICE]
            # volume = self._getVolume(code, int(info[TCQtIdx.VOLUME] or 0))
            # amount = float(info[TCQtIdx.AMOUNT] or 0) * 10000
            # peTTM = float(info[TCQtIdx.PE_TTM]) if info[TCQtIdx.PE_TTM] else 0.0
            # cap = float(info[TCQtIdx.TOTAL_MARKET_VALUE] or 0) * 100000000
            res[code] = (chsName, qtDatetime, lastPrice, chgPct)

        return res

    def fetchData(self, codeList, retry=True):
        res = {}
        try:
            reqCodes = []
            for code in codeList:
                if code[:2] == 'hk':
                    reqCodes.append('r_' + code)
                else:
                    reqCodes.append(code)
            url = self.baseUrl + ','.join(reqCodes)
            req = requests.get(url, timeout=2)
            if 200 == req.status_code:
                # print(req.headers['Content-Type'])
                # match = re.search('charset=(\S+)', req.headers['Content-Type'])
                # if match:
                #     encoding = match.group(1)
                #     print(encoding)
                log.info(f'Get {url} success')
                # text = req.content.decode(req.encoding)
                text = req.text
                res = self._parseData(text, codeList)
            else:
                if retry:
                    log.warning(f'Get {url} failed, ret code:{req.status_code}')
                    time.sleep(2)
                    return self.fetchData(codeList, retry=False)
                log.error(f'Get {url} failed after retry, ret code:{req.status_code}')

            log.info(f'{sys._getframe().f_code.co_name} success')
        except requests.RequestException as e:
            if retry:
                log.error(f'Get {url} failed, error:{e}')
                time.sleep(2)
                return self.fetchData(codeList, retry=False)
            log.error(f'Get {url} failed after retry, error:{e}')
        except Exception as e:
            log.exception(f'{sys._getframe().f_code.co_name} failed: {e}')

        return res


class dataProcess():
    def __init__(self):
        self.buyChgPct = -1.4
        self.sellChgPct = 1.4
        self.totalDownPct1 = -10
        self.totalDownPct2 = -20
        self.totalUpPct1 = 11
        self.totalUpPct2 = 20

    def _getTradeSuggest(self, dtNow, qtDatetime, lastPrice, totalChgPct, chgPct, sellPrice):
        suggest = '无'
        if dtNow.date() != qtDatetime.date():
            suggest = '非交易日'
        # lastPrice达到设定的sellPrice，就考虑卖出
        elif lastPrice >= sellPrice:
            suggest = f'达到{sellPrice}卖出'
        # 总涨幅超过基准点位的totalUpPct1+sellChgPct，就考虑卖出
        elif totalChgPct >= (self.totalUpPct1 + self.sellChgPct):
            if totalChgPct >= self.totalUpPct2:  # 总涨幅超过基准点位的totalUpPct2
                suggest = '强烈卖出'
            elif chgPct >= self.sellChgPct:  # 当天涨幅超过sellChgPct
                suggest = '卖出'
        elif totalChgPct < self.totalUpPct1:  # 总涨幅未超过基准点位的totalUpPct1，就考虑买入
            # 周一或周四，且当天涨幅未超过sellChgPct或总跌幅达到buyChgPct，正常买入
            if dtNow.weekday() in (0, 3) and (chgPct < self.sellChgPct or totalChgPct <= self.buyChgPct):
                suggest = '买入'
            # 总跌幅达到基准点位的totalDownPct1+buyChgPct，考虑加仓买入
            elif totalChgPct <= (self.totalDownPct1 + self.buyChgPct):
                if totalChgPct <= self.totalDownPct2:  # 总跌幅达到基准点位的totalDownPct2
                    suggest = '买入'
                elif chgPct <= self.buyChgPct:  # 当天跌幅达到buyChgPct
                    suggest = '买入'

        return suggest

    def calData(self, codeData, qtData, defaultBaseMoney, powerN):
        res = []
        try:
            dataList = []
            dtNow = datetime.datetime.now()
            for code, (basePrice, sellPrice, secuType, baseMoney) in codeData.items():
                if code not in qtData:
                    log.warning(f'code:{code} not in qtData')
                    res.append((code, 'it not in qtData'))
                    continue

                chsName, qtDatetime, lastPrice, chgPct = qtData[code]
                totalChgPct = round(100 * (lastPrice - basePrice) / basePrice, 2)
                lastToSellPct = round(100 * (lastPrice - sellPrice) / sellPrice, 2)
                sellChgPct = round(100 * (sellPrice - basePrice) / basePrice, 2)
                tradeSuggest = self._getTradeSuggest(dtNow, qtDatetime, lastPrice, totalChgPct, chgPct, sellPrice)
                if baseMoney <= 0:
                    baseMoney = defaultBaseMoney
                buyVol = 0
                buyMoney = 0
                if secuType == 'ETF':
                    buyMoneyInit = baseMoney * pow(basePrice / lastPrice, powerN)
                    buyHand = round(buyMoneyInit / (lastPrice * 100), 0)
                    buyVol = buyHand * 100
                    buyMoney = round(lastPrice * buyVol, 2)
                else:
                    buyVol = pow(basePrice / lastPrice, powerN)
                    buyMoney = round(baseMoney * buyVol, 2)

                dataList.append((code, chsName, qtDatetime.strftime('%m-%d %H:%M:%S'), f'{lastPrice}',
                                 f'{round(chgPct, 2)}%', f'{totalChgPct}%', tradeSuggest, f'{round(buyVol, 2)}',
                                 f'{buyMoney}', f'{lastToSellPct}%', f'{sellChgPct}%'))

            # 按建议买入金额buyMoney由高到低排序
            res = sorted(dataList, key=lambda item: (float(item[5][:-1])), reverse=False)
            log.info(f'{sys._getframe().f_code.co_name} success')
        except Exception as e:
            log.exception(f'{sys._getframe().f_code.co_name} failed: {e}')

        return res


class msgSend():
    def __init__(self):
        self.DDGroupUrl = urls.DDGroupUrl
        self.QyweixinUrl = urls.QyweixinUrl

    def _sendDDGrp(self, text, retry=True):
        try:
            url = self.DDGroupUrl
            headers = {'Content-Type': "application/json; charset=utf-8"}
            data = {'msgtype': 'text', 'text': {"content": text}}
            timeout = (2, 5)
            r = requests.post(url=url, headers=headers, data=json.dumps(data), timeout=timeout)
            if r.status_code == 200:
                res = r.json()
                if res.get('errcode') == 0:
                    pass
                else:
                    reason = res.get('errmsg').encode('utf8')
                    log.error(f'send msg to {url} failed, reason:{reason}')
                    return 'ERROR'
            else:
                if retry:
                    log.warning(f'send msg to {url} failed, ret code:{r.status_code}')
                    time.sleep(3)
                    return self._sendDDGrp(text, retry=False)
                log.error(f'send msg to {url} failed after retry, ret code:{r.status_code}')
                return "ERROR"

            log.info(f'{sys._getframe().f_code.co_name} success')
        except requests.RequestException as e:
            if retry:
                log.error(f'send msg to {url} failed, error:{e}')
                time.sleep(3)
                return self._sendDDGrp(text, retry=False)
            log.error(f'send msg to {url} failed after retry, error:{e}')
            return "ERROR"
        except Exception as e:
            log.error(f'{sys._getframe().f_code.co_name} failed, error:{e}')
            return "ERROR"

        return "OK"

    def _sendQyweixinGrp(self, text, retry=True):
        try:
            url = self.QyweixinUrl
            headers = {'Content-Type': "application/json; charset=utf-8"}
            data = {'msgtype': 'text', 'text': {"content": text}}
            timeout = (2, 5)
            r = requests.post(url=url, headers=headers, data=json.dumps(data), timeout=timeout)
            if r.status_code == 200:
                res = r.json()
                if res.get('errcode') == 0:
                    pass
                else:
                    reason = res.get('errmsg').encode('utf8')
                    log.error(f'send msg to {url} failed, reason:{reason}')
                    return 'ERROR'
            else:
                if retry:
                    log.warning(
                        f'send msg to {url} failed, ret code:{r.status_code}')
                    time.sleep(3)
                    return self._sendDDGrp(text, retry=False)
                log.error(f'send msg to {url} failed after retry, ret code:{r.status_code}')
                return "ERROR"

            log.info(f'{sys._getframe().f_code.co_name} success')
        except requests.RequestException as e:
            if retry:
                log.error(f'send msg to {url} failed, error:{e}')
                time.sleep(3)
                return self._sendDDGrp(text, retry=False)
            log.error(f'send msg to {url} failed after retry, error:{e}')
            return "ERROR"
        except Exception as e:
            log.error(f'{sys._getframe().f_code.co_name} failed, error:{e}')
            return "ERROR"

        return "OK"

    def send(self, sendData):
        sep = '\n'
        sendData = [('code', 'chsName', 'qtDatetime', 'lastPrice', 'chgPct', 'totalChgPct', 'tradeSuggest',
                     'buyVol', 'buyMoney', 'lastToSellPct', 'sellChgPct')] + sendData
        content = [', '.join(line) for line in sendData]
        dtNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        content.append(f'{sep}time: {dtNow}')
        msg = sep.join(content)

        ret = [self._sendDDGrp(msg),
               self._sendQyweixinGrp(msg)
               ]

        return ret


if __name__ == '__main__':
    logname = os.path.splitext(os.path.basename(__file__))[0]
    logInit(f'./log/{logname}.log')
    log = logging.getLogger(logname)

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
        'sh000932': (16504.882, 19299.093, 'index', -1),  # 中证消费。2020-07-10的MA250为基准价、MA30为目标价
        'sz159928': (3.098, 3.649, 'ETF', 20000),  # 中证消费ETF。2020-07-10的MA250为基准价、MA30为目标价
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
    codeList = ['sh688001', 'sz000063', 'sh000001']
    qtData = dataFromTencent().fetchData(list(codeData.keys()))
    log.info(f'qtData:{qtData}')
    resData = dataProcess().calData(codeData, qtData, 200, 4)
    log.info(f'resData:{resData}')
    sendRes = msgSend().send(resData)
    log.info(f'message send {sendRes}')
