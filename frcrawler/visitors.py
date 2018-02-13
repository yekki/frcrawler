# -*- coding: utf-8 -*-

import sys
import frcrawler.visitor as visitor
from frcrawler.model import AnnouncementType, BriefType
from frcrawler.lib import download, error
from terminaltables import DoubleTable
from enum import Enum


def create_visitor(visitor, result):
    try:
        module = sys.modules[__name__]
        class_ = getattr(module, f'{visitor.name}Visitor')
        instance = class_(result.rows)
    except:
        error(f'unsupported visitor type:{visitor}')
    else:
        return instance


class Visitor(Enum):
    File = 0
    Console = 1


class FileVisitor:
    def __init__(self, rows):
        self.rows = rows

    @visitor.on('member')
    def visit(self, member):
        pass

    @visitor.when(AnnouncementType)
    def visit(self, member):
        [download(r[0], r[1]) for r in self.rows]

    @visitor.when(BriefType)
    def visit(self, member):
        raise ValueError('unsupported!')


class ConsoleVisitor:
    def __init__(self, rows):
        self.rows = rows

    @visitor.on('member')
    def visit(self, member):
        pass

    @visitor.when(AnnouncementType)
    def visit(self, member):
        raise ValueError('unsupported!')

    @visitor.when(BriefType)
    def visit(self, member):
        table = DoubleTable(self.rows)
        print(table.table)
