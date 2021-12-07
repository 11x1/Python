def tripsTrapsTrullTulemus(matrix):
    row1 = matrix[0]
    row2 = matrix[1]
    row3 = matrix[2]

    winner = ""

    s1, s2, s3, s4, s5, s6, s7, s8, s9 = row1[0], row1[1], row1[2], row2[0], row2[1], row2[2], row3[0], row3[1], row3[2]
    if (s1 == s2 == s3 or s4 == s5 == s6 or s7 == s8 == s9) or (s1 == s4 == s7 or s2 == s5 == s7 or s3 == s6 == s9) or (s1 == s5 == s9 or s3 == s5 == s7):
        winner = s1

    return winner
