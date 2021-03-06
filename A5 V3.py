# Ivan Lee u1059105
# Penny Kite u1215780

import pygame, sys, random
import pygame.freetype  # Import the freetype module.

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

# Troop types. They differ by cost, image, health, attack, and speed.
class Robot:
    def __init__(self, image, position):
        self.pos = 0
        self.image = image
        self.rect = self.image.get_rect()
        self.health = 50
        self.attack = 0.5
        self.speed = 2
        self.in_battle = False
        self.cost = 50

        x_pos, y_pos = position

        startY = 128
        startX = 128
        space_height = 64
        space_width = 64

        row = (y_pos - startY) // space_height
        col = (x_pos - startX) // space_width

        self.y_position = startY + space_height * row
        self.x_position = startX + space_width * col

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class WeakBot(Robot):
    def __init__(self, image, position):
        super().__init__(image, position)
        self.health = 50
        self.attack = 0.2

class StrongBot(Robot):
    def __init__(self, image, position):
        super().__init__(image, position)
        self.health = 100
        self.attack = 0.7

class Alien:
    def __init__(self, image):
        self.pos = 0
        self.image = image
        self.rect = self.image.get_rect()
        self.health = 50
        self.attack = 0.5
        self.speed = 2
        self.in_battle = False
        self.y_position = random.randint(1, 5) * self.rect.height

class SpeedyAlien(Alien):
    def __init__(self, image):
        super().__init__(image)
        self.speed = 4
        self.health = 50
        self.attack = 0.2

class BigBoiAlien(Alien):
    def __init__(self, image):
        super().__init__(image)
        self.speed = 1
        self.health = 100
        self.attack = 0.7

# UI

class Button:
    def __init__(self, rect, command):
        self.rect = pygame.Rect(rect)
        self.image = pygame.Surface(self.rect.size).convert()
        self.image.fill((200,100,0))
        self.function = command

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.function()

    def draw(self, surf):
        surf.blit(self.image, self.rect)

def button_pressed():
    print("Button was pressed")

class Home:
    def __init__(self, rect, house):
        self.rect = rect
        self.house = house
        self.house = pygame.draw.rect(self.rect, (200, 160, 100, 255), (0, 0, 40, 600))

#use a range for the mouse clicking

# Draw the little bar above showing health
def draw_health_bar(screen, health, position_rect):
    health_bar = position_rect.copy()
    health_bar.height = 5
    health_bar.y -= position_rect.h/2 - 25
    pygame.draw.rect(screen, (50,50,50), health_bar, 1)
    health_bar.width = health_bar.width * health / 100
    pygame.draw.rect(screen, (50,250,50), health_bar)

# The main game setup and loop.
def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))

    frame_count = 0

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Load images
    robot_image = pygame.image.load("robot.png").convert_alpha()
    alien_image = pygame.image.load("alien.png").convert_alpha()

    player1_gold = 50
    build_list = []
    computer_build_list = []
    player1_troops = []
    computer_troops = []

    # Use a font for text on screen
    GAME_FONT = pygame.freetype.SysFont('Consolas',18)

    fast_button = pygame.draw.rect(screen, (200, 100, 0, 255), (50, 50, 105, 25))
    slow_button = pygame.draw.rect(screen, (200, 100, 0, 255), (200, 50, 105, 25))

    fast_store = False
    slow_store = False

    done = False
    while not done:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            mouse_position = pygame.mouse.get_pos()
            # Process key presses as events so as to capture all key presses
            # rather than just those while looking.
            # Depending on the key press, add different troops to the
            # build_list
            if event.type == pygame.MOUSEBUTTONDOWN:
                if fast_button.collidepoint(mouse_position) and int(player1_gold) >= 50 and fast_store == False:
                    player1_gold -= 50
                    fast_store = True
                elif fast_store == True:
                    x_pos, y_pos = mouse_position
                    if x_pos > 64 and y_pos > 64 and x_pos < 600 and y_pos < 600:
                        player1_troops.append(WeakBot(robot_image, mouse_position))
                        fast_store = False

                if slow_button.collidepoint(mouse_position) and int(player1_gold) >= 100 and slow_store == False:
                    player1_gold -= 100
                    slow_store = True
                elif slow_store == True:
                    x_pos, y_pos = mouse_position
                    if x_pos > 64 and y_pos > 64 and x_pos < 600 and y_pos < 600:
                        player1_troops.append(StrongBot(robot_image, mouse_position))
                        slow_store = False

        player1_gold += 1.5

        # Pull a ready object from the factory queue
        if frame_count%30 == 0:
            if random.randint(1,100) > 95:
                computer_troops.append(BigBoiAlien(alien_image))
            if random.randint(1,100) > 85:
                computer_troops.append(SpeedyAlien(alien_image))

        for troop in player1_troops:
            if not troop.in_battle:
                troop.pos += troop.speed
            troop.in_battle = False

        for troop in computer_troops:
            if not troop.in_battle:
                troop.pos += troop.speed
            troop.in_battle = False

        # Erase the screen
        screen.fill((150, 200, 150))
        GAME_FONT.render_to(screen, (40, 20), "Gold: " + str(int(player1_gold)), (200, 100, 120))

        fast_button = pygame.draw.rect(screen, (100, 100, 0, 255), (50, 50, 105, 25))
        slow_button = pygame.draw.rect(screen, (100, 100, 0, 255), (200, 50, 105, 25))

        # Draw the troops
        for troop in player1_troops:
            troop.rect = troop.image.get_rect()
            troop.rect.move_ip((troop.x_position, troop.y_position))
            troop.draw(screen)
            draw_health_bar(screen, troop.health, troop.rect)

        for troop in computer_troops:
            troop.rect = troop.image.get_rect()
            troop.rect.move_ip((600-troop.pos, troop.y_position))
            screen.blit(troop.image, troop.rect)
            draw_health_bar(screen, troop.health, troop.rect)

        # Check for combat
        for troop in player1_troops:
            for enemy in computer_troops:
                if troop.rect.colliderect(enemy.rect):
                    # kind of nasty. Use in_battle False to mean
                    # not in battle. Else use it to track
                    # who we are fighting.
                    # Don't overwrite the enemy if already found.
                    # I hope this means the oldest troop in a pile gets hit.
                    if not troop.in_battle:
                        troop.in_battle = enemy
                    if not enemy.in_battle:
                        enemy.in_battle = troop

        home = Home(screen, house='house')

        # Get damage
        for troop in player1_troops:
            if troop.in_battle:
                troop.health -= troop.in_battle.attack

        for troop in computer_troops:
            if troop.in_battle:
                troop.health -= troop.in_battle.attack

        for troop in computer_troops:
            if troop.rect.colliderect(home.house):
                done = True

        # Remove dead troops. Use a list comprehension to do this by keeping healthy troops.
        player1_troops = [troop for troop in player1_troops if troop.health > 0]

        computer_troops = [troop for troop in computer_troops if troop.health > 0]

        frame_count += 1
        # UI
        pygame.display.update()
        # Bring drawn changes to the front
        pygame.display.flip()
        pygame.event.peek()
        # set fps
        clock.tick(30)

    pygame.event.clear()
    pygame.quit()
    sys.exit()

main()
