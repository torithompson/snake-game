import turtle
import random
import os

WIDTH = 800
HEIGHT = 700
IMAGE_WIDTH = 59
IMAGE_HEIGHT = 80
delay = 150
food_types = ["pizza", "lemmy", "boo"]

offsets = {
    "up": (0,20),
    "down": (0,-20),
    "left": (-20,0),
    "right": (20,0)
}

def get_image_path(image_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, image_name)
    return image_path

def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("left"), "Left")
    screen.onkey(lambda: set_snake_direction("right"), "Right")

def set_snake_direction(direction):
    global snake_direction
    if direction == "up":
        if snake_direction != "down":
            snake_direction = direction
    elif direction == "down":
        if snake_direction != "up":
            snake_direction = direction
    elif direction == "left":
        if snake_direction != "right":
            snake_direction = direction
    elif direction == "right":
        if snake_direction != "left":
            snake_direction = direction

def game_loop():
    global delay 
    stamper.clearstamps()
    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    if new_head in snake or new_head[0] < - WIDTH / 2 or new_head[0] > WIDTH / 2 \
        or new_head[1] < - HEIGHT / 2 or new_head[1] > HEIGHT /2:
        reset_game()
    else:
        snake.append(new_head)

        #Check food collision
        if not food_collision():
            snake.pop(0) #Keep the snake the same length unless fed

        for segment in snake:
            stamper.goto(segment[0],segment[1])
            stamper.stamp()
        update_score()
        screen.update()
        turtle.ontimer(game_loop, delay)

def food_collision():
    global food_pos, score, delay, current_food
    if get_distance(snake[-1], food_pos) < 20:
        if current_food == "pizza":
            score += 1
        elif current_food == "lemmy" or current_food == "boo":
            score += 5

        if score > 5:
            delay = 100
        elif score > 10:
            delay = 50
        elif score > 20:
            delay = 25
        elif score > 50:
            delay = 15
        elif score > 100:
            delay = 0

        food_pos = get_random_food_pos()
        update_score()
        
        # Randomly choose the next food type
        next_food_types = [food for food in food_types if food != current_food]
        current_food = random.choice(next_food_types)        
        # Show the corresponding food on the screen
        if current_food == "pizza":
            pizza.goto(food_pos)
            pizza.showturtle()
            lemmy.hideturtle()
            boo.hideturtle()
        elif current_food == "lemmy":
            lemmy.goto(food_pos)
            lemmy.showturtle()
            pizza.hideturtle()
            boo.hideturtle()
        elif current_food == "boo":
            boo.goto(food_pos)
            boo.showturtle()
            lemmy.hideturtle()
            pizza.hideturtle()
        return True
    return False

def get_random_food_pos():
    x = random.randint(- WIDTH / 2 + IMAGE_WIDTH, WIDTH / 2 - IMAGE_WIDTH)
    y = random.randint(- HEIGHT / 2 + IMAGE_HEIGHT, HEIGHT / 2 - IMAGE_HEIGHT)
    return (x,y)

def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5 
    return distance

def reset_game():
    global score, snake, snake_direction, food_pos, delay
    lemmy.hideturtle()
    boo.hideturtle()

    score=0
    delay = 150
    snake = [[0,0],[20,0],[40,0],[60,0]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    pizza.goto(food_pos)
    global current_food 
    current_food = "pizza"
    pizza.showturtle()

    game_loop()

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake Game")
screen.tracer(0)

score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("black")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, HEIGHT // 2 - 45)
score_display.write("Score: 0", align="center", font=("Jokerman", 24, "normal"))


def update_score():
    score_display.clear()
    score_display.write(f"Score: {score}", align="center", font=("Jokerman", 24, "normal"))

#Event handlers
screen.listen()
bind_direction_keys()

stamper = turtle.Turtle()
stamper.shape("circle")
stamper.penup()

turtle.register_shape(get_image_path("pizza.gif"))
pizza = turtle.Turtle()
pizza.shape(get_image_path("pizza.gif"))
pizza.penup()
pizza.shapesize(1)

turtle.register_shape(get_image_path("lemmy.gif"))
lemmy = turtle.Turtle()
lemmy.shape(get_image_path("lemmy.gif"))
lemmy.penup()
lemmy.shapesize(1)

turtle.register_shape(get_image_path("boo.gif"))
boo = turtle.Turtle()
boo.shape(get_image_path("boo.gif"))
boo.penup()
boo.shapesize(1)

reset_game()
turtle.done()