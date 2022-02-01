import turtle

width = int(input('Width: '))
height = int(input('Height: '))


def chess_board(w: int, h: int):
    dog = turtle.Turtle()

    dog.speed(-1)
    dog.hideturtle()
    black = True
    switch = False

    for row in range(w):
        for column in range(h):
            if black:
                dog.color('black', 'black')
            else:
                dog.color('black', 'white')
            dog.begin_fill()

            for i in range(4):
                dog.forward(10)
                dog.right(90)
            dog.right(90)
            dog.forward(10)
            dog.left(90)
            dog.end_fill()
            black = not black
        if row + 1 == w: break
        if switch:
            dog.right(180)
        else:
            dog.forward(20)
            dog.left(180)
        switch = not switch

    turtle.exitonclick()


chess_board(width, height)
