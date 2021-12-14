file = open("eksam.txt", "r")
lines = file.readlines()
for line in lines:
    line = line.strip("\n").split(" ")
    has_seen_the_weird_post_thing = False
    name = ""
    score = 0
    for elem in line:
        if len(elem) > 0:
            if elem == "|":
                has_seen_the_weird_post_thing = True
            elif not has_seen_the_weird_post_thing:
                    name += f"{elem} "
            else:
                score += int(elem.split(",")[0])
    print(f"{name} | {score}")
file.close()
