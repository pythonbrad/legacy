from tkinter import *
from tkinter.messagebox import *
import math
import random

w = 320
h = 600

block_size = 30

# obstacle
obstacle = []
obj_destroy = []

# bonus
bonus = []
# score
score = 0

# ball
x1 = w / 2 - 10
x2 = w / 2 + 10
r = x2 - x1
y1 = h - r - r - r
y2 = h - r - r
ball_old_coords = (x1, y1, x2, y2)

# player
px1 = w / 2 - 30
px2 = w / 2 + 30
py1 = h - 10
py2 = h
alpha = 45
dx = math.cos(alpha)
dy = math.sin(alpha)
v = 10


def destroy():
    for obj in obj_destroy:
        if Canevas.coords(obj)[3] < h:
            x1, y1, x2, y2 = Canevas.coords(obj)
            y1 += 10
            y2 += 10
            Canevas.coords(obj, x1, y1, x2, y2)
        else:
            Canevas.delete(obj)
            obj_destroy.remove(obj)


def collision_with(coords, obj):
    if obj in Canevas.find_overlapping(*coords):
        return True
    else:
        return False


def is_collision(agent):
    coords = Canevas.coords(agent)
    for obj in obstacle:
        if obj in Canevas.find_overlapping(*coords):
            return (obj, 0)
        else:
            pass
    for obj in bonus:
        if obj in Canevas.find_overlapping(*coords):
            return (obj, 1)
        else:
            pass
    return False


def move(event):
    global px1, py1, px2, py2
    global v
    key = event.keysym
    if key == "Left" and px1 - v > 0:
        px1 -= v
        px2 -= v
    elif key == "Right" and px2 + v < w:
        px1 += v
        px2 += v
    Canevas.coords(player, px1, py1, px2, py2)


def get_map():
    global block_size
    data_map = ""
    for i in range(int(h / 2 / block_size) + 1):
        for ii in range(int(w / block_size) + 1):
            data_map += random.choice(["x", "x", "o", "x", "x"])
        data_map += "\n"
    return data_map


def create_block():
    global block_size
    old_box_x1 = box_x1 = 0
    old_box_y1 = box_y1 = 0
    old_box_x2 = box_x2 = block_size
    old_box_y2 = box_y2 = block_size
    data_map = get_map()
    for i in data_map:
        if i == "o":
            brick_bonus = Canevas.create_rectangle(
                box_x1, box_y1, box_x2, box_y2, fill="orange"
            )
            bonus.append(brick_bonus)
        elif i == "x":
            brick = Canevas.create_rectangle(box_x1, box_y1, box_x2, box_y2, fill="red")
            obstacle.append(brick)
        elif i == "\n":
            box_x1 = old_box_x1
            box_x2 = old_box_x2
            box_y1 += block_size
            box_y2 += block_size
        else:
            pass
        if i != "\n":
            box_x1 += block_size
            box_x2 += block_size


def win_or_lose(x):
    if x == "lose":
        text = "Vous avez perdu!!"
    else:
        text = "Vous avez gagnez!!"
    label_score.config(text="Vous avez gagnez!!", font=(18))
    showinfo(title="Brick", message=text)
    resp = askquestion(title="Partie terminer", message="Voulez-vous rejouer?")
    if resp == "yes":
        retry = (False, True)
    else:
        retry = (False, False)
    return retry


def anim():
    global x1, x2, y1, y2, r
    global dx, dy, v
    global w, h
    global score
    run = (True, True)
    if score in [
        5,
        10,
        15,
        25,
        40,
        65,
        105,
        106,
        108,
        101,
        112,
        118,
        120,
        range(120, 999),
    ]:
        score += 3
        v += 3
    old_coords = (x1, y1, x2, y2)

    if x2 + v * dx > w:
        dx = -dx
        x1 += v * dx
        x2 += v * dx
    elif x1 + v * dx < 0:
        dx = -dx
        x1 += v * dx
        x2 += v * dx
    else:
        x1 += v * dx
        x2 += v * dx

    if y1 + v * dy < 0:
        dy = -dy
        y1 += v * dy
        y2 += v * dy
    elif y2 + v * dy > h:
        run = win_or_lose("lose")
        dy = -dy
        y1 += v * dy
        y2 += v * dy
    else:
        y1 += v * dy
        y2 += v * dy

    new_coords = (x1, y1, x2, y2)
    if collision_with(new_coords, player):
        x1, y1, x2, y2 = old_coords
        dy = -dy
        y1 += v * dy
        y2 += v * dy
    elif is_collision(ball):
        obj = is_collision(ball)
        if obj[1]:
            score += 5
            bonus.remove(obj[0])
        else:
            score += 1
            obstacle.remove(obj[0])
        if not obj[0] in obj_destroy:
            obj_destroy.append(obj[0])
        label_score.config(text="score: %s" % score)
        x1, y1, x2, y2 = old_coords
        if dy < 0:
            dy = -dy
        y1 += v * dy
        y2 += v * dy
    else:
        pass
    destroy()
    if len(obstacle) <= 1:
        run = win_or_lose("win")
    Canevas.coords(ball, x1, y1, x2, y2)
    if run[0]:
        Canevas.after(50, anim)
    else:
        if run[1]:
            score = 0
            for i in obstacle:
                Canevas.delete(i)
            for i in bonus:
                Canevas.delete(i)
            for i in obj_destroy:
                Canevas.delete(i)
            x1, y1, x2, y2 = ball_old_coords
            Canevas.coords(ball, x1, y1, x2, y2)
            create_block()
            Canevas.after(50, anim)
        else:
            Canevas.delete("all")
            Canevas.destroy()
            fen.destroy()


fen = Tk()
fen.title("Brick 2D by Python Brad")
fen.resizable(False, False)
label_score = Label(text="Score: 0")
label_score.pack()
Canevas = Canvas(width=w, height=h)
Canevas.pack()
ball = Canevas.create_oval(x1, y1, x2, y2, fill="black")
player = Canevas.create_rectangle(px1, py1, px2, py2, fill="blue")
create_block()
Canevas.focus_set()
Canevas.bind("<Left>", move)
Canevas.bind("<Right>", move)
anim()
fen.mainloop()
