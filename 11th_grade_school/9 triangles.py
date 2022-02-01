import turtle

while True:
    nurgad = input('Sisestage kolmnurkade arv: ')
    if nurgad.isnumeric():
        nurgad = abs(int(nurgad))
        break
    else:
        print('Sisu peab olema arv!')

c1 = input('Sisestage esimene värv: ')
c2 = input('Sisestage teine värv: ')


def kolmnurgad(num: int, color1: str, color2: str):
    dog = turtle.Turtle()
    dog.speed(-1)
    colors = [color1, color2]
    for n in range(num):
        dog.color(colors[n % 2], colors[n % 2])
        dog.begin_fill()
        for i in range(5):
            dog.forward(20)
            dog.right(120 * ((n % 2) + 1))

            # 120 * ((n % 2) + 1) => 120 * 1 | 120 * 2
            # => dog.right(120*2) == dog.left(120)
            #
            # Does the same as this:
            #
            #  if n % 2 == 0:
            #      dog.right(120)
            #  else:
            #      dog.left(120)
            #

        dog.end_fill()
        dog.right(120 * ((n % 2) + 1))

    turtle.exitonclick()


kolmnurgad(num=nurgad, color1=c1, color2=c2)
