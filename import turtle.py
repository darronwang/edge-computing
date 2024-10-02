import turtle

def draw_tree(branch_length, t):
    if branch_length > 5:
        t.forward(branch_length)
        t.right(20)
        draw_tree(branch_length - 15, t)
        t.left(40)
        draw_tree(branch_length - 15, t)
        t.right(20)
        t.backward(branch_length)

t = turtle.Turtle()
t.left(90)
t.up()
t.backward(100)
t.down()
t.color("brown")

draw_tree(100, t)

turtle.done()
