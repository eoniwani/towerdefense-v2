import math
import pygame

YELLOW = (255, 255, 0)

class Bullet:
    def __init__(self, x, y, target_x, target_y, damage):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.damage = damage
        self.speed = 8
        self.radius = 10
        
        # 목표까지의 방향 계산
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed
        else:
            self.vel_x = 0
            self.vel_y = 0
    
    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y
    
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
    
    def hit_target(self, target):
        distance = math.sqrt((self.x - target.x)**2 + (self.y - target.y)**2)
        return distance <= target.radius + self.radius 