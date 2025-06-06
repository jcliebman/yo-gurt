import turtle
from turtle import *
import math
import random
import time

#main player class with the information all players need
#handles movements and shooting condition
class Player():
    def __init__(self, strength, dribbling, shotpower, shotrange, speed, pname, num,color):
        self.strength = strength
        self.dribbling = dribbling
        self.shotpower =shotpower
        self.speed  = speed
        self.pname = pname
        self.player = Turtle()
        self.player.pu()
        self.num = num
        self.heading = 180
        self.player.setheading(180)
        self.goalx =-360
        self.cor = (120,0)
        self.score = 0
        self.shooting = False
        self.id = Turtle() #this id changes color based on player number
        self.id.color(color)
        self.id.pu()
        self.id.setheading(270)
        self.shotrange = shotrange
        if self.num ==2: #set sp
            self.player.setheading(0)
            self.heading = 0
            self.goalx = 360
            self.cor = (-120,0)
    def id_track(self): #id follows player so they can be identified
        self.id.goto(self.player.xcor(), self.player.ycor()+50)
    def forward(self):
        self.player.setheading(self.heading)
        self.player.forward(self.speed)
    def backward(self):
        self.player.setheading(self.heading+180)
        self.player.forward(self.speed)
    def up(self):
        self.player.setheading(90)
        self.player.forward(self.speed)
    def down(self):
        self.player.setheading(270)
        self.player.forward(self.speed)
    def shoot(self):
        self.shooting = True
    def move(self): #contol all movements
        if self.num == 1:
            turtle.onkey(self.forward, "Left")
            turtle.onkey(self.backward, "Right")
            turtle.onkey(self.up, "Up")
            turtle.onkey(self.down, "Down")
            turtle.onkey(self.shoot, "/")

        else:
            turtle.onkey(self.forward, "d")
            turtle.onkey(self.backward, "a")
            turtle.onkey(self.up, "w")
            turtle.onkey(self.down, "s")
            turtle.onkey(self.shoot, "space")
        self.id_track()
    def reset(self): #reset players after goals and obs
        self.player.goto(self.cor)
        self.player.setheading(self.heading)
        self.shooting = False
        self.id_track()

#heavy player class gives the stats for a heavy player
class HeavyPlayer(Player):
    def __init__(self,pname, num, color):
        super().__init__(strength = 150, dribbling=80, shotpower=100, shotrange = 5, speed = 13, pname = pname, num=num, color = color)
        turtle.addshape(name = 'heavy.gif', shape = None)
        self.player.shape("heavy.gif")
        self.reset()

#light player class gives the stats for a light player
class LightPlayer(Player):
    def __init__(self,pname, num, color):
        super().__init__(strength = 55, dribbling=95, shotpower=75, shotrange= 18, speed = 20, pname = pname, num = num, color=color)
        turtle.addshape(name = 'light.gif', shape = None)
        self.player.shape("light.gif")
        self.reset()

#normal player has average stats, but has the advantage of no big weaknesses
class NormalPlayer(Player):
    def __init__(self,pname,num, color):
        super().__init__(strength = 100, dribbling=91, shotpower=85, shotrange = 10, speed = 16, pname = pname, num = num, color=color)
        turtle.addshape(name = 'player.gif', shape = None)
        self.player.shape("player.gif")
        self.reset()

