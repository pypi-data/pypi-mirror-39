import pandas as pd

from xbbg.core import timezone
from xbbg.asset.equity import Equity
from xbbg.asset.curncy import Curncy
from xbbg.asset.comdty import Comdty
from xbbg.asset.index import Index
from xbbg.asset.corp import Corp

from collections import namedtuple

CurrencyPair = namedtuple('CurrencyPair', ['ticker', 'factor', 'reversal'])


Futures = dict(
    Jan='F', Feb='G', Mar='H', Apr='J', May='K', Jun='M',
    Jul='N', Aug='Q', Sep='U', Oct='V', Nov='X', Dec='Z',
)

Currencies = {
    'AUDUSD': CurrencyPair('AUD Curncy', 1., -1),

    'JPYUSD': CurrencyPair('JPY Curncy', 1., 1),

    'KRWUSD': CurrencyPair('KRW Curncy', 1., 1),
    'KWN+1MUSD': CurrencyPair('KRW+1M Curncy', 1., 1),

    'TWDUSD': CurrencyPair('TWD Curncy', 1., 1),
    'NTN+1MUSD': CurrencyPair('NTN+1M Curncy', 1., 1),

    'CNYHKD': CurrencyPair('CNYHKD Curncy', 1., -1),
    'CNHHKD': CurrencyPair('CNHHKD Curncy', 1., -1),

    'HKDUSD': CurrencyPair('HKD Curncy', 1., 1),

    'EURUSD': CurrencyPair('EUR Curncy', 1., -1),

    'GBPUSD': CurrencyPair('GBP Curncy', 1., -1),
    'GBpUSD': CurrencyPair('GBP Curncy', 100., -1),
    'GBPAUD': CurrencyPair('GBPAUD Curncy', 1., -1),
    'GBpAUD': CurrencyPair('GBPAUD Curncy', 100., -1),
    'GBPEUR': CurrencyPair('GBPEUR Curncy', 1., -1),
    'GBpEUR': CurrencyPair('GBPEUR Curncy', 100., -1),
    'GBPHKD': CurrencyPair('GBPHKD Curncy', 1., -1),
    'GBpHKD': CurrencyPair('GBPHKD Curncy', 100., -1),

    'INT1USD': CurrencyPair('INT1 Curncy', 1., 1),
    'INT2USD': CurrencyPair('INT2 Curncy', 1., 1),

    'IRD1USD': CurrencyPair('IRD1 Curncy', 10000., -1),
    'IRD2USD': CurrencyPair('IRD2 Curncy', 10000., -1),

    'XID1USD': CurrencyPair('XID1 Curncy', 10000., -1),
    'XID2USD': CurrencyPair('XID2 Curncy', 10000., -1),
}


def market_info(ticker: str):
    """
    Get info for given market

    Args:
        ticker: Bloomberg full ticker

    Returns:
        dict

    Examples:
        >>> from xbbg.exchange import TradingHours
        >>>
        >>> info = market_info('SHCOMP Index')['exch']
        >>> isinstance(info, TradingHours)
        True
        >>> info.tz
        'Asia/Shanghai'
        >>> info = market_info('CL1 Comdty')
        >>> info['freq'], info['is_fut']
        ('M', True)
    """
    t_info = ticker.split()

    # ========================== #
    #           Equity           #
    # ========================== #

    if (t_info[-1] == 'Equity') and ('=' not in t_info[0]):
        exch = t_info[-2]
        for info in Equity:
            if 'exch_codes' not in info: continue
            if exch in info['exch_codes']: return info.copy()
        else: return dict()

    # ============================ #
    #           Currency           #
    # ============================ #

    if t_info[-1] == 'Curncy':
        for info in Curncy:
            if 'tickers' not in info: continue
            if (t_info[0].split('+')[0] in info['tickers']) or \
                    (t_info[0][-1].isdigit() and (t_info[0][:-1] in info['tickers'])):
                return info.copy()
        else: return dict()

    if t_info[-1] == 'Comdty':
        for info in Comdty:
            if 'tickers' not in info: continue
            if t_info[0][:-1] in info['tickers']: return info.copy()
        else: return dict()

    # =================================== #
    #           Index / Futures           #
    # =================================== #

    if (t_info[-1] == 'Index') or (
        (t_info[-1] == 'Equity') and ('=' in t_info[0])
    ):
        if t_info[-1] == 'Equity':
            tck = t_info[0].split('=')[0]
        else:
            tck = ' '.join(t_info[:-1])
        for info in Index:
            if 'tickers' not in info: continue
            if (tck[:2] == 'UX') and ('UX' in info['tickers']): return info.copy()
            if tck in info['tickers']:
                if t_info[-1] == 'Equity': return info.copy()
                if not info.get('is_fut', False): return info.copy()
            if tck[:-1].rstrip() in info['tickers']:
                if info.get('is_fut', False): return info.copy()
        else: return dict()

    if t_info[-1] == 'Corp':
        for info in Corp:
            if 'ticker' not in info: continue

    return dict()


def ccy_pair(local, base='USD'):
    """
    Currency pair info

    Args:
        local: local currency
        base: base currency

    Returns:
        CurrencyPair

    Examples:
        >>> ccy_pair(local='HKD', base='USD')
        CurrencyPair(ticker='HKD Curncy', factor=1.0, reversal=1)
        >>> ccy_pair(local='GBp')
        CurrencyPair(ticker='GBP Curncy', factor=100.0, reversal=-1)
        >>> ccy_pair(local='USD', base='GBp')
        CurrencyPair(ticker='GBP Curncy', factor=0.01, reversal=1)
    """
    if f'{local}{base}' in Currencies:
        return Currencies[f'{local}{base}']

    elif f'{base}{local}' in Currencies:
        rev = Currencies[f'{base}{local}']
        return CurrencyPair(
            ticker=rev.ticker, factor=1. / rev.factor, reversal=-rev.reversal
        )

    else:
        raise NameError(f'incorrect currency - local {local} / base {base}')


def market_timing(ticker, dt, timing='EOD', tz='local'):
    """
    Market close time for ticker

    Args:
        ticker: ticker name
        dt: date
        timing: [EOD (default), BOD]
        tz: conversion to timezone

    Returns:
        str: date & time

    Examples:
        >>> market_timing('7267 JT Equity', dt='2018-09-10')
        '2018-09-10 14:58'
        >>> market_timing('7267 JT Equity', dt='2018-09-10', tz=timezone.TimeZone.NY)
        '2018-09-10 01:58:00-04:00'
        >>> market_timing('7267 JT Equity', dt='2018-01-10', tz='NY')
        '2018-01-10 00:58:00-05:00'
        >>> market_timing('7267 JT Equity', dt='2018-09-10', tz='SPX Index')
        '2018-09-10 01:58:00-04:00'
    """
    info = market_info(ticker=ticker).get('exch', None)
    if info is None: raise LookupError(f'No [exch] info found in {ticker} ...')

    if timing == 'BOD': mkt_time = info.hours.day.start_time
    elif timing == 'FINISHED': mkt_time = info.hours.allday.end_time
    else: mkt_time = info.hours.day.end_time

    cur_dt = pd.Timestamp(str(dt)).strftime('%Y-%m-%d')
    if tz == 'local': return f'{cur_dt} {mkt_time}'
    return timezone.tz_convert(f'{cur_dt} {mkt_time}', to_tz=tz, from_tz=info.tz)
