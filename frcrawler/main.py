# -*- coding: utf-8 -*-

import click
from frcrawler import init, get_latest_file, cleanup, model
from frcrawler.model import AnnouncementType, BriefType
from frcrawler.visitors import create_visitor, Visitor
from frcrawler.parser import parse


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
    result = parse(AnnouncementType, type=type, code=code, year=year)
    visitor = create_visitor(Visitor.File, result)
    result.accept(visitor)


@cli.command(short_help='下载统计数据')
@click.option('-t', '--type', required=True, default=0, type=click.Choice((str(t.value) for t in BriefType)),
              help=f'{BriefType.description()}')
@init
def brief(type):
    result = parse(BriefType, type=type)
    visitor = create_visitor(Visitor.Console, result)
    result.accept(visitor)


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


@cli.command(short_help="测试命令")
def debug():
    pass


if __name__ == '__main__':
    cli()
