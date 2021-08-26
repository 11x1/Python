# Ülesanne 2
#
# Description:
# Cypher user's message by given steps
#

# Get user input to cypher
crypt_this = input("Enter plain message: ")

plain  = "abcdefghijklmnopqrstuvwxyz"
cypher = "bcdefghijklmnopqrstuvwxyza"

# make everything an array
list(plain)
list(cypher)
list(crypt_this)


# Find our given word's retters in plain and then
# find the corresponding letter from cypher and add
# it to final
    
final = ""
for i in range(len(crypt_this)):
  # if character in the specified position is space then just add it to our final output
  if crypt_this[i] == " ":
    final += crypt_this;
  else:
    # print(plain.index(crypt_this[i]))
    index = plain.index(crypt_this[i])
    final += cypher[index]
print(final)
