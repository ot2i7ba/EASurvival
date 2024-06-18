import pygame
import pygame_gui
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN_SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Early Access Scam MMO v0.1x (4sshooter) by ot2i7ba")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
TRANSPARENT_BLACK = (0, 0, 0, 128)

# Fonts
FONT_SIZE_SMALL = 22  # 40% smaller than before
FONT_SIZE_EXP = 20  # Font size for experience points
FONT_SIZE_TITLE = 40  # Font size for the title
FONT_SIZE_COPYRIGHT = 18  # Font size for the copyright notice
FONT_SIZE_GITHUB = 14  # Font size for the GitHub link
font = pygame.font.SysFont(None, FONT_SIZE_SMALL)
exp_font = pygame.font.SysFont(None, FONT_SIZE_EXP)
title_font = pygame.font.SysFont(None, FONT_SIZE_TITLE)
copyright_font = pygame.font.SysFont(None, FONT_SIZE_COPYRIGHT)
github_font = pygame.font.SysFont(None, FONT_SIZE_GITHUB)

# Initialize GUI manager
manager = pygame_gui.UIManager(SCREEN_SIZE)

# Create GUI elements
title_label = title_font.render("Early Access Scam MMO", True, BLACK)
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
    'Muschi': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 200), (300, 30)),
                                           text='Muschi',
                                           manager=manager),
    'Normal': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 230), (300, 30)),
                                           text='Normal',
                                           manager=manager),
    'Bürgergeldempfänger': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 260), (300, 30)),
                                                        text='Bürgergeldempfänger',
                                                        manager=manager)
}
class_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((250, 300), (300, 30)),
                                          text='Class:',
                                          manager=manager)
class_buttons = {
    'Flameboy': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 330), (300, 30)),
                                             text='Flameboy',
                                             manager=manager),
    'Propellerkind': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 360), (300, 30)),
                                                  text='Propellerkind',
                                                  manager=manager),
    'Bundeskanzler': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 390), (300, 30)),
                                                  text='Bundeskanzler',
                                                  manager=manager),
    'Klimakleber': pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 420), (300, 30)),
                                                text='Klimakleber',
                                                manager=manager)
}
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((250, 470), (300, 50)),
                                            text='Start',
                                            manager=manager)

# Initialize player information
PLAYER_SIZE = 50
PLAYER_COLOR = (0, 128, 255)
PLAYER_SPEED = 5
player_pos = [WIDTH // 2, HEIGHT // 2]

# Initialize enemy information
ENEMY_SIZE = 50
ENEMY_COLOR = RED
ENEMY_SPEED = PLAYER_SPEED * 0.75  # Enemies are 25% slower than the player

def get_random_enemy_pos():
    return [random.randint(0, WIDTH - ENEMY_SIZE), random.randint(0, HEIGHT - ENEMY_SIZE)]

enemy_pos = get_random_enemy_pos()

# Enemy movement logic
def move_enemy(player_pos, enemy_pos, enemy_speed):
    enemy_dx = player_pos[0] - enemy_pos[0]
    enemy_dy = player_pos[1] - enemy_pos[1]
    distance = (enemy_dx ** 2 + enemy_dy ** 2) ** 0.5
    
    if distance < 150:  # If the player is closer than 150 pixels
        if distance > 0:
            enemy_dx /= distance
            enemy_dy /= distance
        # Move in the opposite direction to the player
        enemy_pos[0] -= enemy_dx * enemy_speed
        enemy_pos[1] -= enemy_dy * enemy_speed
    else:  # If the player is farther away, the enemy moves randomly
        move_direction = random.choice(["left", "right", "up", "down", "circle", "stop"])
        if move_direction == "left":
            enemy_pos[0] -= enemy_speed
        elif move_direction == "right":
            enemy_pos[0] += enemy_speed
        elif move_direction == "up":
            enemy_pos[1] -= enemy_speed
        elif move_direction == "down":
            enemy_pos[1] += enemy_speed
        elif move_direction == "circle":
            angle = random.uniform(0, 2 * 3.14159)
            enemy_pos[0] += enemy_speed * 0.5 * random.choice([-1, 1])
            enemy_pos[1] += enemy_speed * 0.5 * random.choice([-1, 1])
        elif move_direction == "stop":
            pass  # Stays still

    # Limit the enemy position to the screen area
    enemy_pos[0] = max(0, min(WIDTH - ENEMY_SIZE, enemy_pos[0]))
    enemy_pos[1] = max(0, min(HEIGHT - ENEMY_SIZE, enemy_pos[1]))
    return enemy_pos

# Initialize player status
experience_points = 0
level = 1
next_level_exp = 100
game_started = False
player_name = ''
difficulty = ''
player_class = ''
show_death_message_flag = False
death_message = ""
death_message_start_time = 0

# Game time and random death
start_time = 0
last_death_time = 0
death_time = random.randint(15, 30)
lives = 3
total_play_time = 0

death_messages = [
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

def check_collision(player_pos, enemy_pos):
    player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], ENEMY_SIZE, ENEMY_SIZE)
    return player_rect.colliderect(enemy_rect)

