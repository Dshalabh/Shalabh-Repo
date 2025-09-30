import turtle
import math

# Set up the turtle
t = turtle.Turtle()
window = turtle.Screen()
window.bgcolor("black")
t.speed(2)
t.pensize(3)
t.color("red")

# Draw the heart
def draw_heart():
    t.fillcolor("red")
    t.begin_fill()
    
    # Left curve of the heart
    t.left(140)
    t.forward(180)
    for _ in range(200):
        t.right(1)
        t.forward(1)
    
    # Right curve of the heart
    t.left(120)
    for _ in range(200):
        t.right(1)
        t.forward(1)
    t.forward(180)
    
    t.end_fill()

# Position the turtle
t.penup()
t.goto(0, 100)  # Move to starting position
t.pendown()

# Draw the heart
draw_heart()

# Hide the turtle and keep the window open
t.hideturtle()
window.mainloop()