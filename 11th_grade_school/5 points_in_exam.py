kas = {
    "kasutaja": {
        "marii12": {
            "name": "Marii Juhkentali",
            "password": "mariionlohh",
            "punktid": [12, 20, 8, 17, 5]
        },
        "joonasdabest": {
            "name": "Joonas Lambakari",
            "password": "joonas123",
            "punktid": [20, 20, 20, 20, 20]
        },
        "helmet.porgand": {
            "name": "Helmet Põlvast",
            "password": "helmet",
            "punktid": [12, 20, 8, 17, 5]
        },
    },
    "admin": {
        "username": "admin.admin",
        "password": "boss"
    },
}

print("Tere tulemast andmebaasi!")
while True:
    valid_operations = ("admin", "kasutaja", "lahku")
    actiontype = input(f"Vali oma tegevus {valid_operations}: ")

    if actiontype == "lahku":
        break
    elif actiontype not in valid_operations:
        pass
    else:
        if actiontype == "admin":
            usern = input("Logi sisse: ")
            passw = input("Parool: ")
            if kas[actiontype]["username"] == usern and kas[actiontype]["password"] == passw:
                print("Kasutajad: ")
                for name in kas["kasutaja"]:
                    print(f"   {kas['kasutaja'][name]['name']}\n"
                          f"      Tulemus: {sum(kas['kasutaja'][name]['punktid'])}\n")
            pass
        elif actiontype == "kasutaja":
            usern = input("Logi sisse: ")
            if usern in kas[actiontype]:
                passw = input("Parool: ")

                if passw == kas[actiontype][usern]["password"]:
                    print(f"{kas[actiontype][usern]['name']}\n"
                          f"   Tulemus: {sum(kas[actiontype][usern]['punktid'])}")
                    next_message = "Kahjuks ei pääsesnud järgmisesse vooru!\n"
                    if sum(kas[actiontype][usern]['punktid']) > 80:
                        next_message = "Pääsesid järgmisesse vooru!\n"
                    print(f"   {next_message}\n")
