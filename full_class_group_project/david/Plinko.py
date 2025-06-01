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
        WIDTH = 400
        HEIGHT = 500
        GRAVITY = 9.8
        #---------------
        BALL_COLOR = YELLOW
        BALL_RADIUS = 10
        #---------------
        PEG_RADIUS = 5
        PEG_SPACING = 50

    class Controls:
        def __init__(self):
            self.drop = pygame.K_SPACE
            self.quit = pygame.K_ESCAPE
        
        def handle_event(self, event):
            if event.type == pygame.KEYDOWN:
                if event.key == self.drop:
                    print("Drop key pressed")
                elif event.key == self.quit:
                    pygame.quit()
                    exit()
        
    def __init__(self):
        self.screen = pygame.display.set_mode((self.Settings.WIDTH, self.Settings.HEIGHT), pygame.DOUBLEBUF | pygame.NOFRAME)
        self.controls = self.Controls()

    class Page:
        class Ball:
            def __init__(self, x, y):
                self.x = x
                self.y = y
                self.radius = SetUp.Settings.BALL_RADIUS
                self.color = SetUp.Settings.BALL_COLOR

            def draw(self, screen):
                pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

        class BoardNPegs:
            def __init__(self):
    
                # Create the board's boundries:
                self.boundaries = [
                    pygame.Rect(0, 0, SetUp.Settings.WIDTH, SetUp.Settings.HEIGHT),
                    pygame.Rect(0, 0, SetUp.Settings.WIDTH, SetUp.Settings.HEIGHT)
                ]
                
                # Create the board's pegs:
                self.pegs = []
                height = SetUp.Settings.HEIGHT
                width = SetUp.Settings.WIDTH
                spacing = SetUp.Settings.PEG_SPACING

                offset = spacing // 2

                for row, y in enumerate(range(0, height, spacing)):
                    for col, x in enumerate(range(0, width, spacing)):
                        if row % 2 == 0:
                            self.pegs.append((x + offset, y))
                        else:
                            self.pegs.append((x, y))

                self.pegs = [pygame.Rect(x - SetUp.Settings.PEG_RADIUS, y - SetUp.Settings.PEG_RADIUS,
                                         SetUp.Settings.PEG_RADIUS * 2, SetUp.Settings.PEG_RADIUS * 2) for x, y in self.pegs]
                
            def draw(self, screen):
                for peg in self.pegs:
                    pygame.draw.circle(screen, WHITE, peg.center, SetUp.Settings.PEG_RADIUS)

                for boundary in self.boundaries:
                    pygame.draw.rect(screen, BLUE, boundary, 5)


if __name__ == "__main__":

    pygame.init()
    setup = SetUp()
    board = setup.Page.BoardNPegs()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                SetUp.Controls().handle_event(event)

        setup.screen.fill(BLACK)
        board.draw(setup.screen)
        pygame.display.flip()