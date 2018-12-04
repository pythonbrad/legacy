from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
import _thread
import time
import zlib

run = True

img_dir = "img/"

img_ext = ".png"

title = "Le Camerounais Billionaire"

n_x = 1

fen_size = (320, 640)

fen_size_tiny = (int(320 * 2 / 3), int(800 * 2 / 3))

high_score = {
    100: "Le President BOBO",
    57: "Pythonbrad",
    40: "Le bobo",
    50: "Grand pere",
    20: "Ton keke",
    10: "Ton voisin",
    60: "Le chef de village",
}

player = {
    "money": 500,
    "build": 125,
    "upgrade": 10,
    "building": 0,
    "begin": True,
    "tuto": 0,
}

# item, number, price, product, level
items = {
    "orange": [0, 5, 0.5, 1],
    "call_box": [0, 25, 1.25, 1],
    "boutique": [0, 100, 10, 1],
    "boulangerie": [0, 500, 50, 1],
    "resto": [0, 1000, 160, 1],
    "hospital": [0, 10000, 500, 1],
}

items_img = {
    "orange": img_dir + "orange" + img_ext,
    "call_box": img_dir + "call_box" + img_ext,
    "boutique": img_dir + "boutique" + img_ext,
    "boulangerie": img_dir + "boulangerie" + img_ext,
    "resto": img_dir + "resto" + img_ext,
    "hospital": img_dir + "hospital" + img_ext,
}


def aide():
    showinfo(
        title="Besoin d aide?",
        message="Vous etes sans emploie, vous venez de recevoir de l argent.\n"
        "Le but du jeu consiste a investir enfin de devenir le plus riche\n"
        "Au debut vous devez payer un stand de vente d orange\n"
        "C est obliger plus que les autres seront au dessus de vos moyens\n"
        "Apres avoir payer le stand d orange, vous pouvez l ameliorer en fin de gagner plus\n"
        "Econnomisez enfin de pouvoir investir sur de nouveaux infractructures\n"
        "Le boutton x1 que vous verrez au debut, vous permet de dubliquer vos actions\n"
        "Cet a dire x1 est equivaut a un clic, x2 2 clic etc...\n"
        "C est utile pour ameliorer ou payer x fois un batiment\n"
        "Le prix des batiments et le cout des ameliorations depand des chois que vous ferez\n"
        "Tu peux comparer ton rang avec les meilleurs scores des autres\n"
        "Vous gagnerez de l argent meme si le jeux est fermee"
        "Un petit conseil, eviter de trop ameliorer\n"
        "Bonne chance! XD",
    )


def screen(size):
    if size == "tiny":
        fen.geometry("%sx%s" % (int(fen_size_tiny[0]), int(fen_size_tiny[1])))
        label0.config(image=img_orange2)
        label1.config(image=img_call_box2)
        label2.config(image=img_boutique2)
        label3.config(image=img_boulangerie2)
        label4.config(image=img_resto2)
        label5.config(image=img_hospital2)
    else:
        fen.geometry("%sx%s" % fen_size)
        label0.config(image=img_orange)
        label1.config(image=img_call_box)
        label2.config(image=img_boutique)
        label3.config(image=img_boulangerie)
        label4.config(image=img_resto)
        label5.config(image=img_hospital)


def load(ask=False):
    if ask:
        resp = askquestion(
            title="Etes vous sur?", message="Votre parti en cour sera perdu"
        )
    else:
        resp = "yes"
    if resp == "yes":
        open("save.data", "ab").write(b"")
        data = open("save.data", "rb").read()
        try:
            data = zlib.decompress(data)
            exec("global player, items\n" + data.decode())
            if "lastconnect" in player:
                print("rest")
                nb = int(time.time() - player["lastconnect"])
                for i in range(nb):
                    add_money()
            if ask:
                showinfo(title=title, message="Parti charger")
        except Exception as error:
            print(error)
            if ask:
                showinfo(title=title, message="Impossible de charger la parti")
    else:
        pass


def save(ask=False):
    player["lastconnect"] = time.time()
    if ask:
        resp = askquestion(
            title="Voulez vous sauvegarder",
            message="Vous etes sur le point de sauvegarder votre partir",
        )
    else:
        resp = "yes"
    if resp == "yes":
        data = "player = %s;items = %s" % (player, items)
        open("save.data", "wb").write(zlib.compress(data.encode()))
        if ask:
            showinfo(title=title, message="Parti sauvegarder")
    else:
        pass


