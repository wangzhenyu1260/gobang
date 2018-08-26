#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
from sys import exit
from consts import *
from gobang import GoBang
from render import GameRender
from gobang_ai import GobangAI

if __name__ == '__main__':
    for i in range(N + 1):
        for j in range(N + 1):
            list_all.append((i, j))

    gobang = GoBang()
    render = GameRender(gobang)
    ai = GobangAI(gobang, ChessboardState.WHITE)
    result = ChessboardState.EMPTY
    enable_ai = True

    while True:
        # pygame event handle
        for event in pygame.event.get():
            # quit
            if event.type == QUIT:
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                # human move
                if render.one_step():
                    # success
                    result = gobang.get_chess_result()
                else:
                    continue
                if result != ChessboardState.EMPTY:
                    break
                if enable_ai:
                    # AI move
                    ai.one_step()
                    result = gobang.get_chess_result()
                else:
                    render.change_state()

        # render
        render.draw_chess()
        render.draw_mouse()

        if result != ChessboardState.EMPTY:
            render.draw_result(result)

        # update
        pygame.display.update()
