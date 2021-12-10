def func(A, B):
    final = []
    for elem in A:
        for elem_ in B:
            final.append([elem, elem_])
    return final
