# Load packages for graphics drawing and random selection
import turtle
import random

# Set drawing speed to fastest and background to black
turtle.speed(0)
turtle.bgcolor("black")

# Define color palette for the artwork
colors = ["red", "blue", "green", "yellow", "purple", "orange", "white","pink"]

# Create spiral pattern with 100 line segments
for i in range(10000):
    # Pick random color from the palette
    turtle.color(random.choice(colors))
    
    # Draw line with length equal to current loop number
    turtle.forward(i)
    
    # Turn slightly more than 90 degrees to create spiral effect
    turtle.right(91)

# Keep graphics window open to display finished artwork
turtle.done()