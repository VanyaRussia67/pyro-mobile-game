import sys
import random
import pygame

# Инициализация Pygame
pygame.init()

# Настройки экрана (стандартное мобильное соотношение сторон)
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mobile Geometry Dash")
clock = pygame.time.Clock()

# Цвета
BG_COLOR = (15, 20, 40)
FLOOR_COLOR = (40, 50, 80)
PLAYER_COLOR = (0, 255, 200)
SPIKE_COLOR = (255, 50, 100)
TEXT_COLOR = (255, 255, 255)
BTN_COLOR = (50, 150, 255)

# Шрифты
font = pygame.font.SysFont("Arial", 28, bold=True)
large_font = pygame.font.SysFont("Arial", 48, bold=True)

# Физика земли
FLOOR_Y = HEIGHT - 80

# Класс кубика (Игрока)
class Cube:
    def __init__(self):
        self.size = 40
        self.x = 100
        self.y = FLOOR_Y - self.size
        self.gravity = 1.2
        self.jump_force = -18
        self.velocity = 0
        self.is_grounded = True
        self.rotation = 0

    def jump(self):
        if self.is_grounded:
            self.velocity = self.jump_force
            self.is_grounded = False

    def update(self):
        # Применение гравитации
        self.velocity += self.gravity
        self.y += self.velocity

        # Проверка столкновения с землей
        if self.y >= FLOOR_Y - self.size:
            self.y = FLOOR_Y - self.size
            self.velocity = 0
            self.is_grounded = True
            # Выравнивание угла при приземлении
            self.rotation = (self.rotation // 90) * 90
        
        # Анимация вращения в прыжке
        if not self.is_grounded:
            self.rotation += 5

    def draw(self):
        # Отрисовка вращающегося куба
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(surf, PLAYER_COLOR, (0, 0, self.size, self.size), border_radius=6)
        # Внутренний узор кубика (глаза)
        pygame.draw.rect(surf, BG_COLOR, (8, 10, 8, 8), border_radius=2)
        pygame.draw.rect(surf, BG_COLOR, (24, 10, 8, 8), border_radius=2)
        pygame.draw.rect(surf, BG_COLOR, (8, 26, 24, 4), border_radius=2)
        
        rotated_surf = pygame.transform.rotate(surf, -self.rotation)
        new_rect = rotated_surf.get_rect(center=(self.x + self.size//2, self.y + self.size//2))
        screen.blit(rotated_surf, new_rect.topleft)

# Класс препятствия (Шипа)
class Spike:
    def __init__(self, speed):
        self.width = 40
        self.height = 45
        self.x = WIDTH + random.randint(0, 200)
        self.y = FLOOR_Y
        self.speed = speed

    def update(self):
        self.x -= self.speed

    def draw(self):
        # Рисуем треугольный шип
        points = [
            (self.x, self.y),
            (self.x + self.width, self.y),
            (self.x + self.width // 2, self.y - self.height)
        ]
        pygame.draw.polygon(screen, SPIKE_COLOR, points)

    def get_mask_points(self):
        # Точки для точной проверки столкновений
        return [
            pygame.Rect(self.x + 5, self.y - self.height, self.width - 10, self.height)
        ]

# Состояния игры
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2
game_state = STATE_MENU

# Инициализация игровых переменных
player = Cube()
spikes = []
score = 0
game_speed = 7
spawn_timer = 0

# Кнопка перезапуска (для меню и проигрыша)
restart_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 60)

def reset_game():
    global player, spikes, score, game_speed, spawn_timer
    player = Cube()
    spikes = [Spike(game_speed)]
    score = 0
    game_speed = 7
    spawn_timer = 0

# Главный цикл
running = True
while running:
    screen.fill(BG_COLOR)
    
    # Отрисовка земли
    pygame.draw.rect(screen, FLOOR_COLOR, (0, FLOOR_Y, WIDTH, HEIGHT - FLOOR_Y))
    pygame.draw.line(screen, PLAYER_COLOR, (0, FLOOR_Y), (WIDTH, FLOOR_Y), 3)

    # Обработка тач-событий (нажатий на экран)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if game_state == STATE_PLAYING:
                # В самой игре нажатие в ЛЮБОЕ место экрана — это прыжок
                player.jump()
                
            elif game_state == STATE_MENU:
                if restart_btn.collidepoint(mouse_pos):
                    reset_game()
                    game_state = STATE_PLAYING
                    
            elif game_state == STATE_GAMEOVER:
                if restart_btn.collidepoint(mouse_pos):
                    reset_game()
                    game_state = STATE_PLAYING

    # Логика состояний игры
    if game_state == STATE_PLAYING:
        player.update()
        
        # Увеличение сложности со временем
        game_speed += 0.002
        
        # Появление препятствий
        spawn_timer += 1
        if spawn_timer > random.randint(50, 90):
            spikes.append(Spike(game_speed))
            spawn_timer = 0

        # Обновление шипов и проверка столкновений
        player_rect = pygame.Rect(player.x, player.y, player.size, player.size)
        for spike in spikes[:]:
            spike.update()
            if spike.x < -60:
                spikes.remove(spike)
                score += 1
                continue
                
            # Проверка столкновения
            for mask in spike.get_mask_points():
                if player_rect.colliderect(mask):
                    game_state = STATE_GAMEOVER

        # Отрисовка объектов игры
        for spike in spikes:
            spike.draw()
        player.draw()

        # Текущий счет
        score_txt = font.render(f"SCORE: {score}", True, TEXT_COLOR)
        screen.blit(score_txt, (20, 20))

    elif game_state == STATE_MENU:
        title = large_font.render("GEOMETRY DASH", True, PLAYER_COLOR)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 80))
        
        pygame.draw.rect(screen, BTN_COLOR, restart_btn, border_radius=10)
        btn_txt = font.render("START", True, TEXT_COLOR)
        screen.blit(btn_txt, (restart_btn.centerx - btn_txt.get_width() // 2, restart_btn.centery - btn_txt.get_height() // 2))

    elif game_state == STATE_GAMEOVER:
        # Отрисовываем застывший мир на фоне проигрыша
        for spike in spikes:
            spike.draw()
        player.draw()

        # Экран проигрыша
        lost_txt = large_font.render("GAME OVER", True, SPIKE_COLOR)
        screen.blit(lost_txt, (WIDTH // 2 - lost_txt.get_width() // 2, HEIGHT // 2 - 80))
        
        score_txt = font.render(f"FINAL SCORE: {score}", True, TEXT_COLOR)
        screen.blit(score_txt, (WIDTH // 2 - score_txt.get_width() // 2, HEIGHT // 2 - 25))

        pygame.draw.rect(screen, BTN_COLOR, restart_btn, border_radius=10)
        btn_txt = font.render("RETRY", True, TEXT_COLOR)
        screen.blit(btn_txt, (restart_btn.centerx - btn_txt.get_width() // 2, restart_btn.centery - btn_txt.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
