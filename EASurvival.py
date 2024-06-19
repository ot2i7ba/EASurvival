import pygame
import pygame_gui
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 700
SCREEN_SIZE = (WIDTH, HEIGHT)
PLAYER_SIZE = 50
PLAYER_COLOR = (0, 128, 255)
PLAYER_SPEED = 5
ENEMY_SIZE = 50
ENEMY_COLOR = (255, 0, 0)  # RED
ENEMY_SPEED = PLAYER_SPEED * 0.75
FONT_SIZE_SMALL = 22
FONT_SIZE_EXP = 20
FONT_SIZE_TITLE = 40
FONT_SIZE_COPYRIGHT = 18
FONT_SIZE_GITHUB = 14
TRANSPARENT_BLACK = (0, 0, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DEATH_MESSAGES = [
    "just because",
    "thirst",
    "hunger",
    "headwind",
    "just so",
    "bug",
    "latency",
    "update",
    "no idea",
    "old age",
    "server restart",
    "screen time"
]

# Fonts
font = pygame.font.SysFont(None, FONT_SIZE_SMALL)
exp_font = pygame.font.SysFont(None, FONT_SIZE_EXP)
title_font = pygame.font.SysFont(None, FONT_SIZE_TITLE)
copyright_font = pygame.font.SysFont(None, FONT_SIZE_COPYRIGHT)
github_font = pygame.font.SysFont(None, FONT_SIZE_GITHUB)

# Initialize GUI manager
manager = pygame_gui.UIManager(SCREEN_SIZE)

# Set screen dimensions and title
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Early Access Scam MMO v0.1.0 (4sshooter) by ot2i7ba")

# Create GUI elements
title_label = title_font.render("Early Access Scam MMO v0.1.0", True, BLACK)
copyright_label = copyright_font.render("sarcastic copyright by ot2i7ba", True, BLACK)
github_label = github_font.render("github.com/ot2i7ba", True, BLACK)

name_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((250, 100), (300, 30)),
                                         text='Name:',
                                         manager=manager)
name_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((250, 130), (300, 30)),
                                                 manager=manager)
difficulty_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((250, 170), (300, 30)),
                                               text='Difficulty:',
                                               manager=manager)
difficulty_buttons = {
    'Lappten': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 200), (300, 30)),
                                            text='Lappten',
                                            manager=manager),
    'Lutscher': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 230), (300, 30)),
                                             text='Lutscher',
                                             manager=manager),
    'Niveaulos': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 260), (300, 30)),
                                              text='Niveaulos',
                                              manager=manager),
    'Normal': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 290), (300, 30)),
                                           text='Normal',
                                           manager=manager)
}
class_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((250, 330), (300, 30)),
                                          text='Class:',
                                          manager=manager)
class_buttons = {
    'Propellerkind': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 360), (300, 30)),
                                                  text='Propellerkind',
                                                  manager=manager),
    'Klimakleber': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 390), (300, 30)),
                                                text='Klimakleber',
                                                manager=manager),
    'Wirtschaftsminister': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 420), (300, 30)),
                                                        text='Wirtschaftsminister',
                                                        manager=manager),
    'Bundeskanzler': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 450), (300, 30)),
                                                  text='Bundeskanzler',
                                                  manager=manager),
    'Wehganer': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 480), (300, 30)),
                                            text='Wehganer',
                                            manager=manager)
}
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 530), (300, 50)),
                                            text='Start',
                                            manager=manager)


def get_random_enemy_pos():
    return [random.randint(0, WIDTH - ENEMY_SIZE), random.randint(0, HEIGHT - ENEMY_SIZE)]


class Player:
    def __init__(self, x, y, size, color, speed):
        self.pos = [x, y]
        self.size = size
        self.color = color
        self.speed = speed

    def move(self, dx, dy):
        self.pos[0] += dx * self.speed
        self.pos[1] += dy * self.speed
        self.pos[0] = max(0, min(WIDTH - self.size, self.pos[0]))
        self.pos[1] = max(0, min(HEIGHT - self.size, self.pos[1]))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.pos, self.size, self.size))

    def get_rect(self):
        return pygame.Rect(*self.pos, self.size, self.size)


