# -*- coding: utf-8 -*-

import click, os

from frcrawler import cleanup_dirs, download, parse_report, init, Period, STAGE_DIR


@click.group()
def cli():
    pass


@cli.command(short_help='下载资料')
@click.option('-c', '--code', required=True, help='股票代码')
@click.option('-p', '--period', required=True, default=0, type=click.Choice((str(p.value) for p in Period)),
              help=f'{Period.description()}')
@click.option('-y', '--year', required=False, help='年份')
@init
def report(code, period, year):
    ret = parse_report(code, period, year)

    for r in ret:
        download(r[0], r[1])


@cli.command(short_help="清理文件下载目录")
@click.confirmation_option(prompt="您确认要清理下载的文件吗?")
def cleanup():
    cleanup_dirs(STAGE_DIR)


@cli.command(short_help="打开最新下载的文件")
def open():
    files = sorted(os.listdir(STAGE_DIR), key=lambda x: os.path.getmtime(os.path.join(STAGE_DIR, x)), reverse=True)
    if files: click.launch(os.path.join(STAGE_DIR, files[0]))
