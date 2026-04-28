import turtle  # this imports a library called "turtle". A library is (typically someone else's) python code, that you can use in your own program.


def demo():  # demonstration of basic turtle commands
    tom.speed(1)  # fastest: 10, slowest: 1
    for x in range(8):  # do the following for x = 0, 1, 2, 3, 4, 5, 6, 7
        tom.forward(50)  # move 50 pixels
        tom.left(45)  # turn 45 degrees left
        print(f'Tom is now at {tom.position()}, x-value: {tom.position()[0]=:.2f}, y-value: {tom.position()[1]=:.2f}')
    tom.penup()  # do not draw while moving from now on
    tom.forward(100)
    tom.pendown()  # draw while moving from now on
    tom.circle(50)  # draw a circle with radius 50
    tom.pencolor("red")  # draw in red
    tom.right(90)  # turn 90 degrees right
    tom.forward(120)
    tom.right(-90)  # turning -90 degrees right is the same as turning +90 degrees left
    tom.forward(120)
    tom.goto(-100, -200)  # move to coordinates -100, -200  (0, 0 is the middle of the screen)
    tom.home()  # return to the original position in the middle of the window


def circle(radius):
    tom.pendown()
    tom.circle(radius)


def moveto(x, y):
    tom.penup()
    tom.goto(x, y)


def square(length):
    tom.pendown()
    for x in range(4):
        tom.forward(length)
        tom.left(90)


def triangle(length):
    tom.pendown()
    for x in range(3):
        tom.forward(length)
        tom.left(120)


def coloured_triangle(length):
    tom.pendown()
    tom.pencolor("red")
    for x in range(3):
        tom.forward(length)
        tom.left(120)


def many_squares(number_of_squares, size, distance):
    x = -300
    for index in range(number_of_squares):
        square(size)
        x += distance
        moveto(x, 200)


def many_circles():
    x = -300
    for index in range(10):
        circle(30)
        x += 60
        moveto(x, 130)


def draw_square_at(length, x, y):
    moveto(x, y)
    square(length)


def draw_grid(rows, columns, size):
    x = -300
    y = 200
    for row in range(rows):
        moveto(x, y)
        for column in range(columns):
            square(size)
            x += size
            moveto(x, y)
        x = -300
        y -= size


def draw_house(size, base_colour, roof_colour):
    posx = tom.pos()[0]
    posy = tom.pos()[1]
    tom.pencolor(base_colour)
    square(size)
    tom.pencolor(roof_colour)
    moveto(posx, posy + size)
    triangle(size)


def spiral_square_pattern(size):
    tom.right(90)
    increase = 5
    for x in range(size):
        tom.forward(increase)
        tom.left(90)
        increase += 5


def star_polygons(size):
    # tom.penup()
    turn = 180 - 360 / size / 2
    for x in range(size):
        tom.forward(100)
        tom.right(turn)
    tom.penup()
    tom.right(turn)
    tom.forward(100)


def cool_pattern(size):
    turn = size
    forward = 1
    for y in range(300):
        tom.forward(forward)
        forward += size / 50
        tom.left(turn)
    moveto(300, 300)


tom = turtle.Turtle()  # create an object named tom of type Turtle
tom.shape("turtle")  # make Tom look like a turtle
tom.speed(10)
# moveto(-300, 300)
# circle(50)
# moveto(-250, 300)
# square(50)
# moveto(-200, 300)
# triangle(50)
# moveto(-150, 300)
# coloured_triangle(50)
# moveto(-300, 200)
# tom.pencolor("black")
# many_squares(2, 50, 60)
# moveto(-300, 130)
# many_circles()
# draw_square_at(50, -300, 200)
# draw_grid(5, 5, 50)
# draw_house(50, "green", "red")
# spiral_square_pattern(52)
# star_polygons(9)
cool_pattern(50)
turtle.done()  # keep the turtle window open after the program is done
