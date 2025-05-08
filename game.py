import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Battle with Asteroids")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Load images for spaceship and enemy ship
spaceship_image = pygame.image.load("C:\\Users\\ADMIN\\Desktop\\gamee\\413.png")
enemy_ship_image = pygame.image.load("C:\\Users\\ADMIN\\Desktop\\gamee\\417336.png")
enemy_ship_image = pygame.transform.scale(enemy_ship_image, (50, 50))

# Spaceship class
class Spaceship:
    def __init__(self):
        self.image = pygame.transform.scale(spaceship_image, (50, 50))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        self.health = 100
        self.hit_timer = 0

    def move(self, dx):
        self.rect.x += dx
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def shoot(self):
        return Laser(self.rect.centerx, self.rect.top, -1)

    def draw_health_bar(self):
        bar_width = 50
        bar_height = 6
        health_ratio = self.health / 100
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.bottom + 10  # Changed to draw below the spaceship
        pygame.draw.rect(window, RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(window, GREEN, (bar_x, bar_y, bar_width * health_ratio, bar_height))

# Asteroid class
class Asteroid:
    def __init__(self):
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 0))

    def fall(self):
        self.rect.y += 5

# Laser class
class Laser:
    def __init__(self, x, y, direction=-1, target_pos=None):
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = 10
        if target_pos:
            dx = target_pos[0] - x
            dy = target_pos[1] - y
            distance = math.sqrt(dx**2 + dy**2)
            self.vel_x = (dx / distance) * self.speed
            self.vel_y = (dy / distance) * self.speed
        else:
            self.vel_x = 0
            self.vel_y = self.speed * direction

    def move(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

# Enemy Ship class
class EnemyShip:
    def __init__(self):
        self.image = pygame.transform.scale(enemy_ship_image, (50, 50))
        self.rect = self.image.get_rect(center=(random.randint(0, WIDTH), 50))
        self.lasers = []
        self.speed = random.choice([-3, 3])
        self.shoot_cooldown = 0
        self.health = 160

    def move(self):
        self.rect.x += self.speed
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed = -self.speed

    def shoot(self, target_pos):
        if self.shoot_cooldown == 0:
            self.lasers.append(Laser(self.rect.centerx, self.rect.bottom, 1, target_pos))
            self.shoot_cooldown = 50
        else:
            self.shoot_cooldown -= 1

    def draw_health_bar(self):
        bar_width = 50
        health_ratio = self.health / 160
        pygame.draw.rect(window, RED, (self.rect.left, self.rect.top - 10, bar_width, 5))
        pygame.draw.rect(window, YELLOW, (self.rect.left, self.rect.top - 10, bar_width * health_ratio, 5))

# Menu screen
def first_menu():
    font_title = pygame.font.Font(None, 64)
    font_instr = pygame.font.Font(None, 36)
    title = font_title.render("Spaceship Battle", True, RED)
    prompt = font_instr.render("PRESS ENTER TO START NEW GAME", True, YELLOW)
    instructions = font_instr.render("PRESS ESC KEY TO EXIT", True, WHITE)
    while True:
        window.fill(BLACK)
        window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        window.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2 - 20))
        window.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN : 
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_RETURN:
                    return
            
    
def main_menu():
    font_title = pygame.font.Font(None, 64)
    font_instr = pygame.font.Font(None, 36)
    title = font_title.render("Spaceship Battle", True, RED)
    instructions = font_instr.render("Use arrow keys to move, SPACE to shoot", True, WHITE)
    prompt = font_instr.render("Press ENTER to start", True, YELLOW)
    
    while True:
        window.fill(BLACK)
        window.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
        window.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2 - 20))
        window.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, HEIGHT // 2 + 40))
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

# Game loop
def main():
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    asteroids = []
    lasers = []
    enemy_ships = []
    score = 0
    running = True
    enemy_spawn_time = 0
    enemy_destroyed_count = 0
    asteroid_hits = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            spaceship.move(-5)
        if keys[pygame.K_RIGHT]:
            spaceship.move(5)
        if keys[pygame.K_SPACE]:
            lasers.append(spaceship.shoot())

        if random.randint(1, 20) == 1:
            asteroids.append(Asteroid())

        if score >= (enemy_destroyed_count + 25) and enemy_spawn_time <= 0:
            enemy_ships.append(EnemyShip())
            enemy_destroyed_count += 25
            enemy_spawn_time = 200

        for asteroid in asteroids[:]:
            asteroid.fall()
            if asteroid.rect.colliderect(spaceship.rect):
                asteroids.remove(asteroid)
                asteroid_hits += 1
                if asteroid_hits == 2:
                    spaceship.health -= 20
                    asteroid_hits = 0
            if asteroid.rect.top > HEIGHT:
                asteroids.remove(asteroid)

        for laser in lasers[:]:
            laser.move()
            if laser.rect.bottom < 0:
                lasers.remove(laser)
                continue

            for asteroid in asteroids[:]:
                if laser.rect.colliderect(asteroid.rect):
                    asteroids.remove(asteroid)
                    lasers.remove(laser)
                    score += 1
                    break

            for enemy in enemy_ships[:]:
                if laser.rect.colliderect(enemy.rect):
                    enemy.health -= 5
                    lasers.remove(laser)
                    if enemy.health <= 0:
                        enemy_ships.remove(enemy)
                        score += 5
                    break

        for enemy in enemy_ships[:]:
            enemy.move()
            enemy.shoot((spaceship.rect.centerx, spaceship.rect.centery))

            for laser in enemy.lasers[:]:
                laser.move()
                if laser.rect.top > HEIGHT or laser.rect.bottom < 0 or laser.rect.left < 0 or laser.rect.right > WIDTH:
                    enemy.lasers.remove(laser)
                elif laser.rect.colliderect(spaceship.rect):
                    spaceship.health -= 25
                    enemy.lasers.remove(laser)

            if enemy.rect.colliderect(spaceship.rect):
                spaceship.hit_timer += 1
                if spaceship.hit_timer >= 300:
                    spaceship.health -= 50
                    spaceship.hit_timer = 0
            else:
                spaceship.hit_timer = 0

        window.fill(BLACK)

        window.blit(spaceship.image, spaceship.rect)
        spaceship.draw_health_bar()

        for asteroid in asteroids:
            window.blit(asteroid.image, asteroid.rect)
        for laser in lasers:
            window.blit(laser.image, laser.rect)
        for enemy in enemy_ships:
            window.blit(enemy.image, enemy.rect)
            enemy.draw_health_bar()
            for laser in enemy.lasers:
                window.blit(laser.image, laser.rect)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Score: {score}', True, WHITE)
        window.blit(score_text, (10, 10))

        if spaceship.health <= 0:
            running = False

        pygame.display.flip()
        clock.tick(60)
        enemy_spawn_time -= 1

    pygame.quit()

if __name__ == "__main__":
    first_menu()
    main_menu()
    main()
