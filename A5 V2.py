import pygame, sys, random
import pygame.freetype  # Import the freetype module.

# Troop types. They differ by cost, image, health, attack, and speed.
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
    cost = 5
    def __init__(self, image):
        self.pos = 0
        self.image = image
        self.health = 30
        self.attack = 0.2
        self.speed = 4
        self.in_battle = False


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
    robot = Robot(robot_image)
    alien_image = pygame.image.load("alien.png").convert_alpha()
    alien = Alien(alien_image)


    player1_gold = 50
    build_list = []
    computer_build_list = []
    player1_troops = []
    computer_troops = []

    # Use a font for text on screen
    GAME_FONT = pygame.freetype.SysFont('Consolas',18)


    done = False
    while not done:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Process key presses as events so as to capture all key presses
            # rather than just those while looking.

            # Depending on the key press, add different troops to the
            # build_list
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if player1_gold > Robot.cost:
                        player1_gold -= Robot.cost
                        build_list.append(Robot(robot_image))

        # add a bit of gold to the player1 supply
        player1_gold += 0.06

        # Pull a ready object from the factory queue
        if frame_count%30 == 0:
            if build_list:
                new_troop = build_list.pop(0)
                player1_troops.append(new_troop)
        # Add computer troops
            if random.randint(1,100) > 60:
                computer_troops.append(Alien(alien_image))

        # Advance troops that are not engaged in battle
        print(frame_count)
        for troop in player1_troops:
            print(troop)
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

        # Draw the troops
        for troop in player1_troops:
            troop.rect = troop.image.get_rect()
            troop.rect.move_ip((troop.pos, 200))
            screen.blit(troop.image, troop.rect)
            draw_health_bar(screen, troop.health, troop.rect)

        for troop in computer_troops:
            troop.rect = troop.image.get_rect()
            troop.rect.move_ip((600-troop.pos, 200))
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

        # Get damage
        for troop in player1_troops:
            if troop.in_battle:
                troop.health -= troop.in_battle.attack

        for troop in computer_troops:
            if troop.in_battle:
                troop.health -= troop.in_battle.attack

        # Remove dead troops. Use a list comprehension to do this by keeping healthy troops.
        player1_troops = [troop for troop in player1_troops if troop.health > 0]

        computer_troops = [troop for troop in computer_troops if troop.health > 0]

        frame_count += 1
        # Bring drawn changes to the front
        pygame.display.flip()
        pygame.event.peek()
        # set fps
        clock.tick(30)
    # Wait for an event to quit.
    # This also helps a strange issue where the final frame from above
    # doesn't seem to show until after the pygame.quit - for example
    # if a delay is added here instead of the wait.
    # pygame.time.delay(3000)
    pygame.event.clear()
    #pygame.event.wait()
    pygame.quit()
    sys.exit()

main()
