# coding: utf-8
# license: GPLv3

gravitational_constant = 6.67408E-11
"""Гравитационная постоянная G"""


def calculate_acceleration(point, space_bodies):
    """Вычисляет ускорение тела, находящегося в точке с координатами point в системе тел space_bodies"""
    ax = 0
    ay = 0
    for obj in space_bodies:
        x = obj.x - point[0]
        y = obj.y - point[1]
        r = (x ** 2 + y ** 2) ** 0.5
        a = gravitational_constant * obj.m / r ** 2
        ax += a * x / r
        ay += a * y / r
    return ax, ay


def model(space_objects, dt):
    """Пересчитывает координаты объектов.

    Параметры:

    **space_objects** — список оьъектов, для которых нужно пересчитать координаты.
    **dt** — шаг по времени
    """

    for body in space_objects:
        # TODO(fetisu): Этот метод экстраполяции примитивен. Сделаешь Рунге-Кутта 4го порядка? :)
        a = calculate_acceleration((body.x, body.y), set(space_objects) - {body})
        body.vx += a[0] * dt
        body.vy += a[1] * dt
        body.x += body.vx * dt
        body.y += body.vy * dt

        if True:  # TODO(fetisu): Сделай условие обновления траектории
            body.trace.append((body.x, body.y))


if __name__ == "__main__":
    print("This module is not for direct call!")
