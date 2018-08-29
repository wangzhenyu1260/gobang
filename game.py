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

search_depth = 1

def game():
    gobang = GoBang()
    render = GameRender(gobang)
    result = ChessboardState.EMPTY
    enable_ai = False
    keepGoing = True

    while keepGoing:
        for event in pygame.event.get():
            if event.type == QUIT:
                keepGoing = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
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
            # render.draw_result(result)
            gameOver(result)
            keepGoing = False

        # update
        pygame.display.update()


def game_ai():
    del list1[:]
    del list2[:]
    del list3[:]
    del list_all[:]
    for i in range(COLUMN):
        for j in range(ROW):
            list_all.append((i, j))

    gobang = GoBang()
    render = GameRender(gobang)
    ai = GobangAI(gobang, ChessboardState.WHITE, search_depth)
    result = ChessboardState.EMPTY
    enable_ai = True
    keepGoing = True

    while keepGoing:
        # pygame event handle
        for event in pygame.event.get():
            # quit
            if event.type == QUIT:
                keepGoing = False
            elif event.type == KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
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
            # render.draw_result(result)
            gameOver(result)
            keepGoing = False

        # update
        pygame.display.update()


def gameOver(result):
    # Game over screen
    menuTitle = GameMenu(0, ["GAME OVER"])
    menuTitle.set_font(pygame.font.Font(None, 80))
    menuTitle.center_at(270, 200)
    menuTitle.set_highlight_color((255, 255, 255))

    # Game result
    if result == ChessboardState.BLACK:
        tips = "Winner is black"
    elif result == ChessboardState.WHITE:
        tips = "Winner is white"
    else:
        tips = "Tie"
    resInfo = GameMenu(0, [tips])
    resInfo.set_font(pygame.font.Font(None, 60))
    resInfo.center_at(270, 270)
    resInfo.set_highlight_color((255, 0, 0))

    info = GameMenu(0, ["Press ESC back to menu"])
    info.set_font(pygame.font.Font(None, 40))
    info.center_at(270, 320)
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
        resInfo.draw(screen)
        info.draw(screen)
        pygame.display.flip()


def settings():
    # Settings Menu Text
    # Title for Option Menu
    menuTitle = GameMenu(0, ["AI LEVEL"])

    menu = GameMenu(0 if search_depth == 1 else 1, ["Normal", level_option1], ["Hard", level_option2])

    info = GameMenu(0, ["PRESS ESC TO RETURN"])

    # Settings Title Font color, aligment, and font type
    menuTitle.set_font(pygame.font.Font(None, 60))
    menuTitle.center_at(270, 150)
    menuTitle.set_highlight_color((255, 255, 255))

    # Menu settings
    menu.center_at(270, 250)
    menu.set_highlight_color((255, 255, 255))
    menu.set_normal_color((200, 200, 255))

    # Settings info Font color, aligment, and font type
    info.center_at(270, 320)
    info.set_highlight_color((255, 255, 255))
    info.set_normal_color((200, 200, 255))

    clock = pygame.time.Clock()
    keepGoing = True

    while keepGoing:
        clock.tick(30)

        # Events
        events = pygame.event.get()

        # Update Menu
        menu.update(events)

        # Handle input
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    keepGoing = False
                elif event.key == pygame.K_RETURN:
                    keepGoing = False
            elif event.type == QUIT:
                keepGoing = False

        # Draw
        screen.blit(background, (0, 0))
        menuTitle.draw(screen)
        menu.draw(screen)
        info.draw(screen)
        pygame.display.flip()


# Functions
def option1():
    game_ai()


def option2():
    game()


def option3():
    settings()


def option4():
    pygame.quit()
    exit()


def level_option1():
    global search_depth
    search_depth = 1


def level_option2():
    global search_depth
    search_depth = 3


def main():
    menuTitle = GameMenu(0, ["My Gobang"])

    menu = GameMenu(0,
                    ["Human VS. AI", option1],
                    ["Human VS. Human", option2],
                    ["Settings", option3],
                    ["Exit", option4])

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
