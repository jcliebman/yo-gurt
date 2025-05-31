class pCar():
    def __init__(self,x,y,width,height,player_type):
        self.player_type = player_type

        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.head = 0
        self.velo = 0
        self.targ_velo = 0
        self.reverse = False

        self.image = pygame.image.load("player_car.gif")
        self.image = pygame.transform.scale(self.image, (self.width, self.height)) 
        self.og_image = self.image

    def forward(self):
        self.x -= self.velo * math.cos(math.radians(self.head))
        self.y += self.velo * math.sin(math.radians(self.head))
      
    def turn_right(self): # the ability to turn is hindered at higher speeds
        if self.fast_enough():
            adj_turn = TURN_STEP / (1 + REDUCTION_K * abs(self.velo))
            self.head -= adj_turn

            if abs(self.velo) > 0.5: # speed isn't lost too much at very low speeds
                self.velo *= VELO_TURN_LOSS
            else:
                self.targ_velo = self.velo

    def turn_left(self):  # the ability to turn is hindered at higher speeds
        if self.fast_enough():
            adj_turn = TURN_STEP / (1 + REDUCTION_K * abs(self.velo))
            self.head += adj_turn

            if abs(self.velo) > 0.5: # speed isn't lost too much at very low speeds
                self.velo *= VELO_TURN_LOSS
            else:
                self.targ_velo = self.velo

    def fast_enough(self):
        if abs(self.velo) < .25 and abs(self.velo) > 0: # between 0 and .5 velo
            return False
        elif abs(self.velo) > 0 and abs(self.velo) 
        elif abs(self.velo) >= .5: # moving enough to acually turn
            return True

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.turn_left()
        if keys[pygame.K_RIGHT]:
            self.turn_right()

        if keys[pygame.K_UP]:
            self.targ_velo += 2
            self.velo+=.1
        if keys[pygame.K_DOWN]:
            self.targ_velo -= 1
            self.velo -= .1
    
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self, win):
        if self.image:
            self.update_image()
            # If the image exists, draw it. makes sure no mistakes in init
            win.blit(self.image, self.rect.topleft)
        if self.player_type == "user":
            self.move()
        elif self.player_type == "ai":
            self.control() # control() has not been implemented

    def update_image(self):
       # Rotate the image and get the new rect to center it at (x, y)
       self.image = pygame.transform.rotate(self.og_image, self.head+90)
       # Get the new rectangle for the rotated image
       self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
       self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
