import turtle
import time

type = input("""
Name of shape:
1 - square
2 - rectangle
3 - triangle
4 - circle
///////////// : """)

class helpers:
    # these can also be @staticmethod since we dont use objects from this class
    # probably simpler to do with recursion :shrug:
    def square(self, max_size):
        mees = turtle
        size = max_size
        mees.speed(10)
        while size > 0:
            size -= 5
            mees.forward(size)
            mees.left(90)
            mees.forward(size)
            mees.left(90)
        time.sleep(3)
    
    def rect(self, max_size_x, max_size_y):
        mees = turtle
        size_x = max_size_x
        size_y = max_size_y
        mees.speed(10)
        while size_x > 0 and size_y > 0:
            size_x -= 5
            size_y -= 5
            mees.forward(size_x)
            mees.left(90)
            mees.forward(size_y)
            mees.left(90)
        time.sleep(3)

    def triangle(self, max_size):
        mees = turtle
        size = max_size
        mees.speed(10) 
        while size > 0:
            size -= 5
            mees.forward(size)
            mees.left(120)
        time.sleep(5)

    def circle(self, max_size):
        mees = turtle
        size = max_size
        mees.speed(10)
        mees.up()
        mees.right(90)
        mees.forward(max_size)
        mees.right(270)
        mees.down()
        while size > 0:
            mees.circle(size)
            size -= 5
            mees.up()
            mees.left(90)
            mees.forward(5)
            mees.right(90)
            mees.down()

if type == "1":
    side = input("Size: ")
    try:
        helpers().square(int(side))
    except ValueError as e:
        print(f"Palun sisestage number! (Error: {e}")
elif type == 2:
    side_x = input("Size x: ")
    side_y = input("Size y: ")
    try:
        helpers().rect(int(side_x), int(side_y))
    except ValueError as e:
        print(f"Palun sisestage number! (Error: {e}")
elif type == "3":
    side = input("Size: ")
    try:
        helpers().triangle(int(side))
    except ValueError as e:
        print(f"Palun sisestage number! (Error: {e}")
elif type == "4":
    side = input("Radius: ")
    try:
        helpers().circle(int(side))
    except ValueError as e:
        print(f"Palun sisestage number! (Error: {e}")
else:
    print(f"Palun sisestage üks võimalikest tüüpidest. (input: {type})")
        
