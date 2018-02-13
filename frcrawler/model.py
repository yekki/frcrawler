# -*- coding: utf-8 -*-
from enum import Enum
import os

STAGE_DIR = os.path.join(os.getcwd(), 'stage')
HEADERS = {'User-Agent': 'Mozilla/5.0'}


class BriefType(Enum):
    指数 = 0
    涨跌幅 = 1

    @classmethod
    def description(cls):
        return ' '.join(f'{p.value}:{p.name}' for p in cls)

    @property
    def url(self):
        urls = ['http://www.csindex.com.cn/data/js/show_zsgz.js?str=ro84Vujt3qqOm29t',
                'http://www.csindex.com.cn/data/js/show_zsbx.js?str=tHmi5QqVH3e7EG']
        return urls[self.value]

    @property
    def file(self):
        files = ['指标统计.csv', '涨幅统计.csv']
        return os.path.join(STAGE_DIR, files[self.value])

    @property
    def columns(self):
        columns = [('更新日期', '指数名称', '静态市盈率', '滚动市盈率', '市净率', '去年底静态市盈率', '去年底滚动市盈率', '去年底市净率', '指数简称', '股息率'),
                   ('更新日期', '指数简称', '收盘', '日涨跌', '日涨跌幅（%）', '今年以来涨跌',
                    '今年以来涨跌幅（%）', '成交额较昨日增减（亿元）', '成交额较昨日增减（%）')]

        return columns[self.value]

    def accept(self, visitor):
        visitor.visit(self)


class AnnouncementType(Enum):
    年报 = 0
    半年报 = 1
    一季报 = 2
    三季报 = 3
    增发 = 4
    可转债券 = 5
    债券 = 6
    特别融资 = 7
    配股 = 8
    特别机构报告 = 9
    投资者关系 = 10
    其它重大事项 = 11
    首次公开发行 = 12

    def __repr__(self):
        descs = ('category_ndbg_szsh', 'category_bndbg_szsh', 'category_yjdbg_szsh', 'category_sjdbg_szsh',
                 'category_zf_szsh', 'category_kzhz_szsh', 'category_zqgg_szsh', 'category_qtrz_szsh',
                 'category_pg_szsh', 'category_zjjg_szsh', 'category_tzzgx_szsh', 'category_qtzdsx_szsh',
                 'category_scgkfx_szsh')
        return descs[self.value]

    @classmethod
    def description(cls):
        return ' '.join(f'{p.value}:{p.name}' for p in cls)

    def accept(self, visitor):
        visitor.visit(self)


class ResultSet:
    def __init__(self, ctype, rows):
        self._ctype = ctype
        self._rows = rows

    def accept(self, visitor):
        self._ctype.accept(visitor)

    @property
    def rows(self):
        return self._rows