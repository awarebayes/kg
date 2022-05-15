################# ДОП ПРОВЕРКА НА ВЫПУКЛОСТЬ ####################
import numpy as np
from numpy import sign

EPS = 10e-6


def get_d_k_b(ax, ay, cx, cy):
    # Коэффициенты прямой АС
    # Если точки A и С лежат на одной вертикальной прямой
    if abs((cx - ax) - 0) <= 1e-6:
        k = 1
        b = -cx
        d = 0
    else:
        k = (cy - ay) / (cx - ax)
        b = cy - (k * cx)
        d = 1

    return d, k, b


def cross_lines(ax, ay, bx, by, cx, cy, dx, dy):
    d_ab, k_ab, b_ab = get_d_k_b(ax, ay, bx, by)
    d_cd, k_cd, b_cd = get_d_k_b(cx, cy, dx, dy)

    if abs(k_ab - k_cd) < 1e-6:
        return False
    x = (b_cd - b_ab) / (k_ab - k_cd)
    if d_cd == 0:
        y = k_ab * x + b_ab
    elif d_ab == 0:
        y = k_cd * x + b_cd
    else:
        y = k_ab * x + b_ab

    b1 = ax
    b2 = bx
    ax = max(b1, b2)
    bx = min(b1, b2)
    b1 = ay
    b2 = by
    ay = max(b1, b2)
    by = min(b1, b2)

    if (
        (abs(bx - x) < EPS)
        or (abs(ax - x) < EPS)
        or (abs(by - y) < EPS)
        or (abs(ay - y) < EPS)
    ):
        return False
    if (bx < x < ax) and (by < y < ay):
        return True
    else:
        return False


def check_cross(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(i + 1, n, 1):
            if j == n - 1:
                if cross_lines(
                    arr[i][0],
                    arr[i][1],
                    arr[i + 1][0],
                    arr[i + 1][1],
                    arr[j][0],
                    arr[j][1],
                    arr[0][0],
                    arr[0][1],
                ):
                    return True
            elif cross_lines(
                arr[i][0],
                arr[i][1],
                arr[i + 1][0],
                arr[i + 1][1],
                arr[j][0],
                arr[j][1],
                arr[j + 1][0],
                arr[j + 1][1],
            ):
                return True
    return False


def is_convex(arr):
    if len(arr) < 3:
        return False
    a = np.array([arr[0][0] - arr[-1][0], arr[0][1] - arr[-1][1]])
    b = np.array([arr[-1][0] - arr[-2][0], arr[-1][1] - arr[-2][1]])
    prev = sign(np.cross(a, b))
    for i in range(1, len(arr) - 2):
        a = np.array([arr[i][0] - arr[i - 1][0], arr[i][1] - arr[i - 1][1]])
        b = np.array([arr[i - 1][0] - arr[i - 2][0], arr[i - 1][1] - arr[i - 2][1]])
        cur = sign(np.cross(a, b))
        if prev != cur:
            return False
        prev = cur

    if check_cross(arr):
        return False
    return True
