#!/usr/bin/python
# -*- coding: UTF-8 -*-
from enum import Enum

N = 15
COLUMN = 15
ROW = 15

list1 = []  # AI (x,y) list
list2 = []  # human (x,y) list
list3 = []  # all

list_all = []  # All chess pieces


class ChessboardState(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2
