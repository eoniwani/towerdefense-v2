import math
import pygame
import random

# 색상 정의
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

class Enemy:
    def __init__(self, x, y, enemy_type=1):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.path_index = 0
        self.radius = 15
        
        # 적 타입별 설정
        if enemy_type == 1:
            self.health = 30
            self.max_health = 30
            self.speed = 2
            self.color = RED
            self.reward = 10
        elif enemy_type == 2:
            self.health = 60
            self.max_health = 60
            self.speed = 1.5
            self.color = PURPLE
            self.reward = 20
        elif enemy_type == 3:
            self.health = 15
            self.max_health = 15
            self.speed = 3
            self.color = ORANGE
            self.reward = 15
        else:  # enemy_type == 4 (미니 보스)
            self.health = 200
            self.max_health = 200
            self.speed = 1
            self.color = BLACK
            self.reward = 100
            self.radius = 25
        
        # 경로 설정 (화면 왼쪽에서 오른쪽으로)
        self.path = [
            (0, 350), (200, 350), (200, 200), (400, 200),
            (400, 500), (600, 500), (600, 300), (800, 300),
            (800, 450), (1000, 450)
        ]
    
    def move(self):
        if self.path_index < len(self.path) - 1:
            target_x, target_y = self.path[self.path_index + 1]
            dx = target_x - self.x
            dy = target_y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < 10:
                self.path_index += 1
            else:
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
    
    def draw(self, screen):
        # 적 그리기
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # 체력바 그리기
        health_ratio = self.health / self.max_health
        bar_width = 30
        bar_height = 5
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.radius - 10
        
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height))
    
    def reached_end(self):
        return self.path_index >= len(self.path) - 1 