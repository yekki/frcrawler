# -*- coding: utf-8 -*-

import requests, re
from frcrawler.model import HEADERS, ResultSet

__all__ = ['parse']


def parse(ctype, **kwargs):
    parse_func = f'_{ctype.__name__[:-4].lower()}'
    type = ctype(int(kwargs['type']))
    kwargs['ctype'] = type
    rows = globals()[parse_func](**kwargs)
    return ResultSet(type, rows)


def _brief(**kwargs):
    ctype = kwargs['ctype']
    url = ctype.url
    columns = ctype.columns
    results = []

    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        r.encoding = 'gbk'
        all_data = re.findall(re.compile(r'"(.*?)"', re.S), r.text)
        update_time = all_data[0]
        total_num = len(all_data)
        row = total_num // 9

        results.append(columns)

        for j in range(0, row):
            tmp = [all_data[i] for i in range(1 + j * 9, 10 + j * 9)]
            tmp.insert(0, update_time)
            results.append(tmp)
        return results
    else:
        print('network error!')


def _announcement(**kwargs):
    code = kwargs['code']
    ctype = kwargs['ctype']
    year = kwargs['year']

    def report_name(meta):
        sec_name = meta['announcementTitle']
        title = meta['announcementTitle']

        if title.startswith(sec_name):
            parts = [title, '.pdf']
        else:
            parts = [sec_name, title, '.pdf']

        return ''.join(parts)

    base_url = 'http://www.cninfo.com.cn/'
    query_url = f'{base_url}/cninfo-new/announcement/query'
    params = {'stock': code,
              'category': repr(ctype),
              'pageNum': '1',
              'pageSize': '50',
              'column': 'sse',  # 还有个szse_sme,为深市，不过测试002508也没问题
              'tabName': 'fulltext'
              }

    data = requests.post(query_url, params=params, headers=HEADERS).json()
    announcements = data['announcements']
    results = [i for i in announcements if '摘要' not in i['announcementTitle']]

    if year:
        return [(base_url + r['adjunctUrl'], report_name(r)) for r in results if year in r['announcementTitle']]
    else:
        return [(base_url + r['adjunctUrl'], report_name(r)) for r in results]