def print_money(x):
    print("print_money")
    x = str(int(x))
    x = x[::-1]
    r = ""
    it = 0
    for i in range(len(x)):
        if i % 3 == 0:
            r = r + "."
        r = r + x[i]
    return r[1::][::-1]


def multi():
    if not player["begin"]:
        global n_x
        if n_x >= 20:
            n_x = 1
        else:
            n_x = n_x + 1
        button.config(text="x%s" % n_x)
    else:
        showinfo(
            title="Info",
            message="Cet option est disponible apres avoir fini le dictentiel",
        )


def player_rang():
    score = {}
    for i in high_score:
        score[i] = high_score[i]
    score[get_player_level()] = "Moi"
    text = ""
    while len(score) != 0:
        i = max(score)
        text = text + "[%s] level(%s)\n" % (score[i], i)
        score.pop(i)
    showinfo(title="Mon rang", message=text)


def get_player_level():
    return int(player["build"] * player["upgrade"] * player["building"] / 1000)


def player_level():
    showinfo(
        title="Mon status social",
        message="Vous etes au niveaux %s" % get_player_level(),
    )


def get_items(name):
    if items[name][0]:
        return "%s x %s F/s Level %s" % (
            items[name][0],
            print_money(items[name][1]),
            items[name][3],
        )
    else:
        return "Non disponible"


def add_money():
    for item in items:
        if items[item][0]:
            player["money"] += items[item][1] * items[item][0]
        else:
            pass


def add_item(name):
    global n_x
    price = (items[name][0] + 1) * items[name][1] * items[name][2] * player["build"] / 2
    price = price * n_x
    resp = askquestion(
        title=title,
        message="Requis %s F \nCliquer sur OK pour valider" % print_money(price),
    )
    if resp == "yes" and player["money"] >= price:
        player["money"] -= price
        items[name][0] += 1 * n_x
        player["building"] += 1 * n_x
    elif resp == "no":
        pass
    else:
        showwarning("Argent insuffisant", "Requis %s F" % print_money(price))


def upgrade(name):
    global n_x
    price = (items[name][0] + 1) * items[name][1] * items[name][2] * items[name][3]
    price = price * n_x
    if items[name][0]:
        resp = askquestion(
            title=title,
            message="Requis %s F \nCliquer sur OK pour valider" % print_money(price),
        )
        if resp == "yes" and player["money"] >= price:
            player["money"] -= price
            items[name][1] += (
                int(items[name][2] * player["upgrade"] * (items[name][3] + 1) * 0.1)
                * n_x
            )
            items[name][3] += 1 * n_x
        elif resp == "no":
            pass
        else:
            showwarning("Argent insuffisant", "Requis %s F" % print_money(price))
    else:
        showwarning("Manquant", "Requis %s" % name)


def main():
    global run
    load()
    while run:
        time.sleep(1.5)
        try:
            if player["begin"] and player["building"] == player["tuto"] == 0:
                showinfo(
                    title="Dictentiel",
                    message="Bonjour mon enfant\n"
                    "J ai un orangier chez moi qui me sert a rien je pense que sa peut t aider\n"
                    "Prend aussi c est %s F pour etablir ton commerce\n"
                    "HELP\n"
                    "Pour pouvoir ajouter un stand\n"
                    "Va dans le menu ajouter" % player["money"],
                )
                player["tuto"] += 1
            if (
                player["begin"]
                and player["building"] == player["tuto"] == 1
                and player["money"] > 400
                or player["building"] == player["tuto"] + 1 == 2
            ):
                showinfo(
                    title="Dictentiel",
                    message="Je vois que mon vieux orangier ta servi\n"
                    "Je connais un ami qui vend des telephones commercials\n"
                    "Mais il faudra gagnez de l argent pour payer un telephone\n"
                    "HELP\n"
                    "Pour la suite de l aide cliquer sur le menu aide",
                )
                player["tuto"] += 1
            if (
                player["begin"]
                and player["building"] == player["tuto"] == 2
                and player["money"] > 500
            ):
                showinfo(
                    title="Dictentiel",
                    message="Mon petit, je vois que tu peux deja continuer sans moi\n"
                    "Un jour tu deviendra riche, ca je le suis sur\n"
                    "Bon je te laisse\n",
                )
                player["tuto"] += 1
            if player["begin"] and player["tuto"] == 3:
                showinfo(
                    title="Dictentiel",
                    message="HELP\n"
                    "Vous venez de terminez le dictentiel\n"
                    "N oubliez pas que le menu aide est disponible en cas de probleme",
                )
                player["begin"] = False

            add_money()
            save()
            label.config(text="Money: %s F" % print_money(player["money"]))
            label0.config(text="%s" % get_items("orange"))
            label1.config(text="%s" % get_items("call_box"))
            label2.config(text="%s" % get_items("boutique"))
            label3.config(text="%s" % get_items("boulangerie"))
            label4.config(text="%s" % get_items("resto"))
            label5.config(text="%s" % get_items("hospital"))
        except:
            pass


