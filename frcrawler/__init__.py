# -*- coding: utf-8 -*-

import os, shutil, click, requests, cgi
from enum import Enum
from functools import wraps

STAGE_DIR = os.path.join(os.getcwd(), 'stage')
HEADERS = {'User-Agent': 'Mozilla/5.0'}


class ReportType(Enum):
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


def error(msg, fg='red'):
    click.secho(msg, fg=fg)
    exit(-1)


def parse_report(code, type, year):
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
              'category': repr(ReportType(int(type))),
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


def init(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        path = os.path.join(os.getcwd(), STAGE_DIR)
        if not os.path.exists(path): os.mkdir(path)
        ret = func(*args, **kwargs)
        return ret

    return wrapper


def cleanup_dirs(*dirs, rmdir=False):
    for dir in dirs:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        if not rmdir:
            os.makedirs(dir)


def download(url, filename=None, folder=STAGE_DIR, headers=None, params=None):
    if headers is None:
        headers = {'User-Agent': 'Mozilla/5.0'}

    r = requests.get(url, params=params, headers=headers, stream=True)

    if not filename:
        if "Content-Disposition" in r.headers:
            _, params = cgi.parse_header(r.headers["Content-Disposition"])
            filename = params["filename"]
        else:
            filename = url.split("/")[-1]

    try:
        total_length = int(r.headers.get('content-length'))
    except TypeError:
        error('Please try again.')

    download_file_path = os.path.join(folder, filename)
    with open(download_file_path, "wb") as f:
        expected_size = (total_length / 1024) + 1
        with click.progressbar(r.iter_content(1024), length=expected_size, bar_template='%(label)s  %(bar)s | %(info)s',
                               label=filename, fill_char=click.style(
                    u'█', fg='cyan'),
                               empty_char=' ') as chunks:
            for chunk in chunks:
                f.write(chunk)
                f.flush()
    return filename


if __name__ == '__main__':
    print(repr(ReportType(1)))
