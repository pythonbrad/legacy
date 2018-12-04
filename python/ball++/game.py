from tkinter import *
import math
import random

w = 800
h = 600

r = x1 = y1 = w / 4
x2 = y2 = h / 4

p1x1 = p1y1 = 20
p1x2 = 30
p1y2 = 200
p1_color = "brown"

p2x1 = w - 30
p2y1 = 20
p2x2 = w - 20
p2y2 = 200
p2_color = "green"

dx = math.cos(60)
dy = math.sin(60)
v = 30
score = {1: 0, 2: 0}


def collision(coords, obj2):
    if obj2 in Canevas.find_overlapping(*coords):
        return True
    else:
        return False


def add_score(player, x):
    global score
    score[player] += 1
    if score[1] > score[2]:
        label_score.config(
            text="Left: %s VS Right: %s" % (score[1], score[2]), fg=p1_color
        )
    elif score[2] > score[1]:
        label_score.config(
            text="Left: %s VS Right: %s" % (score[1], score[2]), fg=p2_color
        )
    else:
        pass


def move(event):
    global p1x1, p1y1, p1x2, p1y2
    global p2x1, p2y1, p2x2, p2y2
    global v
    key = event.keysym.upper()
    if key == "W" and p1y1 > 0:
        p1y1 -= v
        p1y2 -= v
    elif key == "S" and p1y2 < h:
        p1y1 += v
        p1y2 += v

    if key == "UP" and p2y1 > 0:
        p2y1 -= v
        p2y2 -= v
    elif key == "DOWN" and p2y2 < h:
        p2y1 += v
        p2y2 += v

    Canevas.coords(player1, p1x1, p1y1, p1x2, p1y2)
    Canevas.coords(player2, p2x1, p2y1, p2x2, p2y2)


def anim():
    global x1, x2, y1, y2, r
    global dx, dy, v
    global w, h
    old_coords = (x1, y1, x2, y2)
    if x2 + v + v >= w:
        add_score(1, 1)
        dx = -dx
        x1 += v * dx
        x2 += v * dx
    elif x1 - v - v <= 0:
        add_score(2, 1)
        dx = -dx
        x1 += v * dx
        x2 += v * dx
    else:
        x1 += v * dx
        x2 += v * dx

    if y1 - v - v <= 0:
        dy = -dy
        y1 += v * dy
        y2 += v * dy
    elif y2 + v + v >= h:
        dy = -dy
        y1 += v * dy
        y2 += v * dy
    else:
        y1 += v * dy
        y2 += v * dy

    new_coords = (x1, y1, x2, y2)
    if collision(new_coords, player1):
        x1, y1, x2, y2 = old_coords
        dx = -dx
        x1 += v * dx
        x2 += v * dx
    elif collision(
        (new_coords[0] - v, new_coords[1], new_coords[2] - v, new_coords[3]), player2
    ):
        x1, y1, x2, y2 = old_coords
        dx = -dx
        x1 += v * dx
        x2 += v * dx
    else:
        pass
    Canevas.coords(ball, x1, y1, x2, y2)
    Canevas.after(50, anim)


fen = Tk()
fen.title("Ball 2D by Python Brad")
fen.resizable(False, False)
label_score = Label(text="Left: 0 VS Right: 0")
label_score.pack()
Canevas = Canvas(width=w, height=h)
Canevas.pack()
ball = Canevas.create_oval(x1, y1, x2, y2, fill="red")
player1 = Canevas.create_rectangle(p1x1, p1y1, p1x2, p1y2, fill=p1_color)
player2 = Canevas.create_rectangle(p2x1, p2y1, p2x2, p2y2, fill=p2_color)
Canevas.focus_set()
Canevas.bind("<Key>", move)
anim()
fen.mainloop()
