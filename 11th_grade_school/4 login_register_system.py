class helpers:
    data = {}

    def login(self, name, passw):
        if name in self.data:
            if passw == self.data[name]["password"]:
                print(f"Tere, {name}! Olete sisse logitud")
            else:
                print(f"login for {name} failed, wrong password")
        else:
            self.register(name=name, passw=passw)

    def register(self, name, passw):
        if not name in self.data:
            self.data[name] = {
                "username": name,
                "password": passw,
            }
            print(f"Tere {name}! Olete loonud endale kasutaja")
        else:
            print(f"username {name} already exists!")

    def return_registered_users(self):
        final = []
        for name in self.data:
            final.append([self.data[name]["username"], self.data[name]["password"]])
        return final


while 1:
    interaction_type = input("""
    Mis soovite teha?
    1 - sisse logida
    2 - uue kasutaja luua
    quit - exit
    -------------------------- : 
    """)

    if interaction_type == "quit":
        break
    elif interaction_type == "4":
        print(helpers().return_registered_users())
    else:
        username = input("kasutajanimi: ")
        password = input("parool: ")

        if interaction_type == "1":
            helpers().login(name=username, passw=password)
        elif interaction_type == "2":
            helpers().register(name=username, passw=password)
        else:
            print("Not an available option.")
