import pygame
import random

pygame.init()
pygame.mixer.init()


# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARKGREY = (105, 105, 105)
BLUE = (0, 0, 255)
YELLOW = (255, 69, 0)

# SCREEN SIZE
SCREENWIDTH = 900
SCREENHEIGHT = 600

# Creating Window
WINDOW = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

# Game Title
pygame.display.set_caption("SNAKE GAME")
pygame.display.update()

FPS = 60
CLOCK = pygame.time.Clock()

# Background
wcimg = pygame.image.load(r"gallery\image\wc.png")
wcimg = pygame.transform.scale(
    wcimg, (SCREENWIDTH, SCREENHEIGHT)).convert_alpha()
bg = pygame.image.load(r"gallery\image\bg2.jpg")
bg = pygame.transform.scale(bg, (SCREENWIDTH, SCREENHEIGHT)).convert_alpha()


def textScreen(text, color, x, y, fsize):
    """Show Text on Screen"""
    FONT = pygame.font.SysFont(None, fsize)
    screen_text = FONT.render(text, True, color)
    WINDOW.blit(screen_text, [int(x), int(y)])


def plotSnake(color1, colorh, s_list, s_length, s_size):
    if len(s_list) > s_length:  # remove head of snake
        del s_list[0]

    for i, j in s_list:  # draw whole snake everytime
        pygame.draw.rect(WINDOW, color1, [i, j, s_size, s_size])

    pygame.draw.rect(WINDOW, colorh, [
                     s_list[len(s_list)-1][0], s_list[len(s_list)-1][1], s_size, s_size])


def readHighScore(filename):
    try:
        with open(filename, "r") as f:
            return int(f.read())
    except FileNotFoundError:
        with open(filename, "w") as f:
            f.write("0")
            return 0


def welcome():
    # Music
    pygame.mixer.music.load(r'gallery\audio\wc.mp3')
    pygame.mixer.music.play(100)
    pygame.mixer.music.set_volume(.6)

    EXITGAME = False
    while not EXITGAME:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    gameLoop()

        WINDOW.blit(wcimg, (0, 0))
        textScreen("Welcome To Snake Game", BLUE,
                   200, SCREENHEIGHT/2 - 50, 60)
        textScreen("Enter to Start Game", BLUE, 250, SCREENHEIGHT/2, 60)
        pygame.display.update()
        CLOCK.tick(FPS)


def gameLoop():
    # Music
    pygame.mixer.music.fadeout(200)
    pygame.mixer.music.load(r'gallery\audio\bgm.mp3')
    pygame.mixer.music.play(100)
    pygame.mixer.music.set_volume(.6)

    # Game Variable
    EXITGAME = False
    GAMEOVER = False
    SNAKESIZE = 30
    SNAKE_X = 45
    SNAKE_Y = 55
    VELOCITY_X = 0
    VELOCITY_Y = 0
    INIT_VELOCITY = 4
    FOOD_X = random.randint(0, SCREENWIDTH - 50)
    FOOD_Y = random.randint(0, SCREENHEIGHT - 50)
    SCORE = 0
    SNAKELIST = []
    SNAKELENGTH = 1
    HIGHSCORE = readHighScore("hscore.txt")
    cheat = False

    # Game Loop
    while not EXITGAME:
        if GAMEOVER:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        gameLoop()
            WINDOW.blit(bg, (0, 0))
            textScreen(f"Score: {SCORE}", RED, 5, 5, 30)
            textScreen(f"High Score: {HIGHSCORE}", RED, 5, 35, 30)
            pygame.draw.rect(
                WINDOW, GREEN, [FOOD_X, FOOD_Y, SNAKESIZE, SNAKESIZE])

            plotSnake(DARKGREY, BLACK, SNAKELIST, SNAKELENGTH, SNAKESIZE)
            textScreen("Game Over!", RED, 325, SCREENHEIGHT/2 - 50, 60)
            textScreen("Enter to Start Again", RED, 250, SCREENHEIGHT/2, 60)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        VELOCITY_X = INIT_VELOCITY
                        VELOCITY_Y = 0  # to move in one direction

                    if event.key == pygame.K_LEFT:
                        VELOCITY_X = -INIT_VELOCITY
                        VELOCITY_Y = 0

                    if event.key == pygame.K_UP:
                        VELOCITY_Y = -INIT_VELOCITY
                        VELOCITY_X = 0

                    if event.key == pygame.K_DOWN:
                        VELOCITY_Y = INIT_VELOCITY
                        VELOCITY_X = 0

                    # cheats
                    if event.key == pygame.K_c:
                        cheat = True  # activate cheats if press c

                    if event.key == pygame.K_d and cheat:
                        SCORE += 10
                        cheat = False

                    if event.key == pygame.K_v and cheat:
                        INIT_VELOCITY -= 1
                        cheat = False

            # Auto movement as while loop directly
            SNAKE_X += VELOCITY_X
            SNAKE_Y += VELOCITY_Y

            # Eat Food
            if abs(SNAKE_X - FOOD_X) < 10 and abs(SNAKE_Y - FOOD_Y) < 10:
                SCORE += 10
                SNAKELENGTH += 5
                if SCORE > HIGHSCORE:
                    with open("hscore.txt", "w") as f:
                        f.write(str(SCORE))
                        HIGHSCORE = SCORE
                FOOD_X = random.randint(0, SCREENWIDTH - 50)
                FOOD_Y = random.randint(0, SCREENHEIGHT - 50)

            # DRAW & UPDATE
            WINDOW.blit(bg, (0, 0))
            textScreen(f"Score: {SCORE}", RED, 5, 5, 30)
            textScreen(f"High Score: {HIGHSCORE}", RED, 5, 35, 30)
            pygame.draw.rect(
                WINDOW, GREEN, [FOOD_X, FOOD_Y, SNAKESIZE, SNAKESIZE])

            head = [SNAKE_X, SNAKE_Y]
            SNAKELIST.append(head)
            plotSnake(DARKGREY, BLACK, SNAKELIST, SNAKELENGTH, SNAKESIZE)

            # Game over conditions
            if head in SNAKELIST[:-1]:
                pygame.mixer.music.load(r'gallery\audio\bgm2.mp3')
                pygame.mixer.music.play(1)
                pygame.mixer.music.set_volume(.6)
                GAMEOVER = True

            if SNAKE_X < 0 or SNAKE_X > SCREENWIDTH or SNAKE_Y < 0 or SNAKE_Y > SCREENHEIGHT:
                pygame.mixer.music.load(r'gallery\audio\bgm2.mp3')
                pygame.mixer.music.play(1)
                pygame.mixer.music.set_volume(.6)
                GAMEOVER = True

        pygame.display.update()
        CLOCK.tick(FPS)


def main():
    welcome()


if __name__ == "__main__":
    main()
