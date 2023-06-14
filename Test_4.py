#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 18:53:20 2023

@author: sabiangrier
"""

import pygame
from collections import deque

# Define constants
WIDTH = 800
HEIGHT = 600
GRID_SIZE = 50
ROWS = HEIGHT // GRID_SIZE
COLS = WIDTH // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid")

# Create grid
grid = [[0] * COLS for _ in range(ROWS)]

# Initialize variables
start_pos = None
obstacle_positions = set()

# Helper function to get grid coordinates from mouse position
def get_grid_pos(x, y):
    row = y // GRID_SIZE
    col = x // GRID_SIZE
    return row, col

# Helper function to draw the grid
def draw_grid():
    screen.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if grid[row][col] == 1:
                pygame.draw.rect(screen, GREEN, rect)
            elif grid[row][col] > 1:
                pygame.draw.rect(screen, BLUE, rect)
                if display_option == 0:
                    font = pygame.font.Font(None, 20)
                    text = font.render(str(grid[row][col]), True, BLACK)
                    text_rect = text.get_rect(center=rect.center)
                    screen.blit(text, text_rect)
                elif display_option == 1:
                    arrow_surface = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
                    arrow_shape = get_arrow_shape(row, col)
                    pygame.draw.polygon(arrow_surface, BLACK, arrow_shape)
                    arrow_rotated = pygame.transform.rotate(arrow_surface, -90)
                    arrow_rect = arrow_rotated.get_rect(center=rect.center)
                    screen.blit(arrow_rotated, arrow_rect)

# Helper function to get the arrow shape based on the smallest distance neighbor
def get_arrow_shape(row, col):
    neighbors = [
        ((row - 1, col), 'up'),
        ((row + 1, col), 'down'),
        ((row, col - 1), 'left'),
        ((row, col + 1), 'right')
    ]
    min_distance = float('inf')
    min_direction = None
    for neighbor, direction in neighbors:
        n_row, n_col = neighbor
        if 0 <= n_row < ROWS and 0 <= n_col < COLS and grid[n_row][n_col] < min_distance:
            min_distance = grid[n_row][n_col]
            min_direction = direction
    
    arrow_points = []
    if min_direction == 'up':
        arrow_points = [(GRID_SIZE // 2, GRID_SIZE // 4), (GRID_SIZE - GRID_SIZE // 4, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE - GRID_SIZE // 4)]
    elif min_direction == 'down':
        arrow_points = [(GRID_SIZE // 2, GRID_SIZE - GRID_SIZE // 4), (GRID_SIZE - GRID_SIZE // 4, GRID_SIZE // 2), (GRID_SIZE // 4, GRID_SIZE // 2)]
    elif min_direction == 'left':
        arrow_points = [(GRID_SIZE // 4, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE - GRID_SIZE // 4), (GRID_SIZE // 2, GRID_SIZE // 4)]
    elif min_direction == 'right':
        arrow_points = [(GRID_SIZE - GRID_SIZE // 4, GRID_SIZE // 2), (GRID_SIZE // 2, GRID_SIZE - GRID_SIZE // 4), (GRID_SIZE // 2, GRID_SIZE // 4)]
    
    return arrow_points

# Helper function to perform breadth-first search
def breadth_first_search(start):
    queue = deque([(start, 0)])
    visited = set([start])
    while queue:
        pos, distance = queue.popleft()
        row, col = pos
        grid[row][col] = distance
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for neighbor in neighbors:
            n_row, n_col = neighbor
            if 0 <= n_row < ROWS and 0 <= n_col < COLS and grid[n_row][n_col] != 1 and (n_row, n_col) not in visited:
                visited.add((n_row, n_col))
                queue.append(((n_row, n_col), distance + 1))

# Game loop
running = True
display_option = 0  # 0: Numerical distance, 1: Arrow pointing to neighbor
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                row, col = get_grid_pos(x, y)
                if grid[row][col] != 2:
                    grid[row][col] = 1
                    obstacle_positions.add((row, col))
            elif pygame.mouse.get_pressed()[2]:
                x, y = pygame.mouse.get_pos()
                row, col = get_grid_pos(x, y)
                if grid[row][col] != 1:
                    if start_pos:
                        grid[start_pos[0]][start_pos[1]] = 0
                    grid[row][col] = 2
                    start_pos = (row, col)
                    # Perform breadth-first search
                    breadth_first_search(start_pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                display_option = (display_option + 1) % 2

    draw_grid()
    pygame.display.update()

# Quit the game
pygame.quit()


