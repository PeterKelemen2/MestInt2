# A heurisztika lényeg az hogy ha minél több üres korsót találunk 
# annál távolabb vagyunk a megoldástól
def heuristic_calc_empty_jar(State):
    if State == (4, 0, 1) or State == (4, 1, 0):
        return 0
    c = 0
    for i in State:
        if i == 0:
            c += 1
    return c + 1


def heuristic_zero(State):
    return 0
