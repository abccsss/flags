from flags import *


def main():
    print("Input n:\n> ", end="")
    n = int(input())
    if n < 0:
        print("Error: n must be non-negative")
        return

    if n == 0:
        print("V = d!, where d is the weight.")
        return

    print(f"Input weights for {-n}, ..., {n}, separated by spaces:\n> ", end="")
    l = input().split(" ")
    if len(l) < 2 * n + 1:
        print(f"Error: number of weights must be {2 * n + 1}")
        return

    weights = {}
    for i, w in enumerate(l):
        weights[-n + i] = int(w)

    print("Calculating ...")

    v = v_coefficient(n, weights)
    print(f"V = {v}")


if __name__ == "__main__":
    main()
