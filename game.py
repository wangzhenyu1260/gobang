#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
from sys import exit
from consts import *
from gobang import GoBang
from render import GameRender
from gobang_ai import GobangAI
from gameMenu import GameMenu

pygame.init()
pygame.display.set_caption("My Gobang")
screen = pygame.display.set_mode((530, 530))
pygame.mouse.set_visible(0)

# Background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((100, 100, 255))


def game():
    gobang = GoBang()
    render = GameRender(gobang)
    result = ChessboardState.EMPTY
    enable_ai = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == MOUSEBUTTONDOWN:
                if render.one_step():
                    result = gobang.get_chess_result()
                else:
                    continue
                if result != ChessboardState.EMPTY:
                    break
                if enable_ai:
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


def game_ai():
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


def gameOver():
    # Game over screen
    menuTitle = GameMenu(["GAME OVER"])
    menuTitle.set_font(pygame.font.Font(None, 80))
    menuTitle.center_at(270, 230)
    menuTitle.set_highlight_color((255, 255, 255))

    info = GameMenu(["Press ESC back to menu"])
    info.set_font(pygame.font.Font(None, 40))
    info.center_at(270, 350)
    info.set_highlight_color((255, 255, 255))

    keepGoing = True
    while keepGoing:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
            elif event.type == pygame.QUIT:
                keepGoing = False

        menuTitle.draw(screen)
        info.draw(screen)
        pygame.display.flip()


# Functions
def option1():
    game_ai()


def option2():
    game()


def option3():
    pygame.quit()
    exit()


def main():
    menuTitle = GameMenu(["My Gobang"])

    menu = GameMenu(
        ["Human VS. AI", option1],
        ["Human VS. Human", option2],
        ["Exit", option3])

    # Title
    menuTitle.set_font(pygame.font.Font(None, 60))
    menuTitle.center_at(270, 150)
    menuTitle.set_highlight_color((255, 255, 255))
    # Menu settings
    menu.center_at(270, 320)
    menu.set_highlight_color((255, 255, 255))
    menu.set_normal_color((200, 200, 255))
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)

        # Events
        events = pygame.event.get()

        # Update Menu
        menu.update(events)

        # Handle quit event
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                return

        # Draw
        screen.blit(background, (0, 0))
        menu.draw(screen)
        menuTitle.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
