import turtle
from turtle import *
import math
import random
import time
class Player():
    def __init__(self, strength, dribbling, shooting, shotpower, speed, pname, num):
        self.strength = strength
        self.dribbling = dribbling
        self.shooting = shooting
        self.shotpower =shotpower
        self.speed  = speed
        self.pname = pname
        self.player = Turtle()
        self.player.pu()
        self.num = num
        self.heading = 0
        self.goalx =-360
        self.cor = (100,0)
        self.score = 0
        if self.num ==2:
            self.player.setheading(180)
            self.heading = 180
            self.goalx = 360
            self.cor = (-100,0)
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
    def move(self):
        if self.num == 1:
            turtle.onkey(self.forward, "Right")
            turtle.onkey(self.backward, "Left")
            turtle.onkey(self.up, "Up")
            turtle.onkey(self.down, "Down")

        else:
            turtle.onkey(self.forward, "a")
            turtle.onkey(self.backward, "d")
            turtle.onkey(self.up, "w")
            turtle.onkey(self.down, "s")
    def reset(self):
        self.player.goto(self.cor)

class HeavyPlayer(Player):
    def __init__(self,pname, num):
        super().__init__(strength = 100, dribbling=87, shooting = 85, shotpower=100, speed = 6.5, pname = pname, num=num)
        turtle.addshape(name = 'heavy.gif', shape = None)
        self.player.shape("heavy.gif")
        self.player.goto(self.cor)
class LightPlayer(Player):
    def __init__(self,pname, num):
        super().__init__(strength = 55, dribbling=95, shooting = 90, shotpower=75, speed = 10, pname = pname, num = num)
        turtle.addshape(name = 'light.gif', shape = None)
        self.player.shape("light.gif")
        self.player.goto(self.cor)
class NormalPlayer(Player):
    def __init__(self,pname,num):
        super().__init__(strength = 70, dribbling=91, shooting = 80, shotpower=85, speed = 8, pname = pname, num = num)
        turtle.addshape(name = 'player.gif', shape = None)
        self.player.shape("player.gif")
        self.player.goto(self.cor)

class Ball():
    def __init__(self):
        self.carrier = None
        self.goal = False

    def dribble(self, ball, players):
        nearby_players = []

        for player in players:
            distance = math.dist((player.player.xcor(), player.player.ycor()), (ball.xcor(), ball.ycor()))
            distance2 = math.dist((player.player.xcor(), player.player.ycor()-30), (ball.xcor(), ball.ycor()))
            if distance < 31 or distance2 < 31:
                nearby_players.append(player)

        if nearby_players: 
            strengths = [p.strength for p in nearby_players] 
            winner = random.choices(nearby_players, weights=strengths, k=1)[0]
            self.carrier = winner
            ball.setheading(winner.player.heading())
            offset = 115 - winner.dribbling
            rad = math.radians(winner.player.heading())
            dx = offset * math.cos(rad)
            dy = offset * math.sin(rad)
            ball.goto(winner.player.xcor() + dx, winner.player.ycor() + dy - 30)
    def check_goal(self,ball,players, writers):
        if self.carrier:
            if (math.dist((ball.xcor(), 0), (self.carrier.goalx, 0)) <= 5) and (50>ball.ycor()>-50):
                self.goal = True
                self.carrier.score+=1
                prompt = f"{self.carrier.pname} scored!"
                msg = Turtle()
                msg.hideturtle()
                msg.pu()
                msg.goto(0,110)
                msg.write(prompt, align = "center", font = ("Roboto", 70, "bold"))
                write_score(writers[self.carrier.num-1], self.carrier)
                time.sleep(2)
                msg.clear()
                ball.goto(0,0)
                for player in players:
                    player.player.goto(player.cor)
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

def write_score(writer, player):
    writer.clear()
    writer.write(f"{player.pname}: {player.score}", align = "center", font = ("Roboto", 40, "bold"))
def stands():
    stands = [Turtle(), Turtle()]
    for stand in stands:
        stand.pu()
        stand.shape('square')
        stand.shapesize(2, 20, 0)
    stands[0].goto(200, -290)
    stands[0].color("Red")
    stands[1].goto(-200,-290)
    stands[1].color("Blue")
def playercreate():
    players = []
    for num in range(0,2):
        while True:
            type = screen.textinput(f"Player {num+1}", "Select player type (1. Heavy, 2. Light, 3. Normal)")
            name = screen.textinput(f"Player {num+1}", "Type your name")
            try:
                if int(type) == 1:
                    p = HeavyPlayer(name, num+1)
                    break
                if int(type) == 2:
                    p = LightPlayer(name, num+1)
                    break
                if int(type) == 3:
                    p = NormalPlayer(name, num+1)
                    break
                else:
                    continue
            except ValueError:
                continue
        players.append(p)
    return players

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
for writer in writers:
    writer.pu()
    writer.hideturtle()
    writer.shapesize(1,1,100)
    writer.goto(cor, 265)
    cor-=400
    write_score(writer, players[p])
    p+=1

# Main Loop
while True:
    turtle.listen()
    for player in players:
        player.move()
        # for writer in writers:
        #     write_score(writer, player)
    b.dribble(ball,players)
    b.check_goal(ball, players, writers)
    screen.update()
