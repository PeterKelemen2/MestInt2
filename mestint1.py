from cups import Cup3
from problem import Problem


# https://robertlakatos.github.io/me//teaching/AI

def main():
    # problem = Problem((5, 0, 0), [(4, 1, 0), (4, 0, 1)])
    # print(problem.initial, ", ", problem.goal)

    c = Cup3((5, 0, 0), [(4, 1, 0), (4, 0, 1)])
    print(c.actions((5, 0, 0)))


if __name__ == "__main__":
    main()
