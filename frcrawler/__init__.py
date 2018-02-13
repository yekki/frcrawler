# -*- coding: utf-8 -*-

import os, requests, re, csv

from functools import wraps

from frcrawler import visitor
from frcrawler.lib import cleanup_dirs, download
from frcrawler.model import HEADERS, STAGE_DIR


def save_to_csv(brief):
    url = brief.url
    file = brief.file
    columns = brief.columns

    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        r.encoding = 'gbk'
        all_data = re.findall(re.compile(r'"(.*?)"', re.S), r.text)
        update_time = all_data[0]
        total_num = len(all_data)
        row = total_num // 9

        with open(file, 'w+', newline='', encoding='gbk') as f:
            ff = csv.writer(f)
            ff.writerow(columns)
            for j in range(0, row):
                tmp = [all_data[i] for i in range(1 + j * 9, 10 + j * 9)]
                tmp.insert(0, update_time)
                ff.writerow(tuple(tmp))
    else:
        print('network error!')


# command actions
def get_latest_file():
    files = sorted(os.listdir(STAGE_DIR), key=lambda x: os.path.getmtime(os.path.join(STAGE_DIR, x)), reverse=True)
    if files: return os.path.join(STAGE_DIR, files[0])


def cleanup():
    cleanup_dirs(STAGE_DIR)


# wrappers
def init(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        path = os.path.join(os.getcwd(), STAGE_DIR)
        if not os.path.exists(path): os.mkdir(path)
        ret = func(*args, **kwargs)
        return ret

    return wrapper


if __name__ == '__main__':
    pass
    # rows = model(AnnouncementType, type='1', code='600036', year='2016')
    # v = PrinterVisitor(rows)
    # b = BriefType(0)
    # b.accept(v)
