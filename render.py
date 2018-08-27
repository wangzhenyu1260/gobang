#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame
from consts import *

IMAGE_PATH = 'images/'

WIDTH = 530
HEIGHT = 530
MARGIN = 20
GRID = (WIDTH - 2 * MARGIN) / (N - 1)
PIECE = 27


class GameRender(object):
    def __init__(self, gobang):
        # bind gobang class
        self.__gobang = gobang
        # Black chess start
        self.__currentPieceState = ChessboardState.BLACK

        # init pygame
        pygame.init()
        # pygame.display.set_mode((width, height), flags, depth)
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        pygame.display.set_caption('Gobang')

        # UI assets
        self.__ui_chessboard = pygame.image.load(IMAGE_PATH + 'chessboard.jpg').convert()
        self.__ui_piece_black = pygame.image.load(IMAGE_PATH + 'piece_black.png').convert_alpha()
        self.__ui_piece_white = pygame.image.load(IMAGE_PATH + 'piece_white.png').convert_alpha()

    def coordinate_transform_map2pixel(self, i, j):
        return MARGIN + j * GRID - PIECE / 2, MARGIN + i * GRID - PIECE / 2

    def coordinate_transform_pixel2map(self, x, y):
        i, j = int(round((y - MARGIN + PIECE / 2) / GRID)), int(round((x - MARGIN + PIECE / 2) / GRID))
        # cross the border
        if i < 0 or i >= N or j < 0 or j >= N:
            return None, None
        else:
            return i, j

    def draw_chess(self):
        # chessboard
        self.__screen.blit(self.__ui_chessboard, (0, 0))
        # chess
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
        # get mouse position
        x, y = pygame.mouse.get_pos()
        # Chess moves with the mouse
        if self.__currentPieceState == ChessboardState.BLACK:
            self.__screen.blit(self.__ui_piece_black, (x - PIECE / 2, y - PIECE / 2))
        else:
            self.__screen.blit(self.__ui_piece_white, (x - PIECE / 2, y - PIECE / 2))

    def draw_result(self, result):
        font = pygame.font.Font(None, 40)
        tips = u"Game over: "
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
        # mouse click
        mouse_button = pygame.mouse.get_pressed()
        # mouse left
        if mouse_button[0]:
            x, y = pygame.mouse.get_pos()
            i, j = self.coordinate_transform_pixel2map(x, y)

        if not i is None and not j is None:
            # There are already pieces on the chessboard.
            if self.__gobang.get_chessboard_state(i, j) != ChessboardState.EMPTY:
                return False
            else:
                self.__gobang.set_chessboard_state(i, j, self.__currentPieceState)
                list2.append((i, j))
                list3.append((i, j))
                return True

        return False

    def change_state(self):
        if self.__currentPieceState == ChessboardState.BLACK:
            self.__currentPieceState = ChessboardState.WHITE
        else:
            self.__currentPieceState = ChessboardState.BLACK