fen = Tk()
fen.title(title)
fen.geometry("%sx%s" % fen_size)

img_orange = PhotoImage(file=items_img["orange"])
img_call_box = PhotoImage(file=items_img["call_box"])
img_boutique = PhotoImage(file=items_img["boutique"])
img_boulangerie = PhotoImage(file=items_img["boulangerie"])
img_resto = PhotoImage(file=items_img["resto"])
img_hospital = PhotoImage(file=items_img["hospital"])

img_orange2 = img_orange.subsample(2, 2)
img_call_box2 = img_call_box.subsample(2, 2)
img_boutique2 = img_boutique.subsample(2, 2)
img_boulangerie2 = img_boulangerie.subsample(2, 2)
img_resto2 = img_resto.subsample(2, 2)
img_hospital2 = img_hospital.subsample(2, 2)

menubar = Menu(fen)

menu_add = Menu(menubar, tearoff=1)
menu_add.add_command(label="Orange", command=lambda: add_item("orange"))
menu_add.add_command(label="Call_box", command=lambda: add_item("call_box"))
menu_add.add_command(label="Boutique", command=lambda: add_item("boutique"))
menu_add.add_command(label="Boulangerie", command=lambda: add_item("boulangerie"))
menu_add.add_command(label="Restorant", command=lambda: add_item("resto"))
menu_add.add_command(label="Hospital", command=lambda: add_item("hospital"))
menubar.add_cascade(label="Ajouter", menu=menu_add)

menu_upgrade = Menu(menubar, tearoff=1)
menu_upgrade.add_command(label="Orange", command=lambda: upgrade("orange"))
menu_upgrade.add_command(label="Call_box", command=lambda: upgrade("call_box"))
menu_upgrade.add_command(label="Boutique", command=lambda: upgrade("boutique"))
menu_upgrade.add_command(label="Boulangerie", command=lambda: upgrade("boulangerie"))
menu_upgrade.add_command(label="Restorant", command=lambda: upgrade("resto"))
menu_upgrade.add_command(label="Hospital", command=lambda: upgrade("hospital"))
menubar.add_cascade(label="Ameliorer", menu=menu_upgrade)

menu_player = Menu(menubar, tearoff=1)
menu_player.add_command(label="Mon Niveau social", command=player_level)
menu_player.add_command(label="Mon Rang", command=player_rang)
menubar.add_cascade(label="Player", menu=menu_player)

menu_screen = Menu(menubar, tearoff=1)
menu_screen.add_command(label="Normal", command=lambda: screen("normal"))
menu_screen.add_command(label="Petit", command=lambda: screen("tiny"))
menubar.add_cascade(label="Screen", menu=menu_screen)

menubar.add_command(label="Aide", command=aide)

fen.config(menu=menubar)

button = Button(text="x%s" % n_x, width=5, command=multi)
button.place(x=0, y=0)
label = Label(fen, text="Money: %s F" % player["money"], font=(9))
label.pack()
label0 = Label(
    fen, image=img_orange, text="%s" % get_items("orange"), compound=TOP, font=(9)
)
label0.pack()
label1 = Label(
    fen, image=img_call_box, text="%s" % get_items("call_box"), compound=TOP, font=(9)
)
label1.pack()
label2 = Label(
    fen, image=img_boutique, text="%s" % get_items("boutique"), compound=TOP, font=(9)
)
label2.pack()
label3 = Label(
    fen,
    image=img_boulangerie,
    text="%s" % get_items("boulangerie"),
    compound=TOP,
    font=(9),
)
label3.pack()
label4 = Label(
    fen, image=img_resto, text="%s" % get_items("resto"), compound=TOP, font=(9)
)
label4.pack()
label5 = Label(
    fen, image=img_hospital, text="%s" % get_items("hospital"), compound=TOP, font=(9)
)
label5.pack()
_thread.start_new_thread(main, (()))

fen.resizable(width=False, height=False)
fen.mainloop()

run = False

time.sleep(3)
