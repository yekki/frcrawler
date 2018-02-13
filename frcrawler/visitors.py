# -*- coding: utf-8 -*-

import sys, csv
import frcrawler.visitor as visitor
from frcrawler.model import AnnouncementType, BriefType
from frcrawler.lib import download, error
from terminaltables import DoubleTable
from enum import Enum


def create_visitor(visitor, result):
    try:
        module = sys.modules[__name__]
        class_ = getattr(module, f'{visitor.name}Visitor')
        instance = class_(result)
    except Exception as e:
        error(f'unsupported visitor type: {visitor}. error: {e}')
    else:
        return instance


class Visitor(Enum):
    File = 0
    Console = 1


class FileVisitor:
    def __init__(self, result):
        self._result = result

    @visitor.on('member')
    def visit(self, member):
        pass

    @visitor.when(AnnouncementType)
    def visit(self, member):
        [download(r[0], r[1]) for r in self._result.records]

    @visitor.when(BriefType)
    def visit(self, member):
        with open(self._result.ctype.file, 'w+', encoding='gbk') as file:
            writer = csv.writer(file)
            writer.writerows(self._result.records)


class ConsoleVisitor:
    def __init__(self, result):
        self._result = result

    @visitor.on('member')
    def visit(self, member):
        pass

    @visitor.when(AnnouncementType)
    def visit(self, member):
        raise ValueError('unsupported!')

    @visitor.when(BriefType)
    def visit(self, member):
        table = DoubleTable(self._result.records)
        print(table.table)
