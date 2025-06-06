import turtle
from turtle import *

# Constants for map elements
PATH = 0
WALL = 1
RIVER = 2
MATERIALS = 3
KEYS = 4
DOORS = 5
FINISH = 6
BM_count=0
# Create the turtles
t = turtle.Turtle()  # Map draw turtle
t.hideturtle()
p = turtle.Turtle()  # Player move turtle
c = turtle.Turtle()
t.speed(0)  # Set the speed
p.speed(0)
screen= Screen()
screen.setup(750, 950)

# Map data
Map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 6, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 5, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 1, 2, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 2, 1, 1, 1],
    [1, 3, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 3, 0, 0, 2, 2, 4, 1, 1, 1],
    [1, 0, 1, 1, 1, 0, 3, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 4, 1, 1, 1, 5, 1, 1, 1, 1, 1, 1],
    [1, 0, 3, 1, 1, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 3, 1, 1, 1, 0, 3, 0, 4, 0, 1, 1],
    [1, 0, 5, 1, 0, 0, 1, 1, 1, 2, 1, 1],
    [1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Start position of the turtles
x_start = -150
y_start = 150
box_size = 30

# Setup initial position for player
player_start_x = 5
player_start_y = 15

#Write the controls
def controls(t):
    screen.tracer(0)
    t.penup()
    t.goto(-150, 180)
    t.pendown()
    t.write("Move with arrow keys, press 'q' to quit", move=False, align='left', font=('Arial', 20, "normal"))
    t.hideturtle()
    screen.update()
    screen.tracer(1)
    
#Formula to used allow the turtle navigate the map while following the text layout
def map_to_screen(x, y):
    return x_start + x * box_size +13, y_start - y * box_size - 13 

# Setup player's turtle
p.penup()
p.shape("turtle")
player_x, player_y = map_to_screen(player_start_x, player_start_y)
p.goto(player_x, player_y)

# Initialize variables
Mats = 0
Keys = 0


def drawMap(currX, currY):
    print()
    for y in range(0, len(Map)):
        for x in range(0, len(Map[y])):
            # Show numbers as symbols
            if currX == x and currY == y:
                print("*  ", end="")
            elif Map[y][x] == RIVER:  # River tile
                print("~  ", end="")
            elif Map[y][x] == MATERIALS:  # Item
                print("?  ", end="")  # '?' means item
            elif Map[y][x] == KEYS:
                print("?  ", end="")  # Key
            elif Map[y][x] == PATH:
                print("   ", end="")  # path
            elif Map[y][x] == DOORS:
                print("D  ", end="")  # Door
            elif Map[y][x] == FINISH:
                print("F  ", end="")  # End
            else:
                print(Map[y][x], " ", end="")
        print()
    print()

# Define our function that will move the player
def movePlayer(x, y, moveDir):
    global Map, Mats, Keys
    # Calculate the new coordinates based on the move direction
    new_x = x
    new_y = y
    if moveDir == "u":
        new_y = new_y - 1
    elif moveDir == "d":
        new_y = new_y + 1
    elif moveDir == "l":
        new_x = new_x - 1
    elif moveDir == "r":
        new_x = new_x + 1
    # Check if the new coordinates are within bounds and not a wall
    if 0 <= new_x < len(Map[0]) and 0 <= new_y < len(Map) and Map[new_y][new_x] != 1 and Map[new_y][new_x] != 2 and Map[new_y][new_x] != 5:
        return (new_x, new_y)
    elif Map[new_y][new_x] == RIVER:
        if Mats >= 1:
            Buildit = turtle.textinput("River!","This river is too dangerous to cross...Would you like to use your building materials? (y/n): ")
            if Buildit.lower() == 'y':
                Map[new_y][new_x] = 0
                Mats -= 1
                print("You have", Mats, "building materials left")
                print(" ")
                t.clear()
                draw_map(Map, x_start, y_start, box_size)
                listen()
                return (new_x, new_y)
                
            else:
                print("You've decided to keep your building materials...")
                print(" ")
                listen()
                return (x, y)
        else:
            print("This river is too dangerous to swim across. If only we had something to build over it with...")
            print(" ")
            return (x, y)
    elif Map[new_y][new_x] == DOORS:
        if Keys >= 1:
            Unlock = turtle.textinput("Did you just walk face first into a door", "Unlock it? (y/n): ")
            if Unlock.lower() == 'y':
                Map[new_y][new_x] = 0
                Keys= Keys - 1
                print("You unlocked the door! You have", Keys, "keys left.")
                print(" ")
                t.clear()
                draw_map(Map, x_start, y_start, box_size)
                listen()
                return (new_x, new_y)
            else:
                print("You chose not to unlock this door")
                print(" ")
                listen
                return (x, y)
        else:
            print("Did you just walk face first into a door? Nevermind...I'll pretend I didn't see that")
            print(" ")
            return (x, y)
    else:
        print("**Invalid move** Try again.")
        print(" ")
        return (x, y)



def GAME_END(x, y):
    if Map[y][x] == FINISH:
        print("You Win!!!")
        turtle.bye()

def draw_square(size, color):
    t.fillcolor(color)
    t.begin_fill()
    for fill in range(4):
        t.forward(size)
        t.right(90)
    t.end_fill()

def get_color(element):
    if element == PATH:
        return ""
    elif element == WALL:
        return "black"
    elif element == RIVER:
        return "blue"
    elif element == MATERIALS:
        return "brown"
    elif element == KEYS:
        return "yellow"
    elif element == DOORS:
        return "orange"
    elif element == FINISH:
        return "green"
    

def draw_map(map_data, x_start, y_start, box_size):
    screen.tracer(0)
    t.penup()
    t.goto(x_start, y_start)
    t.pendown()
    
    for row in map_data:
        for element in row:
            color = get_color(element)
            draw_square(box_size, color)
            t.penup()
            t.forward(box_size)
            t.pendown()
        t.penup()
        t.goto(x_start, t.ycor() - box_size)
        t.pendown()
    screen.update()
    screen.tracer(1)


#Function to grab, and erase items from the map
def item_grab(x, y):
    global Mats, Keys, Map, BM_count
    if Map[y][x] == MATERIALS and BM_count <= 2:
        decision = turtle.textinput("!?!?!?!", "You found building materials! Wanna pick 'em up 'y'/'n'")
        if decision == "y":
            Mats= Mats + 1
            print("You picked up the building materials!")
            print("You currently have", Mats, "building materials")
            print(" ")
            Map[y][x] = 0
            BM_count=BM_count+1
            t.clear()
            draw_map(Map, x_start, y_start, box_size)
            listen()
        elif Map[y][x] == MATERIALS and decision != "y":
            print("You decided not to pick up the building materials.")
            print("You currently have", Mats, "building materials.")
            print(" ")
            listen()
        
    elif Map[y][x] == MATERIALS and BM_count==3:
        decision1 = turtle.textinput("More mats 😐", "PICK THEM UP!?!?!?! 'y'/'n'")
        if decision1 == "y":
            Mats= Mats + 1
            print("You picked up the building materials!")
            print("You currently have", Mats, "building materials")
            print(" ")
            Map[y][x] = 0
            BM_count=BM_count+1
            t.clear()
            draw_map(Map, x_start, y_start, box_size)
            listen()
        elif Map[y][x] == MATERIALS and decision != "y":
            print("You decided not to pick up the building materials.")
            print("You currently have", Mats, "building materials.")
            print(" ")
            listen()
        
    elif Map[y][x] == MATERIALS and BM_count>=4:
        BM_count=0
        decision2 = turtle.textinput("For Real?", "Pick that shit up? 'y'/'n'")
        if decision2 == "y":
            Mats= Mats + 1
            print("You picked up the building materials!")
            print("You currently have", Mats, "building materials")
            print(" ")
            Map[y][x] = 0
            BM_count=BM_count+1
            t.clear()
            draw_map(Map, x_start, y_start, box_size)
            listen()
        elif Map[y][x] == MATERIALS and decision != "y":
            print("You decided not to pick up the building materials.")
            print("You currently have", Mats, "building materials.")
            print(" ")
            listen()
            
                


    if Map[y][x] == KEYS:
        key_pickup = turtle.textinput("You found a key!", "Perhaps it opens a door somewhere... Pick it up? (y/n):")
        if key_pickup.lower() == "y":
            Keys= Keys+1
            print("You've picked up a key!")
            print("You have", Keys, "keys...")
            Map[y][x] = 0
            t.clear()
            draw_map(Map, x_start, y_start, box_size)
            listen()
        else:
            print("You decided not to pick up the key")
            print(" ")
            listen()
####Game controls            
def move_up():
    global currX, currY
    p.setheading(90)
    currX, currY = movePlayer(currX, currY, "u")
    player_x, player_y = map_to_screen(currX, currY)
    p.goto(player_x, player_y)
    item_grab(currX, currY)
    GAME_END(currX, currY)
    
def move_down():
    global currX, currY
    p.setheading(270)
    currX, currY = movePlayer(currX, currY, "d")
    player_x, player_y = map_to_screen(currX, currY)
    p.goto(player_x, player_y)
    item_grab(currX, currY)
    GAME_END(currX, currY)

def move_left():
    global currX, currY
    p.setheading(180)
    currX, currY = movePlayer(currX, currY, "l")
    player_x, player_y = map_to_screen(currX, currY)
    p.goto(player_x, player_y)
    item_grab(currX, currY)
    GAME_END(currX, currY)

def move_right():
    global currX, currY
    p.setheading(0)
    currX, currY = movePlayer(currX, currY, "r")
    player_x, player_y = map_to_screen(currX, currY)
    p.goto(player_x, player_y)
    item_grab(currX, currY)
    GAME_END(currX, currY)
###QUIT GAME
def quit_game():
    turtle.bye()
# Start position for player
currX = player_start_x
currY = player_start_y  

# Draw the map
draw_map(Map, x_start, y_start, box_size)

# Write the game controls
controls(c)
# Movement controls
listen()
onkey(move_up, "Up")
onkey(move_down, "Down")
onkey(move_left, "Left")
onkey(move_right, "Right")
onkey(quit_game, "q")
t.hideturtle()
done()
