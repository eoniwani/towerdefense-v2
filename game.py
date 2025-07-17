import pygame
import math
import random
import json
import os
from enemy import Enemy
from tower import Tower
from bullet import Bullet

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("타워 디펜스 - 아이들과 함께!")
        self.clock = pygame.time.Clock()
        
        self.enemies = []
        self.towers = []
        self.bullets = []
        
        self.money = 1500
        self.lives = 10
        self.score = 0
        self.wave = 1
        self.frame_count = 0
        self.enemy_spawn_timer = 0
        self.enemies_in_wave = 30  # 기존 15에서 2배로 증가
        self.enemies_spawned = 0
        self.boss_spawned = False
        # self.boss_spawn_point = random.randint(int(self.enemies_in_wave * 0.3), int(self.enemies_in_wave * 0.7))
        
        # 한글 지원 폰트 설정
        self.font = self.get_korean_font(36)
        self.small_font = self.get_korean_font(24)
        
        self.selected_tower_pos = None
        self.placing_tower = False
        self.tower_build_mode = True  # 기본적으로 타워 건설 모드 활성화
        self.last_click_time = 0
        self.click_debounce_time = 100  # 100ms 디바운싱
        self.tower_cost = 450  # 타워 비용을 상수로 정의
        
        # 최고 점수 로드
        self.high_score = self.load_high_score()
        
        # 커서 설정
        self.default_cursor = pygame.SYSTEM_CURSOR_ARROW
        self.hand_cursor = pygame.SYSTEM_CURSOR_HAND
        self.update_cursor()
    
    def get_korean_font(self, size):
        korean_fonts = [
            '/System/Library/Fonts/AppleSDGothicNeo.ttc',
            '/System/Library/Fonts/Apple SD Gothic Neo.ttc',
            '/Library/Fonts/NanumGothic.ttf',
            '/System/Library/Fonts/Helvetica.ttc'
        ]
        korean_fonts.extend([
            'C:/Windows/Fonts/malgun.ttf',
            'C:/Windows/Fonts/gulim.ttc',
            'C:/Windows/Fonts/dotum.ttc'
        ])
        for font_path in korean_fonts:
            try:
                if os.path.exists(font_path):
                    return pygame.font.Font(font_path, size)
            except:
                continue
        try:
            return pygame.font.SysFont('applesystemui', size)
        except:
            try:
                return pygame.font.SysFont('malgungothic', size)
            except:
                try:
                    return pygame.font.SysFont('gulim', size)
                except:
                    return pygame.font.Font(None, size)
    
    def load_high_score(self):
        try:
            if os.path.exists('high_score.json'):
                with open('high_score.json', 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            pass
        return 0
    
    def update_cursor(self):
        """타워 건설 모드에 따라 커서 모양 변경"""
        if self.tower_build_mode:
            pygame.mouse.set_cursor(self.hand_cursor)
        else:
            pygame.mouse.set_cursor(self.default_cursor)
    
    def save_high_score(self):
        try:
            with open('high_score.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass
    
    def spawn_enemy(self):
        # 웨이브 시작 시 보스가 아직 안 나왔으면 바로 스폰
        if not self.boss_spawned:
            boss = Enemy(0, 350, 4)  # 미니보스 타입
            self.enemies.append(boss)
            self.boss_spawned = True
        if self.enemies_spawned < self.enemies_in_wave:
            if self.enemy_spawn_timer <= 0:
                enemy_type = random.choice([1, 2, 3]) if self.wave > 2 else 1
                enemy = Enemy(0, 350, enemy_type)
                self.enemies.append(enemy)
                self.enemies_spawned += 1
                self.enemy_spawn_timer = 30
            else:
                self.enemy_spawn_timer -= 1
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.placing_tower:
                        self.placing_tower = False
                        self.selected_tower_pos = None
                    else:
                        return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                current_time = pygame.time.get_ticks()
                
                if event.button == 1:
                    # 타워 건설 모드 토글 버튼 클릭 (디바운싱 적용)
                    if 10 <= mouse_x <= 160 and 250 <= mouse_y <= 290:
                        if current_time - self.last_click_time > self.click_debounce_time:
                            self.last_click_time = current_time
                            self.tower_build_mode = not self.tower_build_mode
                            self.update_cursor()  # 커서 모양 업데이트
                    # 타워 건설 모드가 활성화되어 있으면 직접 타워 배치 (디바운싱 없음)
                    elif self.tower_build_mode:
                        print(f"건설 모드에서 클릭: 위치({mouse_x}, {mouse_y}), 돈: {self.money}")  # 디버깅
                        
                        if self.money >= self.tower_cost:
                            # UI 영역만 제외하고 어디서나 타워 설치 가능
                            if mouse_x < 200 and mouse_y < 320:
                                print(f"UI 영역 제한: 클릭 위치가 UI 영역에 포함됨")
                            else:
                                tower = Tower(mouse_x, mouse_y)
                                self.towers.append(tower)
                                self.money -= self.tower_cost
                                print(f"타워 건설 완료: 위치({mouse_x}, {mouse_y}), 남은 돈: {self.money}")
                        else:
                            print(f"타워 건설 실패: 돈 부족 (현재: {self.money}, 필요: {self.tower_cost})")
        return True
    
    def update(self):
        self.frame_count += 1
        self.spawn_enemy()
        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.reached_end():
                self.enemies.remove(enemy)
                self.lives -= 1
            elif enemy.health <= 0:
                self.enemies.remove(enemy)
                self.money += enemy.reward
                self.score += enemy.reward * 10
        for tower in self.towers:
            target = tower.find_target(self.enemies)
            bullet = tower.shoot(target, self.frame_count)
            if bullet:
                self.bullets.append(bullet)
        for bullet in self.bullets[:]:
            bullet.move()
            hit = False
            for enemy in self.enemies[:]:
                if bullet.hit_target(enemy):
                    enemy.health -= bullet.damage
                    self.bullets.remove(bullet)
                    hit = True
                    break
            if not hit and (bullet.x < 0 or bullet.x > SCREEN_WIDTH or 
                           bullet.y < 0 or bullet.y > SCREEN_HEIGHT):
                self.bullets.remove(bullet)
        if self.enemies_spawned >= self.enemies_in_wave and self.boss_spawned and len(self.enemies) == 0:
            self.wave += 1
            self.enemies_spawned = 0
            self.boss_spawned = False
            self.enemies_in_wave += min(20 + self.wave * 4, 60)
            self.money += 50
    
    def draw_path(self):
        path = [(0, 350), (200, 350), (200, 200), (400, 200),
                (400, 500), (600, 500), (600, 300), (800, 300),
                (800, 450), (1000, 450)]
        for i in range(len(path) - 1):
            pygame.draw.line(self.screen, GRAY, path[i], path[i + 1], 5)
    
    def draw_ui(self):
        money_text = self.font.render(f"돈: ${self.money}", True, BLACK)
        lives_text = self.font.render(f"생명: {self.lives}", True, BLACK)
        score_text = self.font.render(f"점수: {self.score}", True, BLACK)
        wave_text = self.font.render(f"웨이브: {self.wave}", True, BLACK)
        high_score_text = self.font.render(f"최고 점수: {self.high_score}", True, BLACK)
        self.screen.blit(money_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))
        self.screen.blit(score_text, (10, 90))
        self.screen.blit(wave_text, (10, 130))
        self.screen.blit(high_score_text, (10, 170))
        tower_cost_text = self.small_font.render(f"타워 비용: ${self.tower_cost}", True, BLACK)
        self.screen.blit(tower_cost_text, (10, 210))
        # 타워 건설 모드 토글 버튼
        btn_color = GREEN if self.tower_build_mode else RED
        pygame.draw.rect(self.screen, btn_color, (10, 250, 150, 40))
        btn_text = self.small_font.render("타워 건설 모드", True, WHITE)
        self.screen.blit(btn_text, (20, 255))
        
        # 타워 건설 모드 상태 표시
        if self.tower_build_mode:
            mode_text = self.small_font.render("건설 모드 활성화!", True, GREEN)
            self.screen.blit(mode_text, (10, 295))
        else:
            mode_text = self.small_font.render("건설 모드 비활성화", True, RED)
            self.screen.blit(mode_text, (10, 295))
        if self.tower_build_mode:
            controls_text = self.small_font.render("조작: 건설 모드 활성화 - 원하는 위치를 클릭하여 타워 배치", True, BLACK)
        else:
            controls_text = self.small_font.render("조작: 타워 건설 모드 버튼을 클릭한 후 원하는 위치를 클릭하여 타워 배치", True, BLACK)
        self.screen.blit(controls_text, (10, 650))
        if self.lives <= 0:
            game_over_text = self.font.render("게임 오버! ESC를 눌러 종료하세요", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
    
    def draw(self):
        self.screen.fill(WHITE)
        self.draw_path()
        for tower in self.towers:
            tower.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        # 타워 건설 모드 시 마우스 위치에 타워 범위 원 시각화
        if self.tower_build_mode:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # UI 영역이 아닌 곳에만 범위 표시
            if not (mouse_x < 200 and mouse_y < 320):
                # 타워 범위 원 그리기
                tower_range = 100
                tower_radius = 20
                
                # 반투명 범위 원 (공격 가능 범위)
                range_surface = pygame.Surface((tower_range * 2, tower_range * 2), pygame.SRCALPHA)
                pygame.draw.circle(range_surface, (0, 255, 0, 60), (tower_range, tower_range), tower_range)
                self.screen.blit(range_surface, (mouse_x - tower_range, mouse_y - tower_range))
                
                # 범위 테두리 원
                pygame.draw.circle(self.screen, (0, 255, 0), (mouse_x, mouse_y), tower_range, 2)
                
                # 타워 위치 표시 (이미지 또는 원)
                if Tower.tower_image is not None:
                    # 타워 이미지가 있으면 반투명하게 표시
                    tower_preview = Tower.tower_image.copy()
                    tower_preview.set_alpha(150)  # 반투명 효과
                    image_rect = tower_preview.get_rect(center=(mouse_x, mouse_y))
                    self.screen.blit(tower_preview, image_rect)
                else:
                    # 이미지가 없으면 기존 원으로 표시
                    pygame.draw.circle(self.screen, (0, 255, 0), (mouse_x, mouse_y), tower_radius, 2)
                    pygame.draw.circle(self.screen, (0, 255, 0, 100), (mouse_x, mouse_y), tower_radius)
        self.draw_ui()
        pygame.display.flip()
    
    def run(self):
        running = True
        while running and self.lives > 0:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        if self.lives <= 0:
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
            pygame.time.wait(3000)
        pygame.quit() 