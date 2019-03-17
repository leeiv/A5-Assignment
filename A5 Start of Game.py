# Ivan Lee u1059105
# Penny Kite u1215780

import pygame, sys, random
import pygame.freetype  # Import the freetype module.import random, pygame

class Field:
    def __init__(self, max_rows, max_cols, startx, starty, image):
        # An animal shows up in a random row and col for a random number of frames.
        self.image = image
        row = random.randrange(0, max_rows)
        col = random.randrange(0, max_cols)
        self.timer = random.randrange(50, 200)
        self.rect = self.image.get_rect()

        # Calculate the x, y location of the top left corner of the Animal
        # Add your code here
        x = startx + col*self.rect.width
        y = starty + row*self.rect.width

        # Then use the x,y to shift the rectangle there.
        self.rect.topleft = (x,y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def decrease_timer(self):
        self.timer -= 1

class Robot:
    cost = 20
    def __init__(self, image):
        self.pos = 0
        self.image = image
        self.health = 100
        self.attack = 0.5
        self.speed = 2
        self.in_battle = False


class Alien:
    cost = 20
    def __init__(self, image):
        self.pos = 0
        self.image = image
        self.health = 100
        self.attack = 0.5
        self.speed = 2
        self.in_battle = False
        self.y_position = random.randint(1, 5) * 64

def draw_health_bar(screen, health, position_rect):
    health_bar = position_rect.copy()
    health_bar.height = 5
    health_bar.y -= position_rect.h/2 - 25
    pygame.draw.rect(screen, (50,50,50), health_bar, 1)
    health_bar.width = health_bar.width * health / 100
    pygame.draw.rect(screen, (50,250,50), health_bar)

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))

    build_list = []
    player1_troops = []
    computer_troops = []

    robot_image = pygame.image.load("robot.png").convert_alpha()
    robot = Robot(robot_image)
    alien_image = pygame.image.load("alien.png").convert_alpha()
    alien = Alien(alien_image)

    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Load images
    # frog_image = pygame.image.load("wizard.png").convert_alpha()

    # Use a font for text on screen
    GAME_FONT = pygame.freetype.SysFont('Consolas',18)

    animals = []

    done = False
    score = 0

    while not done:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Look for a mouse click event
            # if event.type == pygame.MOUSEBUTTONUP:
            #     mouse_pos = pygame.mouse.get_pos()
            #     for animal in animals:
            #         if animal.rect.collidepoint(mouse_pos):
            #             animal.timer = 0

        if frame_count % 30 == 0:
            # if build_list:
            #     new_troop = build_list.pop(0)
            #     player1_troops.append(new_troop)
            # Add computer troops
            if random.randint(1, 100) > 60:
                computer_troops.append(Alien(alien_image))


        # Advance troops that are not engaged in battle
        print(frame_count)
        # for troop in player1_troops:
        #     print(troop)
        #     if not troop.in_battle:
        #         troop.pos += troop.speed
        #     troop.in_battle = False

        for troop in computer_troops:
            if not troop.in_battle:
                troop.pos += troop.speed
            troop.in_battle = False

        # Erase the screen
        screen.fill((150, 200, 150))
        GAME_FONT.render_to(screen, (40, 20), "Score: " + str(score), (200, 100, 120))

        # Decrease the timer
        for animal in animals:
            animal.draw(screen)

        # Remove animals with a timer <= 0

        # add in animals
        if random.randint(0, 100) > 95:
            animal = Field(5, 5, 50, 50, robot_image)  # this places the animals in columns (5) and rows (5)
            animals.append(animal)


        # Draw the troops
        for troop in player1_troops:
            troop.rect = troop.image.get_rect()
            troop.rect.move_ip((troop.pos, 200))
            screen.blit(troop.image, troop.rect)
            draw_health_bar(screen, troop.health, troop.rect)

        for troop in computer_troops:
            troop.rect = troop.image.get_rect()
            troop.rect.move_ip((600 - troop.pos, troop.y_position))
            screen.blit(troop.image, troop.rect)
            draw_health_bar(screen, troop.health, troop.rect)

        # Check for combat
        for troop in player1_troops:
            for enemy in computer_troops:
                if troop.rect.colliderect(enemy.rect):
                    if not troop.in_battle:
                        troop.in_battle = enemy
                    if not enemy.in_battle:
                        enemy.in_battle = troop

        for troop in player1_troops:
            if troop.in_battle:
                troop.health -= troop.in_battle.attack

        for troop in computer_troops:
            if troop.in_battle:
                troop.health -= troop.in_battle.attack

        player1_troops = [troop for troop in player1_troops if troop.health > 0]

        computer_troops = [troop for troop in computer_troops if troop.health > 0]


        # Draw the animals
        for animal in animals:
            animal.draw(screen)

        frame_count += 1
        # Bring drawn changes to the front
        pygame.display.flip()
        pygame.event.peek()
        # set fps
        clock.tick(30)

    # Wait for an event to quit.
    pygame.quit()
    sys.exit()

main()
