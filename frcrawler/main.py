# -*- coding: utf-8 -*-

import click, os
from frcrawler import download, init, parser_factory, get_latest_file, cleanup, save_to_csv
from frcrawler import Parser, AnnouncementType, BriefType


@click.group()
def cli():
    pass


@cli.command(short_help='下载资料')
@click.option('-c', '--code', required=True, help='股票代码')
@click.option('-t', '--type', required=True, default=0, type=click.Choice((str(t.value) for t in AnnouncementType)),
              help=f'{AnnouncementType.description()}')
@click.option('-y', '--year', required=False, help='年份')
@init
def announcement(code, type, year):
    parse = parser_factory(Parser.Announcement)
    results = parse(code=code, type=type, year=year)
    [download(r[0], r[1]) for r in results]


@cli.command(short_help='下载统计数据')
@click.option('-t', '--type', required=True, default=0, type=click.Choice((str(t.value) for t in BriefType)),
              help=f'{BriefType.description()}')
@init
def brief(type):
    parse = parser_factory(Parser.Brief)
    results = parse(BriefType(int(type)))

    for r in results:
        print(r)


@cli.command(short_help="清理文件下载目录")
@click.confirmation_option(prompt="您确认要清理下载的文件吗?")
def clean():
    cleanup()


@cli.command(short_help="清空终端屏幕")
def clear():
    click.clear()


@cli.command(short_help="打开最新下载的文件")
def open():
    click.launch(get_latest_file())

if __name__ == '__main__':
    cli()
