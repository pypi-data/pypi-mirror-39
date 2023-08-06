#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/6/20 19:53
@File    : md_agent.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import json
import time
from queue import Queue
from ibats_common.md import MdAgentBase, md_agent
from ibats_common.utils.mess import bytes_2_str
from ibats_common.common import PeriodType, RunMode, ExchangeName
from ibats_bitmex_trader.backend import engine_md, get_redis
from ibats_common.utils.redis import get_channel
from ibats_bitmex_feeder.backend.orm import MDMin1, MDMin5, MDHour1, MDDaily
from ibats_common.utils.db import with_db_session, get_db_session
import pandas as pd
from ibats_bitmex_trader.config import config

period_model_dic = {
    PeriodType.Min1: MDMin1,
    PeriodType.Min5: MDMin5,
    PeriodType.Hour1: MDHour1,
    PeriodType.Day1: MDDaily,
}


class MdAgentPub(MdAgentBase):

    def load_history(self, date_from=None, date_to=None, load_md_count=None) -> (pd.DataFrame, dict):
        """
        从mysql中加载历史数据
        实时行情推送时进行合并后供数据分析使用
        :param date_from: None代表沿用类的 init_md_date_from 属性
        :param date_to: None代表沿用类的 init_md_date_from 属性
        :param load_md_count: 0 代表不限制，None代表沿用类的 init_load_md_count 属性，其他数字代表相应的最大加载条数
        :return: md_df 或者
         ret_data {
            'md_df': md_df, 'datetime_key': 'ts_start',
            'date_key': **, 'time_key': **, 'microseconds_key': **
            }
        """
        # 如果 init_md_date_from 以及 init_md_date_to 为空，则不加载历史数据
        if self.init_md_date_from is None and self.init_md_date_to is None:
            ret_data = {'md_df': None, 'datetime_key': 'timestamp'}
            return ret_data

        if self.md_period not in period_model_dic:
            raise ValueError('%s error' % self.md_period)

        # 将sql 语句形势改成由 sqlalchemy 进行sql 拼装方式
        # sql_str = """select * from md_min_1
        #     where InstrumentID in ('j1801') and tradingday>='2017-08-14'
        #     order by ActionDay, ActionTime, ActionMillisec limit 200"""
        # sql_str = """SELECT * FROM md_min_1
        # WHERE InstrumentID IN (%s) %s
        # ORDER BY ActionDay DESC, ActionTime DESC %s"""
        model = period_model_dic[self.md_period]
        with with_db_session(engine_md) as session:
            sub_query = session.query(
                model.symbol.label('symbol'), model.timestamp.label('timestamp'),
                model.open.label('open'), model.high.label('high'),
                model.low.label('low'), model.close.label('close'),
                model.volume.label('volume'), model.turnover.label('turnover'), model.trades.label('trades')
            ).filter(
                model.symbol.in_(self.instrument_id_list)
            ).order_by(model.timestamp.desc())
            # 设置参数
            params = list(self.instrument_id_list)
            # date_from 起始日期
            if date_from is None:
                date_from = self.init_md_date_from
            if date_from is not None:
                # qry_str_date_from = " and tradingday>='%s'" % date_from
                sub_query = sub_query.filter(model.timestamp >= date_from)
                params.append(date_from)
            # date_to 截止日期
            if date_to is None:
                date_to = self.init_md_date_to
            if date_to is not None:
                # qry_str_date_to = " and tradingday<='%s'" % date_to
                sub_query = sub_query.filter(model.timestamp <= date_to)
                params.append(date_to)

            # load_limit 最大记录数
            if load_md_count is None:
                load_md_count = self.init_load_md_count
            if load_md_count is not None and load_md_count > 0:
                # qry_str_limit = " limit %d" % load_md_count
                sub_query = sub_query.limite(load_md_count)
                params.append(load_md_count)

            sub_query = sub_query.subquery('t')
            query = session.query(
                sub_query.c.symbol.label('symbol'), sub_query.c.timestamp.label('timestamp'),
                sub_query.c.open.label('open'), sub_query.c.high.label('high'),
                sub_query.c.low.label('low'), sub_query.c.close.label('close'),
                sub_query.c.volume.label('volume'), sub_query.c.turnover.label('turnover'),
                sub_query.c.trades.label('trades')
            ).order_by(sub_query.c.timestamp)
            sql_str = str(query)

        # 合约列表
        # qry_str_inst_list = "'" + "', '".join(self.instrument_id_list) + "'"
        # 拼接sql
        # qry_sql_str = sql_str % (qry_str_inst_list, qry_str_date_from + qry_str_date_to, qry_str_limit)

        # 加载历史数据
        self.logger.debug("%s on:\n%s", params, sql_str)
        md_df = pd.read_sql(sql_str, engine_md, params=params)
        # self.md_df = md_df
        ret_data = {'md_df': md_df, 'datetime_key': 'timestamp', 'symbol_key': 'symbol', 'close_key': 'close'}
        return ret_data


