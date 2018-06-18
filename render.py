#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
from consts import *
from gobang import GoBang

IMAGE_PATH = 'images/'

WIDTH = 530
HEIGHT = 530
MARGIN = 20
GRID = (WIDTH - 2 * MARGIN) / (N - 1)
PIECE = 27


class GameRender(object):
    def __init__(self, gobang):
        # 绑定逻辑类
        self.__gobang = gobang
        # 黑棋开局
        self.__currentPieceState = ChessboardState.BLACK

        # 初始化 pygame
        pygame.init()
        # pygame.display.set_mode((width, height), flags, depth)
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption('Gobang')

        # UI 资源
        self.__ui_chessboard = pygame.image.load(IMAGE_PATH + 'chessboard.jpg').convert()
        self.__ui_piece_black = pygame.image.load(IMAGE_PATH + 'piece_black.png').convert_alpha()
        self.__ui_piece_white = pygame.image.load(IMAGE_PATH + 'piece_white.png').convert_alpha()

    def coordinate_transform_map2pixel(self, i, j):
        # 从 chessMap 里的逻辑坐标到 UI 上的绘制坐标的转换
        return MARGIN + j * GRID - PIECE / 2, MARGIN + i * GRID - PIECE / 2

    def coordinate_transform_pixel2map(self, x, y):
        # 从 UI 上的绘制坐标到 chessMap 里的逻辑坐标的转换
        i, j = int(round((y - MARGIN + PIECE / 2) / GRID)), int(round((x - MARGIN + PIECE / 2) / GRID))
        # 有MAGIN, 排除边缘位置导致 i,j 越界
        if i < 0 or i >= N or j < 0 or j >= N:
            return None, None
        else:
            return i, j

    def draw_chess(self):
        # 棋盘
        self.__screen.blit(self.__ui_chessboard, (0, 0))
        # 棋子
        for i in range(0, N):
            for j in range(0, N):
                x, y = self.coordinate_transform_map2pixel(i, j)
                state = self.__gobang.get_chessboard_state(i, j)
                if state == ChessboardState.BLACK:
                    self.__screen.blit(self.__ui_piece_black, (x, y))
                elif state == ChessboardState.WHITE:
                    self.__screen.blit(self.__ui_piece_white, (x, y))
                else:  # ChessboardState.EMPTY
                    pass

    def draw_mouse(self):
        # 鼠标的坐标
        x, y = pygame.mouse.get_pos()
        # 棋子跟随鼠标移动
        if self.__currentPieceState == ChessboardState.BLACK:
            self.__screen.blit(self.__ui_piece_black, (x - PIECE / 2, y - PIECE / 2))
        else:
            self.__screen.blit(self.__ui_piece_white, (x - PIECE / 2, y - PIECE / 2))

    def draw_result(self, result):
        font = pygame.font.SysFont('Helvetica', 50)
        tips = u"End: "
        if result == ChessboardState.BLACK:
            tips = tips + u"winner is black"
        elif result == ChessboardState.WHITE:
            tips = tips + u"winner is white"
        else:
            tips = tips + u"tie"
        text = font.render(tips, True, (255, 0, 0))
        self.__screen.blit(text, (WIDTH / 2 - 200, HEIGHT / 2 - 50))

    def one_step(self):
        i, j = None, None
        # 鼠标点击
        mouse_button = pygame.mouse.get_pressed()
        # 左键
        if mouse_button[0]:
            x, y = pygame.mouse.get_pos()
            i, j = self.coordinate_transform_pixel2map(x, y)

        if not i is None and not j is None:
            # 格子上已经有棋子
            if self.__gobang.get_chessboard_state(i, j) != ChessboardState.EMPTY:
                return False
            else:
                self.__gobang.set_chessboard_state(i, j, self.__currentPieceState)
                return True

        return False

    def change_state(self):
        if self.__currentPieceState == ChessboardState.BLACK:
            self.__currentPieceState = ChessboardState.WHITE
        else:
            self.__currentPieceState = ChessboardState.BLACK