#ball class handles everything that happens with the ball
class Ball():
    def __init__(self):
        self.carrier = None
        self.goal = False
        self.shot_count = 0
        self.shooter=None
        self.scorer = None
        self.ob = False
        self.last_dribble = False #this is used as a way to start the cooldown timer when possesion switches players
    def reset(self): #reset all variables before kickoff
        self.carrier = None
        self.goal = False
        self.shot_count = 0
        self.shooter=None
        self.scorer = None
        self.ob = False
        self.last_dribble = False
    def cooldown(self): #check if the cooldown period has passed to reactive the ability to steal the ball.
        if time.time()-self.last_dribble>=1.2:
            self.last_dribble = False

    def dribble(self, ball, players): #dribbling the ball takes into account the strength and loc of players
        nearby_players = []
        if not self.last_dribble:
            for player in players:
                distance = math.dist((player.player.xcor(), player.player.ycor()), (ball.xcor(), ball.ycor()))
                distance2 = math.dist((player.player.xcor(), player.player.ycor()-30), (ball.xcor(), ball.ycor()))
                if distance < 31 or distance2 < 31: #two distances to cover more of the player
                    nearby_players.append(player)

            if nearby_players: 
                strengths = [p.strength for p in nearby_players] 
                winner = random.choices(nearby_players, weights=strengths, k=1)[0] #use strength to weight random choice
                if self.carrier: 
                    if self.carrier.num != winner.num: # start cooldown timer if ball changes hands
                        self.last_dribble = time.time()
                if len(nearby_players)>1:
                    self.last_dribble = time.time() #start cooldown timer if a duel is won
                self.carrier = winner
                ball.setheading(winner.player.heading())
                offset = 105 - winner.dribbling #better dribbling stat means ball stays closer
                rad = math.radians(winner.player.heading())
                dx = offset * math.cos(rad)
                dy = offset * math.sin(rad)
                ball.goto(winner.player.xcor() + dx, winner.player.ycor() + dy - 30)#place ball lower on the player
            else:
                self.carrier = None
        if self.last_dribble and self.carrier:
            self.cooldown()
            ball.setheading(self.carrier.player.heading())
            offset = 105 - self.carrier.dribbling #better dribbling stat means ball stays closer
            rad = math.radians(self.carrier.player.heading())
            dx = offset * math.cos(rad)
            dy = offset * math.sin(rad)
            ball.goto(self.carrier.player.xcor() + dx, self.carrier.player.ycor() + dy - 30)#place ball lower on the player
            
    #check is a goal has been scored
    #check for both shooter and carrier so that goals will always be detected
    def check_goal(self,ball,players, writers):
        if self.carrier:
            if self.carrier.num ==1:
                if (self.carrier.goalx>= ball.xcor()) and (60>ball.ycor()>-60):
                    self.goal = True
                    self.scorer= self.carrier
                    self.carrier = None
            else:
                if (self.carrier.goalx<= ball.xcor()) and (60>ball.ycor()>-60):
                    self.goal = True
                    self.scorer = self.carrier
                    self.carrier = None
        if self.shooter:
            if self.shooter.num ==1:
                if (self.shooter.goalx>= ball.xcor()) and (60>ball.ycor()>-60):
                    self.goal = True
                    self.scorer = self.shooter
                    self.shooter = None
            else:
                if (self.shooter.goalx<= ball.xcor()) and (60>ball.ycor()>-60):
                    self.goal = True
                    self.scorer = self.shooter
                    self.shooter = None
        if self.goal:
            unlisten()
            self.goal = False
            self.scorer.score+=1
            prompt = f"{self.scorer.pname} scored!"
            msg = Turtle()
            msg.hideturtle()
            msg.pu()
            msg.goto(0,70)
            msg.write(prompt, align = "center", font = ("Press Start 2P", 60, "bold"))
            write_score(writers[self.scorer.num-1], self.scorer)
            screen.update()
            time.sleep(2)
            msg.clear()
            for player in players:
                if player.num!=self.scorer.num:
                    player.shooting=False
                    player.player.goto(0,0)
                    player.id_track()
                    player.player.setheading(player.heading)
                else:
                    player.reset()
            self.reset()
            ball.goto(0,0)
            screen.update()
            time.sleep(2)
            self.scorer=None
    #shooting uses a bool from the player to tell when they should shoot
    def shoot(self, ball):
        if self.carrier:
            h = self.carrier.player.heading()
            if self.carrier.shooting and self.shot_count<self.carrier.shotpower//2:
                ball.setheading(random.randint(h-self.carrier.shotrange,h+self.carrier.shotrange)) #pick a random range for the shot to be taken in
                ball.forward(35)
                self.shot_count+=1
                self.shooter = self.carrier
        if self.shooter:
            if self.shooter.shooting and self.shot_count<self.shooter.shotpower//2:
                ball.forward(self.shooter.shotpower//12)
                self.shot_count+=1
            if self.shot_count>=self.shooter.shotpower//2:
                self.shooter.shooting = False
                self.shot_count = 0
                self.shooter = None
    #similar logic to check goal
    def outofbounds(self,ball,players):#player who did not send ball out gets ball at half line
        if abs(ball.ycor())>=265 or abs(ball.xcor())>=370:
            unlisten()
            screen.update()
            time.sleep(1.5)
            self.ob = True
            for player in players:
                if self.carrier:
                    if player.num!=self.carrier.num:
                        player.shooting = False
                        player.player.goto(0,0)
                        player.id_track()
                        player.player.setheading(player.heading)
                    else:
                        player.reset()
                if self.shooter:
                    if player.num!=self.shooter.num:
                        player.shooting = False
                        player.player.goto(0,0)
                        player.id_track()
                        player.player.setheading(player.heading)
                    else:
                        player.reset()
            self.reset()
            ball.goto(0,0)
            self.ob = False
            screen.update()
            time.sleep(2)

def sb(): #background for scoreboard
    sbs = [Turtle(), Turtle()]
    for sb in sbs:
        sb.pu()
        sb.shape('square')
        sb.shapesize(2, 20, 0)
    sbs[0].goto(-200, 290)
    sbs[0].color("Red")
    sbs[1].goto(200,290)
    sbs[1].color("Blue")
    for sb in sbs:
        sb.stamp()
        sb.hideturtle()

def write_score(writer, player): #write the score for both players
    writer.clear()
    writer.write(f"{player.pname}: {player.score}", align = "center", font = ("Press Start 2P", 27, "bold"))

def stands():#create the stands
    stands = [Turtle(), Turtle()]
    for stand in stands:
        stand.pu()
        stand.shape('square')
        stand.shapesize(2, 20, 0)
    stands[0].goto(200, -290)
    stands[0].color("Red")
    stands[1].goto(-200,-290)
    stands[1].color("Blue")
    for stand in stands:
        stand.stamp()
        stand.hideturtle()

#create the player, take user input for name and player type
def playercreate():
    colors = ["Blue","Red"]
    players = []
    for num in range(0,2):
        while True:
            type = screen.textinput(f"Player {num+1}", "Select player type (1. Heavy, 2. Light, 3. Normal)")
            name = screen.textinput(f"Player {num+1}", "Type your name")
            try:
                if int(type) == 1:
                    p = HeavyPlayer(name, num+1, colors[num])
                    break
                if int(type) == 2:
                    p = LightPlayer(name, num+1, colors[num])
                    break
                if int(type) == 3:
                    p = NormalPlayer(name, num+1, colors[num])
                    break
                else:
                    continue
            except ValueError:
                continue
        players.append(p)
    return players

#create a countdown timer to end the game after a given amount of time in seconds
def countdown(time_left):
    global match_over
    minutes = time_left//60
    seconds = time_left%60
    timer_writer.clear()
    timer_writer.write(f"{minutes}:{seconds:02}", align="center", font=("Press Start 2P", 22,"bold"))
    if time_left > 0:
        screen.ontimer(lambda: countdown(time_left-1), 1000) #ontimer doesn't want a func with a parameter, so lambda gets around that
    else:
        unlisten()
        match_over= True
        timer_writer.goto(0,-60)
        timer_writer.write(f"{minutes}:{seconds:02}", align="center", font=("Press Start 2P", 115,"bold"))
        time.sleep(1.5)
        timer_writer.clear()
        timer_writer.write("GAME OVER", align="center", font=("Press Start 2P",80,"bold"))
        time.sleep(1.5)
def gameover(players): #when game ends, give game end message and say who won or tied
    timer_writer.clear()
    writer = Turtle()
    writer.pu()
    writer.goto(0,-40)
    win = max(players[0].score, players[1].score)
    if players[0].score == players[1].score:
        writer.write("TIE GAME", align="center", font=("Press Start 2P",90,"bold"))
    else:
        for player in players:
            if player.score == win:
                writer.write(f"{player.pname} Wins!", align="center", font=("Press Start 2P",70,"bold"))
def unlisten(): #unbind all keys so you cannot move after a goal or out of bounds
    turtle.onkey(None, "Left")
    turtle.onkey(None, "Right")
    turtle.onkey(None, "Up")
    turtle.onkey(None, "Down")
    turtle.onkey(None, "/")
    turtle.onkey(None, "d")
    turtle.onkey(None, "a")
    turtle.onkey(None, "w")
    turtle.onkey(None, "s")
    turtle.onkey(None, "space")
# Game Setup
TK_SILENCE_DEPRECATION=1 
screen = Screen()
turtle.setup(800,620)
screen.bgpic(picname='field.gif')
screen.tracer(0)
sb()
stands()
screen.update()
players = playercreate()
ball = Turtle()
turtle.addshape(name = 'ball.gif', shape = None)
ball.shape("ball.gif")
ball.pu()
ball.goto(0, 0)
b = Ball()
cor = 200
p = 0
writers = [Turtle(), Turtle()]
for writer in writers: #initialize score writing
    writer.pu()
    writer.hideturtle()
    writer.shapesize(1,1,100)
    writer.goto(cor, 275)
    cor-=400
    write_score(writer, players[p])
    p+=1
match_over = False
timer_writer = Turtle() #initialize timer writing
timer_writer.hideturtle()
timer_writer.pu()
timer_writer.goto(0, 276) 
timer_box = Turtle() #initialize timer background
timer_box.hideturtle()
timer_box.penup()
timer_box.shape('square')
timer_box.color('white')
timer_box.shapesize(stretch_wid=2, stretch_len=5)
timer_box.goto(-3, 290)
timer_box.stamp()

countdown(90) # countdown timer that determines the length of the game
# Main Loop
while True:
    if not match_over and not b.ob:
        turtle.listen()
        for player in players:
            player.move()
        b.dribble(ball,players)
        b.check_goal(ball, players, writers)
        b.shoot(ball)
        b.outofbounds(ball, players)
        screen.update()
    if match_over: #when the game ends this happens
        gameover(players)
        time.sleep(5)
        exit()
