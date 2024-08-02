import pygame
from pygame import mixer
from player import Player

mixer.init()
pygame.init()

# Game Configs
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pyter")

# Set Framerate
clock = pygame.time.Clock()
FPS = 60

# Define Game Variables
intro_count =  3
last_count_update = pygame.time.get_ticks()
score = [0, 0] # Player Scores [Player1, Player2]
round_over = False
ROUND_OVER_CD = 3000

# Define Fighter Variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load Music and FX
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)

magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.5)


# Define Font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# Function to Draw Text
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Load BG Image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# Scale BG Image
scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load Victory Image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Load Spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Define Number of Steps in Each Animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Create player instances.
player1 = Player(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
player2 = Player(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

# Def Draw HP Bar
def draw_hp_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, "black", (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, "red", (x, y, 400, 30))
    pygame.draw.rect(screen, "green", (x, y, 400 * ratio, 30))


run = True
# Game Loop
while run:
    clock.tick(FPS)

    # Draw Background
    screen.blit(scaled_bg, (0, 0))

    # Show Player Stats
    draw_hp_bar(player1.hp, 20, 20)
    draw_hp_bar(player2.hp, 580, 20)
    draw_text(f"{str(score[0])}", score_font, "RED", 20, 60)
    draw_text(f"{str(score[1])}", score_font, "RED", 970, 60)

    # Game Intro
    if intro_count <= 0:
        # Player Movements
        player1.move(SCREEN_WIDTH, SCREEN_HEIGHT, player2, round_over)
        player2.move(SCREEN_WIDTH, SCREEN_HEIGHT, player1, round_over)
    else:
        # Update Timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
        draw_text(str(intro_count), count_font, "RED", SCREEN_WIDTH/2, SCREEN_HEIGHT / 3)  

    # Update Players
    player1.update()
    player2.update()

    # Draw Players
    player1.draw(screen)
    player2.draw(screen)

    # Check Player Defeat
    if round_over == False:
        if player1.dead == True:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif player2.dead == True:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_CD:
            round_over = False
            intro_count = 4
            player1 = Player(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
            player2 = Player(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

    # Event Handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update Display
    pygame.display.update()

pygame.quit()