from PyQt5.QtWidgets import QMessageBox

from is_convex import is_convex


def scalar_mult(a, b):
    return a[0] * b[0] + a[1] * b[1]


def vector_mult(a, b):
    return a[0] * b[1] - a[1] * b[0]
    # Ax * By - Ay * Bx --- это будет координата Z, которая нам нужна


def normal(a, b, pos):
    fvec = [b[0] - a[0], b[1] - a[1]]
    posvec = [pos[0] - b[0], pos[1] - b[1]]

    if fvec[1]:
        fpoint = -fvec[0] / fvec[1]
        normvec = [1, fpoint]
    else:
        normvec = [0, 1]

    if scalar_mult(posvec, normvec) < 0:
        normvec[0] = -normvec[0]
        normvec[1] = -normvec[1]

    return normvec


def cut_one(line, count, rect):
    # Вычисление директрисы заданного отрезка:
    # D = P_2-P_1
    d = [line[1][0] - line[0][0], line[1][1] - line[0][1]]

    # Инициализация пределов значений параметра t при условии,
    # что отрезок полностью видим:
    # t_н=0,t_к=1
    top = 0
    bottom = 1

    # Начало цикла по всем сторонам отсекателя.
    # Для каждой i-ой стороны отсекателя выполнить следующие действия:
    for i in range(-2, count - 2):
        print(i)
        # Вычисление вектора внутренней нормали к очередной
        # i-ой стороне отсекателя - N_вi
        norm = normal(rect[i], rect[i + 1], rect[i + 2])

        # Вычисление вектора W_i=P_1-f_i (f_i берем за вершины стороны)
        w = [line[0][0] - rect[i][0], line[0][1] - rect[i][1]]

        # Вычисление скалярного произведения векторов:
        # W_iскал=W_i N_вi
        # D_скал=DN_вi
        d_scal = scalar_mult(d, norm)
        w_scal = scalar_mult(w, norm)

        # Если D_скал=0, Если W_скi>0, то отрезок
        # (точка) видим(-а) относительно текущей стороны отсекателя
        # Проверка видимости точки, в которую выродился отрезок, или проверка видимости произвольной
        # точки отрезка в случае его параллельности стороне отсекателя: если W_скi<0, то отрезок (точка)
        # невидим(-а). Если W_скi>0, то отрезок (точка) видим(-а) относительно текущей
        # стороны отсекателя.
        if d_scal == 0:
            if w_scal < 0:  # невидима
                return []
            else:
                continue

        # Вычисление параметра t:
        # t=-W_скi/D_ск
        param = -w_scal / d_scal

        if d_scal > 0:  # нижняя граница видимости (выбираем из 0 и получившегося)
            if param <= 1:
                top = max(top, param)
            else:
                return

        elif d_scal < 0:  # верхняя граница видимости (выбираем из 1 и получившегося)
            if param >= 0:
                bottom = min(bottom, param)
            else:
                return

        # Проверка фактической видимости отсечённого отрезка. Если t_н > t_в, то выход
        if top > bottom:
            break

    # Проверка фактической видимости отсечённого отрезка.
    #  Если t_н≤t_в, то изобразить отрезок в
    # интервале от P(t_н ) до P(t_н ).
    # TOP - нижнее BOTTOM вернее
    if top <= bottom:
        return [
            [round(line[0][0] + d[0] * top), round(line[0][1] + d[1] * top)],
            [round(line[0][0] + d[0] * bottom), round(line[0][1] + d[1] * bottom)],
        ]

    return []


# 1 - Ввод исходных данных: точки отрезка P_1 (P_(1.x),P_(1.y) )  и P_2 (P_(2.x),P_(2.y) )
# 2 - Ввод числа сторон m выпуклого многоугольника и координат его вершин (массив C)
def cyrus_beck_alg(lines, rect):

    if not is_convex(rect):
        QMessageBox.warning(None, "Waring!", "Отсекатель невыпуклый.")
        return

    n_sides = len(rect)

    to_draw = []
    for line in lines:
        cut = cut_one(line, n_sides, rect)
        if cut:
            to_draw.append(cut)

    return to_draw
