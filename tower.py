import math
import pygame
import os
from bullet import Bullet

BLUE = (0, 0, 255)

class Tower:
    # 클래스 변수로 이미지 저장 (한 번만 로드)
    tower_image = None
    
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
        
        # 타워 이미지 로드 (첫 번째 타워 생성 시에만)
        if Tower.tower_image is None:
            self.load_tower_image()
    
    def load_tower_image(self):
        """타워 이미지를 로드하고 크기 조정"""
        try:
            # 이미지 파일 경로
            image_path = os.path.join("assets", "tower.png")
            if os.path.exists(image_path):
                # 이미지 로드
                original_image = pygame.image.load(image_path)
                # 기존 원 크기(반지름 20)에 맞춰 40x40 크기로 조정
                Tower.tower_image = pygame.transform.scale(original_image, (40, 40))
                print(f"타워 이미지 로드 완료: {image_path}")
            else:
                print(f"타워 이미지 파일을 찾을 수 없음: {image_path}")
                Tower.tower_image = None
        except Exception as e:
            print(f"타워 이미지 로드 실패: {e}")
            Tower.tower_image = None
    
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
        if Tower.tower_image is not None:
            # 이미지가 있으면 이미지로 그리기
            # 이미지 중심을 타워 위치에 맞춤
            image_rect = Tower.tower_image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(Tower.tower_image, image_rect)
        else:
            # 이미지가 없으면 기존 원으로 그리기
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius) 