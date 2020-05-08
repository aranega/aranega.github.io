from uuid import uuid4
from flask import Flask, abort, request

app = Flask(__name__)

uuid = uuid4().int


class DeadException(Exception):
    pass


class WallException(Exception):
    pass


class NotSameRoomException(Exception):
    pass


@app.route("/connect", methods=["POST"])
def connect():
    result = {
        "guid": uuid,
        "totalvie": 100,
        # retourne ici presque toujours la même salle pour pouvoir
        "salle": {
            "description": "Vous êtes dans la première salle",
            "passages": ["N", "S", "W"],
            "entites": [uuid],
        },
    }
    return result


@app.route("/<guid>/regarder")
def regarder(guid):
    return {
        "description": "Vous êtes dans une salle depuis laquelle on ne peut pas se déplacer à l'ouest (testez pour déclancher une erreur)",
        "passages": ["N", "S", "E"],
        "entites": [33, 44, 55],
    }


@app.route("/<guid>/deplacement", methods=["POST"])
def deplacer(guid):
    direction = request.json["direction"]
    print(f"L'utilisateur {guid} veut se déplacer vers {direction}")
    if direction == "W":
        print("Il ne peut pas aller vers l'ouest")
        raise WallException()
    return {
        "description": "Vous êtes dans une autre salle (ici toujours la même)",
        "passages": ["N", "S"],
        "entites": [123, 234],
    }


@app.route("/<guid>/examiner/33")
def examiner33(guid):
    print(f"L'utilisateur {guid} veut examiner le perso 33")
    return {
        "description": "C'est un joueur (description plus longue si envie)",
        "type": "JOUEUR",
        "vie": 100,
        "totalvie": 100,
    }


@app.route("/<guid>/examiner/44")
def examiner44(guid):
    print(f"L'utilisateur {guid} veut examiner le perso 44")
    return {
        "description": "C'est un joueur (description plus longue si envie)",
        "type": "JOUEUR",
        "vie": 98,
        "totalvie": 100,
    }


@app.route("/<guid>/examiner/55")
def examiner55(guid):
    print(f"L'utilisateur {guid} veut examiner le perso 55")
    return {
        "description": "C'est un monstre ",
        "type": "MONSTRE",
        "vie": 50,
        "totalvie": 100,
    }


@app.route("/<guid>/examiner/66")
def examiner66(guid):
    print(
        f"L'utilisateur {guid} veut examiner le perso 66, mais il n'est pas dans la même salle"
    )
    raise NotSameRoomException()


@app.route("/<guid>/examiner/77")
def examiner77(guid):
    print(f"L'utilisateur {guid} veut examiner le perso 77, mais il n'existe pas")
    abort(404)


@app.route("/<guid>/examiner/<guiddest>")
def examiner(guid, guiddest):
    from random import randint

    print(f"L'utilisateur {guid} veut examiner le perso {guiddest}")
    return {
        "description": "Description générique",
        "type": "JOUEUR" if randint(0, 2) % 2 else "MONSTRE",
        "vie": randint(10, 100),
        "totalvie": 100,
    }


@app.route("/<guid>/taper", methods=["POST"])
def taper(guid):
    cible = request.json["cible"]
    print(f"L'utilisateur {guid} veut tapper la cible {cible}")
    return examiner(guid, cible)


@app.errorhandler(DeadException)
def error_dead(error):
    return {"type": "MORT", "message": "Vous êtes mort (pas de bol)"}, 409


@app.errorhandler(NotSameRoomException)
def error_notsameroom(error):
    return {"type": "DIFFSALLE", "message": "Vous n'êtes pas dans la même salle"}, 409


@app.errorhandler(WallException)
def error_wall(error):
    return {"type": "MUR", "message": "Vous avez pris un mur"}, 409


print(
    """!!!!
ATTENTION: LES JSON RENVOYES PAR CE SERVER DE TEST SONT TOUJOURS LES MEMES.
POUR AVOIR UN VRAI SERVEUR UTILISABLE, RAPPROCHEZ-VOUS D'UN DE VOS COLLEGUES
!!!!"""
)

app.run()
