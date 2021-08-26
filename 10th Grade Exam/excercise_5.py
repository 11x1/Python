# Ülesanne 5
#
# Description:
# Take an array containing finished tic-tac-toe game table and check who won
#

def tripsTrapsTrullTulemus(l1, l2, l3):
    winner = "-"
    
    # Non-efficient way of checking who won but :shrug:
    p1 = l1[0]; p2 = l1[1]; p3 = l1[2];
    p4 = l2[0]; p5 = l2[1]; p6 = l2[2];
    p7 = l3[0]; p8 = l3[1]; p9 = l3[2];
    
    # Vertical check
    if p1 == p4 == p7: winner = p1
    elif p2 == p5 == p8: winner = p2
    elif p3 == p6 == p9: winner = p3
    
    # Horizontal check
    elif p1 == p2 == p3: winner = p1
    elif p4 == p5 == p6: winner = p4
    elif p7 == p8 == p9: winner = p7
    
    # Diagonal check
    elif p1 == p5 == p9: winner = p1
    elif p3 == p5 == p7: winner = p3
    
    # Print our winner
    if not winner == "-": print(winner); return
    print("-")

    
tul1 = ["X", "O", "X"]
tul2 = [" ", "X", "O"]
tul3 = ["X", "O", " "]
tripsTrapsTrullTulemus(tul1, tul2, tul3)
