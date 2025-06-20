
import pygame, sys, random, math

from pygame.locals import *

pygame.init()


def main():
    width = 1000
    height = 600
    collector_speed = 0
    falling_speed = 2

    score = 0

    screen = pygame.display.set_mode((width, height), 0, 32)

    clock = pygame.time.Clock()

    pygame.time.set_timer(USEREVENT + 1, 1000)

    background = pygame.Surface((1000, 600))  # Placeholder for wonderland image
    background.fill((0, 255, 0))  # Green color for the placeholder

    fallingitem = pygame.Surface((70, 70))  # Placeholder for drinkme image
    fallingitem.fill((255, 0, 0))  # Red color for the placeholder

    collector = pygame.Surface((150, 225))  # Placeholder for alice image
    collector.fill((0, 0, 255))  # Blue color for the placeholder

    font = pygame.font.Font(None, 72)

    maddhatter = pygame.Surface((150, 225))  # Placeholder for madhatter image
    maddhatter.fill((255, 255, 0))  # Yellow color for the placeholder

    hatterhat = pygame.Surface((70, 70))  # Placeholder for hat image
    hatterhat.fill((255, 128, 0))  # Orange color for the placeholder

    redcastle = pygame.Surface((1000, 600))  # Placeholder for castle image
    redcastle.fill((255, 0, 0))  # Red color for the placeholder

    redqueen = pygame.Surface((150, 225))  # Placeholder for queen image
    redqueen.fill((255, 192, 203))  # Pink color for the placeholder

    queenofhearts = pygame.Surface((70, 70))  # Placeholder for cards image
    queenofhearts.fill((128, 0, 128))  # Purple color for the placeholder

    whitecastlewhite = pygame.Surface((1000, 600))  # Placeholder for whitecastle image
    whitecastlewhite.fill((255, 255, 255))  # White color for the placeholder

    whitequeenwhite = pygame.Surface((175, 225))  # Placeholder for whitequeen image
    whitequeenwhite.fill((192, 192, 192))  # Light gray color for the placeholder

    whitecrown = pygame.Surface((50, 50))  # Placeholder for crown image
    whitecrown.fill((255, 215, 0))  # Golden color for the placeholder

    pygame.mixer.music.load("Themesong.mp3")
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)

    falling_x = random.randrange(0, width - 70)
    falling_y = -25

    background_x = 0
    background_y = 0

    alice_x = width / 2
    alice_y = height - 250

    done = False

    while not done:

        clock.tick(60)
        alice_rect = collector.get_rect()
        alice_rect.top = alice_y
        alice_rect.left = alice_x

        falling_rect = fallingitem.get_rect()
        falling_rect.top = falling_y
        falling_rect.left = falling_x

        if alice_rect.colliderect(falling_rect):
            falling_x = random.randrange(0, width)
            falling_y = -25
            score += 1

        if score <= 5:  # level 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        collector_speed = 10
                    if event.key == pygame.K_LEFT:
                        collector_speed = -10
                    if event.key == pygame.K_ESCAPE:
                        done = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        collector_speed = 0

            alice_x += collector_speed

            falling_y += falling_speed
            if falling_y > height:
                gameover = font.render('You lost!!!', 1, Color('white'))
                screen.blit(gameover, (width / 2, height / 2))
                main()

        if 5 < score <= 10:

            falling_speed = 5

            collector = maddhatter

            fallingitem = hatterhat

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        collector_speed = 10
                    if event.key == pygame.K_LEFT:
                        collector_speed = -10
                    if event.key == pygame.K_ESCAPE:
                        done = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        collector_speed = 0

            alice_x += collector_speed

            falling_y += falling_speed
            if falling_y > height:
                gameover = font.render('You lost!!!', 1, Color('white'))
                screen.blit(gameover, (width / 2, height / 2))
                main()

        if 10 < score <= 15:

            falling_speed = 7

            background = redcastle

            collector = redqueen

            fallingitem = queenofhearts

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        collector_speed = 10
                    if event.key == pygame.K_LEFT:
                        collector_speed = -10
                    if event.key == pygame.K_ESCAPE:
                        done = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        collector_speed = 0

            alice_x += collector_speed

            falling_y += falling_speed

            if falling_y > height:
                gameover = font.render('You lost!!!', 1, Color('white'))
                screen.blit(gameover, (width / 2, height / 2))
                main()

        if 15 < score <= 20:

            background = whitecastlewhite

            collector = whitequeenwhite

            fallingitem = whitecrown

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        collector_speed = 10
                    if event.key == pygame.K_LEFT:
                        collector_speed = -10
                    if event.key == pygame.K_ESCAPE:
                        done = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        collector_speed = 0

            alice_x += collector_speed

            falling_speed = 9
            falling_y += falling_speed
            if falling_y > height:
                gameover = font.render('You lost!!!', 1, Color('white'))
                screen.blit(gameover, (width / 2, height / 2))
                main()

        if 20 < score <= 30:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        collector_speed = 10
                    if event.key == pygame.K_LEFT:
                        collector_speed = -10
                    if event.key == pygame.K_ESCAPE:
                        done = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        collector_speed = 0

            alice_x += collector_speed

            falling_speed = 12
            falling_y += falling_speed
            if falling_y > height:
                gameover = font.render('You lost!!!', 1, Color('white'))
                screen.blit(gameover, (width / 2, height / 2))
                main()

        if score > 30:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        collector_speed = 10
                    if event.key == pygame.K_LEFT:
                        collector_speed = -10
                    if event.key == pygame.K_ESCAPE:
                        done = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        collector_speed = 0

            alice_x += collector_speed

            falling_speed = 18
            falling_y += falling_speed
            if falling_y > height:
                gameover = font.render('You lost!!!', 1, Color('white'))
                screen.blit(gameover, (width / 2, height / 2))
                main()

        if alice_x > width:
            alice_x = 0

        if alice_x < 0:
            alice_x = width

        screen.blit(background, (0, 0))

        screen.blit(collector, (alice_x, alice_y))

        screen.blit(fallingitem, (falling_x, falling_y))

        score_text = font.render(" Score: {}".format(score), 1, Color('white'))

        screen.blit(score_text, (width - 300, 20))

        pygame.display.flip()

    pygame.quit()


main()