class Enemy:
    def __init__(self, x, y, size, color, speed):
        self.pos = [x, y]
        self.size = size
        self.color = color
        self.speed = speed

    def move(self, player_pos):
        enemy_dx = player_pos[0] - self.pos[0]
        enemy_dy = player_pos[1] - self.pos[1]
        distance = (enemy_dx ** 2 + enemy_dy ** 2) ** 0.5

        if distance < 150:
            if distance > 0:
                enemy_dx /= distance
                enemy_dy /= distance
            self.pos[0] -= enemy_dx * self.speed
            self.pos[1] -= enemy_dy * self.speed
        else:
            move_direction = random.choice(["left", "right", "up", "down", "circle", "stop"])
            if move_direction == "left":
                self.pos[0] -= self.speed
            elif move_direction == "right":
                self.pos[0] += self.speed
            elif move_direction == "up":
                self.pos[1] -= self.speed
            elif move_direction == "down":
                self.pos[1] += self.speed
            elif move_direction == "circle":
                self.pos[0] += self.speed * 0.5 * random.choice([-5, 5])
                self.pos[1] += self.speed * 0.5 * random.choice([-5, 5])
            elif move_direction == "stop":
                pass

        self.pos[0] = max(0, min(WIDTH - self.size, self.pos[0]))
        self.pos[1] = max(0, min(HEIGHT - self.size, self.pos[1]))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (*self.pos, self.size, self.size))

    def get_rect(self):
        return pygame.Rect(*self.pos, self.size, self.size)


