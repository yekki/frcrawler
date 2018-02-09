# -*- coding: utf-8 -*-

import os, shutil, click, requests, cgi
from enum import Enum


class Period(Enum):
    M12 = 0
    M6 = 1
    M3 = 2
    M9 = 3
    ALL = 0

    def __str__(self):
        descs = ('年报', '半年报', '一季报', '三季报', '全部')
        return descs[self.value]

    def __repr__(self):
        descs = ('category_ndbg_szsh', 'category_bndbg_szsh', 'category_yjdbg_szsh', 'category_sjdbg_szsh',
                 'category_scgkfx_szsh', '0')
        return descs[self.value]

    @classmethod
    def description(cls):
        return ','.join(f'{p.value}:{str(p)}' for p in cls)


STAGE_DIR = os.path.join(os.getcwd(), 'stage')
HEADERS = {'User-Agent': 'Mozilla/5.0'}


def error(msg, fg='red'):
    click.secho(msg, fg=fg)
    exit(-1)


def parse_report(code, period, year):
    base_url = 'http://www.cninfo.com.cn/'
    query_url = f'{base_url}/cninfo-new/announcement/query'
    params = {'stock': code,
              # category_ndbg_szsh;category_bndbg_szsh;category_yjdbg_szsh;category_sjdbg_szsh;category_scgkfx_szsh;
              'category': repr(Period(int(period))),
              'pageNum': '1',
              'pageSize': '50',
              'column': 'sse',  # 还有个szse_sme,为深市，不过测试002508也没问题
              'tabName': 'fulltext'
              }

    data = requests.post(query_url, params=params, headers=HEADERS).json()
    announcements = data['announcements']
    results = [i for i in announcements if '摘要' not in i['announcementTitle']]

    for i in results:
        sec_name = i['announcementTitle']

        if year in sec_name:
            url = f"{base_url}{i['adjunctUrl']}"
            title = i['announcementTitle']

            if title.startswith(sec_name):
                parts = ['data/', title, '.pdf']
            else:
                parts = ['data/', sec_name, title, '.pdf']

            path = ''.join(parts)

            return (url, path)
    else:
        error('report not found!')


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
    print(repr(Period(1)))
