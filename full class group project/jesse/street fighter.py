#street fighter
#by jesse 😛

import pygame
#chat how do i use pygame
import sys

pygame.init()

#constants
FPS=60

#fighters

# -- CLASSES --
class Game:
    def __init__(self):
        self.player1=Player1(ryu)
        self.player2=Player2(ken)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Street Fighter")
        self.clock = pygame.time.Clock()
    
    def run(self):
        running = True
        while running:
            #print("Running...")
            self.clock.tick(FPS)  # Controls frame rate

            # --- Event Handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # --- Key Input ---
            keys = pygame.key.get_pressed()
            self.player1.handle_input(keys, pygame.K_a, pygame.K_d, pygame.K_w)
            self.player2.handle_input(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)

            # --- Update ---
            self.player1.update(gravity=1)
            self.player2.update(gravity=1)

            # --- Draw ---
            self.screen.fill((100, 149, 237))  # Background color (Cornflower Blue)
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)

            # --- Display ---
            pygame.display.flip()

        # --- Quit ---
        pygame.quit()
        sys.exit()

class Fighter:
    def __init__(self, name, hp, atk, speed, jumpheight=25):
        self.name = name
        self.hp = hp
        self.maxhp = hp
        self.atk = atk
        self.speed = speed
        self.jumpheight = jumpheight
        self.is_attacking = False
        self.is_jumping = False
        self.yVel = 0
        self.direction = 'right'
        
        #use a rectangle for position and size
        self.rect = pygame.Rect(100, 300, 50, 100)  # x, y, width, height
        
        #visual placeholder
        self.color = (255, 255, 255)

        #input state
        self.moving_left = False
        self.moving_right = False

    def move(self):
        if self.moving_left:
            self.rect.x -= self.speed
        if self.moving_right:
            self.rect.x += self.speed

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.yVel = -self.jumpheight  # Going up

    def apply_gravity(self, gravity, floor_y):
        if self.is_jumping:
            self.yVel += gravity
            self.rect.y += self.yVel
            if self.rect.y >= floor_y:
                self.rect.y = floor_y
                self.is_jumping = False
                self.yVel = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
#players
class Player1:
    def __init__(self, fighter):
        self.fighter=fighter

    def handle_input(self, keys, left, right, jump):
        self.fighter.moving_left = keys[left]
        self.fighter.moving_right = keys[right]
        if keys[jump]:
            self.fighter.jump()

    def update(self, gravity):
        self.fighter.move()
        self.fighter.apply_gravity(gravity, floor_y=300)

    def draw(self, screen):
        self.fighter.draw(screen)

class Player2:
    def __init__(self, fighter):
        self.fighter=fighter
        
    def handle_input(self, keys, left, right, jump):
        self.fighter.moving_left = keys[left]
        self.fighter.moving_right = keys[right]
        if keys[jump]:
            self.fighter.jump()

    def update(self, gravity):
        self.fighter.move()
        self.fighter.apply_gravity(gravity, floor_y=300)

    def draw(self, screen):
        self.fighter.draw(screen)

#fighters
ryu = Fighter("Ryu", 100, 10, 5)
ken = Fighter("Ken", 100, 10, 5)





if __name__ == "__main__":
    game = Game()
    game.run()
