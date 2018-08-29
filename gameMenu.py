#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame


class GameMenu:
    # Define the initalize self options
    def __init__(self, start=0, *options):
        self.options = options
        self.x = 0
        self.y = 0
        self.font = pygame.font.Font(None, 32)
        self.option = start
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [0, 0, 0]
        self.height = len(options) * self.font.get_height()
        for o in options:
            text = o[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    # Draw the menu
    def draw(self, surface):
        i = 0
        for o in self.options:
            if i == self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o[0]
            ren = self.font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, (self.x, self.y + i * self.font.get_height()))
            i += 1

    # Handle events
    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.option -= 1
                elif e.key == pygame.K_DOWN:
                    self.option += 1
                elif e.key == pygame.K_RETURN:
                    self.options[self.option][1]()
            if self.option > len(self.options) - 1:
                self.option = 0
            elif self.option < 0:
                self.option = len(self.options) - 1

    # Position of menu
    def set_pos(self, x, y):
        self.x = x
        self.y = y

    # Font Style
    def set_font(self, font):
        self.font = font
        for o in self.options:
            text = o[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    # Highlight Color
    def set_highlight_color(self, color):
        self.hcolor = color

    # Font Color
    def set_normal_color(self, color):
        self.color = color

    # Font position
    def center_at(self, x, y):
        self.x = x - (self.width / 2)
        self.y = y - (self.height / 2)
