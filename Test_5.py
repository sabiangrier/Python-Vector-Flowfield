#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 19:22:17 2023

@author: sabiangrier
"""

import pygame
import heapq

# Constants
GRID_SIZE = 20
WIDTH = 800
HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (255, 255, 255)
OBSTACLE_COLOR = (0, 0, 0)
FLOW_COLOR = (200, 200, 200)
BALL_COLOR = (255, 0, 0)
FONT_COLOR = (0, 0, 0)
FONT_SIZE = 16

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, FONT_SIZE)

# Grid class
class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[0] * cols for _ in range(rows)]
        self.obstacles = set()

    def is_valid(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def add_obstacle(self, row, col):
        if self.is_valid(row, col):
            self.obstacles.add((row, col))

    def remove_obstacle(self, row, col):
        if self.is_valid(row, col):
            self.obstacles.remove((row, col))

    def is_obstacle(self, row, col):
        return (row, col) in self.obstacles

    def compute_flow_field(self, start_row, start_col):
        # Initialize distances to infinity
        distances = [[float('inf')] * self.cols for _ in range(self.rows)]

        # Initialize priority queue for breadth-first walk
        queue = [(0, start_row, start_col)]
        heapq.heapify(queue)
        distances[start_row][start_col] = 0

        # Perform breadth-first walk
        while queue:
            dist, row, col = heapq.heappop(queue)

            # Check neighbors
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = row + dr, col + dc

                # Ignore invalid cells or obstacles
                if not self.is_valid(new_row, new_col) or self.is_obstacle(new_row, new_col):
                    continue

                new_dist = dist + 1

                # Update distance and enqueue neighbor
                if new_dist < distances[new_row][new_col]:
                    distances[new_row][new_col] = new_dist
                    heapq.heappush(queue, (new_dist, new_row, new_col))

        return distances

    def draw(self, flow_field=None, ball_pos=None):
        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw obstacles
        for row, col in self.obstacles:
            pygame.draw.rect(screen, OBSTACLE_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Draw flow field
        if flow_field is not None:
            for row in range(self.rows):
                for col in range(self.cols):
                    value = flow_field[row][col]
                    pygame.draw.rect(screen, FLOW_COLOR, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                    text_surface = font.render(str(value), True, FONT_COLOR)
                    screen.blit(text_surface, (col * GRID_SIZE + GRID_SIZE // 2 - text_surface.get_width() // 2,
                                               row * GRID_SIZE + GRID_SIZE // 2 - text_surface.get_height() // 2))

        # Draw ball
        if ball_pos is not None:
            row, col = ball_pos
            pygame.draw.circle(screen, BALL_COLOR,
                               (col * GRID_SIZE + GRID_SIZE // 2, row * GRID_SIZE + GRID_SIZE // 2),
                               GRID_SIZE // 2)

        # Update the screen
        pygame.display.flip()

# Initialize grid
grid = Grid(HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE)
flow_field = None
ball_pos = None
placing_obstacles = False

# Game loop
running = True

while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            row = mouse_pos[1] // GRID_SIZE
            col = mouse_pos[0] // GRID_SIZE

            if event.button == 1:  # Left click to add/remove obstacles
                if placing_obstacles:
                    grid.remove_obstacle(row, col)
                else:
                    grid.add_obstacle(row, col)
            elif event.button == 3:  # Right click to compute flow field
                placing_obstacles = False
                flow_field = grid.compute_flow_field(row, col)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Press SPACE to toggle obstacle placement mode
                placing_obstacles = not placing_obstacles
                flow_field = None  # Reset flow field when switching modes
                ball_pos = None

    # Update and render
    if flow_field is not None and ball_pos is not None:
        row, col = ball_pos
        value = flow_field[row][col]

        # Move the ball towards the neighbor with the smallest distance
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc

            if grid.is_valid(new_row, new_col) and flow_field[new_row][new_col] < value:
                ball_pos = (new_row, new_col)
                break

    grid.draw(flow_field, ball_pos)
    clock.tick(FPS)

# Quit the game
pygame.quit()

