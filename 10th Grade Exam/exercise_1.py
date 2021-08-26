# Ülesanne 1
#
# Description:
# Remove any continuous letters from string
#

def test(sõne):
    list(sõne) # -> array
    final = "" # define final string
    lastletter = ""
    # loop through all the letters in list we created earlier
    for i in range(len(sõne)): # starts from 0 -> last array elem
        if not sõne[i] == lastletter: # if the letter is not the same as the letter before, add it to the final string variable
            final += sõne[i]
        lastletter = sõne[i] # lastletter variable is the current letter to compare it to a letter afterwards
    print(final)
    
test("pprrrrrrrrrrrrrogrammeeriminnnne")
test("jäääär")
