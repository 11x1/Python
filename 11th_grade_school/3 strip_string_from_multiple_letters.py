def func(our_string):
    final = []
    for letter in our_string:
        if not letter in final:
            final.append(letter)
    return final
