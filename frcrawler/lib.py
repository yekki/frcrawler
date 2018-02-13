# -*- coding: utf-8 -*-

import os, shutil, click, requests, cgi
from frcrawler.model import STAGE_DIR


def error(msg, fg='red'):
    click.secho(msg, fg=fg)
    exit(-1)


def cleanup_dirs(*dirs, rmdir=False):
    for dir in dirs:
        if os.path.exists(dir):
            shutil.rmtree(dir)
        if not rmdir:
            os.makedirs(dir)


def download(url, filename=None, folder=STAGE_DIR):
    r = requests.get(url, stream=True)

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
