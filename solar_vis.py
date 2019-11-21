# coding: utf-8
# license: GPLv3

"""Модуль визуализации.
Нигде, кроме этого модуля, не используются экранные координаты объектов.
Функции, создающие графические объекты и перемещающие их на экране, принимают физические координаты
"""

header_font = "Arial-16"
"""Шрифт в заголовке"""

window_width = 900
"""Ширина окна"""

window_height = 800
"""Высота окна"""

scale_factor = None
v_scale_factor = None
"""Масштабирование экранных координат по отношению к физическим.
Тип: float
Мера: количество пикселей на один метр."""

name_dist = 20
"""Расстояние в процентах от скорости для отображения названия объекта"""

max_trace_dist = 10
"""минимальное расстояние между штрихами траекторий"""


def calculate_scale_factor(space):
    """Вычисляет значение глобальной переменной **scale_factor** по данной характерной длине"""
    global scale_factor
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space.bodies])
    scale_factor = 0.4 * min(window_height, window_width) / max_distance
    print('Scale factor:', scale_factor)


def calculate_v_scale_factor(space):
    global v_scale_factor
    max_velocity = max([obj.get_velocity() for obj in space.bodies])
    v_scale_factor = 30 / (max_velocity * scale_factor) if max_velocity > 0 else 0


def create_image(space, space_body):
    """Создаёт отображаемый объект звезды.

    Параметры:

    **space** — холст для рисования.
    **star** — объект звезды.
    """

    x = int(space_body.x * scale_factor) + window_width // 2
    y = int(space_body.y * scale_factor) + window_height // 2
    vx = space_body.vx * scale_factor * v_scale_factor
    vy = space_body.vy * scale_factor * v_scale_factor
    r = space_body.r
    space_body.ids = {'ball': space.create_oval((0, 0), (0, 0), fill=space_body.color),
                      'arrow_body': space.create_line((0, 0), (0, 0), fill=space_body.color),
                      'arrow_end': [space.create_line((0, 0), (0, 0), fill=space_body.color),
                                    space.create_line((0, 0), (0, 0), fill=space_body.color)],
                      'trace': [space.create_oval((0, 0), (0, 0), fill=space_body.color)],
                      'label': space.create_text(0, 0, text=space_body.name, fill=space_body.color)
                      }


def update_system_name(space, system_name):
    """Создаёт на холсте текст с названием системы небесных тел.
    Если текст уже был, обновляет его содержание.

    Параметры:

    **space** — холст для рисования.
    **system_name** — название системы тел.
    """
    space.create_text(30, 80, tag="header", text=system_name, font=header_font)


def update_object_position(space_obj, space_body):
    """Перемещает отображаемый объект на холсте.

    Параметры:

    **space** — холст для рисования.
    **body** — тело, которое нужно переместить.
    """
    calculate_v_scale_factor(space_obj)
    space = space_obj.canvas
    x = int(space_body.x * scale_factor) + window_width // 2
    y = int(space_body.y * scale_factor) + window_height // 2
    vx = space_body.vx * scale_factor * v_scale_factor
    vy = space_body.vy * scale_factor * v_scale_factor
    r = space_body.r

    space.coords(space_body.ids['ball'],
                 x - r, y - r,
                 x + r, y + r)
    space.coords(space_body.ids['arrow_body'],
                 x, y,
                 x + vx, y + vy)
    space.coords(space_body.ids['arrow_end'][0],
                 x + vx, y + vy,
                 x + 0.8 * vx - 0.1 * vy,
                 y + 0.8 * vy + 0.1 * vx)
    space.coords(space_body.ids['arrow_end'][1],
                 x + vx, y + vy,
                 x + 0.8 * vx + 0.1 * vy,
                 y + 0.8 * vy - 0.1 * vx)
    space.coords(space_body.ids['label'],
                 x, y - (r + name_dist) * ((vy > 0) * 2 - 1))

    trace_dist = int(space_body.get_dist_from_last_trace() * scale_factor)

    if trace_dist > max_trace_dist:
        space_body.ids['trace'].append(space.create_oval([x - 1, y - 1], [x + 1, y + 1],
                                                         fill=space_body.color))

        space_body.trace.append((space_obj.time, space_body.x, space_body.y, space_body.vx, space_body.vy))

        if len(space_body.trace) > space_obj.trace_length.get():
            for i in range(- int(space_obj.trace_length.get()) - 1, -len(space_body.trace) - 1, -1):
                space.delete(space_body.ids['trace'][i])


if __name__ == "__main__":
    print("This module is not for direct call!")
