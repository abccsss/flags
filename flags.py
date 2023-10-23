from fractions import Fraction


def sgn(i: float) -> int:
    return 0 if i == 0 else 1 if i > 0 else -1


def reciprocal(i: int) -> float:
    return 0 if i == 0 else 1 / i


def list_add(a: list[int], b: list[int]) -> list[int]:
    return [x + y for x, y in zip(a, b)]


def valid_permutations(m: int, n: int) -> list[list[int]]:
    result = []
    sum = [0] * (m + 1)
    quota = [n, *range(1, m + 1)]

    _valid_permutations_helper(m, n, result, [], sum, quota)

    return result


def _valid_permutations_helper(
    m: int,
    n: int,
    result: list[list[int]],
    seq: list[int],
    sum: list[int],
    quota: list[int],
) -> None:
    level = len(seq)

    sign = 0
    for i in range(1, m + 1):
        if sum[i] != 0:
            sign = sgn(sum[i])
            break

    if level == m * (m + 1) / 2 + n:
        if sign == 1 and seq[level - 1] < 0:
            return
        if sign == -1 and seq[level - 1] > 0:
            return

        result.append(seq)
        return

    valid_moves: list[int] = []

    if sign == -1:
        if seq[level - 1] < 0:
            valid_moves = [*range(seq[level - 1], -m - 1, -1), 0, *range(m, 0, -1)]
        elif seq[level - 1] == 0:
            valid_moves = [0, *range(m, 0, -1)]
        else:
            valid_moves = [*range(seq[level - 1], 0, -1)]

    if sign == 0:
        valid_moves = [*range(-1, -m - 1, -1), 0, *range(m, 0, -1)]

    if sign == 1:
        if seq[level - 1] > 0:
            valid_moves = [*range(-1, -m - 1, -1), 0, *range(m, seq[level - 1] - 1, -1)]
        elif seq[level - 1] == 0:
            valid_moves = [*range(-1, -m - 1, -1), 0]
        else:
            valid_moves = [*range(-1, seq[level - 1] - 1, -1)]

    for i in valid_moves:
        absi = abs(i)
        if quota[absi] == 0:
            continue

        new_seq = seq + [i]
        quota[absi] -= 1
        sum[absi] += sgn(i)

        _valid_permutations_helper(m, n, result, new_seq, sum, quota)

        quota[absi] += 1
        sum[absi] -= sgn(i)


def binom(n: Fraction, k: int) -> Fraction:
    result = Fraction(1)
    for i in range(k):
        result *= Fraction(n - i, i + 1)

    return result


def factorial(n: int) -> int:
    result = 1
    for i in range(1, n + 1):
        result *= i

    return result


def v_coefficient(n: int, weights: dict[int, int]) -> Fraction:
    result = 0
    m = sum([weights[i] for i in range(-n, n + 1)])

    for seq in valid_permutations(m, n):
        aux = seq + [0] + [-x for x in reversed(seq)]
        aux = [x for x in aux if x >= 0]

        w = 1
        for i in range(1, m):
            t = 0
            for j in range(len(aux)):
                if aux[j] == i + 1:
                    t += 1
                if aux[j] == i:
                    w *= t
                    t -= 1

        t = 0
        zero_index = 1 if n > 0 else 0
        for j in range(len(aux)):
            if aux[j] == 0:
                t += weights[zero_index]
                zero_index += (
                    -n if zero_index == n or zero_index == 0 else zero_index + 1
                )
            if aux[j] == m:
                w *= t
                t -= 1

        if w == 0:
            continue

        u = u_coefficient(seq)
        # print(seq, w, u)
        result += w * u

    return result


def u_coefficient(seq: list[int]) -> Fraction:
    m = max(abs(x) for x in seq)

    sign = []
    convex = []

    sum = [0] * (m + 1)
    for i in range(len(seq)):
        sum[abs(seq[i])] += sgn(seq[i])

        new_sign = 0
        for j in range(1, m + 1):
            if sum[j] != 0:
                new_sign = sgn(sum[j])
                break
        sign.append(new_sign)

        if i == len(seq) - 1:
            convex.append(-sgn(seq[i]))
        else:
            convex.append(sgn(reciprocal(seq[i + 1]) - reciprocal(seq[i])))

    zero_places = [i + 1 for i in range(len(sign)) if sign[i] == 0]

    # all subsequences of zero_places
    subsequences = []
    for i in range(1 << len(zero_places)):
        subsequence = [0]
        for j in range(len(zero_places)):
            if i & (1 << j):
                subsequence.append(zero_places[j])
        subsequences.append(subsequence)

    result = Fraction(0)
    for subsequence in subsequences:
        subresult = Fraction(1)

        for i in range(len(subsequence) - 1):
            new_sign = sign[subsequence[i] : subsequence[i + 1]]
            new_convex = convex[subsequence[i] : subsequence[i + 1]]
            subresult *= s_coefficient(new_sign, new_convex)

        last_sign = sign[subsequence[-1] :]
        last_convex = convex[subsequence[-1] :]
        subresult *= s_coefficient(last_sign, last_convex, True)

        subresult *= binom(Fraction(-1, 2), len(subsequence) - 1)
        result += subresult

    return result


def s_coefficient(
    sign: list[int], convex: list[int], is_last: bool = False
) -> Fraction:
    result = Fraction(1)
    n = len(sign)

    degen_pos = 0
    degen_neut = 0
    degen_neg = 0
    reset_degen = False

    for i in range(n - 1):
        if sign[i] > 0:
            if convex[i] > 0:
                return Fraction(0)

            result *= -1

            if convex[i] == 0:
                degen_pos += 1
                reset_degen = i == n - 2 or convex[i + 1] != 0

        if sign[i] == 0:
            if convex[i] < 0:
                return Fraction(0)

            if convex[i] == 0:
                degen_neut += 1
                reset_degen = i == n - 2 or convex[i + 1] != 0

        if sign[i] < 0:
            if convex[i] < 0:
                return Fraction(0)

            if convex[i] == 0:
                degen_neg += 1
                reset_degen = i == n - 2 or convex[i + 1] != 0

        if reset_degen:
            result *= Fraction(1, factorial(degen_pos + degen_neut + degen_neg + 1))

            if degen_neut > 0:
                result *= binom(degen_pos + degen_neut + degen_neg, degen_pos)

            degen_pos = 0
            degen_neut = 0
            degen_neg = 0

    if is_last:
        if sign[n - 1] > 0:
            if convex[n - 1] > 0:
                return Fraction(0)
            result *= -1

        if sign[n - 1] < 0 and convex[n - 1] < 0:
            return Fraction(0)

        last_flat = n - 1
        while last_flat >= 0 and convex[last_flat] == 0:
            last_flat -= 1

        result *= Fraction(1, 1 << (n - 1 - last_flat))

    return result
