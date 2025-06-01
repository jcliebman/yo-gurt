# Written by David Alexander | May 31, 2025
import pygame

# Standard Constants:
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class SetUp:

    class Settings:
        WIDTH = 800
        HEIGHT = 600
        GRAVITY = 9.8
        #---------------
        BALL_COLOR = YELLOW
        BALL_RADIUS = 10
        #---------------
        PEG_RADIUS = 5
        PEG_SPACING = 50

    class Pages:
        def __init__(self):
            self.start_page = "Start Page"
            self.game_page = "Game Page"
            self.end_page = "End Page"

        def display_startpage(self):
            print("Displaying Start Page")

        def display_game_page(self):
            print("Displaying Game Page")

        def display_end_page(self):
            print("Displaying End Page")

    class Controls:
        def __init__(self):
            self.left = pygame.K_a
            self.right = pygame.K_d
            self.drop = pygame.K_SPACE
            self.quit = pygame.K_ESCAPE
        
        def handle_event(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == self.left:
                    print("Left key pressed")
                elif event.key == self.right:
                    print("Right key pressed")
                elif event.key == self.drop:
                    print("Drop key pressed")
                elif event.key == self.quit:
                    print("Quit key pressed")
        
    def __init__(self):
        self.screen = pygame.display.set_mode((self.Settings.WIDTH, self.Settings.HEIGHT))
        pygame.display.set_caption("Plinko")
        self.controls = self.Controls()
        self.pages = self.pages()

        
if __name__ == "__main__":

    pygame.init()
    setup = SetUp()
    controls = setup.controls
    
    ON = True
    while ON:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ON = False
            if event.type == pygame.KEYDOWN:
                controls.handle_event(event)
        
        

        setup.screen.fill(BLACK)
        pygame.display.flip()

    pygame.quit()