def update_experience():
    global experience_points, level, next_level_exp
    experience_points += 10
    if experience_points >= next_level_exp:
        experience_points -= next_level_exp
        level += 1
        next_level_exp = int(next_level_exp * 1.1)

def reset_game():
    global experience_points, level, next_level_exp, player_pos, enemy_pos, start_time, last_death_time, death_time, lives, game_started, show_death_message_flag, death_message
    experience_points = 0
    level = 1
    next_level_exp = 100
    player_pos = [WIDTH // 2, HEIGHT // 2]
    enemy_pos = get_random_enemy_pos()
    start_time = time.time()
    last_death_time = start_time
    death_time = random.randint(15, 30)
    lives = 3
    game_started = True
    show_death_message_flag = False
    death_message = ""

def show_game_over_screen():
    global game_started, total_play_time, experience_points, level
    total_play_time = time.time() - start_time
    game_over_message = (f"Game over!\nLevel: {level}\nEXP: {experience_points}\n"
                         f"Total play time: {int(total_play_time)}s")
    game_over_window = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((150, 200), (500, 200)),
        html_text=game_over_message,
        manager=manager
    )
    close_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 450), (100, 50)),
        text='Close',
        manager=manager
    )
    return game_over_window, close_button

def show_death_message():
    global last_death_time, death_time, show_death_message_flag, death_message, death_message_start_time
    elapsed_time = time.time() - start_time
    time_since_last_death = time.time() - last_death_time
    death_message = f"You died because {random.choice(death_messages)}.\n"
    death_message += f"Total play time: {int(elapsed_time)}s\n"
    death_message += f"Time since last death: {int(time_since_last_death)}s"
    show_death_message_flag = True
    death_message_start_time = time.time()
    last_death_time = time.time()
    death_time = random.randint(15, 30)

# Function to manage selections
def reset_selections(category):
    if category == 'difficulty':
        for key in difficulty_buttons:
            difficulty_buttons[key].set_text(key)
    elif category == 'class':
        for key in class_buttons:
            class_buttons[key].set_text(key)

def handle_selection(event_ui_element, category):
    reset_selections(category)
    event_ui_element.set_text('<' + event_ui_element.text + '>')

# Main loop
clock = pygame.time.Clock()
running = True
game_over_window = None
close_button = None
death_window = None
game_over = False

def reset_to_main_menu():
    global game_started, game_over
    game_over = False
    game_started = False
    manager.clear_and_reset()
    name_input.set_text('')
    global player_name, difficulty, player_class
    player_name = ''
    difficulty = ''
    player_class = ''
    # Make GUI elements visible again
    name_label.show()
    name_input.show()
    difficulty_label.show()
    for btn in difficulty_buttons.values():
        btn.show()
    class_label.show()
    for btn in class_buttons.values():
        btn.show()
    start_button.show()