class Game:
    def __init__(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED)
        self.enemy = Enemy(*get_random_enemy_pos(), ENEMY_SIZE, ENEMY_COLOR, ENEMY_SPEED)
        self.experience_points = 0
        self.level = 1
        self.next_level_exp = 100
        self.game_started = False
        self.player_name = ''
        self.difficulty = ''
        self.player_class = ''
        self.show_death_message_flag = False
        self.death_message = ""
        self.death_message_start_time = 0
        self.start_time = 0
        self.last_death_time = 0
        self.death_time = random.randint(15, 30)
        self.lives = 3
        self.total_play_time = 0
        self.game_over_window = None
        self.close_button = None

    def reset(self):
        self.experience_points = 0
        self.level = 1
        self.next_level_exp = 100
        self.player = Player(WIDTH // 2, HEIGHT // 2, PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED)
        self.enemy = Enemy(*get_random_enemy_pos(), ENEMY_SIZE, ENEMY_COLOR, ENEMY_SPEED)
        self.start_time = time.time()
        self.last_death_time = self.start_time
        self.death_time = random.randint(15, 30)
        self.lives = 3
        self.game_started = True
        self.show_death_message_flag = False
        self.death_message = ""
        self.game_over_window = None
        self.close_button = None

    def reset_to_main_menu(self):
        self.game_started = False
        manager.clear_and_reset()
        name_input.set_text('')
        self.player_name = ''
        self.difficulty = ''
        self.player_class = ''
        name_label.show()
        name_input.show()
        difficulty_label.show()
        for btn in difficulty_buttons.values():
            btn.show()
        class_label.show()
        for btn in class_buttons.values():
            btn.show()
        start_button.show()

    def update_experience(self):
        self.experience_points += 10
        if self.experience_points >= self.next_level_exp:
            self.experience_points -= self.next_level_exp
            self.level += 1
            self.next_level_exp = int(self.next_level_exp * 1.1)

    def show_game_over_screen(self):
        total_play_time = time.time() - self.start_time
        game_over_message = (f"Game over!\nLevel: {self.level}\nEXP: {self.experience_points}\n"
                             f"Total play time: {int(total_play_time)}s")
        self.game_over_window = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((150, 200), (500, 200)),
            html_text=game_over_message,
            manager=manager
        )
        self.close_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 450), (100, 50)),
            text='Close',
            manager=manager
        )

    def show_death_message(self):
        elapsed_time = time.time() - self.start_time
        time_since_last_death = time.time() - self.last_death_time
        self.death_message = f"You died because {random.choice(DEATH_MESSAGES)}.\n"
        self.death_message += f"Total play time: {int(elapsed_time)}s\n"
        self.death_message += f"Time since last death: {int(time_since_last_death)}s"
        self.show_death_message_flag = True
        self.death_message_start_time = time.time()
        self.last_death_time = time.time()
        self.death_time = random.randint(15, 30)

    def check_collision(self):
        return self.player.get_rect().colliderect(self.enemy.get_rect())

    def handle_events(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                self.player_name = name_input.get_text()
                for key, btn in difficulty_buttons.items():
                    if btn.text.startswith('<'):
                        self.difficulty = key
                for key, btn in class_buttons.items():
                    if btn.text.startswith('<'):
                        self.player_class = key

                if self.player_name and self.difficulty and self.player_class:
                    self.reset()

            if event.ui_element in difficulty_buttons.values():
                handle_selection(event.ui_element, 'difficulty')

            if event.ui_element in class_buttons.values():
                handle_selection(event.ui_element, 'class')

            if event.ui_element == self.close_button:
                if self.game_over_window:
                    self.game_over_window.kill()
                    self.reset_to_main_menu()
                self.close_button.kill()
                self.game_started = False

    def update(self):
        if not self.show_death_message_flag:
            elapsed_time = time.time() - self.start_time
            time_since_last_death = time.time() - self.last_death_time

            if time_since_last_death >= self.death_time and not self.show_death_message_flag:
                self.lives -= 1
                if self.lives == 0:
                    self.show_game_over_screen()
                    self.game_started = False
                else:
                    self.show_death_message()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.player.pos[0] > 0:
                self.player.move(-1, 0)
            if keys[pygame.K_RIGHT] and self.player.pos[0] < WIDTH - PLAYER_SIZE:
                self.player.move(1, 0)
            if keys[pygame.K_UP] and self.player.pos[1] > 0:
                self.player.move(0, -1)
            if keys[pygame.K_DOWN] and self.player.pos[1] < HEIGHT - PLAYER_SIZE:
                self.player.move(0, 1)

            if self.check_collision():
                self.update_experience()
                self.enemy = Enemy(*get_random_enemy_pos(), ENEMY_SIZE, ENEMY_COLOR, ENEMY_SPEED)

            self.enemy.move(self.player.pos)

    def draw(self, screen):
        screen.fill(WHITE)
        self.player.draw(screen)
        self.enemy.draw(screen)

        name_text = font.render(f"Name: {self.player_name}", True, WHITE)
        difficulty_text = font.render(f"Difficulty: {self.difficulty}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        class_text = font.render(f"Class: {self.player_class}", True, WHITE)

        for i, text in enumerate([name_text, difficulty_text, level_text, class_text]):
            text_width, text_height = text.get_size()
            bg_rect = pygame.Surface((text_width + 20, text_height + 10), pygame.SRCALPHA)
            bg_rect.fill(TRANSPARENT_BLACK)
            screen.blit(bg_rect, (10, 10 + i * 40))
            screen.blit(text, (20, 15 + i * 40))

        exp_text = exp_font.render(f"EXP: {self.experience_points}", True, WHITE)
        exp_bg_rect = pygame.Surface((exp_text.get_width() + 20, exp_text.get_height() + 10), pygame.SRCALPHA)
        exp_bg_rect.fill(TRANSPARENT_BLACK)
        screen.blit(exp_bg_rect, (WIDTH // 2 - exp_text.get_width() // 2 - 10, HEIGHT - 50))
        screen.blit(exp_text, (WIDTH // 2 - exp_text.get_width() // 2, HEIGHT - 45))

        elapsed_time = time.time() - self.start_time
        elapsed_time_text = font.render(f"Time: {int(elapsed_time)}s", True, WHITE)
        elapsed_time_width, elapsed_time_height = elapsed_time_text.get_size()
        elapsed_time_bg = pygame.Surface((elapsed_time_width + 20, elapsed_time_height + 10), pygame.SRCALPHA)
        elapsed_time_bg.fill(TRANSPARENT_BLACK)
        screen.blit(elapsed_time_bg, (WIDTH - elapsed_time_width - 30, 10))
        screen.blit(elapsed_time_text, (WIDTH - elapsed_time_width - 20, 15))

        lives_text = font.render(f"Lives: {self.lives} of 3", True, WHITE)
        lives_width, lives_height = lives_text.get_size()
        lives_bg = pygame.Surface((lives_width + 20, lives_height + 10), pygame.SRCALPHA)
        lives_bg.fill(TRANSPARENT_BLACK)
        screen.blit(lives_bg, (WIDTH - lives_width - 30, 50))
        screen.blit(lives_text, (WIDTH - lives_width - 20, 55))

        if self.show_death_message_flag:
            death_msg_text = font.render(self.death_message, True, WHITE)
            death_msg_width, death_msg_height = death_msg_text.get_size()
            death_msg_bg = pygame.Surface((death_msg_width + 20, death_msg_height + 10), pygame.SRCALPHA)
            death_msg_bg.fill(TRANSPARENT_BLACK)
            screen.blit(death_msg_bg, (WIDTH // 2 - death_msg_width // 2 - 10, HEIGHT // 2 - 50))
            screen.blit(death_msg_text, (WIDTH // 2 - death_msg_width // 2, HEIGHT // 2 - 45))

            if time.time() - self.death_message_start_time > 3:
                self.show_death_message_flag = False
                if self.lives == 0:
                    self.show_game_over_screen()
                    self.game_started = False


def handle_selection(event_ui_element, category):
    if category == 'difficulty':
        for key in difficulty_buttons:
            difficulty_buttons[key].set_text(key)
    elif category == 'class':
        for key in class_buttons:
            class_buttons[key].set_text(key)
    event_ui_element.set_text('<' + event_ui_element.text + '>')


clock = pygame.time.Clock()
running = True
game = Game()

while running:
    time_delta = clock.tick(30) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        manager.process_events(event)
        game.handle_events(event)

    manager.update(time_delta)
    game.update()

    if not game.game_started:
        screen.fill(WHITE)
        manager.draw_ui(screen)
        screen.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, 30))
        screen.blit(copyright_label, (WIDTH // 2 - copyright_label.get_width() // 2, HEIGHT - 60))
        screen.blit(github_label, (WIDTH // 2 - github_label.get_width() // 2, HEIGHT - 30))
    else:
        game.draw(screen)

    pygame.display.flip()
