from problem import Problem


def main():
    problem = Problem((5, 0, 0), [(4, 1, 0), (4, 0, 1)])
    print(problem.initial, ", ", problem.goal)


if __name__ == "__main__":
    main()
