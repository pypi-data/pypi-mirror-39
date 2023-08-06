# -*- coding: utf-8 -*-
"""
Created on 2017/6/9
@author: MG
"""
import logging
from ibats_common.config import ConfigBase as ConBase, update_db_config
from ibats_common.common import ExchangeName

logger = logging.getLogger(__name__)


class ConfigBase(ConBase):

    # 交易所名称
    MARKET_NAME = ExchangeName.HuoBi.name

    # api configuration
    EXCHANGE_ACCESS_KEY = '4c810270-924f3295-c426eac6-43f33'
    EXCHANGE_SECRET_KEY = '9fab81fc-60c843c7-4eb088a8-82c20'

    # mysql db info
    DB_HANDLER_ENABLE = True
    DB_SCHEMA_MD = 'md_huobi'
    DB_URL_DIC = {
        DB_SCHEMA_MD: 'mysql://mg:Dcba1234@localhost/' + DB_SCHEMA_MD
    }

    # redis info
    REDIS_PUBLISHER_HANDLER_ENABLE = False
    REDIS_INFO_DIC = {'REDIS_HOST': 'localhost',  # '192.168.239.131'
                      'REDIS_PORT': '6379',
                      }

    def __init__(self):
        """
        初始化一些基本配置信息
        """
        # 设置rest调用日志输出级别
        # logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)
        logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)
        logging.getLogger('DBHandler->md_min1_tick_bc').setLevel(logging.INFO)
        logging.getLogger('DBHandler->md_min1_bc').setLevel(logging.INFO)
        logging.getLogger('DBHandler->md_min60_bc').setLevel(logging.INFO)
        logging.getLogger('DBHandler->md_daily_bc').setLevel(logging.INFO)
        logging.getLogger('MDFeeder').setLevel(logging.INFO)
        # logging.getLogger('md_min1_bc').setLevel(logging.INFO)
        # logging.getLogger('md_min1_tick_bc').setLevel(logging.INFO)


# 测试配置（测试行情库）
config = ConfigBase()
update_db_config(config.DB_URL_DIC)


def update_config(config_new: ConfigBase, update_db=True):
    global config
    config = config_new
    logger.info('更新默认配置信息 %s < %s', ConfigBase, config_new.__class__)
    if update_db:
        update_db_config(config.DB_URL_DIC)


if __name__ == "__main__":
    pass