@md_agent(RunMode.Realtime, ExchangeName.BitMex, is_default=False)
class MdAgentRealtime(MdAgentPub):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pub_sub = None
        self.md_queue = Queue()

    def connect(self):
        """链接redis、初始化历史数据"""
        redis_client = get_redis()
        self.pub_sub = redis_client.pubsub()

    def release(self):
        """释放channel资源"""
        self.pub_sub.close()

    def subscribe(self, instrument_id_list=None):
        """订阅合约"""
        super().subscribe(instrument_id_list)
        if instrument_id_list is None:
            instrument_id_list = self.instrument_id_list
        # channel_head = Config.REDIS_CHANNEL[self.md_period]
        # channel_list = [channel_head + instrument_id for instrument_id in instrument_id_list]
        channel_list = [get_channel(config.MARKET_NAME, self.md_period, instrument_id)
                        for instrument_id in instrument_id_list]
        self.pub_sub.psubscribe(*channel_list)

    def run(self):
        """启动多线程获取MD"""
        if not self.keep_running:
            self.keep_running = True
            for item in self.pub_sub.listen():
                if self.keep_running:
                    if item['type'] == 'pmessage':
                        # self.logger.debug("pmessage:", item)
                        md_dic_str = bytes_2_str(item['data'])
                        md_dic = json.loads(md_dic_str)
                        self.md_queue.put(md_dic)
                    else:
                        self.logger.debug("%s response: %s", self.name, item)
                else:
                    break

    def unsubscribe(self, instrument_id_list):
        """退订合约"""
        if instrument_id_list is None:
            instrument_id_list = self.instrument_id_list

        super().unsubscribe(instrument_id_list)

        # channel_head = config.REDIS_CHANNEL[self.md_period]
        # channel_list = [channel_head + instrument_id for instrument_id in instrument_id_list]
        channel_list = [get_channel(config.MARKET_NAME, self.md_period, instrument_id)
                        for instrument_id in instrument_id_list]
        if self.pub_sub is not None:  # 在回测模式下有可能不进行 connect 调用以及 subscribe 订阅，因此，没有 pub_sub 实例
            self.pub_sub.punsubscribe(*channel_list)

    def pull(self, timeout=None):
        """阻塞方式提取合约数据"""
        md = self.md_queue.get(block=True, timeout=timeout)
        self.md_queue.task_done()
        return md


@md_agent(RunMode.Backtest, ExchangeName.BitMex, is_default=False)
class MdAgentBacktest(MdAgentPub):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timeout = 1
        self.timestamp_key = 'timestamp'
        self.symbol_key = 'symbol'
        self.close_key = 'close'

    def connect(self):
        """链接redis、初始化历史数据"""
        pass

    def release(self):
        """释放channel资源"""
        pass

    def run(self):
        """启动多线程获取MD"""
        if not self.keep_running:
            self.keep_running = True
            while self.keep_running:
                time.sleep(self.timeout)
            else:
                self.logger.info('%s job finished', self.name)
