# Ülesanne 5
#
# Description:
# Take an array containing finished tic-tac-toe game table and check who won
#

# Update (07.12.2021)
# This would not work if one of the elements position isn't in win condition position but that element type still won:
# ex.
#
#    X X O   table (x)  1 1 0
#    X O O      ->      1 0 0
#    X                  1 0 0
#
# X still won but table [1, 1, 0, 1, 0, 0, 1, 0, 0] isn't in win conditions -> use exercise_5_re_p.py
#


def tripsTrapsTrullTulemus(table_array):
    winner = "-" # define winner
    X_series = [] # define X spots array
    O_series = [] # define O spots array
    X_ = "" # define X spots string to later add it to X spots array and compare it
    O_ = "" # --"--
    WIN_series = [["111000000"], ["000111000"], ["000000111"], ["100100100"], ["010010010"], ["001001001"], ["10001001"], ["001010100"]]
    # ^ defien all win possibilities
    for line in table_array: # for each array in our table_array
        for elem in line: # for each element in the 'line' array
            if elem == "X": # if element is X or O, add 0 or 1 correspondingly
                X_ += "1"
                O_ += "0"
            elif elem == "O":
                X_ += "0"
                O_ += "1"
            else:
                X_ += "0"
                O_ += "0"
    X_series.append(X_) # add X string to X array
    O_series.append(O_) # add O string to O array
    if X_series in WIN_series: # if winning conditions array contains X array 
        winner = "X"
    elif O_series in WIN_series: # else if winning conditions array contains Y array
        winner = "O"
    print("Winner: " + winner)

table = [["X", " ", "O"], ["X", " ", "O"], ["X", " ", " "]]
tripsTrapsTrullTulemus(table)
