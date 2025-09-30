import turtle

# Create screen and set it up
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Heart Shape")

# Set up the turtle
t = turtle.Turtle()
t.speed(3)  # Medium speed
t.pensize(3)
t.color('red', 'pink')

def draw_heart():
    # Start from center position
    t.penup()
    t.goto(0, -100)  # Start lower on the screen
    t.pendown()
    
    t.begin_fill()
    
    # Draw the left half of the heart
    t.left(140)
    t.forward(224)
    for _ in range(200):
        t.right(1)
        t.forward(2)
    
    # Draw the right half of the heart    
    t.left(120)
    for _ in range(200):
        t.right(1)
        t.forward(2)
    t.forward(224)
    
    t.end_fill()

# Draw the heart
try:
    draw_heart()
    t.hideturtle()  # Hide the turtle cursor
    screen.mainloop()  # Keep the window open
except:
    print("An error occurred while drawing")
finally:
    print("Drawing complete")





    