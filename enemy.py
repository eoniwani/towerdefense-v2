import math
import pygame
import random
import os

# 색상 정의
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)

class Enemy:
    # 클래스 변수로 적 이미지들 저장 (한 번만 로드)
    enemy_images = {}
    def __init__(self, x, y, enemy_type=1):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.path_index = 0
        self.radius = 15
        
        # 적 이미지 로드 (처음 생성될 때만)
        if not Enemy.enemy_images:
            self.load_enemy_images()
        
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
    
    def load_enemy_images(self):
        """적 이미지들을 로드하고 크기 조정"""
        try:
            # enemy_1.png 로드
            image_path = os.path.join("assets", "enemy_1.png")
            if os.path.exists(image_path):
                original_image = pygame.image.load(image_path)
                # 더 크게 조정: 45x45 크기로 변경
                Enemy.enemy_images[1] = pygame.transform.scale(original_image, (45, 45))
                print(f"적 이미지 로드 완료: {image_path}")
            else:
                print(f"적 이미지 파일을 찾을 수 없음: {image_path}")
            
            # enemy2.png 로드 (타입 2용)
            image_path_2 = os.path.join("assets", "enemy2.png")
            if os.path.exists(image_path_2):
                original_image_2 = pygame.image.load(image_path_2)
                Enemy.enemy_images[2] = pygame.transform.scale(original_image_2, (45, 45))
                print(f"적 이미지 로드 완료: {image_path_2}")
            else:
                print(f"적 이미지 파일을 찾을 수 없음: {image_path_2}")
                
            # 다른 적 타입들도 같은 이미지 사용 (색상 변경)
            if 1 in Enemy.enemy_images:
                base_image = Enemy.enemy_images[1]
                
                # 타입 2가 이미지 없으면 색상 변경 버전 사용
                if 2 not in Enemy.enemy_images:
                    purple_image = base_image.copy()
                    purple_image.fill(PURPLE, special_flags=pygame.BLEND_MULT)
                    Enemy.enemy_images[2] = purple_image
                
                # 타입 3: 주황색 색조
                orange_image = base_image.copy()
                orange_image.fill(ORANGE, special_flags=pygame.BLEND_MULT)
                Enemy.enemy_images[3] = orange_image
                
                # 타입 4 (보스): 검은색 색조 + 더 큰 사이즈
                black_image = base_image.copy()
                black_image.fill(BLACK, special_flags=pygame.BLEND_MULT)
                Enemy.enemy_images[4] = pygame.transform.scale(black_image, (70, 70))
                
        except Exception as e:
            print(f"적 이미지 로드 실패: {e}")
            Enemy.enemy_images = {}
    
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
        if self.enemy_type in Enemy.enemy_images:
            # 이미지가 있으면 이미지로 그리기
            enemy_image = Enemy.enemy_images[self.enemy_type]
            image_rect = enemy_image.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(enemy_image, image_rect)
        else:
            # 이미지가 없으면 기존 원으로 그리기
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # 체력바 그리기
        health_ratio = self.health / self.max_health
        bar_width = 35  # 체력바도 약간 크게
        bar_height = 6
        bar_x = self.x - bar_width // 2
        # 이미지 크기에 맞춰 체력바 위치 조정
        bar_y = self.y - 30 if self.enemy_type == 4 else self.y - 25
        
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height))
    
    def reached_end(self):
        return self.path_index >= len(self.path) - 1 