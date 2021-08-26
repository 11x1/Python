# Ülesanne 4
#
# Description:
# Add together all possible combinations of two strings' characters
#

def test(A, B):
    final = [] # define final string
    list(A) # Safety check, to assure we get arrays
    list(B) # to work with

    for i in range(len(A)): # Loop through 1st array
        for s in range(len(B)): # Loop through 2nd array
            final.append(A[i] + B[s]) # Add combination to
                                      # final string
    print(final)

str1 = list("ab")
str2 = list("123")
test(str1, str2)