while running:
    time_delta = clock.tick(30) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                player_name = name_input.get_text()
                for key, btn in difficulty_buttons.items():
                    if btn.text.startswith('<'):
                        difficulty = key
                for key, btn in class_buttons.items():
                    if btn.text.startswith('<'):
                        player_class = key

                if player_name and difficulty and player_class:
                    reset_game()

            if event.ui_element in difficulty_buttons.values():
                handle_selection(event.ui_element, 'difficulty')

            if event.ui_element in class_buttons.values():
                handle_selection(event.ui_element, 'class')

            if event.ui_element == close_button:
                if game_over_window:
                    game_over_window.kill()
                    reset_to_main_menu()
                else:
                    death_window.kill()
                    show_death_message_flag = False
                    if lives == 0:
                        game_over_window, close_button = show_game_over_screen()
                        game_over = True
                close_button.kill()
                death_window = None

        manager.process_events(event)

    manager.update(time_delta)

    if game_started and not game_over:
        if not show_death_message_flag:
            elapsed_time = time.time() - start_time
            time_since_last_death = time.time() - last_death_time

            if time_since_last_death >= death_time and not show_death_message_flag:
                lives -= 1
                show_death_message()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - PLAYER_SIZE:
                player_pos[0] += PLAYER_SPEED
            if keys[pygame.K_UP] and player_pos[1] > 0:
                player_pos[1] -= PLAYER_SPEED
            if keys[pygame.K_DOWN] and player_pos[1] < HEIGHT - PLAYER_SIZE:
                player_pos[1] += PLAYER_SPEED

            # Check for collision
            if check_collision(player_pos, enemy_pos):
                update_experience()
                enemy_pos = get_random_enemy_pos()
            
            # Enemy movement (fleeing from the player and random movement)
            enemy_pos = move_enemy(player_pos, enemy_pos, ENEMY_SPEED)

        # Fill screen with white color
        screen.fill(WHITE)

        # Draw the player (a simple square)
        pygame.draw.rect(screen, PLAYER_COLOR, (player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE))
        
        # Draw the enemy
        pygame.draw.rect(screen, ENEMY_COLOR, (enemy_pos[0], enemy_pos[1], ENEMY_SIZE, ENEMY_SIZE))
        
        # Display player's name, difficulty, level, and class
        name_text = font.render(f"Name: {player_name}", True, WHITE)
        difficulty_text = font.render(f"Difficulty: {difficulty}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        class_text = font.render(f"Class: {player_class}", True, WHITE)

        # Draw backgrounds
        for i, text in enumerate([name_text, difficulty_text, level_text, class_text]):
            text_width, text_height = text.get_size()
            bg_rect = pygame.Surface((text_width + 20, text_height + 10), pygame.SRCALPHA)
            bg_rect.fill(TRANSPARENT_BLACK)
            screen.blit(bg_rect, (10, 10 + i * 40))
            screen.blit(text, (20, 15 + i * 40))

        # Display EXP
        exp_text = exp_font.render(f"EXP: {experience_points}", True, WHITE)
        exp_bg_rect = pygame.Surface((exp_text.get_width() + 20, exp_text.get_height() + 10), pygame.SRCALPHA)
        exp_bg_rect.fill(TRANSPARENT_BLACK)
        screen.blit(exp_bg_rect, (WIDTH // 2 - exp_text.get_width() // 2 - 10, HEIGHT - 50))
        screen.blit(exp_text, (WIDTH // 2 - exp_text.get_width() // 2, HEIGHT - 45))

        # Display elapsed time
        elapsed_time_text = font.render(f"Time: {int(elapsed_time)}s", True, WHITE)
        elapsed_time_width, elapsed_time_height = elapsed_time_text.get_size()
        elapsed_time_bg = pygame.Surface((elapsed_time_width + 20, elapsed_time_height + 10), pygame.SRCALPHA)
        elapsed_time_bg.fill(TRANSPARENT_BLACK)
        screen.blit(elapsed_time_bg, (WIDTH - elapsed_time_width - 30, 10))
        screen.blit(elapsed_time_text, (WIDTH - elapsed_time_width - 20, 15))

        # Display remaining lives
        lives_text = font.render(f"Lives: {lives} of 3", True, WHITE)
        lives_width, lives_height = lives_text.get_size()
        lives_bg = pygame.Surface((lives_width + 20, lives_height + 10), pygame.SRCALPHA)
        lives_bg.fill(TRANSPARENT_BLACK)
        screen.blit(lives_bg, (WIDTH - lives_width - 30, 50))
        screen.blit(lives_text, (WIDTH - lives_width - 20, 55))

        # Display death message
        if show_death_message_flag:
            death_msg_text = font.render(death_message, True, WHITE)
            death_msg_width, death_msg_height = death_msg_text.get_size()
            death_msg_bg = pygame.Surface((death_msg_width + 20, death_msg_height + 10), pygame.SRCALPHA)
            death_msg_bg.fill(TRANSPARENT_BLACK)
            screen.blit(death_msg_bg, (WIDTH // 2 - death_msg_width // 2 - 10, HEIGHT // 2 - 50))
            screen.blit(death_msg_text, (WIDTH // 2 - death_msg_width // 2, HEIGHT // 2 - 45))

            # Pause game during death message
            if time.time() - death_message_start_time > 3:
                show_death_message_flag = False
                if lives == 0:
                    game_over_window, close_button = show_game_over_screen()
                    game_over = True

    else:
        screen.fill(WHITE)
        manager.draw_ui(screen)
        screen.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, 30))
        screen.blit(copyright_label, (WIDTH // 2 - copyright_label.get_width() // 2, HEIGHT - 60))
        screen.blit(github_label, (WIDTH // 2 - github_label.get_width() // 2, HEIGHT - 30))
    
    # Update the screen
    pygame.display.flip()
