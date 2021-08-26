# Ülesanne 2
#
# Description:
# Cypher user's message by given steps
#

def crypt_func(default_text, step):
    final = "" # define final string variable
    cypher_source = "abcdefghijklmnopqrstuvwxyz" # define cryption key
    list(cypher_source) # -> array
    list(default_text) # -> array
    for i in range(len(default_text)): # loop through the given text's letters
        if default_text[i] == " ": # if the current letter is a space, add it
            final += default_text
        else: # else 
            index = cypher_source.index(default_text[i]) # get the index of the current given string letter in cypher key
            while index + step >= len(cypher_source): # while we are out of cypher_source array range, fix it
                index = index - len(cypher_source)
            final += cypher_source[index + step] # add the cyphered letter to final string
    print(final)

crypt_func("abcdefgxyz", 3) 
