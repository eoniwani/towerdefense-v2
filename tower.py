import math
import pygame
from bullet import Bullet

BLUE = (0, 0, 255)

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.damage = 20
        self.fire_rate = 50  # 프레임 단위
        self.last_shot = 0
        self.radius = 20
        self.color = BLUE
        self.cost = 400
    
    def can_shoot(self, current_frame):
        return current_frame - self.last_shot >= self.fire_rate
    
    def find_target(self, enemies):
        closest_enemy = None
        closest_distance = float('inf')
        
        for enemy in enemies:
            distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
            if distance <= self.range and distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy
        
        return closest_enemy
    
    def shoot(self, target, current_frame):
        if target and self.can_shoot(current_frame):
            self.last_shot = current_frame
            return Bullet(self.x, self.y, target.x, target.y, self.damage)
        return None
    
    def draw(self, screen):
        # 타워 그리기
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius) 