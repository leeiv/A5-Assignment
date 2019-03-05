# Ivan Lee u1059105
# Penny Kite uu1215780

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


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))

    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Load images
    frog_image = pygame.image.load("wizard.png").convert_alpha()

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
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                for animal in animals:
                    if animal.rect.collidepoint(mouse_pos):
                        animal.timer = 0


        # Decrease the timer
        for animal in animals:
            animal.draw(screen)


        # Remove animals with a timer <= 0

        # add in animals
        if random.randint(0, 100) > 95:
            animal = Field(5, 5, 100, 50, frog_image)
            animals.append(animal)

        # Erase the screen
        screen.fill((150, 200, 150))
        GAME_FONT.render_to(screen, (40, 20), "Score: " + str(score), (200, 100, 120))

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
